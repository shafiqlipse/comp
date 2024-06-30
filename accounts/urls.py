from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

# from competition.views import get_teams


urlpatterns = [
    path("schools/", schools, name="schools"),
    # path("schools", schools, name="schools"),
    path("school/<int:id>", schoolDetail, name="schoolDetail"),
    path("athlete/<int:id>", AthleteDetail, name="athleteDetail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
