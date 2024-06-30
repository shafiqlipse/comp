from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from .clientviews import *


# from competition.views import get_teams


urlpatterns = [
    path("football", Futball, name="football"),
    path("fixtures/", fixtures, name="football_fixtures"),
    path("futourn/<int:id>", ftourn_details, name="football_tournament"),
    path("fixture/<int:id>", edit_fixtures_view, name="update_fixture"),
    path("fixturedetail/<int:id>", FixtureDetail, name="fixture"),
    path(
        "generate_futfixtures/<int:id>/",
        generate_futfixtures_view,
        name="generate_futfixtures",
    ),
    path(
        "generate-knockout-futfixtures/<int:id>/",
        generate_knockout_futfixtures,
        name="generate_knockout_futfixtures",
    ),
    path("standings/", footballStandings, name="football_standings"),
    # path("fixtures/", fixtures, name="fixtures"),
    #  # path("addtourn", addchampionship, name="addchampionship"),
    #  # path("fixtures/", fixtures, name="fixtures"),
    path("Football<int:id>", Furtbol, name="Football"),
    # path("Football_fixtures", Fixtures, name="Footfixtures"),
    path("Football", Fhome, name="Football"),
    path("Football_rankings", get_rankings, name="Footrankigs"),
    # path("Footbalstandings", footbollStandings, name="Footstandings"),
    # path("Football_rankings", get_rankings, name="Footrankigs"),
    # path("Footbalstandings", footbollStandings, name="Footstandings"),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
