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
def Beaches(request):
    beachsoccer = Sport.objects.get(name="Beachsoccer")
    fcomps = Beachsoccer.objects.filter(sport=beachsoccer)

    if request.method == "POST":
        cform = CompForm(request.POST, request.FILES)

        if cform.is_valid():
            competn = cform.save(commit=False)
            competn.sport = beachsoccer
            competn.save()
            teams = cform.cleaned_data.get(
                "teams"
            )  # Replace 'athletes' with the actual form field name
            competn.teams.set(teams)
            competn.save()
            return HttpResponseRedirect(reverse("beachsoccer"))
    else:
        cform = CompForm()

    # If form is invalid, re-render form with errors
    context = {"cform": cform, "fcomps": fcomps}
    return render(request, "server/beachsoccer.html", context)


# delete
def delete_beachsoccer(request, id):
    beachsoccer = get_object_or_404(Beachsoccer, id=id)

    if request.method == "POST":
        beachsoccer.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_comp.html", {"beachsoccer": beachsoccer})


# view official details
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import inlineformset_factory
from django.http import JsonResponse
from .models import Beachsoccer, BSGroup, BSFixture
from .forms import BSGroupForm, FixtureForm


def bstourn_details(request, id):
    tournament = get_object_or_404(Beachsoccer, id=id)
    bsgroups = BSGroup.objects.filter(competition=tournament)

    GroupFormset = inlineformset_factory(
        Beachsoccer,
        BSGroup,
        form=BSGroupForm,
        extra=0,
    )

    if request.method == "POST":
        formset = GroupFormset(request.POST, instance=tournament)
        if formset.is_valid():
            formset.save()
            return redirect("beachsoccer_tournament", tournament.id)

        fixture_form = FixtureForm(request.POST)
        if fixture_form.is_valid():
            fixture = fixture_form.save(commit=False)
            fixture.beachsoccer = tournament
            fixture.save()
            return redirect("beachsoccer_tournament", tournament.id)
        else:
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        formset = GroupFormset(instance=tournament)
        fixture_form = FixtureForm()

    fixtures = BSFixture.objects.filter(competition=tournament)

    context = {
        "tournament": tournament,
        "formset": formset,
        "fixture_form": fixture_form,
        "fixtures": fixtures,
        "fgroups": bsgroups,
    }
    return render(request, "server/bstournament.html", context)


from datetime import datetime


def generate_bsfixtures_view(request, id):
    beachsoccer = get_object_or_404(Beachsoccer, id=id)
    season = beachsoccer.season
    now = datetime.now()

    time = now.time()
    # Fetch all teams for the beachsoccer (assuming you have a Team model)
    teams = SchoolTeam.objects.all()

    # Fetch all groups for the beachsoccer
    groups = BSGroup.objects.filter(competition=beachsoccer)

    # Implement your fixture generation logic here
    fixtures = []
    for group in groups:
        group_teams = teams.filter(bsgroup=group)
        team_count = group_teams.count()

        # Simple round-robin algorithm for group stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = BSFixture(
                    competition=beachsoccer,
                    season=season,
                    round=1,
                    group=group,
                    stage="Group",
                    date=now,  # Capturing the current date and time
                    time=time,  # Capturing the current date and time
                    team1=group_teams[i],
                    team2=group_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    BSFixture.objects.bulk_create(fixtures)

    return JsonResponse({"success": True, "message": "Fixtures generated successfully"})


def edit_bsfixtures_view(request, id):
    fixture = get_object_or_404(BSFixture, id=id)

    if request.method == "POST":
        form = FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "update_bsfixture", id=id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "server/edit_bsfixture.html", {"form": form, "fixture": fixture}
    )


from django.db.models import Q


