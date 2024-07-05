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
def Hutball(request):
    handball = Sport.objects.get(name="Handball")
    fcomps = Handball.objects.filter(sport=handball)

    if request.method == "POST":
        cform = CompForm(request.POST, request.FILES)

        if cform.is_valid():
            competn = cform.save(commit=False)
            competn.sport = handball
            competn.save()
            teams = cform.cleaned_data.get(
                "teams"
            )  # Replace 'athletes' with the actual form field name
            competn.teams.set(teams)
            competn.save()
            return HttpResponseRedirect(reverse("handball"))
    else:
        cform = CompForm()

    # If form is invalid, re-render form with errors
    context = {"cform": cform, "fcomps": fcomps}
    return render(request, "server/handball.html", context)


# delete
def delete_handball(request, id):
    handball = get_object_or_404(Handball, id=id)

    if request.method == "POST":
        handball.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_comp.html", {"handball": handball})


# view official details
from django.forms import inlineformset_factory


def htourn_details(request, id):
    tournament = get_object_or_404(Handball, id=id)
    fgroups = HGroup.objects.filter(competition=tournament)

    # Create a formset for editing existing groups
    GroupFormset = inlineformset_factory(
        Handball,
        HGroup,
        form=HGroupForm,
        extra=0,  # Set extra=0 to prevent new group creation
    )

    if request.method == "POST":
        formset = GroupFormset(request.POST, instance=tournament)
        if formset.is_valid():
            formset.save()
            return redirect("handball_tournament", tournament.id)
    else:
        formset = GroupFormset(instance=tournament)

    if request.method == "POST":
        fixture_form = FixtureForm(request.POST)
        if fixture_form.is_valid():
            fixture = fixture_form.save(commit=False)
            fixture.handball = tournament
            fixture.save()

            return redirect(
                "handball", tournament.id
            )  # Replace with the actual success URL name
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        fixture_form = FixtureForm()
    fixtures = Fixture.objects.filter(competition=tournament)
    context = {
        "tournament": tournament,
        "formset": formset,
        "fixtures": fixtures,
        "fgroups": fgroups,
    }
    return render(request, "server/htournament.html", context)


from datetime import datetime


def generate_hfixtures_view(request, id):
    handball = get_object_or_404(Handball, id=id)
    season = handball.season
    now = datetime.now()
    time = now.time()
    # Fetch all teams for the handball (assuming you have a Team model)
    teams = SchoolTeam.objects.all()

    # Fetch all groups for the handball
    groups = HGroup.objects.filter(competition=handball)

    # Implement your fixture generation logic here
    fixtures = []
    for group in groups:
        group_teams = teams.filter(hgroup=group)
        team_count = len(group_teams)

        # Simple round-robin algorithm for group stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = Fixture(
                    competition=handball,
                    season=season,
                    group=group,
                    stage="Group",
                    date=now,
                    time=time,
                    team1=group_teams[i],
                    team2=group_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    Fixture.objects.bulk_create(fixtures)

    return JsonResponse({"success": True, "message": "Fixtures generated successfully"})


def edit_fixtures_view(request, id):
    fixture = get_object_or_404(Fixture, id=id)

    if request.method == "POST":
        form = FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "hfixture", id=id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "server/hedit_fixture.html", {"form": form, "fixture": fixture}
    )


from django.db.models import Q


from django.db.models import Q


def FixtureDetail(request, id):
    fixture = get_object_or_404(Fixture, id=id)
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
                return redirect("hfixture", id=id)
        elif "event_form" in request.POST:
            eform = MatchEventForm(request.POST, fixture_instance=fixture)
            cform = MatchOfficialForm()  # Initialize empty official form
            if eform.is_valid():
                new_event = eform.save(commit=False)
                new_event.match = fixture
                new_event.save()
                return redirect("hfixture", id=id)
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

    return render(request, "server/hfixture.html", context)


def fixtures(request):
    fixtures = Fixture.objects.filter(competition_id=4).order_by("-date")
    context = {"fixtures": fixtures}
    return render(request, "server/hfixtures.html", context)


