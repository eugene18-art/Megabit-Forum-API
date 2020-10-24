from django.urls import path

from .views import (
    CreateOrListPost,
    ReadUpdateDeletePost,
)

app_name = "post-api"

urlpatterns = [
    path("", CreateOrListPost.as_view(), name="create-or-list-post"),
    path("<str:postid>/", ReadUpdateDeletePost.as_view(), name="rud-post"),
]