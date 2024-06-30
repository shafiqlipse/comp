from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from .b3views import *

# from competition.views import get_teams


urlpatterns = [
    path("basketball3", Busketball3, name="basketball3"),
    # path("addtourn", addchampionship, name="addchampionship"),
    path("b3fixtures/", fixtures, name="basketball3_fixtures"),
    path("b3tourn/<int:id>", b3tourn_details, name="basketball3_tournament"),
    path("b3fixture/<int:id>", edit_fixtures_view, name="update_b3fixture"),
    path("b3fixturedetail/<int:id>", FixtureDetail, name="b3fixture"),
    path(
        "generate_fixtures/<int:id>/",
        generate_b3fixtures_view,
        name="generate_b3fixtures",
    ),
    # path("fixtures/", fixtures, name="fixtures"),
    # path("fixtures/", fixtures, name="fixtures"),
    path("Basketball3/<int:id>", B3bol, name="Basketball3"),
    # path("Football_fixtures", Fixtures, name="Footfixtures"),
    path("Basketball3", B3home, name="Basketball3"),
    # path("fixtures/", fixtures, name="fixtures"),
    path("b3standings/", basketball3Standings, name="basketball3_standings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
