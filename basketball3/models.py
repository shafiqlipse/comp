from django.db import models
from accounts.models import *
from dashboard.models import *

# Create your models here.


# Create your models here.
class Basketball3(models.Model):
    name = models.CharField(max_length=255)
    championship = models.ForeignKey(
        Championship, on_delete=models.CASCADE, related_name="basketball3"
    )
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="basketball3"
    )
    sport = models.ForeignKey(
        Sport, on_delete=models.CASCADE, related_name="basketball3"
    )
    age = models.CharField(
        choices=(("U16", "U16"), ("U18", "U18"), ("U20", "U20")),
        max_length=50,
        null=True,
        blank=True,
    )
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


class B3Group(models.Model):
    competition = models.ForeignKey(
        Basketball3, on_delete=models.CASCADE, related_name="b3comp"
    )
    name = models.CharField(max_length=255)
    teams = models.ManyToManyField(SchoolTeam)

    def __str__(self):
        return self.name


class B3Fixture(models.Model):
    statuses = (
        ("Pending", "Pending"),
        ("InPlay", "InPlay"),
        ("Complete", "Complete"),
        ("Postponed", "Postponed"),
    )

    stages = (("Group", "Group"), ("Knockout", "Knockout"))
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    competition = models.ForeignKey(
        Basketball3,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="b3tourn",
    )
    stage = models.CharField(choices=stages, max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=statuses, max_length=100, null=True, blank=True, default="Pending"
    )
    round = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(
        B3Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="b3group",
    )

    # Use UUIDField for match_number

    venue = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    team1 = models.ForeignKey(
        SchoolTeam, related_name="b3team1", on_delete=models.CASCADE
    )
    team2 = models.ForeignKey(
        SchoolTeam, related_name="b3team2", on_delete=models.CASCADE
    )
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Match {self.id}: {self.team1} vs {self.team2}"


class MatchEvent(models.Model):
    match = models.ForeignKey(
        B3Fixture, on_delete=models.CASCADE, related_name="basketfixture"
    )
    EVENT_CHOICES = [
        ("1-Pointer", "1-Pointer"),
        ("2-Pointer", "2-Pointer"),
        ("Inbound Pass", "Inbound Pass"),
        ("Foul", "Foul"),
        ("rebound", "rebound"),
        ("steal", "steal"),
        ("turnover", "turnover"),
        ("Assist", "Assist"),
        ("3-Pointer", "3-Pointer"),
        ("Block", "Block"),
        ("Substitution", "Substitution"),
        ("Shot Made (3-Pointer)", "Shot Made (3-Pointer)"),
        ("Shot Missed (3-Pointer)", "Shot Missed (3-Pointer)"),
        ("Free Throw", "Free Throw"),
        # Add more choices as needed
    ]

    event_type = models.CharField(
        max_length=25,
        choices=EVENT_CHOICES,
    )  # Example: "Card", "Corner", "Foul", "Assist"
    team = models.ForeignKey(
        SchoolTeam,
        on_delete=models.CASCADE,
        related_name="basket_team",
    )
    athlete = models.ForeignKey(
        Athlete,
        related_name="b3athlete",
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
        B3Fixture,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="b3fixture",
    )
    official = models.ForeignKey(
        Official,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="b3officicial",
    )
    match_role = models.CharField(choices=role, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fixture

