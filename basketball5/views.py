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


# Create your views here.
def Busketball5(request):
    basketball5 = Sport.objects.get(name="Basketball5X5")
    b5comps = Basketball5.objects.filter(sport=basketball5)

    if request.method == "POST":
        cform = Co3mpForm(request.POST, request.FILES)

        if cform.is_valid():
            competn = cform.save(commit=False)
            competn.sport = basketball5
            competn.save()
            return HttpResponseRedirect(reverse("basketball5"))
    else:
        cform = Co3mpForm()

    # If form is invalid, re-render form with errors
    context = {"cform": cform, "b5comps": b5comps}
    return render(request, "server/basketball5.html", context)


# delete
def delete_basketball5(request, id):
    basketball5 = get_object_or_404(Basketball5, id=id)

    if request.method == "POST":
        basketball5.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_comp.html", {"basketball5": basketball5})


# view official details
from django.forms import inlineformset_factory


def b5tourn_details(request, id):
    tournament = get_object_or_404(Basketball5, id=id)
    fgroups = B5Group.objects.filter(competition=tournament)

    # Create a formset for editing existing groups
    GroupFormset = inlineformset_factory(
        Basketball5,
        B5Group,
        form=B5GroupForm,
        extra=0,  # Set extra=0 to prevent new group creation
    )

    if request.method == "POST":
        formset = GroupFormset(request.POST, instance=tournament)
        if formset.is_valid():
            formset.save()
            return redirect("basketball5_tournament", tournament.id)
    else:
        formset = GroupFormset(instance=tournament)

    if request.method == "POST":
        fixture_form = B5FixtureForm(request.POST)
        if fixture_form.is_valid():
            fixture = fixture_form.save(commit=False)
            fixture.basketball5 = tournament
            fixture.save()

            return redirect(
                "basketball5", tournament.id
            )  # Replace with the actual success URL name
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        fixture_form = B5FixtureForm()
    fixtures = B5Fixture.objects.filter(competition=tournament)
    context = {
        "tournament": tournament,
        "formset": formset,
        "fixtures": fixtures,
        "fgroups": fgroups,
    }
    return render(request, "server/b5tournament.html", context)


def generate_b5fixtures_view(request, id):
    basketball5 = get_object_or_404(Basketball5, id=id)
    season = basketball5.season

    # Fetch all teams for the basketball5 (assuming you have a Team model)
    teams = SchoolTeam.objects.all()

    # Fetch all groups for the basketball5
    groups = B5Group.objects.filter(competition=basketball5)

    # Implement your fixture generation logic here
    fixtures = []
    for group in groups:
        group_teams = teams.filter(b5group=group)
        team_count = len(group_teams)

        # Simple round-robin algorithm for group stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = B5Fixture(
                    competition=basketball5,
                    season=season,
                    group=group,
                    team1=group_teams[i],
                    team2=group_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    B5Fixture.objects.bulk_create(fixtures)

    return JsonResponse(
        {"success": True, "message": "Basket Fixtures generated successfully"}
    )


def edit_fixtures_view(request, id):
    fixture = get_object_or_404(B5Fixture, id=id)

    if request.method == "POST":
        form = B5FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "fixture", id=id
            )  # Replace 'success_url' with the actual URL
    else:
        form = B5FixtureForm(instance=fixture)

    return render(
        request, "server/b5edit_fixture.html", {"form": form, "fixture": fixture}
    )


def FixtureDetail(request, id):
    fixture = get_object_or_404(B5Fixture, id=id)
    officials = match_official.objects.filter(fixture_id=id)
    events = MatchEvent.objects.filter(match_id=id)

    if request.method == "POST":

        eform = MatchEventForm(request.POST)
        if eform.is_valid():
            new_event = eform.save(commit=False)
            new_event.match = fixture
            new_event.save()
            return redirect("b5fixture", id=id)
    else:

        eform = MatchEventForm()

    context = {
        "fixture": fixture,
        "eform": eform,
        "officials": officials,
        "events": events,
    }

    return render(request, "server/b5fixture.html", context)


def fixtures(request):
    fixtures = B5Fixture.objects.all().order_by("-date")
    context = {"fixtures": fixtures}
    return render(request, "server/b5fixtures.html", context)


def basketball5Standings(request):
    sports = Sport.objects.all()

    standings_data = []
    for sport in sports:
        basketball_competitions = Basketball5.objects.filter(sport=sport)

        for basketball in basketball_competitions:
            groups = B5Group.objects.filter(competition=basketball)
            competition_standings = {}

            for group in groups:
                # Initialize standings with default values for all teams in the group
                standings = {}
                for team in group.teams.all():
                    standings[team] = {
                        "wins": 0,
                        "losses": 0,
                        "played": 0,
                        "pf": 0,  # Points For
                        "pa": 0,  # Points Against
                        "pd": 0,  # Point Differential
                    }

                # Update standings based on fixtures
                fixtures = B5Fixture.objects.filter(group=group)
                for fixture in fixtures:
                    if (
                        fixture.team1_score is not None
                        and fixture.team2_score is not None
                    ):
                        # Update played matches
                        standings[fixture.team1]["played"] += 1
                        standings[fixture.team2]["played"] += 1

                        # Update points for and points against
                        standings[fixture.team1]["pf"] += fixture.team1_score
                        standings[fixture.team2]["pf"] += fixture.team2_score
                        standings[fixture.team1]["pa"] += fixture.team2_score
                        standings[fixture.team2]["pa"] += fixture.team1_score

                        # Update match results
                        if fixture.team1_score > fixture.team2_score:
                            standings[fixture.team1]["wins"] += 1
                            standings[fixture.team2]["losses"] += 1
                        elif fixture.team1_score < fixture.team2_score:
                            standings[fixture.team2]["wins"] += 1
                            standings[fixture.team1]["losses"] += 1

                        # Update point differential
                        standings[fixture.team1]["pd"] = (
                            standings[fixture.team1]["pf"]
                            - standings[fixture.team1]["pa"]
                        )
                        standings[fixture.team2]["pd"] = (
                            standings[fixture.team2]["pf"]
                            - standings[fixture.team2]["pa"]
                        )

                # Calculate winning percentage and sort standings
                for team, stats in standings.items():
                    stats["win_percentage"] = (
                        stats["wins"] / stats["played"] if stats["played"] > 0 else 0
                    )

                sorted_standings = sorted(
                    standings.items(),
                    key=lambda x: (x[1]["win_percentage"], x[1]["pd"], x[1]["pf"]),
                    reverse=True,
                )
                competition_standings[group] = sorted_standings

            standings_data.append(
                {
                    "sport": sport,
                    "competition": basketball,
                    "standings": competition_standings,
                }
            )

    context = {
        "standings_data": standings_data,
    }

    return render(request, "server/b5standings.html", context)
