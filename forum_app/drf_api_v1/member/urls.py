from django.urls import path

from .views import (
    CreateMember,
    ReadUpdateDeleteMember,
    Login,
    Logout
)

app_name = "member-api"

urlpatterns = [
    path("auth/signup/", CreateMember.as_view(), name="create"),
    path("auth/signin/", Login.as_view(), name="login"),
    path("auth/signout/", Logout.as_view(), name="logout"),
    path("member/<str:username>/", ReadUpdateDeleteMember.as_view(), name="rud"),
]
