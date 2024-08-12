from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from .r15tviews import *

# from competition.views import get_teams


urlpatterns = [
    path("rugby15s", Ragby15, name="rugby15s"),
    # path("addtourn", addchampionship, name="addchampionship"),
    path("fixtures/", fixtures, name="rugby15s_fixtures"),
    path("r15tourn/<int:id>", r15tourn_details, name="rugby15s_tournament"),
    path("r15fixture/<int:id>", edit_r15fixtures_view, name="update_r15fixture"),
    path("fixturedetail/<int:id>", R15FixtureDetail, name="r15fixture"),
    path("nstandings/", rugby15sStandings, name="rugby15s_standings"),
    path(
        "generate_r15fixtures/<int:id>/",
        generate_r15fixtures_view,
        name="generate_r15fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path(
        "generate-next-round-fixtures/",
        generate_next_round_fixtures,
        name="generate_next_round_fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path("addfixtures/", create_r15fixture, name="addfixture"),
    # path("fixtures/", fixtures, name="fixtures"),
    path("Rugby15s/<int:id>", Rug15s, name="Rugby15s"),
    path("Rugby15s_fixtures", R15Fixtures, name="Netfixtures"),
    path("netfixtures/", netfixtures, name="netfixtures"),
    path("Rugby15s/", R15home, name="Ragby15s"),
    path("Rugby15s_results", R15Results, name="Netresults"),
    # path("Netbalstandings", netbollStandings, name="Netstandings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
