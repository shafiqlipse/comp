from django import forms
from .models import Championship
from .models import *
from django.forms import CheckboxSelectMultiple


class CompForm(forms.ModelForm):
    class Meta:
        model = Rugby7s
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



class R7GroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=SchoolTeam.objects.none(),  # We'll set this in __init__
        # widget=CheckboxSelectMultiple,
        required=False,  # Set to True if you want to require at least one team
    )

    class Meta:
        model = R7Group
        fields = ["name", "teams"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "competition"):
            self.fields["teams"].queryset = self.instance.competition.teams.all()

    # In your Django form
    widgets = {
        "teams": forms.SelectMultiple(
            attrs={
                "class": "js-example-basic-multiple",
                "multiple": "multiple",
                "id": "id_teams",  # Add this line
            }
        )
    }


from django.forms import inlineformset_factory

GroupFormSet = inlineformset_factory(
    parent_model=Rugby7s,
    model=R7Group,
    form=R7GroupForm,  # Use our custom form
    fields=["name", "teams"],
    extra=0,
    can_delete=False,
)


# from django.forms import TimeInput


class R7FixtureForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"})
    )

    class Meta:
        model = R7Fixture
        fields = [
            "season",
            "competition",
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
        widgets = {
            "season": forms.Select(attrs={"class": "form-control"}),
            "competition": forms.Select(attrs={"class": "form-control"}),
            "stage": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "round": forms.TextInput(attrs={"class": "form-control"}),
            "group": forms.TextInput(attrs={"class": "form-control"}),
            "venue": forms.TextInput(attrs={"class": "form-control"}),
            "team1": forms.Select(attrs={"class": "form-control"}),
            "team2": forms.Select(attrs={"class": "form-control"}),
            "team1_score": forms.NumberInput(attrs={"class": "form-control"}),
            "team2_score": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.update({"class": "form-control"})


class MatchOfficialForm(forms.ModelForm):
    class Meta:
        model = match_official
        fields = "__all__"


class MatchEventForm(forms.ModelForm):
    class Meta:
        model = MatchEvent
        fields = ["event_type", "team", "player", "minute", "commentary"]

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
