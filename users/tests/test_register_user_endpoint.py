from django.urls import reverse
from rest_framework import status

from tests.base_test_case import BaseAPITestCase
from users.models import CustomUser


class TestRegisterUserEndpoint(BaseAPITestCase):
    register_url = None

    def setUp(self):
        super().setUp()
        # Logout the user to be able to register a new user
        logout_response = self.client.post(reverse('logout'), format='json')
        self.assertEqual(status.HTTP_200_OK, logout_response.status_code)
        self.client.credentials()

        self.register_url = reverse('register')

    def test_register_user_success(self):
        data = {
            'email': 'new@example.com',
            'password': '123456',
            'name': 'Test User',
            'profile_picture': None,
            'short_description': 'A short bio'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user_qs = CustomUser.objects.filter(email='new@example.com')
        self.assertTrue(user_qs.exists())
        user = user_qs.first()
        self.assertEqual('Test User', user.name)
        self.assertEqual('', user.profile_picture)
        self.assertEqual('A short bio', user.short_description)
        self.assertFalse(user.is_valid)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.created_at)  # Assert that the field has a value

    def test_register_user_missing_email(self):
        data = {
            'password': '123456',
            'name': 'Test User',
            'profile_picture': None,
            'short_description': 'A short bio'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('email', response.data)

    def test_reguster_invalid_email(self):
        data = {
            'email': 'invalid-email',
            'password': '123456',
            'name': 'Test User',
            'profile_picture': None,
            'short_description': 'A short bio'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('email', response.data)

    def test_register_user_missing_password(self):
        data = {
            'email': 'new@example.com',
            'name': 'Test User',
            'profile_picture': None,
            'short_description': 'A short bio'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('password', response.data)
