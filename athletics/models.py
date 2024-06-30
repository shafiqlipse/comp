from django.db import models
from accounts.models import *
from dashboard.models import *
from django.db import models

# Define choices outside the models
GENDER_CHOICES = [("MALE", "Male"), ("FEMALE", "Female"), ("MIXED", "Mixed")]
AGE_CHOICES = [("U16", "U16"), ("U18", "U18"), ("U20", "U20")]
EVENT_TYPE_CHOICES = [("TRACK", "Track"), ("FIELD", "Field"), ("COMBINED", "Combined")]


class Athletics(models.Model):
    name = models.CharField(max_length=255)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, null=True, blank=True
    )
    age = models.CharField(choices=AGE_CHOICES, max_length=10, null=True, blank=True)
    teams = models.ManyToManyField(SchoolTeam, related_name="ateams")

    def __str__(self):
        return self.name


class AthleticsEvent(models.Model):
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    venue = models.CharField(max_length=10, null=True, blank=True)
    time = models.TimeField()
    date = models.DateField()
    teams = models.ManyToManyField(SchoolTeam, related_name="events_team")
    athletes = models.ManyToManyField(Athlete, related_name="events_athletes")
    age = models.CharField(choices=AGE_CHOICES, max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class AthleticsResult(models.Model):
    event = models.ForeignKey(AthleticsEvent, on_delete=models.CASCADE)
    team = models.ManyToManyField(SchoolTeam, related_name="results_team")
    athlete = models.ManyToManyField(Athlete, related_name="results_athlete")
    time_seconds = models.FloatField()  # Time in seconds
    position = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.athlete.name} - {self.event.name} - {self.time_seconds} seconds"


class Medal(models.Model):
    type = models.CharField(
        max_length=10,
        choices=[("GOLD", "Gold"), ("SILVER", "Silver"), ("BRONZE", "Bronze")],
    )
    team = models.ManyToManyField(SchoolTeam, related_name="medal_team")
    athlete = models.ManyToManyField(Athlete, related_name="medal_athletes")
    event = models.ForeignKey(AthleticsEvent, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.athlete.name} - {self.type} - {self.event.name}"
