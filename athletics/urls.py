from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


# from competition.views import get_teams


urlpatterns = [
    path("athletics", athletic_list_create_update, name="athletics"),
    path("athletic/<int:id>", athletic_detail, name="athletic"),
    path("athletics/<int:id>/", athletic_list_create_update, name="athletic_update"),
    path("delete_athletics/<int:id>/", athletic_delete, name="athletic_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
