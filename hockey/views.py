from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from accounts.decorators import *
from accounts.models import Sport
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db import connection

# template


# Create your views here.
@school_required
def Hotball(request):
    hockey = Sport.objects.get(name="Hockey")
    fcomps = Hockey.objects.filter(sport=hockey)

    if request.method == "POST":
        cform = CompForm(request.POST, request.FILES)

        if cform.is_valid():
            competn = cform.save(commit=False)
            competn.sport = hockey
            competn.save()
            teams = cform.cleaned_data.get(
                "teams"
            )  # Replace 'athletes' with the actual form field name
            competn.teams.set(teams)
            competn.save()
            return HttpResponseRedirect(reverse("hockey"))
    else:
        cform = CompForm()

    # If form is invalid, re-render form with errors
    context = {"cform": cform, "fcomps": fcomps}
    return render(request, "server/hockey.html", context)


# Create your views here.
@school_required
def delete_hockey(request, id):
    hockey = get_object_or_404(Hockey, id=id)

    if request.method == "POST":
        hockey.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_comp.html", {"hockey": hockey})


# view official details
from django.forms import inlineformset_factory


# Create your views here.
@school_required
def hotourn_details(request, id):
    tournament = get_object_or_404(Hockey, id=id)
    fgroups = HoGroup.objects.filter(competition=tournament)

    GroupFormset = inlineformset_factory(
        Hockey,
        HoGroup,
        form=HoGroupForm,
        extra=0,
    )

    if request.method == "POST":
        formset = GroupFormset(request.POST, instance=tournament)
        if formset.is_valid():
            formset.save()
            return redirect("hockey_tournament", tournament.id)

        fixture_form = FixtureForm(request.POST)
        if fixture_form.is_valid():
            fixture = fixture_form.save(commit=False)
            fixture.football = tournament
            fixture.save()
            return redirect("hockey_tournament", tournament.id)
        else:
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        formset = GroupFormset(instance=tournament)
        fixture_form = FixtureForm()

    fixtures = HoFixture.objects.filter(competition=tournament)
    results = HoFixture.objects.filter(competition=tournament, status="InPlay")

    context = {
        "tournament": tournament,
        "formset": formset,
        "fixture_form": fixture_form,
        "fixtures": fixtures,
        "results": results,
        "fgroups": fgroups,
    }
    return render(request, "server/hotournament.html", context)


from datetime import datetime


# Create your views here.
@school_required
def generate_hofixtures_view(request, id):
    hockey = get_object_or_404(Hockey, id=id)
    season = hockey.season
    now = datetime.now()
    time = now.time()
    # Fetch all teams for the hockey (assuming you have a Team model)
    teams = SchoolTeam.objects.all()

    # Fetch all groups for the hockey
    groups = HoGroup.objects.filter(competition=hockey)

    # Implement your fixture generation logic here
    fixtures = []
    for group in groups:
        group_teams = teams.filter(hogroup=group)
        team_count = len(group_teams)

        # Simple round-robin algorithm for group stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = HoFixture(
                    competition=hockey,
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
    HoFixture.objects.bulk_create(fixtures)

    return JsonResponse({"success": True, "message": "Fixtures generated successfully"})


def edit_hofixtures_view(request, id):
    fixture = get_object_or_404(HoFixture, id=id)

    if request.method == "POST":
        form = FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "hofixture", id=id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "server/hoedit_fixture.html", {"form": form, "fixture": fixture}
    )


from django.db.models import Q


def HoFixtureDetail(request, id):
    fixture = get_object_or_404(HoFixture, id=id)
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
                return redirect("hofixture", id=id)
        elif "event_form" in request.POST:
            eform = MatchEventForm(request.POST, fixture_instance=fixture)
            cform = MatchOfficialForm()  # Initialize empty official form
            if eform.is_valid():
                new_event = eform.save(commit=False)
                new_event.match = fixture
                new_event.save()
                return redirect("hofixture", id=id)
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

    return render(request, "server/hofixture.html", context)


# Create your views here.
@school_required
def fixtures(request):
    fixtures = HoFixture.objects.filter(competition_id=4).order_by("-date")
    context = {"fixtures": fixtures}
    return render(request, "server/hofixtures.html", context)


def hockeyStandings(request):
    sports = Sport.objects.all()

    standings_data = []
    for sport in sports:
        hockey_competitions = Hockey.objects.filter(sport=sport)

        for hockey in hockey_competitions:
            groups = HoGroup.objects.filter(competition=hockey)
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
                fixtures = HoFixture.objects.filter(group=group)
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
                    "competition": hockey,
                    "standings": competition_standings,
                }
            )

    context = {
        "standings_data": standings_data,
    }

    return render(request, "server/hostandings.html", context)


from django.shortcuts import render


from .models import Sport, Hockey, HoGroup, HoFixture


def generate_next_round_fixtures(request):
    sports = Sport.objects.all()
    next_round_fixtures = []

    for sport in sports:
        hockey_competitions = Hockey.objects.filter(sport=sport)

        for hockey in hockey_competitions:
            groups = HoGroup.objects.filter(competition=hockey)
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

                fixtures = HoFixture.objects.filter(group=group)
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

    return render(request, "server/hotournament.html", context)


def netfixtures(request):
    fixures = HoFixture.objects.all()
    context = {"fixures": fixures}
    return render(request, "frontend/hotfixtures.html", context)


def create_nfixture(request):
    if request.method == "POST":
        fixture_form = FixtureForm(request.POST)
        if fixture_form.is_valid():
            fixture = fixture_form.save(commit=False)

            # Set the season (e.g., get the current season)
            current_season = Season.objects.get(id=1)
            fixture.season = current_season

            # Set the competition (e.g., get a specific competition)
            hockey_competition = Hockey.objects.get(id=1)
            fixture.competition = hockey_competition

            fixture.save()
            messages.success(
                request, f"Fixture {fixture.id} has been created successfully."
            )
            return redirect(
                "fixture_list"
            )  # Replace with your actual fixture list URL name
    else:
        fixture_form = FixtureForm()

    return render(request, "server/create_fixture.html", {"fixture_form": fixture_form})
