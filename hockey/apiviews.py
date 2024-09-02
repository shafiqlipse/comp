from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Create your views here.
def getnet_teams(request):
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
    tournament = get_object_or_404(Hockey, id=id)

    # Get all teams associated with this tournament
    teams = tournament.teams.all()

    teams_list = [{"id": team.id, "name": team.school.name} for team in teams]

    return JsonResponse({"teams": teams_list})


def get_fixture_teams(request):
    competition_id = request.GET.get("competition")
    competition = Hockey.objects.get(id=competition_id)
    teams = competition.teams.all().values("id", "school__name")
    teams_list = list(teams)
    return JsonResponse({"teams": teams_list})


# def get_fixteams(request, id):
#     # Get the fixture object or return a 404 error if not found
#     fixture = get_object_or_404(Fixture, id=id)

#     # Get the team1 and team2 involved in the fixture
#     team1 = fixture.team1
#     team2 = fixture.team2

#     # Prepare the data to be returned in the response
#     data = {
#         "team1": {
#             "id": team1.id,
#             "school": team1.school.name,  # Assuming `school` has a `name` field
#         },
#         "team2": {
#             "id": team2.id,
#             "school": team2.school.name,  # Assuming `school` has a `name` field
#         },
#     }

#     # Return the data as a JSON response
#     return JsonResponse(data)


from django.http import JsonResponse
from accounts.models import Athlete


def get_nteams_for_match(request):
    match_id = request.GET.get("match_id")
    fixture = get_object_or_404(HoFixture, id=match_id)
    teams = [fixture.team1, fixture.team2]
    return JsonResponse(
        {"teams": [{"id": team.id, "name": str(team)} for team in teams]}
    )


def get_nathletes_for_team(request):
    team_id = request.GET.get("team_id")
    team = SchoolTeam.objects.get(id=team_id)
    athletes = team.athletes.all()
    return JsonResponse(
        {"athletes": [{"id": athlete.id, "name": str(athlete)} for athlete in athletes]}
    )
