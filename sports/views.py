from django.shortcuts import render, redirect
from accounts.models import Sport
from dashboard.models import *
from dashboard.forms import *
from .forms import *


# Create your views here.
def Sports(request):
    sports = Sport.objects.all()
    if request.method == "POST":
        tform = sportForm(request.POST, request.FILES)

        if tform.is_valid():
            tform.save()
            return redirect("sports")
    else:
        tform = sportForm()
    context = {"sports": sports, "tform": tform}
    return render(request, "sport/sports.html", context)


def SportDetail(request, id):
    sport = Sport.objects.get(id=id)

    tournaments = Competition.objects.filter(sport=sport)
    new_tournament = None

    if request.method == "POST":
        tform = tournamentForm(request.POST, request.FILES)

        if tform.is_valid():
            new_tournament = tform.save(commit=False)
            new_tournament.sport = sport

            new_tournament.save()
            return redirect("champDetail", sport.id)
    else:
        tform = tournamentForm()

    context = {
        "sport": sport,
        "tournaments": tournaments,
        "tform": tform,
    }

    return render(request, "sport/sport.html", context)
