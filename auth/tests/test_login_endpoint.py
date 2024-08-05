from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class TestAuthLoginEndpoint(APITestCase):
    user = None
    login_url = None

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='123456',
        )
        self.user.is_valid = True
        self.user.save()

        self.login_url = reverse('login')

    def test_login_success(self):
        data = {
            'username': 'test@example.com',
            'password': '123456'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.email, response.data['email'])
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        data = {
            'username': 'test@example.com',
            'password': 'wrong-password'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Invalid credentials', response.data['error'])

        data = {
            'username': 'other@example.com',
            'password': '123456'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Invalid credentials', response.data['error'])

    def test_invalid_user(self):
        self.user.is_valid = False
        self.user.save()

        data = {
            'username': 'test@example.com',
            'password': '123456'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Not a valid user. Please contact admin.', response.data['error'])
