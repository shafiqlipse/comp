from django.shortcuts import render, redirect, get_object_or_404


from .forms import *
from .models import *

from accounts.models import Sport
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.db.models import Count, Q
from django.db import connection

# template


def get_rankings(competition):
    # Athlete Rankings
    athlete_rankings = (
        Athlete.objects.filter(vathlete__match__competition=competition)
        .annotate(
            kills=Count("vathlete", filter=Q(vathlete__event_type="Kill")),
            aces=Count("vathlete", filter=Q(vathlete__event_type="Ace")),
            blocks=Count("vathlete", filter=Q(vathlete__event_type="Block")),
            digs=Count("vathlete", filter=Q(vathlete__event_type="Dig")),
            sets=Count("vathlete", filter=Q(vathlete__event_type="Set")),
        )
        .order_by("-kills", "-aces")
    )

    # Team Rankings
    team_rankings = (
        SchoolTeam.objects.filter(vteam__match__competition=competition)
        .annotate(
            kills=Count("vteam", filter=Q(vteam__event_type="Kill")),
            aces=Count("vteam", filter=Q(vteam__event_type="Ace")),
            blocks=Count("vteam", filter=Q(vteam__event_type="Block")),
            digs=Count("vteam", filter=Q(vteam__event_type="Dig")),
            sets=Count("vteam", filter=Q(vteam__event_type="Set")),
        )
        .order_by("-kills")
    )

    top_killers = athlete_rankings.order_by("-kills")[:10]
    top_servers = athlete_rankings.order_by("-aces")[:10]
    top_blockers = athlete_rankings.order_by("-blocks")[:10]
    top_diggers = athlete_rankings.order_by("-digs")[:10]
    top_setters = athlete_rankings.order_by("-sets")[:10]

    team_kills = team_rankings.order_by("-kills")[:10]
    team_aces = team_rankings.order_by("-aces")[:10]
    team_blocks = team_rankings.order_by("-blocks")[:10]
    team_digs = team_rankings.order_by("-digs")[:10]

    return {
        "athlete_rankings": athlete_rankings,
        "team_rankings": team_rankings,
    }


def Volbol(request, id):
    competition = Volleyball.objects.get(id=id)
    vgroups = VGroup.objects.filter(competition=competition)
    pending_fixtures = Fixture.objects.filter(
        status="Pending", competition=competition
    ).order_by("date")
    results = Fixture.objects.filter(status="InPlay", competition=competition).order_by(
        "date"
    )
    rankings = get_rankings(competition)

    standings_data = {}
    groups = VGroup.objects.filter(competition=competition)

    for group in groups:
        standings = {
            team: {
                "points": 0,
                "played": 0,
                "won": 0,
                "lost": 0,
                "sets_won": 0,
                "sets_lost": 0,
                "points_for": 0,
                "points_against": 0,
                "set_ratio": 0,
                "point_ratio": 0,
            }
            for team in group.teams.all()
        }

        group_fixtures = Fixture.objects.filter(group=group)
        for fixture in group_fixtures:
            if fixture.team1_score is not None and fixture.team2_score is not None:
                standings[fixture.team1]["played"] += 1
                standings[fixture.team2]["played"] += 1

                standings[fixture.team1]["points_for"] += fixture.team1_score or 0
                standings[fixture.team2]["points_for"] += fixture.team2_score or 0
                standings[fixture.team1]["points_against"] += fixture.team2_score or 0
                standings[fixture.team2]["points_against"] += fixture.team1_score or 0

                standings[fixture.team1]["sets_won"] += fixture.team1_sets_won or 0
                standings[fixture.team2]["sets_won"] += fixture.team2_sets_won or 0
                standings[fixture.team1]["sets_lost"] += fixture.team2_sets_won or 0
                standings[fixture.team2]["sets_lost"] += fixture.team1_sets_won or 0

                if (fixture.team1_sets_won or 0) > (fixture.team2_sets_won or 0):
                    standings[fixture.team1]["points"] += 3
                    standings[fixture.team1]["won"] += 1
                    standings[fixture.team2]["lost"] += 1
                elif (fixture.team1_sets_won or 0) < (fixture.team2_sets_won or 0):
                    standings[fixture.team2]["points"] += 3
                    standings[fixture.team2]["won"] += 1
                    standings[fixture.team1]["lost"] += 1

        for team, stats in standings.items():
            stats["set_ratio"] = stats["sets_won"] / max(stats["sets_lost"], 1)
            stats["point_ratio"] = stats["points_for"] / max(stats["points_against"], 1)

        sorted_standings = sorted(
            standings.items(),
            key=lambda x: (
                x[1]["points"],
                x[1]["set_ratio"],
                x[1]["point_ratio"],
                x[1]["sets_won"],
                x[1]["points_for"],
            ),
            reverse=True,
        )
        standings_data[group] = sorted_standings

    context = {
        "competition": competition,
        "vgroups": vgroups,
        "results": results,
        "fixtures": pending_fixtures,
        "rankings": rankings,
        "standings_data": standings_data,
    }
    return render(request, "frontend/volleyball.html", context)


def Vhome(request):

    context = {}
    return render(request, "frontend/vhome.html", context)
