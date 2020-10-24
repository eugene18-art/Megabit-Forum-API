from django.urls import path

from .views import (
    CreatePost
)

app_name = "post-api"

urlpatterns = [
    path("", CreatePost.as_view(), name="create-post"),
]