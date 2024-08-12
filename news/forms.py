from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget
from .models import *


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "thumbnail",
            "author",
            "sport",
            "championship",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter title"}
            ),
            "pub_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "thumbnail": forms.FileInput(attrs={"class": "form-control-file"}),
            "author": forms.Select(attrs={"class": "form-control"}),
            "sport": forms.Select(attrs={"class": "form-control"}),
            "championship": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update({"class": "form-control"})

    widgets = {
        "content": SummernoteWidget(),
    }


class CategoriesForm(forms.ModelForm):

    class Meta:
        model = Categories
        fields = ["name", "description"]
