from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

# from competition.views import get_teams


urlpatterns = [
    path("basketball5", Busketball5, name="basketball5"),
    # path("addtourn", addchampionship, name="addchampionship"),
    path("b5fixtures/", fixtures, name="basketball5_fixtures"),
    path("b5tourn/<int:id>", b5tourn_details, name="basketball5_tournament"),
    path("b5fixture/<int:id>", edit_fixtures_view, name="update_b5fixture"),
    path("b5fixturedetail/<int:id>", FixtureDetail, name="b5fixture"),
    path(
        "generate_fixtures/<int:id>/",
        generate_b5fixtures_view,
        name="generate_b5fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path("b5standings/", basketball5Standings, name="basketball5_standings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
