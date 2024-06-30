from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from .volviews import *

# from competition.views import get_teams


urlpatterns = [
    path("volleyball", Votball, name="volleyball"),
    # path("addtourn", addchampionship, name="addchampionship"),
    path("fixtures/", fixtures, name="volleyball_fixtures"),
    path("futourn/<int:id>", vtourn_details, name="volleyball_tournament"),
    path("vfixture/<int:id>", edit_vfixtures_view, name="update_vfixture"),
    path("vfixturedetail/<int:id>", VFixtureDetail, name="vfixture"),
    path(
        "generate_fixtures/<int:id>/",
        generate_fixtures_view,
        name="generate_fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path(
        "generate-next-round-fixtures/",
        generate_next_round_fixtures,
        name="generate_next_round_fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path("vstandings/", volleyballStandings, name="volleyball_standings"),
    # path("fixtures/", fixtures, name="fixtures"),
    path("Volleyball", Vhome, name="Volleyball"),
    # path("fixtures/", fixtures, name="fixtures"),
    # path("fixtures/", fixtures, name="fixtures"),
    path("Volleyball/<int:id>", Volbol, name="Volleyball"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
