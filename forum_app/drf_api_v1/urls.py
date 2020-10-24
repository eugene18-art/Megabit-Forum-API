from django.urls import path, include

urlpatterns = [
    path('', include("forum_app.drf_api_v1.member.urls")),
    path('post/', include("forum_app.drf_api_v1.post.urls"))
]