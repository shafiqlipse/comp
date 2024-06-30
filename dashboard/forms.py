from django import forms
from .models import Championship
from .models import *


class ChampForm(forms.ModelForm):
    class Meta:
        model = Championship
        fields = ["name", "thumbnail"]


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = [
            "name",
            "championship",
            "host",
            "address",
            "start_date",
            "end_date",
        ]


class SchoolTeamForm(forms.ModelForm):
    class Meta:
        model = SchoolTeam
        fields = [
            "sport",
            "school",
            "gender",
            "championship",
            "season",
            "age",
            "athletes",
        ]
        widgets = {
            "athletes": forms.CheckboxSelectMultiple,
        }




class OfficialForm(forms.ModelForm):
    class Meta:
        model = Official
        fields = [
            "name",
            "nin",
            "bio",
            "sport",
            "photo",
            "phone_number",
            "email",
            "gender",
            "role",
        ]

    widgets = {
        "date_of_birth": forms.DateInput(attrs={"type": "date"}),
    }

    def __init__(self, *args, **kwargs):
        super(OfficialForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"