from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"groups", GroupViewSet, basename="groups")
router.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
)
router.register(r"follow", FollowViewSet, basename="follow")

jwt_patterns = [
    path("create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns = [
    path("v1/jwt/", include(jwt_patterns)),
    path("v1/", include(router.urls)),
]
