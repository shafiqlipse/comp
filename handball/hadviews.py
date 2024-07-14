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
from django.db.models import F

def get_rankings(competition):
    # Athlete Rankings
    athlete_rankings = (
        Athlete.objects.filter(hathlete__match__competition=competition)
        .annotate(
            goals=Count("hathlete", filter=Q(hathlete__event_type="Goal")),
            assists=Count("hathlete", filter=Q(hathlete__event_type="Assist")),
            saves=Count("hathlete", filter=Q(hathlete__event_type="Save")),
            yellow_cards=Count(
                "hathlete", filter=Q(hathlete__event_type="Yellow Card")
            ),
            red_cards=Count("hathlete", filter=Q(hathlete__event_type="Red Card")),
            suspensions=Count("hathlete", filter=Q(hathlete__event_type="Suspension")),
            blocks=Count("hathlete", filter=Q(hathlete__event_type="Block")),
            interceptions=Count(
                "hathlete", filter=Q(hathlete__event_type="Interception")
            ),
        )
        .order_by("-goals", "-assists")
    )

    # Team Rankings
    team_rankings = (
        SchoolTeam.objects.filter(hteam__match__competition=competition)
        .annotate(
            goals=Count("hteam", filter=Q(hteam__event_type="Goal")),
            assists=Count("hteam", filter=Q(hteam__event_type="Assist")),
            saves=Count("hteam", filter=Q(hteam__event_type="Save")),
            yellow_cards=Count("hteam", filter=Q(hteam__event_type="Yellow Card")),
            red_cards=Count("hteam", filter=Q(hteam__event_type="Red Card")),
            suspensions=Count("hteam", filter=Q(hteam__event_type="Suspension")),
            blocks=Count("hteam", filter=Q(hteam__event_type="Block")),
            interceptions=Count("hteam", filter=Q(hteam__event_type="Interception")),
        )
        .order_by("-goals")
    )

    top_scorers = athlete_rankings.order_by("-goals")[:10]
    top_assisters = athlete_rankings.order_by("-assists")[:10]
    top_goalkeepers = athlete_rankings.order_by("-saves")[:10]
    most_yellow_cards = athlete_rankings.order_by("-yellow_cards")[:10]
    most_red_cards = athlete_rankings.order_by("-red_cards")[:10]
    most_suspensions = athlete_rankings.order_by("-suspensions")[:10]
    top_blockers = athlete_rankings.order_by("-blocks")[:10]
    top_interceptors = athlete_rankings.order_by("-interceptions")[:10]

    team_goals = team_rankings.order_by("-goals")[:10]
    team_assists = team_rankings.order_by("-assists")[:10]
    team_saves = team_rankings.order_by("-saves")[:10]
    team_yellow_cards = team_rankings.order_by("-yellow_cards")[:10]
    team_red_cards = team_rankings.order_by("-red_cards")[:10]
    team_suspensions = team_rankings.order_by("-suspensions")[:10]
    team_blocks = team_rankings.order_by("-blocks")[:10]
    team_interceptions = team_rankings.order_by("-interceptions")[:10]

    return {
        "athlete_rankings": athlete_rankings,
        "team_rankings": team_rankings,
        "top_scorers": top_scorers,
        "top_assisters": top_assisters,
        "top_goalkeepers": top_goalkeepers,
        "most_yellow_cards": most_yellow_cards,
        "most_red_cards": most_red_cards,
        "most_suspensions": most_suspensions,
        "top_blockers": top_blockers,
        "top_interceptors": top_interceptors,
        "team_goals": team_goals,
        "team_assists": team_assists,
        "team_saves": team_saves,
        "team_yellow_cards": team_yellow_cards,
        "team_red_cards": team_red_cards,
        "team_suspensions": team_suspensions,
        "team_blocks": team_blocks,
        "team_interceptions": team_interceptions,
    }


from django.shortcuts import render
from .models import Handball, HGroup, Fixture


def Handbol(request, id):
    competition = Handball.objects.get(id=id)
    hgroups = HGroup.objects.filter(competition=competition)
    pending_fixtures = Fixture.objects.filter(competition=competition).order_by(
        F("group").asc(nulls_last=True), "date", "time"
    )
    results = Fixture.objects.filter(status="InPlay", competition=competition).order_by(
        "date"
    )
    rankings = get_rankings(competition)

    standings_data = {}
    groups = HGroup.objects.filter(competition=competition)

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
                    standings[team]["played"] += 1
                    standings[team]["gs"] += team_score
                    standings[team]["gc"] += opponent_score

                    if team_score > opponent_score:
                        standings[team]["points"] += 2  # 2 points for a win in handball
                        standings[team]["won"] += 1
                    elif team_score < opponent_score:
                        standings[team]["lost"] += 1
                    else:
                        standings[team]["points"] += 1  # 1 point for a draw
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
        "hgroups": hgroups,
        "results": results,
        "fixtures": pending_fixtures,
        "rankings": rankings,
        "standings_data": standings_data,
    }
    return render(request, "frontend/handball.html", context)


from django.db.models import Q


def HFixtureDetail(request, id):
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

    return render(request, "frontend/fixture.html", context)


def Hhome(request):

    context = {}
    return render(request, "frontend/hhome.html", context)
