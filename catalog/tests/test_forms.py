from django.test import TestCase

from catalog.forms import (
    LoginForm,
    RegistrationForm,
)


class AuthFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.login_form_data = {
            "username": "admin",
            "password": "test12password",
        }
        cls.registration_form_data = {
            "username": "user1_username",
            "email": "user1_email@test.com",
            "first_name": "user1_fname",
            "last_name": "user1_lname",
            "city": "user1_city",
            "password1": "test12password",
            "password2": "test12password",
        }

    def test_login_form_valid(self):
        form = LoginForm(data=self.login_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.login_form_data)

    def test_registration_form_valid(self):
        form = RegistrationForm(data=self.registration_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.registration_form_data)
