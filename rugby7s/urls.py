from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from .netviews import *

# from competition.views import get_teams


urlpatterns = [
    path("rugby7s", Ragby7, name="rugby7s"),
    # path("addtourn", addchampionship, name="addchampionship"),
    path("fixtures/", fixtures, name="rugby7s_fixtures"),
    path("r7tourn/<int:id>", r7tourn_details, name="rugby7s_tournament"),
    path("r7fixture/<int:id>", edit_r7fixtures_view, name="update_r7fixture"),
    path("fixturedetail/<int:id>", R7FixtureDetail, name="r7fixture"),
    path("nstandings/", rugby7sStandings, name="rugby7s_standings"),
    path(
        "generate_r7fixtures/<int:id>/",
        generate_r7fixtures_view,
        name="generate_r7fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path(
        "generate-next-round-fixtures/",
        generate_next_round_fixtures,
        name="generate_next_round_fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path("addfixtures/", create_r7fixture, name="addfixture"),
    # path("fixtures/", fixtures, name="fixtures"),
    path("Rugby7s/<int:id>", Rug7s, name="Rugby7s"),
    path("Rugby7s_fixtures", R7Fixtures, name="Netfixtures"),
    path("netfixtures/", netfixtures, name="netfixtures"),
    path("Rugby7s/", R7home, name="Ragby7s"),
    path("Rugby7s_results", R7Results, name="Netresults"),
    # path("Netbalstandings", netbollStandings, name="Netstandings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
