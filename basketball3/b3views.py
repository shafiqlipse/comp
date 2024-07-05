from django.shortcuts import render, redirect, get_object_or_404


from .forms import *
from .models import *

from accounts.models import Sport
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


from django.db import connection

# template

from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce


# Usage


from django.db.models import Sum, Case, When, IntegerField


def get_rankings(competition):
    # Athlete Rankings
    athlete_rankings = (
        Athlete.objects.filter(b3athlete__match__competition=competition)
        .annotate(
            points=Sum(
                Case(
                    When(b3athlete__event_type="1-Pointer", then=1),
                    When(b3athlete__event_type="2-Pointer", then=2),
                    When(b3athlete__event_type="3-Pointer", then=3),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
            two_pointers=Count(
                "b3athlete", filter=Q(b3athlete__event_type="2-Pointer")
            ),
            three_pointers=Count(
                "b3athlete", filter=Q(b3athlete__event_type="3-Pointer")
            ),
            rebounds=Count("b3athlete", filter=Q(b3athlete__event_type="rebound")),
            assists=Count("b3athlete", filter=Q(b3athlete__event_type="Assist")),
            steals=Count("b3athlete", filter=Q(b3athlete__event_type="steal")),
            blocks=Count("b3athlete", filter=Q(b3athlete__event_type="Block")),
            fouls=Count("b3athlete", filter=Q(b3athlete__event_type="Foul")),
        )
        .order_by("-points", "-rebounds")
    )

    # Team Rankings
    team_rankings = (
        SchoolTeam.objects.filter(basket_team__match__competition=competition)
        .annotate(
            points=Sum(
                Case(
                    When(basket_team__event_type="1-Pointer", then=1),
                    When(basket_team__event_type="2-Pointer", then=2),
                    When(basket_team__event_type="3-Pointer", then=3),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
            two_pointers=Count(
                "basket_team", filter=Q(basket_team__event_type="2-Pointer")
            ),
            three_pointers=Count(
                "basket_team", filter=Q(basket_team__event_type="3-Pointer")
            ),
            rebounds=Count("basket_team", filter=Q(basket_team__event_type="rebound")),
            assists=Count("basket_team", filter=Q(basket_team__event_type="Assist")),
            steals=Count("basket_team", filter=Q(basket_team__event_type="steal")),
            blocks=Count("basket_team", filter=Q(basket_team__event_type="Block")),
            fouls=Count("basket_team", filter=Q(basket_team__event_type="Foul")),
        )
        .order_by("-points")
    )

    # The rest of the function remains the same
    top_scorers = athlete_rankings.order_by("-points")[:10]
    top_rebounders = athlete_rankings.order_by("-rebounds")[:10]
    top_assisters = athlete_rankings.order_by("-assists")[:10]
    top_stealers = athlete_rankings.order_by("-steals")[:10]
    top_blockers = athlete_rankings.order_by("-blocks")[:10]
    most_fouls = athlete_rankings.order_by("-fouls")[:10]

    team_points = team_rankings.order_by("-points")[:10]
    team_rebounds = team_rankings.order_by("-rebounds")[:10]
    team_assists = team_rankings.order_by("-assists")[:10]
    team_steals = team_rankings.order_by("-steals")[:10]
    team_blocks = team_rankings.order_by("-blocks")[:10]
    team_fouls = team_rankings.order_by("-fouls")[:10]

    return {
        "athlete_rankings": athlete_rankings,
        "team_rankings": team_rankings,
        "top_scorers": top_scorers,
        "top_rebounders": top_rebounders,
        "top_assisters": top_assisters,
        "top_stealers": top_stealers,
        "top_blockers": top_blockers,
        "most_fouls": most_fouls,
        "team_points": team_points,
        "team_rebounds": team_rebounds,
        "team_assists": team_assists,
        "team_steals": team_steals,
        "team_blocks": team_blocks,
        "team_fouls": team_fouls,
    }


def B3bol(request, id):
    competition = Basketball3.objects.get(id=id)
    b3groups = B3Group.objects.filter(competition=competition)
    pending_fixtures = B3Fixture.objects.filter(
        status="Pending", competition=competition
    ).order_by("date")
    results = B3Fixture.objects.filter(
        status="InPlay", competition=competition
    ).order_by("date")
    rankings = get_rankings(competition)

    standings_data = {}
    groups = B3Group.objects.filter(competition=competition)

    for group in groups:
        standings = {
            team: {
                "points": 0,
                "played": 0,
                "won": 0,
                "lost": 0,
                "pd": 0,
                "ps": 0,
                "pc": 0,
            }
            for team in group.teams.all()
        }

        group_fixtures = B3Fixture.objects.filter(group=group)
        for fixture in group_fixtures:
            if fixture.team1_score is not None and fixture.team2_score is not None:
                for team, opponent, team_score, opponent_score in [
                    (
                        fixture.team1,
                        fixture.team2,
                        fixture.team1_score,
                        fixture.team2_score,
                    ),
                    (
                        fixture.team2,
                        fixture.team1,
                        fixture.team2_score,
                        fixture.team1_score,
                    ),
                ]:
                    standings[team]["played"] += 1
                    standings[team]["ps"] += team_score
                    standings[team]["pc"] += opponent_score

                    if team_score > opponent_score:
                        standings[team]["points"] += 2  # 2 points for a win in 3x3
                        standings[team]["won"] += 1
                    else:
                        standings[team]["lost"] += 1

                    standings[team]["pd"] = (
                        standings[team]["ps"] - standings[team]["pc"]
                    )

        sorted_standings = sorted(
            standings.items(),
            key=lambda x: (x[1]["points"], x[1]["pd"], x[1]["ps"]),
            reverse=True,
        )
        standings_data[group] = sorted_standings

    context = {
        "competition": competition,
        "b3groups": b3groups,
        "results": results,
        "fixtures": pending_fixtures,
        "rankings": rankings,
        "standings_data": standings_data,
    }
    return render(request, "frontend/basketball3.html", context)


from django.db.models import Q


def FB3FixtureDetail(request, id):
    fixture = get_object_or_404(B3Fixture, id=id)
    officials = match_official.objects.filter(fixture_id=id)
    events = MatchEvent.objects.filter(match_id=id)

    team1_yellowcards = events.filter(
        event_type="YellowCard", team=fixture.team1
    ).count()
    team2_yellowcards = events.filter(
        event_type="YellowCard", team=fixture.team2
    ).count()
    team1_redcards = events.filter(event_type="RedCard", team=fixture.team1).count()
    team2_redcards = events.filter(event_type="RedCard", team=fixture.team2).count()
    team1_goals = events.filter(event_type="Goal", team=fixture.team1).count()
    team2_goals = events.filter(event_type="Goal", team=fixture.team2).count()
    # ------fixtures by team
    team1_fixtures = B3Fixture.objects.filter(
        Q(team1=fixture.team1) | Q(team2=fixture.team1)
    ).distinct()
    team2_fixtures = B3Fixture.objects.filter(
        Q(team1=fixture.team2) | Q(team2=fixture.team2)
    ).distinct()
    context = {
        "fixture": fixture,
        "officials": officials,
        "events": events,
        # sevents
        "team1_yellowcards": team1_yellowcards,
        "team2_yellowcards": team2_yellowcards,
        "team1_goals": team1_goals,
        "team2_redcards": team2_redcards,
        "team1_redcards": team1_redcards,
        "team2_goals": team2_goals,
        # fixtures
        "team1_fixtures": team1_fixtures,
        "team2_fixtures": team2_fixtures,
    }

    return render(request, "frontend/fixture.html", context)


def B3home(request):

    context = {}
    return render(request, "frontend/b3home.html", context)


def b3bollStandings(request):
    sports = Sport.objects.all()

    standings_data = []
    for sport in sports:
        basketball3_competitions = Basketball3.objects.filter(sport=sport)

        for basketball3 in basketball3_competitions:
            groups = B3Group.objects.filter(competition=basketball3)
            competition_standings = {}

            for group in groups:
                # Initialize standings with default values for all teams in the group
                standings = {}
                for team in group.teams.all():
                    standings[team] = {
                        "points": 0,
                        "played": 0,
                        "won": 0,
                        "drawn": 0,
                        "lost": 0,
                        "gd": 0,
                        "gs": 0,
                        "gc": 0,
                    }

                # Update standings based on fixtures
                fixtures = B3Fixture.objects.filter(group=group)
                for fixture in fixtures:
                    if (
                        fixture.team1_score is not None
                        and fixture.team2_score is not None
                    ):
                        # Update played matches
                        standings[fixture.team1]["played"] += 1
                        standings[fixture.team2]["played"] += 1

                        # Update goals scored and conceded
                        standings[fixture.team1]["gs"] += fixture.team1_score
                        standings[fixture.team2]["gs"] += fixture.team2_score
                        standings[fixture.team1]["gc"] += fixture.team2_score
                        standings[fixture.team2]["gc"] += fixture.team1_score

                        # Update match results
                        if fixture.team1_score > fixture.team2_score:
                            standings[fixture.team1]["points"] += 3
                            standings[fixture.team1]["won"] += 1
                            standings[fixture.team2]["lost"] += 1
                        elif fixture.team1_score < fixture.team2_score:
                            standings[fixture.team2]["points"] += 3
                            standings[fixture.team2]["won"] += 1
                            standings[fixture.team1]["lost"] += 1
                        else:
                            standings[fixture.team1]["points"] += 1
                            standings[fixture.team2]["points"] += 1
                            standings[fixture.team1]["drawn"] += 1
                            standings[fixture.team2]["drawn"] += 1

                        # Update goal difference
                        standings[fixture.team1]["gd"] = (
                            standings[fixture.team1]["gs"]
                            - standings[fixture.team1]["gc"]
                        )
                        standings[fixture.team2]["gd"] = (
                            standings[fixture.team2]["gs"]
                            - standings[fixture.team2]["gc"]
                        )

                # Sort standings by points, goal difference, and goals scored
                sorted_standings = sorted(
                    standings.items(),
                    key=lambda x: (x[1]["points"], x[1]["gd"], x[1]["gs"]),
                    reverse=True,
                )
                competition_standings[group] = sorted_standings

            standings_data.append(
                {
                    "sport": sport,
                    "competition": basketball3,
                    "standings": competition_standings,
                }
            )

    context = {
        "standings_data": standings_data,
    }

    return render(request, "frontend/standings.html", context)


def competition_rankings(request, competition_id):
    competition = get_object_or_404(Basketball3, id=competition_id)
    rankings = get_rankings(competition)

    context = {
        "competition": competition,
        "rankings": rankings,
    }

    return render(request, "frotend/futrankings.html", context)
