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


def Nhome(request):

    context = {}
    return render(request, "frontend/nhome.html", context)


from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce
from django.db.models import F


def get_rankings(competition):
    # Athlete Rankings
    athlete_rankings = (
        Athlete.objects.filter(nathlete__match__competition=competition)
        .annotate(
            goals=Count("nathlete", filter=Q(nathlete__event_type="Goal")),
            intercepts=Count("nathlete", filter=Q(nathlete__event_type="Intercept")),
            turnovers=Count("nathlete", filter=Q(nathlete__event_type="Turnover")),
            penalties=Count("nathlete", filter=Q(nathlete__event_type="Penalty")),
        )
        .order_by("-goals", "-intercepts")
    )

    # Team Rankings
    team_rankings = (
        SchoolTeam.objects.filter(nteam__match__competition=competition)
        .annotate(
            goals=Count("nteam", filter=Q(nteam__event_type="Goal")),
            intercepts=Count("nteam", filter=Q(nteam__event_type="Intercept")),
            turnovers=Count("nteam", filter=Q(nteam__event_type="Turnover")),
            penalties=Count("nteam", filter=Q(nteam__event_type="Penalty")),
        )
        .order_by("-goals")
    )

    top_scorers = athlete_rankings.order_by("-goals")[:10]
    top_interceptors = athlete_rankings.order_by("-intercepts")[:10]
    most_turnovers = athlete_rankings.order_by("-turnovers")[:10]
    most_penalties = athlete_rankings.order_by("-penalties")[:10]

    team_goals = team_rankings.order_by("-goals")[:10]
    team_intercepts = team_rankings.order_by("-intercepts")[:10]
    team_turnovers = team_rankings.order_by("-turnovers")[:10]
    team_penalties = team_rankings.order_by("-penalties")[:10]

    return {
        "athlete_rankings": athlete_rankings,
        "team_rankings": team_rankings,
        "top_scorers": top_scorers,
        "top_interceptors": top_interceptors,
        "most_turnovers": most_turnovers,
        "most_penalties": most_penalties,
        "team_goals": team_goals,
        "team_intercepts": team_intercepts,
        "team_turnovers": team_turnovers,
        "team_penalties": team_penalties,
    }


def Nutbol(request, id):
    competition = Netball.objects.get(id=id)
    ngroups = NGroup.objects.filter(competition=competition)
    pending_fixtures = Fixture.objects.filter(
        competition=competition, status="Pending"
    ).order_by(F("group").asc(nulls_last=True), "date", "time")
    results = Fixture.objects.filter(status="InPlay", competition=competition).order_by(
        "date"
    )
    rankings = get_rankings(competition)

    standings_data = {}
    groups = NGroup.objects.filter(competition=competition)

    for group in groups:
        standings = {
            team: {
                "points": 0,
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "gd": 0,
                "gs": 0,
                "gc": 0,
            }
            for team in group.teams.all()
        }

        group_fixtures = Fixture.objects.filter(group=group)
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
                        standings[team]["played"] += 1
                        standings[team]["gs"] += team_score
                        standings[team]["gc"] += opponent_score

                        if team_score > opponent_score:
                            standings[team]["points"] += 2
                            standings[team]["won"] += 1
                        elif team_score < opponent_score:
                            standings[team]["lost"] += 1
                        else:
                            standings[team]["points"] += 1
                            standings[team]["drawn"] += 1

                        standings[team]["gd"] = (
                            standings[team]["gs"] - standings[team]["gc"]
                        )

        sorted_standings = sorted(
            standings.items(),
            key=lambda x: (x[1]["points"], x[1]["gd"], x[1]["gs"]),
            reverse=True,
        )
        standings_data[group] = sorted_standings

    context = {
        "competition": competition,
        "ngroups": ngroups,
        "results": results,
        "fixtures": pending_fixtures,
        "rankings": rankings,
        "standings_data": standings_data,
    }
    return render(request, "frontend/netball.html", context)


def NGroups(request):
    ngroups = NGroup.objects.all()

    context = {
        "ngroups": ngroups,
    }
    return render(request, "frontend/ngroups.html", context)


from django.db.models import Q


def FixtureDetail(request, id):
    fixture = get_object_or_404(Fixture, id=id)
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
    team1_fixtures = Fixture.objects.filter(
        Q(team1=fixture.team1) | Q(team2=fixture.team1)
    ).distinct()
    team2_fixtures = Fixture.objects.filter(
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

    return render(request, "frontend/nfixture.html", context)


def NFixtures(request):
    fixtures = Fixture.objects.filter(status="InPlay").order_by("-date")
    context = {"fixtures": fixtures}
    return render(request, "frontend/netfixtures.html", context)


def NResults(request):
    results = Fixture.objects.filter(status="InPlay").order_by("-date")
    context = {"results": results}
    return render(request, "frontend/netfixtures.html", context)


def netbollStandings(request):
    sports = Sport.objects.all()

    standings_data = []
    for sport in sports:
        netball_competitions = Netball.objects.filter(sport=sport)

        for netball in netball_competitions:
            groups = NGroup.objects.filter(competition=netball)
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
                fixtures = Fixture.objects.filter(group=group)
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
                    "competition": netball,
                    "standings": competition_standings,
                }
            )

    context = {
        "standings_data": standings_data,
    }

    return render(request, "frontend/netstandings.html", context)
