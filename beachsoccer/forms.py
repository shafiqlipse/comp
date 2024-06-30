from django import forms
from .models import Championship
from .models import *
from django.forms import CheckboxSelectMultiple

class CompForm(forms.ModelForm):
    class Meta:
        model = BeachSoccer
        fields = [
            "name",
            "championship",
            "season",
            "sport",
            "gender",
            "teams",
            "participants",
            "number_of_groups",
        ]


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

class BSGroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=SchoolTeam.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = BSGroup
        fields = ["name", "teams"]


GroupFormSet = forms.inlineformset_factory(
    parent_model=BeachSoccer,
    model=BSGroup,
    fields=["name", "teams"],
    extra=0,  # Set this to the number of forms you want initially
    can_delete=False,  # If you want to allow deleting groups, set this to True
)



# from django.forms import TimeInput


class FixtureForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    # time = forms.TimeField(widget=TimeInput(attrs={"type": "time"}))

    class Meta:
        model = Fixture
        fields = [
            "stage",
            "status",
            "round",
            "group",
            "venue",
            "date",
            "team1",
            "team2",
            "team1_score",
            "team2_score",
        ]
        widgets = {"group": forms.Select(attrs={"class": "select2"})}


class MatchOfficialForm(forms.ModelForm):
    class Meta:
        model = match_official
        fields = "__all__"
        


class MatchEventForm(forms.ModelForm):
    class Meta:
        model = MatchEvent
        fields = "__all__"
        
