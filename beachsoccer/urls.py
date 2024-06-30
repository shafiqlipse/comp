from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

# from competition.views import get_teams


urlpatterns = [
    path("beachsoccer", BSball, name="beachsoccer"),
    # path("addtourn", addchampionship, name="addchampionship"),
    path("fixtures/", bsfixtures, name="beachsoccer_fixtures"),
    path("futourn/<int:id>", bstourn_details, name="beachsoccer_tournament"),
    path("fixture/<int:id>", edit_bsfixtures_view, name="update_fixture"),
    path("fixturedetail/<int:id>", FixtureDetail, name="fixture"),
    path(
        "generate_fixtures/<int:id>/",
        generate_bsfixtures_view,
        name="bsgenerate_fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path(
        "generate-next-round-fixtures/",
        generate_next_round_fixtures,
        name="generate_next_round_fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path("bstandings/", beachsoccerStandings, name="beachsoccer_standings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
