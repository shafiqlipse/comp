from django.db import models
from django_summernote.fields import SummernoteTextField
from accounts.models import *


class Categories(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    thumbnail = models.ImageField(upload_to="postImages/", blank=True, null=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = SummernoteTextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to="postImages/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, blank=True, null=True)
    championship = models.ForeignKey(
        Championship, on_delete=models.CASCADE, blank=True, null=True
    )
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ["-title"]

    def __str__(self):
        return self.title
