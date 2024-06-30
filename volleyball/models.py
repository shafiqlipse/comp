from django.db import models
from accounts.models import *
from dashboard.models import *

# Create your models here.


# Create your models here.
class Volleyball(models.Model):
    name = models.CharField(max_length=255)
    championship = models.ForeignKey(
        Championship, related_name="volchamp", on_delete=models.CASCADE
    )
    season = models.ForeignKey(
        Season, related_name="volseason", on_delete=models.CASCADE
    )
    sport = models.ForeignKey(Sport, related_name="volsport", on_delete=models.CASCADE)
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


class VGroup(models.Model):
    competition = models.ForeignKey(
        Volleyball, related_name="volgroup", on_delete=models.CASCADE
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
        Season, related_name="volfix", on_delete=models.CASCADE, null=True, blank=True
    )
    competition = models.ForeignKey(
        Volleyball, on_delete=models.CASCADE, null=True, blank=True
    )
    stage = models.CharField(choices=stages, max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=statuses, max_length=100, null=True, blank=True, default="Pending"
    )
    round = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(VGroup, on_delete=models.CASCADE, null=True, blank=True)

    # Use UUIDField for match_number

    venue = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    team1 = models.ForeignKey(
        SchoolTeam, related_name="vteam1", on_delete=models.CASCADE
    )
    team2 = models.ForeignKey(
        SchoolTeam, related_name="vteam2", on_delete=models.CASCADE
    )
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    team1_sets_won = models.IntegerField(null=True, blank=True, default=0)
    team2_sets_won = models.IntegerField(null=True, blank=True, default=0)

    # Add any additional fields as necessary

    def __str__(self):
        return f"{self.team1} vs {self.team2} - {self.competition}"

    class Meta:
        verbose_name = "Fixture"
        verbose_name_plural = "Fixtures"




class MatchEvent(models.Model):
    match = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    EVENT_CHOICES = [
        ("Serve", "Serve"),
        ("Ace", "Ace"),
        ("Block", "Block"),
        ("Attack", "Attack"),
        ("Kill", "Kill"),
        ("Dig", "Dig"),
        ("Set", "Set"),
        ("Substitution", "Substitution"),
        ("Timeout", "Timeout"),
        ("Injury", "Injury"),
        ("Service Error", "Service Error"),
        ("Attack Error", "Attack Error"),
        ("Blocking Error", "Blocking Error"),
        ("Ball Handling Error", "Ball Handling Error"),
        # Add more choices as needed
    ]

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
    )
    # Example: "Card", "Corner", "Foul", "Assist"
    team = models.ForeignKey(SchoolTeam, related_name="vteam", on_delete=models.CASCADE)
    athlete = models.ForeignKey(
        Athlete,
        related_name="vathlete",
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
        Fixture, on_delete=models.CASCADE, related_name="vofix", null=True, blank=True
    )
    official = models.ForeignKey(
        Official,
        on_delete=models.CASCADE,
        related_name="vofficial",
        null=True,
        blank=True,
    )
    match_role = models.CharField(choices=role, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fixture