def BsFixtureDetail(request, id):
    fixture = get_object_or_404(BSFixture, id=id)
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
                return redirect("bsfixture", id=id)
        elif "event_form" in request.POST:
            eform = MatchEventForm(request.POST, fixture_instance=fixture)
            cform = MatchOfficialForm()  # Initialize empty official form
            if eform.is_valid():
                new_event = eform.save(commit=False)
                new_event.match = fixture
                new_event.save()
                return redirect("bsfixture", id=id)
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

    return render(request, "server/bsfixture.html", context)
    # team1_yellowcards = events.filter(
    #     event_type="YellowCard", team=fixture.team1
    # ).count()
    # team2_yellowcards = events.filter(
    #     event_type="YellowCard", team=fixture.team2
    # ).count()
    # team1_redcards = events.filter(event_type="RedCard", team=fixture.team1).count()
    # team2_redcards = events.filter(event_type="RedCard", team=fixture.team2).count()
    # team1_goals = events.filter(event_type="Goal", team=fixture.team1).count()
    # team2_goals = events.filter(event_type="Goal", team=fixture.team2).count()

    # # fixtures by team
    # team1_fixtures = BSFixture.objects.filter(
    #     Q(team1=fixture.team1) | Q(team2=fixture.team1)
    # ).distinct()
    # team2_fixtures = BSFixture.objects.filter(
    #     Q(team1=fixture.team2) | Q(team2=fixture.team2)
    # ).distinct()


def Fixturepage(request, id):
    fixture = get_object_or_404(BSFixture, id=id)
    events = MatchEvent.objects.filter(match_id=id)
    goals1 = events.filter(event_type="Goal", team=fixture.team1)
    goals2 = events.filter(event_type="Goal", team=fixture.team2)
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
    team1_fouls = events.filter(event_type="Foul", team=fixture.team1).count()
    team2_fouls = events.filter(event_type="Foul", team=fixture.team2).count()
    team1_Save = events.filter(event_type="Save", team=fixture.team1).count()
    team2_Save = events.filter(event_type="Save", team=fixture.team2).count()
    context = {
        "fixture": fixture,
        "events": events,
        "team1_yellowcards": team1_yellowcards,
        "team2_yellowcards": team2_yellowcards,
        "team1_redcards": team1_redcards,
        "team2_redcards": team2_redcards,
        "team1_goals": team1_goals,
        "team2_goals": team2_goals,
        "team1_fouls": team1_fouls,
        "team2_fouls": team2_fouls,
        "team1_Save": team1_Save,
        "team2_Save": team2_Save,
        "goals1": goals1,
        "goals2": goals2,
    }
    return render(request, "frontend/fixturepage.html", context)


def bsfixtures(request):
    fixtures = BSFixture.objects.filter(competition_id=4).order_by("-date")
    context = {"fixtures": fixtures}
    return render(request, "server/bsfixtures.html", context)


def beachsoccerStandings(request):
    sports = Sport.objects.all()

    standings_data = []
    for sport in sports:
        beachsoccer_competitions = Beachsoccer.objects.filter(sport=sport)

        for beachsoccer in beachsoccer_competitions:
            groups = BSGroup.objects.filter(competition=beachsoccer)
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
                fixtures = BSFixture.objects.filter(group=group)
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
                    "competition": beachsoccer,
                    "standings": competition_standings,
                }
            )

    context = {
        "standings_data": standings_data,
    }

    return render(request, "server/bsstandings.html", context)


import math

import random


