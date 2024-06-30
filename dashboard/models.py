from django.db import models
from accounts.models import *


# Create your models here.
class Season(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    host = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return self.name


class SchoolTeam(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=True)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    age = models.CharField(
        choices=(("U16", "U16"), ("U18", "U18"), ("U20", "U20")), max_length=50
    )
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
    )
    status = models.CharField(
        max_length=10,
        default="Inactive",
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        null=True,
    )
    athletes = models.ManyToManyField(Athlete)

    def __str__(self):
        return str(self.school)









class Official(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default="")
    email = models.EmailField(null=True, blank=True, default="")
    phone_number = models.CharField(max_length=15, null=True, blank=True, default="")
    nin = models.CharField(max_length=20, null=True, blank=True, default="")
    gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
        null=True,
        blank=True,
    )

    role = models.CharField(
        max_length=10,
        choices=[
            ("Referee", "Referee"),
            ("Umpire", "Umpire"),
            ("Moderator", "Moderator"),
        ],
        null=True,
        blank=True,
    )
    sport = models.ForeignKey(
        Sport, related_name="official", on_delete=models.CASCADE, null=True
    )
    bio = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="photos/",
        blank=True,
        null=True,
        default="/images/profile.png",
    )

    def __str__(self):
        return self.name