def handballStandings(request):
    sports = Sport.objects.all()

    standings_data = []
    for sport in sports:
        handball_competitions = Handball.objects.filter(sport=sport)

        for handball in handball_competitions:
            groups = HGroup.objects.filter(competition=handball)
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
                        "gd": 0,  # Goal Difference
                        "gs": 0,  # Goals Scored
                        "gc": 0,  # Goals Conceded
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
                            standings[fixture.team1]["points"] += 3
                            standings[fixture.team1]["won"] += 1
                            standings[fixture.team2]["lost"] += 1
                        elif fixture.team1_score < fixture.team2_score:
                            standings[fixture.team2]["points"] += 3
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
                    "competition": handball,
                    "standings": competition_standings,
                }
            )

    context = {
        "standings_data": standings_data,
    }

    return render(request, "server/hstandings.html", context)


from django.shortcuts import render
from .models import Sport, Handball, HGroup, Fixture


def generate_next_round_fixtures(request):
    sports = Sport.objects.all()
    next_round_fixtures = []

    for sport in sports:
        handball_competitions = Handball.objects.filter(sport=sport)

        for handball in handball_competitions:
            groups = HGroup.objects.filter(competition=handball)
            competition_standings = {}

            group_winners_runners_up = {}

            for group in groups:
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

                fixtures = Fixture.objects.filter(group=group)
                for fixture in fixtures:
                    if (
                        fixture.team1_score is not None
                        and fixture.team2_score is not None
                    ):
                        standings[fixture.team1]["played"] += 1
                        standings[fixture.team2]["played"] += 1
                        standings[fixture.team1]["gs"] += fixture.team1_score
                        standings[fixture.team2]["gs"] += fixture.team2_score
                        standings[fixture.team1]["gc"] += fixture.team2_score
                        standings[fixture.team2]["gc"] += fixture.team1_score

                        if fixture.team1_score > fixture.team2_score:
                            standings[fixture.team1]["points"] += 3
                            standings[fixture.team1]["won"] += 1
                            standings[fixture.team2]["lost"] += 1
                        elif fixture.team1_score < fixture.team2_score:
                            standings[fixture.team2]["points"] += 3
                            standings[fixture.team2]["won"] += 1
                            standings[fixture.team1]["lost"] += 1
                        else:
                            standings[fixture.team1]["points"] += 1
                            standings[fixture.team2]["points"] += 1
                            standings[fixture.team1]["drawn"] += 1
                            standings[fixture.team2]["drawn"] += 1

                        standings[fixture.team1]["gd"] = (
                            standings[fixture.team1]["gs"]
                            - standings[fixture.team1]["gc"]
                        )
                        standings[fixture.team2]["gd"] = (
                            standings[fixture.team2]["gs"]
                            - standings[fixture.team2]["gc"]
                        )

                sorted_standings = sorted(
                    standings.items(),
                    key=lambda x: (x[1]["points"], x[1]["gd"], x[1]["gs"]),
                    reverse=True,
                )
                competition_standings[group] = sorted_standings

                if len(sorted_standings) >= 2:
                    group_winners_runners_up[group] = {
                        "winner": sorted_standings[0][0],
                        "runner_up": sorted_standings[1][0],
                    }

            current_round_fixtures = []
            group_keys = list(group_winners_runners_up.keys())

            while len(group_keys) > 1:
                new_group_winners_runners_up = {}
                for i in range(0, len(group_keys), 2):
                    if i + 1 < len(group_keys):
                        group1 = group_keys[i]
                        group2 = group_keys[i + 1]

                        # Ensure both groups have a runner-up before generating fixtures
                        if (
                            "runner_up" in group_winners_runners_up[group1]
                            and "runner_up" in group_winners_runners_up[group2]
                        ):
                            match1 = {
                                "team1": group_winners_runners_up[group1]["winner"],
                                "team2": group_winners_runners_up[group2]["runner_up"],
                            }
                            match2 = {
                                "team1": group_winners_runners_up[group2]["winner"],
                                "team2": group_winners_runners_up[group1]["runner_up"],
                            }
                            current_round_fixtures.append(match1)
                            current_round_fixtures.append(match2)

                            new_group_winners_runners_up[group1] = {
                                "winner": match1["team1"]
                            }  # Mock winner for the next round
                            new_group_winners_runners_up[group2] = {
                                "winner": match2["team1"]
                            }  # Mock winner for the next round

                next_round_fixtures.append(current_round_fixtures)
                group_keys = list(new_group_winners_runners_up.keys())
                group_winners_runners_up = new_group_winners_runners_up
                current_round_fixtures = []

    context = {
        "next_round_fixtures": next_round_fixtures,
    }

    return render(request, "server/ntournament.html", context)
