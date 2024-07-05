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
def Busketball3(request):
    basketball3 = Sport.objects.get(name="Basketball3X3")
    b3comps = Basketball3.objects.filter(sport=basketball3)

    if request.method == "POST":
        cform = Co3mpForm(request.POST, request.FILES)

        if cform.is_valid():
            competn = cform.save(commit=False)
            competn.sport = basketball3
            competn.save()
            teams = cform.cleaned_data.get(
                "teams"
            )  # Replace 'athletes' with the actual form field name
            competn.teams.set(teams)
            competn.save()
            return HttpResponseRedirect(reverse("basketball3"))
    else:
        cform = Co3mpForm()

    # If form is invalid, re-render form with errors
    context = {"cform": cform, "b3comps": b3comps}
    return render(request, "server/basketball3.html", context)


# delete
def delete_basketball3(request, id):
    basketball3 = get_object_or_404(Basketball3, id=id)

    if request.method == "POST":
        basketball3.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_comp.html", {"basketball3": basketball3})


# view official details
from django.forms import inlineformset_factory


def b3tourn_details(request, id):
    tournament = get_object_or_404(Basketball3, id=id)
    fgroups = B3Group.objects.filter(competition=tournament)

    # Create a formset for editing existing groups
    GroupFormset = inlineformset_factory(
        Basketball3,
        B3Group,
        form=B3GroupForm,
        extra=0,  # Set extra=0 to prevent new group creation
    )

    if request.method == "POST":
        formset = GroupFormset(request.POST, instance=tournament)
        if formset.is_valid():
            formset.save()
            return redirect("basketball3_tournament", tournament.id)
    else:
        formset = GroupFormset(instance=tournament)

    if request.method == "POST":
        fixture_form = B3FixtureForm(request.POST)
        if fixture_form.is_valid():
            fixture = fixture_form.save(commit=False)
            fixture.basketball3 = tournament
            fixture.save()

            return redirect(
                "basketball3", tournament.id
            )  # Replace with the actual success URL name
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        fixture_form = B3FixtureForm()
    fixtures = B3Fixture.objects.filter(competition=tournament)
    context = {
        "tournament": tournament,
        "formset": formset,
        "fixtures": fixtures,
        "fgroups": fgroups,
    }
    return render(request, "server/b3tournament.html", context)


from datetime import datetime


def generate_b3fixtures_view(request, id):
    basketball3 = get_object_or_404(Basketball3, id=id)
    season = basketball3.season
    now = datetime.now()
    time = now.time()
    # Fetch all teams for the basketball3 (assuming you have a Team model)
    teams = SchoolTeam.objects.all()

    # Fetch all groups for the basketball3
    groups = B3Group.objects.filter(competition=basketball3)

    # Implement your fixture generation logic here
    fixtures = []
    for group in groups:
        group_teams = teams.filter(b3group=group)
        team_count = len(group_teams)

        # Simple round-robin algorithm for group stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = B3Fixture(
                    competition=basketball3,
                    season=season,
                    group=group,
                    round=1,
                    stage="Group",
                    date=now,
                    time=time,
                    team1=group_teams[i],
                    team2=group_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    B3Fixture.objects.bulk_create(fixtures)

    return JsonResponse(
        {"success": True, "message": "Basket Fixtures generated successfully"}
    )


def edit_fixtures_view(request, id):
    fixture = get_object_or_404(B3Fixture, id=id)

    if request.method == "POST":
        form = B3FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "b3fixture", id=id
            )  # Replace 'success_url' with the actual URL
    else:
        form = B3FixtureForm(instance=fixture)

    return render(
        request, "server/b3edit_fixture.html", {"form": form, "fixture": fixture}
    )


from django.db.models import Q


def FixtureDetail(request, id):
    fixture = get_object_or_404(B3Fixture, id=id)
    officials = match_official.objects.filter(fixture_id=id)
    events = MatchEvent.objects.filter(match_id=id)

    if request.method == "POST":
        if "official_form" in request.POST:
            cform = MatchOfficialForm(request.POST, request.FILES)
            eform = MatchEventForm()  # Initialize empty event form
            if cform.is_valid():
                new_official = cform.save(commit=False)
                new_official.fixture = fixture
                new_official.save()
                return redirect("b3fixture", id=id)
        elif "event_form" in request.POST:
            eform = MatchEventForm(request.POST, fixture_instance=fixture)
            cform = MatchOfficialForm()  # Initialize empty official form
            if eform.is_valid():
                new_event = eform.save(commit=False)
                new_event.match = fixture
                new_event.save()
                return redirect("b3fixture", id=id)
        else:
            cform = MatchOfficialForm()
            eform = MatchEventForm(
                fixture_instance=fixture
            )  # Initialize event form with fixture_instance
    else:
        cform = MatchOfficialForm()
        eform = MatchEventForm(
            fixture_instance=fixture
        )  # Initialize event form with fixture_instance

    context = {
        "fixture": fixture,
        "cform": cform,
        "eform": eform,
        "officials": officials,
        "events": events,
    }

    return render(request, "server/b3fixture.html", context)


def fixtures(request):
    fixtures = B3Fixture.objects.all().order_by("-date")
    context = {"fixtures": fixtures}
    return render(request, "server/b3fixtures.html", context)


def basketball3Standings(request):
    sports = Sport.objects.all()

    standings_data = []
    for sport in sports:
        basketball_competitions = Basketball3.objects.filter(sport=sport)

        for basketball in basketball_competitions:
            groups = B3Group.objects.filter(competition=basketball)
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
                fixtures = B3Fixture.objects.filter(group=group)
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

    return render(request, "server/b3standings.html", context)
