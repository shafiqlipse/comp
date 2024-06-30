from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=245)
    thumbnail = models.ImageField(upload_to="sportImages/", blank=True, null=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class User(AbstractUser):

    is_games = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Championship(models.Model):
    name = models.CharField(max_length=245)
    thumbnail = models.ImageField(upload_to="champImages/", blank=True, null=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=245)
    badge = models.ImageField(upload_to="badge/", blank=True, null=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Athlete(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)

    gender = models.CharField(
        choices=(("Male", "Male"), ("Female", "Female")), max_length=50
    )
    age = models.CharField(
        choices=(("U16", "U16"), ("U18", "U18"), ("U20", "U20")), max_length=50
    )

    class Meta:
        ordering = ["-fname"]

    def __str__(self):
        return f"{self.fname} {self.lname}"
