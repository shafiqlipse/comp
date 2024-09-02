from django.db import models
from accounts.models import *
from dashboard.models import *

# Create your models here.


# Create your models here.
class Hockey(models.Model):
    name = models.CharField(max_length=255)
    championship = models.ForeignKey(
        Championship, related_name="hochamp", on_delete=models.CASCADE
    )
    season = models.ForeignKey(
        Season, related_name="hoseason", on_delete=models.CASCADE
    )
    sport = models.ForeignKey(Sport, related_name="hosport", on_delete=models.CASCADE)
    gender = models.CharField(
        choices=[("Male", "male"), ("Female", "female")],
        max_length=10,
        null=True,
        blank=True,
    )
    age = models.CharField(
        choices=(("U16", "U16"), ("U18", "U18"), ("U20", "U20")),
        max_length=50,
        null=True,
        blank=True,
    )
    teams = models.ManyToManyField(SchoolTeam)
    participants = models.IntegerField()
    number_of_groups = models.IntegerField()

    def __str__(self):
        return self.name


class HoGroup(models.Model):
    competition = models.ForeignKey(
        Hockey, related_name="hogroup", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    teams = models.ManyToManyField(SchoolTeam)

    def __str__(self):
        return self.name


class HoFixture(models.Model):
    statuses = (
        ("Pending", "Pending"),
        ("InPlay", "InPlay"),
        ("Complete", "Complete"),
        ("Postponed", "Postponed"),
    )

    stages = (("Group", "Group"), ("Knockout", "Knockout"))
    season = models.ForeignKey(
        Season, related_name="hofix", on_delete=models.CASCADE, null=True, blank=True
    )
    competition = models.ForeignKey(
        Hockey, on_delete=models.CASCADE, null=True, blank=True
    )
    stage = models.CharField(choices=stages, max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=statuses, max_length=100, null=True, blank=True, default="Pending"
    )
    round = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(HoGroup, on_delete=models.CASCADE, null=True, blank=True)

    # Use UUIDField for match_number

    venue = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    team1 = models.ForeignKey(
        SchoolTeam, related_name="hoteam1", on_delete=models.CASCADE
    )
    team2 = models.ForeignKey(
        SchoolTeam, related_name="hoteam2", on_delete=models.CASCADE
    )
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Match {self.id}: {self.team1} vs {self.team2}"


class MatchEvent(models.Model):
    match = models.ForeignKey(HoFixture, on_delete=models.CASCADE)
    EVENT_CHOICES = [
        ("Goal", "Goal"),
        ("Shot", "Shot"),
        ("Save", "Save"),
        ("Penalty", "Penalty"),
        ("Timeout", "Timeout"),
        ("Substitution", "Substitution"),
        ("Injury", "Injury"),
        ("PenaltyCorner", "Penalty Corner"),
        ("FreeHit", "Free Hit"),
        ("Card", "Card"),
        ("Assist", "Assist"),
        ("PenaltyShot", "Penalty Shot"),
        ("ShootoutGoal", "Shootout Goal"),
        ("PowerPlayGoal", "Power Play Goal"),
        # Add more choices as needed
    ]

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
    )
    # Example: "Card", "Corner", "Foul", "Assist"
    team = models.ForeignKey(
        SchoolTeam, related_name="hoteam", on_delete=models.CASCADE
    )
    athlete = models.ForeignKey(
        Athlete,
        related_name="hoathlete",
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
        HoFixture,
        on_delete=models.CASCADE,
        related_name="hoofix",
        null=True,
        blank=True,
    )
    official = models.ForeignKey(
        Official,
        on_delete=models.CASCADE,
        related_name="hoofficial",
        null=True,
        blank=True,
    )
    match_role = models.CharField(choices=role, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fixture