def generate_knockout_bsfixtures(request, id):
    beachsoccer = get_object_or_404(Beachsoccer, id=id)
    season = beachsoccer.season
    now = datetime.now()

    # Fetch all groups for the beachsoccer
    groups = BSGroup.objects.filter(competition=beachsoccer)

    # Get standings for each group
    standings = {}
    for group in groups:
        group_fixtures = BSFixture.objects.filter(
            competition=beachsoccer, group=group, stage="Group"
        )
        group_standings = calculate_group_standings(group_fixtures)
        standings[group] = group_standings

    # Generate knockout fixtures
    knockout_fixtures = []

    advancing_teams = []
    for group, group_standings in standings.items():
        print(f"Group: {group}")
        print(f"Group standings: {group_standings}")

        # Check if there are at least 2 teams before adding them
        if len(group_standings) >= 2:
            try:
                top_two = group_standings[:2]
                for item in top_two:
                    if isinstance(item, dict) and "team" in item:
                        advancing_teams.append((group, item["team"]))
                    elif isinstance(item, (list, tuple)) and len(item) >= 1:
                        advancing_teams.append((group, item[0]))
                    elif hasattr(item, "team"):
                        advancing_teams.append((group, item.team))
                    else:
                        advancing_teams.append((group, item))
            except Exception as e:
                print(f"Error processing group {group}: {str(e)}")
        else:
            print(f"Warning: Group {group} doesn't have enough teams")

    print(f"Advancing teams: {advancing_teams}")

    # Shuffle the teams to randomize matchups
    random.shuffle(advancing_teams)

    # Determine the round name based on the number of teams
    num_teams = len(advancing_teams)
    if num_teams >= 2:
        round_name = f"Round of {num_teams}"
        if num_teams == 2:
            round_name = "Final"
        elif num_teams == 4:
            round_name = "Semi-Finals"
        elif num_teams == 8:
            round_name = "Quarter-Finals"
        elif num_teams == 16:
            round_name = "Round of 16"

        fixtures = []
        for i in range(0, num_teams, 2):
            if i + 1 < num_teams:
                group1, team1 = advancing_teams[i]
                group2, team2 = advancing_teams[i + 1]

                # Ensure teams are from different groups
                if group1 != group2:
                    fixtures.append(
                        BSFixture(
                            competition=beachsoccer,
                            season=season,
                            stage="Knockout",
                            round=round_name,
                            team1=team1,
                            team2=team2,
                            date=now.date(),
                            time=now.time(),
                        )
                    )
                else:
                    # If from same group, swap with next team
                    if i + 2 < num_teams:
                        group3, team3 = advancing_teams[i + 2]
                        advancing_teams[i + 1], advancing_teams[i + 2] = (
                            advancing_teams[i + 2],
                            advancing_teams[i + 1],
                        )
                        fixtures.append(
                            BSFixture(
                                competition=beachsoccer,
                                season=season,
                                stage="Knockout",
                                round=round_name,
                                team1=team1,
                                team2=team3,
                                date=now.date(),
                                time=now.time(),
                            )
                        )
                    else:
                        print(
                            f"Warning: Could not avoid same-group matchup for {team1} and {team2}"
                        )
            else:
                print(
                    f"Warning: Odd number of teams, {advancing_teams[i][1]} doesn't have an opponent"
                )

        if fixtures:
            knockout_fixtures.extend(fixtures)
        else:
            print(f"Not enough teams to generate fixtures for {beachsoccer}")
    else:
        print(f"Not enough teams to generate fixtures for {beachsoccer}")

    # Bulk create knockout fixtures
    if knockout_fixtures:
        BSFixture.objects.bulk_create(knockout_fixtures)
        return JsonResponse(
            {
                "success": True,
                "message": f"Knockout fixtures for {round_name} generated successfully",
            }
        )
    else:
        return JsonResponse(
            {"success": False, "message": "No knockout fixtures were generated"}
        )


def calculate_group_standings(fixtures):
    standings = {}
    for fixture in fixtures:
        if fixture.team1_score is not None and fixture.team2_score is not None:
            for team, score, opponent_score in [
                (fixture.team1, fixture.team1_score, fixture.team2_score),
                (fixture.team2, fixture.team2_score, fixture.team1_score),
            ]:
                if team not in standings:
                    standings[team] = {
                        "team": team,
                        "points": 0,
                        "goal_difference": 0,
                        "goals_for": 0,
                    }

                standings[team]["goals_for"] += score
                standings[team]["goal_difference"] += score - opponent_score

                if score > opponent_score:
                    standings[team]["points"] += 3
                elif score == opponent_score:
                    standings[team]["points"] += 1

    return sorted(
        standings.values(),
        key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]),
        reverse=True,
    )

def beachfixtures(request):
    bsfixures = BSFixture.objects.all()
    context = {"bsfixures": bsfixures}
    return render(request, "frontend/bsfixtures.html", context)