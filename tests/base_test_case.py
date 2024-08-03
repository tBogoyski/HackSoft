from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class BaseAPITestCase(APITestCase):
    user = None
    token = None

    def setUp(self):
        super().setUp()

        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='123456',
        )
        self.user.is_valid = True
        self.user.save()

        # Log in to get the token
        login_data = {
            'username': 'test@example.com',
            'password': '123456'
        }
        login_response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(status.HTTP_200_OK, login_response.status_code)
        self.token = login_response.data['token']
        # Add the token to the headers so the views can access it
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
