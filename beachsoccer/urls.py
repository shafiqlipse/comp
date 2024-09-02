from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from .clientviews import *


# from competition.views import get_teams


urlpatterns = [
    path("beachsoccer", Beaches, name="beachsoccer"),
    path("fixtures/", bsfixtures, name="beachsoccer_fixtures"),
    path("bsourn/<int:id>", bstourn_details, name="beachsoccer_tournament"),
    path("fixture/<int:id>", edit_bsfixtures_view, name="update_bsfixture"),
    path("bsfixturedetail/<int:id>", BsFixtureDetail, name="bsfixture"),
    path(
        "generate_bsfixtures/<int:id>/",
        generate_bsfixtures_view,
        name="generate_bsfixtures",
    ),
    path(
        "generate-knockout-bsfixtures/<int:id>/",
        generate_knockout_bsfixtures,
        name="generate_knockout_bsfixtures",
    ),
    path("standings/", beachsoccerStandings, name="beachsoccer_standings"),
    # path("fixtures/", fixtures, name="fixtures"),
    #  # path("addtourn", addchampionship, name="addchampionship"),
    #  # path("fixtures/", fixtures, name="fixtures"),
    path("fixtured/<int:id>/", Fixturepage, name="fixtured"),
    path("Beachsoccer/<int:id>", Furtbol, name="Beachsoccer"),
    # path("Beachsoccer_fixtures", Fixtures, name="Footfixtures"),
    path("Beachsoccer", Fhome, name="Beachsoccer"),
    path("Beachsoccer_rankings", get_bsrankings, name="bsrankigs"),
    # path("Footbalstandings", beachbollStandings, name="Footstandings"),
    path("beachfixtures/", beachfixtures, name="beachfixtures"),
    # path("Beachsoccer_rankings", get_rankings, name="Footrankigs"),
    # path("Footbalstandings", beachbollStandings, name="Footstandings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
