from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

# from competition.views import get_teams


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("championships/", championships, name="championships"),
    path("addchampionship/", addchampionship, name="addchampionship"),
    path("championship/<int:id>", ChampDetail, name="champDetail"),
    # path("championship/<int:id>", ChampDetail, name="champDetail"),
    path("teams/", teams, name="teams"),
    path("addteam/", addteam, name="addteam"),
    path("team/<int:id>", TeamDetail, name="teamDetail"),
    # path("team/<int:id>", TeamDetail, name="teamDetail"),
    path("official/<int:id>", official_details, name="official"),
    path("officials/", officials, name="officials"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
