from django.db import models
from accounts.models import *
from dashboard.models import *

# Create your models here.


# Create your models here.
class BeachSoccer(models.Model):
    name = models.CharField(max_length=255)
    championship = models.ForeignKey(
        Championship, related_name="bschamp", on_delete=models.CASCADE
    )
    season = models.ForeignKey(
        Season, related_name="bsseason", on_delete=models.CASCADE
    )
    sport = models.ForeignKey(Sport, related_name="bssport", on_delete=models.CASCADE)
    gender = models.CharField(
        choices=[("Male", "male"), ("Female", "female")],
        max_length=10,
        null=True,
        blank=True,
    )
    teams = models.ManyToManyField(SchoolTeam)
    participants = models.IntegerField()
    number_of_groups = models.IntegerField()

    def __str__(self):
        return self.name


class BSGroup(models.Model):
    competition = models.ForeignKey(
        BeachSoccer, related_name="bscomp", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    teams = models.ManyToManyField(SchoolTeam)

    def __str__(self):
        return self.name


class Fixture(models.Model):
    statuses = (
        ("Pending", "Pending"),
        ("InPlay", "InPlay"),
        ("Complete", "Complete"),
        ("Postponed", "Postponed"),
    )

    stages = (("Group", "Group"), ("Knockout", "Knockout"))
    season = models.ForeignKey(
        Season, related_name="bssn", on_delete=models.CASCADE, null=True, blank=True
    )
    competition = models.ForeignKey(
        BeachSoccer,
        on_delete=models.CASCADE,
        related_name="bscomps",
        null=True,
        blank=True,
    )
    stage = models.CharField(choices=stages, max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=statuses, max_length=100, null=True, blank=True, default="Pending"
    )
    round = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(
        BSGroup, related_name="bsgroup", on_delete=models.CASCADE, null=True, blank=True
    )

    # Use UUIDField for match_number

    venue = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    team1 = models.ForeignKey(
        SchoolTeam, related_name="bsteam1", on_delete=models.CASCADE
    )
    team2 = models.ForeignKey(
        SchoolTeam, related_name="bsteam2", on_delete=models.CASCADE
    )
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Match {self.id}: {self.team1} vs {self.team2}"


class MatchEvent(models.Model):
    match = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    EVENT_CHOICES = [
        ("RedCard", "Red Card"),
        ("YellowCard", "Yellow Card"),
        ("Corner", "Corner"),
        ("Foul", "Foul"),
        ("Assist", "Assist"),
        ("Goal", "Goal"),
        ("Save", "Save"),
        ("Substitution", "Substitution"),
        ("ShotOnGoal", "Shot on Goal"),
        ("ShotOffTarget", "Shot off Target"),
        ("Penalty", "Penalty"),
        ("BicycleKickGoal", "Bicycle Kick Goal"),
        ("FreeKickGoal", "Free Kick Goal"),
        ("SandSave", "Sand Save"),
        ("OverheadKick", "Overhead Kick"),
        ("Dribble", "Dribble"),
        ("BeachDive", "Beach Dive"),
        # Add more choices as needed
    ]

    event_type = models.CharField(
        max_length=30,
        choices=EVENT_CHOICES,
    )
    # Example: "Card", "Corner", "Foul", "Assist"
    team = models.ForeignKey(
        SchoolTeam, related_name="bsteam", on_delete=models.CASCADE
    )
    athlete = models.ForeignKey(
        Athlete,
        related_name="bsathlete",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    minute = models.IntegerField()
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.team} - {self.event_type} at {self.minute}'"


class match_official(models.Model):
    role = (
        ("Referee", "Referee"),
        ("Umpire", "Umpire"),
        ("First assistant", "First assistant "),
        ("Second assistant", "Second assistant "),
        ("4th Official", "4th Official"),
    )

    fixture = models.ForeignKey(
        Fixture, on_delete=models.CASCADE, related_name="bsfix", null=True, blank=True
    )
    official = models.ForeignKey(
        Official,
        on_delete=models.CASCADE,
        related_name="bsofficial",
        null=True,
        blank=True,
    )
    match_role = models.CharField(choices=role, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fixture
