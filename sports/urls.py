from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

# from competition.views import get_teams


urlpatterns = [
  
    path("sports", Sports, name="sports"),
    # path("addsport", addsport, name="addsport"),
    path("sport/<int:id>", SportDetail, name="sportDetail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
