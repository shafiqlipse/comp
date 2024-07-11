from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from .netviews import *

# from competition.views import get_teams


urlpatterns = [
    path("netball", Nutball, name="netball"),
    # path("addtourn", addchampionship, name="addchampionship"),
    path("fixtures/", fixtures, name="netball_fixtures"),
    path("futourn/<int:id>", ntourn_details, name="netball_tournament"),
    path("nfixture/<int:id>", edit_nfixtures_view, name="update_nfixture"),
    path("fixturedetail/<int:id>", NFixtureDetail, name="nfixture"),
    path("nstandings/", netballStandings, name="netball_standings"),
    path(
        "generate_nfixtures/<int:id>/",
        generate_nfixtures_view,
        name="generate_nfixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path(
        "generate-next-round-fixtures/",
        generate_next_round_fixtures,
        name="generate_next_round_fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    # path("fixtures/", fixtures, name="fixtures"),
    path("Netball/<int:id>", Nutbol, name="Netball"),
    path("Netball_fixtures", NFixtures, name="Netfixtures"),
    path("Netball/", Nhome, name="Netball"),
    path("Netball_results", NResults, name="Netresults"),
    path("Netbalstandings", netbollStandings, name="Netstandings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
