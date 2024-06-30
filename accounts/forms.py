from django import forms
from .models import *


class AthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = ["school", "fname", "lname", "gender", "age"]


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ["name", "badge"]


from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "username",
            "password1",
            "password2",
        ]
