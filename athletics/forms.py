from django import forms
from .models import Championship
from .models import *
from django.forms import CheckboxSelectMultiple


class AthleticsForm(forms.ModelForm):
    class Meta:
        model = Athletics
        fields = [
            "name",
            "championship",
            "season",
            "sport",
            "gender",
            "age",
            "teams",
        ]


class AthleticsEventForm(forms.ModelForm):
    class Meta:
        model = AthleticsEvent
        fields = [
            "name",
            "event_type",
            "gender",
            "age",
            "time",
            "date",
            "venue",
            "teams",
            "athletes",
        ]


class AthleticsResultForm(forms.ModelForm):
    class Meta:
        model = AthleticsResult
        fields = [
            "event",
            "team",
            "athlete",
            "time_seconds",
            "position",
        ]


class MedalForm(forms.ModelForm):
    class Meta:
        model = Medal
        fields = [
            "type",
            "team",
            "athlete",
            "event",
            "date",
        ]
