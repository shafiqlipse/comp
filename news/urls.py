from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

#


urlpatterns = [
    path("newpost", create_post, name="newpost"),
    path("posts", post_list, name="posts"),
    path("post/<int:id>", post_detail, name="post"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
