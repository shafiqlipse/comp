from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from .clientviews import *


# from competition.views import get_teams


urlpatterns = [
    path("rugby7", Rug7, name="rugby7"),
    path("fixtures/", fixtures, name="rugby7_fixtures"),
    path("rug7ourn/<int:id>", rug7tourn_details, name="rugby7_tournament"),
    path("fixture/<int:id>", edit_fixtures_view, name="update_fixture"),
    path("fixturedetail/<int:id>", FixtureDetail, name="fixture"),
    path(
        "generate_rug7fixtures/<int:id>/",
        generate_rug7fixtures_view,
        name="generate_rug7fixtures",
    ),
    path(
        "generate-knockout-rug7fixtures/<int:id>/",
        generate_knockout_rug7fixtures,
        name="generate_knockout_rug7fixtures",
    ),
    path("standings/", rugby7Standings, name="rugby7_standings"),
    # path("fixtures/", fixtures, name="fixtures"),
    #  # path("addtourn", addchampionship, name="addchampionship"),
    #  # path("fixtures/", fixtures, name="fixtures"),
    path("Rugby7<int:id>", Furtbol, name="Rugby7"),
    # path("Rugby7_fixtures", Fixtures, name="Footfixtures"),
    path("Rugby7", Fhome, name="Rugby7"),
    path("Rugby7_rankings", get_rankings, name="Footrankigs"),
    # path("Footbalstandings", footbollStandings, name="Footstandings"),
    # path("Rugby7_rankings", get_rankings, name="Footrankigs"),
    # path("Footbalstandings", footbollStandings, name="Footstandings"),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
