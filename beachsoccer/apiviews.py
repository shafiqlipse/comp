from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.


def get_fixteams(request, id):
    # Get the fixture object or return a 404 error if not found
    fixture = get_object_or_404(Fixture, id=id)

    # Get the team1 and team2 involved in the fixture
    team1 = fixture.team1
    team2 = fixture.team2

    # Prepare the data to be returned in the response
    data = {
        "team1": {
            "id": team1.id,
            "school": team1.school.name,  # Assuming `school` has a `name` field
        },
        "team2": {
            "id": team2.id,
            "school": team2.school.name,  # Assuming `school` has a `name` field
        },
    }

    # Return the data as a JSON response
    return JsonResponse(data)
