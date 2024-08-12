from django.db import models
from accounts.models import *
from dashboard.models import *

# Create your models here.


# Create your models here.
class Handball(models.Model):
    name = models.CharField(max_length=255)
    championship = models.ForeignKey(
        Championship, related_name="handchamp", on_delete=models.CASCADE
    )
    season = models.ForeignKey(
        Season, related_name="handseason", on_delete=models.CASCADE
    )
    sport = models.ForeignKey(Sport, related_name="handsport", on_delete=models.CASCADE)
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


class HGroup(models.Model):
    competition = models.ForeignKey(
        Handball, related_name="handgroup", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    teams = models.ManyToManyField(SchoolTeam)

    def __str__(self):
        return self.name


class HFixture(models.Model):
    statuses = (
        ("Pending", "Pending"),
        ("InPlay", "InPlay"),
        ("Complete", "Complete"),
        ("Postponed", "Postponed"),
    )

    stages = (("Group", "Group"), ("Knockout", "Knockout"))
    season = models.ForeignKey(
        Season, related_name="handfix", on_delete=models.CASCADE, null=True, blank=True
    )
    competition = models.ForeignKey(
        Handball, on_delete=models.CASCADE, null=True, blank=True
    )
    stage = models.CharField(choices=stages, max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=statuses, max_length=100, null=True, blank=True, default="Pending"
    )
    round = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(HGroup, on_delete=models.CASCADE, null=True, blank=True)

    # Use UUIDField for match_number

    venue = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    team1 = models.ForeignKey(
        SchoolTeam, related_name="hteam1", on_delete=models.CASCADE
    )
    team2 = models.ForeignKey(
        SchoolTeam, related_name="hteam2", on_delete=models.CASCADE
    )
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Match {self.id}: {self.team1} vs {self.team2}"


class MatchEvent(models.Model):
    match = models.ForeignKey(HFixture, on_delete=models.CASCADE)
    EVENT_CHOICES = [
        ("Goal", "Goal"),
        ("Save", "Save"),
        ("Assist", "Assist"),
        ("Penalty Goal", "Penalty Goal"),
        ("Penalty Miss", "Penalty Miss"),
        ("Yellow Card", "Yellow Card"),
        ("Red Card", "Red Card"),
        ("Suspension", "Suspension"),
        ("Timeout", "Timeout"),
        ("Substitution", "Substitution"),
        ("Injury", "Injury"),
        ("Fast Break", "Fast Break"),
        ("Turnover", "Turnover"),
        ("Interception", "Interception"),
        ("Block", "Block"),
        ("Foul", "Foul"),
        ("Technical Foul", "Technical Foul"),
        ("Offensive Foul", "Offensive Foul"),
        ("Defensive Foul", "Defensive Foul"),
        ("Dribbling Violation", "Dribbling Violation"),
        ("Steps Violation", "Steps Violation"),
        ("Passive Play", "Passive Play"),
        ("Goalkeeper Save", "Goalkeeper Save"),
        ("7-Meter Throw", "7-Meter Throw"),
        # Add more choices as needed
    ]

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
    )
    # Example: "Card", "Corner", "Foul", "Assist"
    team = models.ForeignKey(SchoolTeam, related_name="hteam", on_delete=models.CASCADE)
    athlete = models.ForeignKey(
        Athlete,
        related_name="hathlete",
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
        HFixture, on_delete=models.CASCADE, related_name="hofix", null=True, blank=True
    )
    official = models.ForeignKey(
        Official,
        on_delete=models.CASCADE,
        related_name="hofficial",
        null=True,
        blank=True,
    )
    match_role = models.CharField(choices=role, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fixture
