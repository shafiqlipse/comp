from django import forms
from .models import Championship
from .models import *
from django.forms import CheckboxSelectMultiple


class Co3mpForm(forms.ModelForm):
    class Meta:
        model = Basketball5
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


class B5GroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=SchoolTeam.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = B5Group
        fields = ["name", "teams"]


GroupFormSet = forms.inlineformset_factory(
    parent_model=Basketball5,
    model=B5Group,
    fields=["name", "teams"],
    extra=0,  # Set this to the number of forms you want initially
    can_delete=False,  # If you want to allow deleting groups, set this to True
)


# from django.forms import TimeInput


class B5FixtureForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    # time = forms.TimeField(widget=TimeInput(attrs={"type": "time"}))

    class Meta:
        model = B5Fixture
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
