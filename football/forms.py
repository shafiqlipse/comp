from django import forms
from .models import Championship
from .models import *
from django.forms import CheckboxSelectMultiple


class CompForm(forms.ModelForm):
    class Meta:
        model = Football
        fields = [
            "name",
            "championship",
            "season",
            "sport",
            "gender",
            "age",
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


class FGroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=SchoolTeam.objects.none(),  # We'll set this in __init__
        widget=CheckboxSelectMultiple,
        required=False,  # Set to True if you want to require at least one team
    )

    class Meta:
        model = FGroup
        fields = ["name", "teams"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "competition"):
            self.fields["teams"].queryset = self.instance.competition.teams.all()


from django.forms import inlineformset_factory

GroupFormSet = inlineformset_factory(
    parent_model=Football,
    model=FGroup,
    form=FGroupForm,  # Use our custom form
    fields=["name", "teams"],
    extra=0,
    can_delete=False,
)

from django.forms import TimeInput


class FixtureForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "date"}))
    time = forms.TimeField(widget=TimeInput(attrs={"type": "time"}))

    class Meta:
        model = Fixture
        fields = [
            "stage",
            "status",
            "round",
            "group",
            "venue",
            "date",
            "time",
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
        fields = ["event_type", "team", "athlete", "minute", "commentary"]

    def __init__(self, *args, **kwargs):
        match = kwargs.pop("match", None)
        super().__init__(*args, **kwargs)

        if match:
            self.fields["team"].queryset = SchoolTeam.objects.filter(
                id__in=[match.team1.id, match.team2.id]
            )
        else:
            self.fields["team"].queryset = SchoolTeam.objects.none()

        self.fields["athlete"].queryset = Athlete.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        team = cleaned_data.get("team")
        if team:
            self.fields["athlete"].queryset = Athlete.objects.filter(schoolteam=team)
        return cleaned_data
