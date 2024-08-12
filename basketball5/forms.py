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
            "age",
            "teams",
            "participants",
            "number_of_groups",
        ]


class B5GroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=SchoolTeam.objects.none(),  # We'll set this in __init__
        widget=CheckboxSelectMultiple,
        required=False,  # Set to True if you want to require at least one team
    )

    class Meta:
        model = B5Group
        fields = ["name", "teams"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "competition"):
            self.fields["teams"].queryset = self.instance.competition.teams.all()


from django.forms import inlineformset_factory

GroupFormSet = inlineformset_factory(
    parent_model=Basketball5,
    model=B5Group,
    form=B5GroupForm,  # Use our custom form
    fields=["name", "teams"],
    extra=0,
    can_delete=False,
)


# from django.forms import TimeInput


class B5FixtureForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "date"}))
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
        fields = ["event_type", "team", "athlete", "minute", "commentary"]

    def __init__(self, *args, **kwargs):
        fixture_instance = kwargs.pop("fixture_instance", None)
        super().__init__(*args, **kwargs)

        if fixture_instance:
            # Filter team choices based on the fixture_instance
            team_choices = [
                (fixture_instance.team1.id, str(fixture_instance.team1)),
                (fixture_instance.team2.id, str(fixture_instance.team2)),
            ]
            self.fields["team"].choices = team_choices
        else:
            self.fields["team"].queryset = self.fields["team"].queryset.none()