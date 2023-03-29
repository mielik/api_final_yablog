from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet

v1_router = SimpleRouter()
v1_router.register("posts", PostViewSet, basename="post")
v1_router.register("groups", GroupViewSet, basename="group")
v1_router.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
)
v1_router.register("follow", FollowViewSet, basename="follow")

app_name = "api"

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/", include("djoser.urls")),
    # JWT-эндпоинты, для управления JWT-токенами:
    path("v1/", include("djoser.urls.jwt")),
]
