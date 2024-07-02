from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Create your views here.
def getfoot_teams(request):
    sport_id = request.GET.get("sport")
    gender = request.GET.get("gender")
    age = request.GET.get("age")

    print(f"Received: sport={sport_id}, gender={gender}, age={age}")

    teams = SchoolTeam.objects.all()

    if sport_id:
        teams = teams.filter(sport_id=sport_id)

    if gender:
        teams = teams.filter(gender=gender)

    if age:
        teams = teams.filter(age=age)

    teams = teams.values("id", "school__name")

    teams_list = [
        {"id": team["id"], "school_name": team["school__name"]} for team in teams
    ]

    data = {"teams": teams_list}

    return JsonResponse(data)


# Create your views here.
def getgroup_teams(request, id):
    tournament = get_object_or_404(Football, id=id)

    # Get all teams associated with this tournament
    teams = tournament.teams.all()

    teams_list = [{"id": team.id, "name": team.school.name} for team in teams]

    return JsonResponse({"teams": teams_list})


from django.http import JsonResponse
from accounts.models import Athlete


def get_teams_for_match(request):
    match_id = request.GET.get("match_id")
    fixture = get_object_or_404(Fixture, id=match_id)
    teams = [fixture.team1, fixture.team2]
    return JsonResponse(
        {"teams": [{"id": team.id, "name": str(team)} for team in teams]}
    )


from django.shortcuts import get_object_or_404


import logging

logger = logging.getLogger(__name__)


import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def get_athletes_for_team(request):
    match_id = request.GET.get("match_id")
    team_id = request.GET.get("team_id")

    logger.info(f"Received request for match_id: {match_id}, team_id: {team_id}")

    if not match_id or not team_id:
        logger.error("Missing match_id or team_id")
        return JsonResponse({"error": "Missing match_id or team_id"}, status=400)

    try:
        match = get_object_or_404(Fixture, id=match_id)
        team = get_object_or_404(SchoolTeam, id=team_id)

        logger.info(f"Match: {match}, Team: {team}")

        if team not in [match.team1, match.team2]:
            logger.warning(f"Team {team_id} is not part of match {match_id}")
            return JsonResponse({"error": "Selected team is not part of this match"}, status=400)

        athletes = team.athletes.all()

        athlete_data = [
            {"id": athlete.id, "name": f"{athlete.fname} {athlete.lname}"}
            for athlete in athletes
        ]
        logger.info(f"Found {len(athlete_data)} athletes for team {team_id}")
        logger.debug(f"Athlete data: {athlete_data}")

        return JsonResponse({"athletes": athlete_data})
    except Exception as e:
        logger.exception(f"Error processing request: {str(e)}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)
