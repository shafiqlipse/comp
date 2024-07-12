from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from .hadviews import *

# from competition.views import get_teams


urlpatterns = [
    path("handball", Hutball, name="handball"),
    # path("addtourn", addchampionship, name="addchampionship"),
    path("hfixtures/", fixtures, name="handball_fixtures"),
    path("hhtourn/<int:id>", htourn_details, name="handball_tournament"),
    path("hfixture/<int:id>", edit_fixtures_view, name="update_hfixture"),
    path("hfixturedetail/<int:id>", FixtureDetail, name="hfixture"),
    path(
        "generate_fixtures/<int:id>/",
        generate_hfixtures_view,
        name="generate_hfixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    path(
        "generate-next-round-fixtures/",
        generate_next_round_fixtures,
        name="generate_next_round_fixtures",
    ),
    path("hstandings/", handballStandings, name="handball_standings"),
    # path("fixtures/", fixtures, name="fixtures"),
    path("handfixtures/", handfixtures, name="handfixtures"),
    # path("fixtures/", fixtures, name="fixtures"),
    path("Handball/<int:id>", Handbol, name="Handball"),
    path("Handball/", Hhome, name="Handball"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
