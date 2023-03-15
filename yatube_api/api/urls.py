from django.urls import path
from .views import get_following, add_follow

urlpatterns = [
    path("follow/", get_following, name="get_following"),
    path("follow/add/", add_follow, name="add_follow"),
]
