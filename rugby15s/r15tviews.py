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


def R15home(request):

    context = {}
    return render(request, "frontend/r15home.html", context)


from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce
from django.db.models import F


def get_rankings(competition):
    # Player Rankings
    player_rankings = (
        Athlete.objects.filter(r15player__match__competition=competition)
        .annotate(
            tries=Count("r15player", filter=Q(r15player__event_type="Try")),
            conversions=Count("r15player", filter=Q(r15player__event_type="Conversion")),
            penalty_kicks=Count(
                "r15player", filter=Q(r15player__event_type="PenaltyKick")
            ),
            drop_goals=Count("r15player", filter=Q(r15player__event_type="DropGoal")),
            tackles=Count("r15player", filter=Q(r15player__event_type="Tackle")),
            yellow_cards=Count("r15player", filter=Q(r15player__event_type="YellowCard")),
        )
        .order_by("-tries", "-conversions")
    )

    # Team Rankings
    team_rankings = (
        SchoolTeam.objects.filter(r15team__match__competition=competition)
        .annotate(
            tries=Count("r15team", filter=Q(r15team__event_type="Try")),
            conversions=Count("r15team", filter=Q(r15team__event_type="Conversion")),
            penalty_kicks=Count("r15team", filter=Q(r15team__event_type="PenaltyKick")),
            drop_goals=Count("r15team", filter=Q(r15team__event_type="DropGoal")),
            tackles=Count("r15team", filter=Q(r15team__event_type="Tackle")),
            yellow_cards=Count("r15team", filter=Q(r15team__event_type="YellowCard")),
        )
        .order_by("-tries")
    )

    top_try_scorers = player_rankings.order_by("-tries")[:10]
    top_points_scorers = player_rankings.annotate(
        total_points=(F("tries") * 5)
        + (F("conversions") * 2)
        + (F("penalty_kicks") * 3)
        + (F("drop_goals") * 3)
    ).order_by("-total_points")[:10]
    top_tacklers = player_rankings.order_by("-tackles")[:10]
    most_yellow_cards = player_rankings.order_by("-yellow_cards")[:10]

    team_tries = team_rankings.order_by("-tries")[:10]
    team_points = team_rankings.annotate(
        total_points=(F("tries") * 5)
        + (F("conversions") * 2)
        + (F("penalty_kicks") * 3)
        + (F("drop_goals") * 3)
    ).order_by("-total_points")[:10]
    team_tackles = team_rankings.order_by("-tackles")[:10]
    team_yellow_cards = team_rankings.order_by("-yellow_cards")[:10]

    return {
        "player_rankings": player_rankings,
        "team_rankings": team_rankings,
        "top_try_scorers": top_try_scorers,
        "top_points_scorers": top_points_scorers,
        "top_tacklers": top_tacklers,
        "most_yellow_cards": most_yellow_cards,
        "team_tries": team_tries,
        "team_points": team_points,
        "team_tackles": team_tackles,
        "team_yellow_cards": team_yellow_cards,
    }


def Rug15s(request, id):
    competition = Rugby15s.objects.get(id=id)
    r15groups = R15Group.objects.filter(competition=competition)
    pending_fixtures = R15Fixture.objects.filter(
        competition=competition, status="Pending"
    ).order_by(F("group").asc(nulls_last=True), "date", "time")
    Results = R15Fixture.objects.filter(
        status="InPlay", competition=competition
    ).order_by(F("group").asc(nulls_last=True), "date", "time")
    rankings = get_rankings(competition)

    standings_data = {}
    groups = R15Group.objects.filter(competition=competition)

    for group in groups:
        standings = {
            team: {
                "p": 0,  # Played
                "w": 0,  # Won
                "d": 0,  # Drawn
                "l": 0,  # Lost
                "fs": 0,  # For Score (Points scored)
                "fa": 0,  # Against Score (Points conceded)
                "pd": 0,  # Point Difference
                "pts": 0,  # Total Points
            }
            for team in group.teams.all()
        }

        group_fixtures = R15Fixture.objects.filter(group=group)
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
                    if team in standings:
                        standings[team]["p"] += 1
                        standings[team]["fs"] += team_score
                        standings[team]["fa"] += opponent_score

                        if team_score > opponent_score:
                            standings[team]["w"] += 1
                            standings[team]["pts"] += 3
                        elif team_score < opponent_score:
                            standings[team]["l"] += 1
                        else:
                            standings[team]["d"] += 1
                            standings[team]["pts"] += 1

                        standings[team]["pd"] = (
                            standings[team]["fs"] - standings[team]["fa"]
                        )

        sorted_standings = sorted(
            standings.items(),
            key=lambda x: (x[1]["pts"], x[1]["pd"], x[1]["fs"]),
            reverse=True,
        )
        standings_data[group] = sorted_standings

    context = {
        "competition": competition,
        "r15groups": r15groups,
        "results": Results,
        "fixtures": pending_fixtures,
        "rankings": rankings,
        "standings_data": standings_data,
    }
    return render(request, "frontend/rugby15s.html", context)


def R15Groups(request):
    ngroups = R15Group.objects.all()

    context = {
        "ngroups": ngroups,
    }
    return render(request, "frontend/ngroups.html", context)


from django.db.models import Q


def FixtureDetail(request, id):
    fixture = get_object_or_404(R15Fixture, id=id)
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
    team1_fixtures = R15Fixture.objects.filter(
        Q(team1=fixture.team1) | Q(team2=fixture.team1)
    ).distinct()
    team2_fixtures = R15Fixture.objects.filter(
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

    return render(request, "frontend/r15fixture.html", context)


def R15Fixtures(request):
    fixtures = R15Fixture.objects.filter(status="InPlay").order_by("-date")
    context = {"fixtures": fixtures}
    return render(request, "frontend/rug15fixtures.html", context)


def R15Results(request):
    results = R15Fixture.objects.filter(status="InPlay").order_by("-date")
    context = {"results": results}
    return render(request, "frontend/rug15fixtures.html", context)


def rug15bollStandings(request):
    sports = Sport.objects.all()

    standings_data = []
    for sport in sports:
        rug15ball_competitions = Rugby15s.objects.filter(sport=sport)

        for rug15ball in rug15ball_competitions:
            groups = R15Group.objects.filter(competition=rug15ball)
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
                fixtures = R15Fixture.objects.filter(group=group)
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
                            standings[fixture.team1]["points"] += 2
                            standings[fixture.team1]["won"] += 1
                            standings[fixture.team2]["lost"] += 1
                        elif fixture.team1_score < fixture.team2_score:
                            standings[fixture.team2]["points"] += 2
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
                    "competition": rug15ball,
                    "standings": competition_standings,
                }
            )

    context = {
        "standings_data": standings_data,
    }

    return render(request, "frontend/rug15standings.html", context)
