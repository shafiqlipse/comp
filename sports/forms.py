from django import forms

from accounts.models import *


class sportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ["name", "thumbnail"]
