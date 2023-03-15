from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from posts.models import Follow


class FollowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="testpass"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="testpass"
        )
        self.client.force_authenticate(user=self.user1)

    def test_anonymous_user_access(self):
        self.client.logout()
        response = self.client.get(reverse("follow"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(
            reverse("follow"), {"following": self.user2.id}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow_user(self):
        response = self.client.post(
            reverse("follow"), {"following": self.user2.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)
        self.assertEqual(Follow.objects.first().user, self.user1)
        self.assertEqual(Follow.objects.first().following, self.user2)
        response = self.client.post(
            reverse("follow"), {"following": self.user2.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Follow.objects.count(), 1)

    def test_get_following(self):
        Follow.objects.create(user=self.user1, following=self.user2)
        Follow.objects.create(user=self.user1, following=self.user3)
        response = self.client.get(reverse("follow"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["following"], self.user2.id)
        self.assertEqual(response.data[1]["following"], self.user3.id)

    def test_search_following(self):
        Follow.objects.create(user=self.user1, following=self.user2)
        Follow.objects.create(user=self.user1, following=self.user3)
        response = self.client.get(reverse("follow") + "?search=user2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["following"], self.user2.id)
