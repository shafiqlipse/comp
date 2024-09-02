from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# from competition.views import get_teams
from client.views import Home
from accounts.views import user_login
from football.apiviews import *
from netball.apiviews import *
from basketball3.apiviews import *

# from competition.views import get_teams


urlpatterns = [
    path("admin/", admin.site.urls),
    # includes
    path("", Home, name="home"),
    path("login/", user_login, name="login"),
    # path("get_fteams/", getfoot_teams, name="get_fteams"),--football
    path("get_fteams/", getfoot_teams, name="get_fteams"),
    path("get_teams_for_match/", get_teams_for_match, name="get_teams_for_match"),
    path("get_athletes_for_team/", get_athletes_for_team, name="get_athletes_for_team"),
    # path("get_fteams/", getfoot_teams, name="get_fteams"),--netball
    path("get_nteams/", getnet_teams, name="get_nteams"),
    # path("get_nteams/", getnet_teams, name="get_nteams"),
    path("get_fixture_teams/", get_fixture_teams, name="get_fixture_teams"),
    path("get_b3teams/", getb3_teams, name="get_b3teams"),
    # path("get_teams_for_match/", get_teams_for_match, name="get_teams_for_match"),
    path("summernote/", include("django_summernote.urls")),
    # path("get_athletes_for_team/", get_athletes_for_team, name="get_athletes_for_team"),
    # path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("sport/", include("sports.urls")),
    path("accounts/", include("accounts.urls")),
    path("football/", include("football.urls")),
    path("netball/", include("netball.urls")),
    path("handball/", include("handball.urls")),
    path("news/", include("news.urls")),
    path("rugby7s/", include("rugby7s.urls")),
    path("rugby15s/", include("rugby15s.urls")),
    path("volleyball/", include("volleyball.urls")),
    # path("beachsoccer/", include("beachsoccer.urls")),
    path("basketball3/", include("basketball3.urls")),
    path("athletics/", include("athletics.urls")),
    path("hockey/", include("hockey.urls")),
    path("basketball5/", include("basketball5.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
