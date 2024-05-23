from django.contrib.auth import get_user_model, get_user
from django.test import TestCase
from django.urls import reverse

from catalog.models import *


USER_DATA = {
    "username": "user1_username",
    "email": "user1_email@test.com",
    "first_name": "user1_fname",
    "last_name": "user1_lname",
    "city": "user1_city",
    "password": "test12password",
}


class UserAuthTest(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(**USER_DATA)
        self.login_url = reverse("catalog:login")
        self.logout_url = reverse("catalog:logout")
        self.success_url = reverse("catalog:product_list")

    def test_user_login(self):
        response = self.client.post(
            self.login_url,
            {
                "username": USER_DATA["username"],
                "password": USER_DATA["password"]
            },
        )
        self.assertTrue(self.test_user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

        user = get_user(self.client)
        self.assertEqual(user, self.test_user)

    def test_user_logout(self):
        self.client.login(username=USER_DATA["username"], password=USER_DATA["password"])

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, self.success_url)
        user = get_user(self.client)
        self.assertTrue(user.is_anonymous)

    def test_user_cannot_login(self):
        pass


class UserCreateViewTest(TestCase):
    def setUp(self):
        self.login_url = reverse("catalog:login")
        self.register_url = reverse("catalog:register")
        self.success_url = reverse("catalog:product_list")

    def test_user_registration(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "user1_username",
                "email": "user1_email@test.com",
                "first_name": "user1_fname",
                "last_name": "user1_lname",
                "city": "user1_city",
                "password1": "test12password",
                "password2": "test12password",
            }
        )
        self.client.login(username=USER_DATA["username"], password=USER_DATA["password"])
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
