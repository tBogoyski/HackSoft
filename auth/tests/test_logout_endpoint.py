from django.urls import reverse
from rest_framework import status

from tests.base_test_case import BaseAPITestCase


class TestAuthLogoutEndpoint(BaseAPITestCase):
    logout_url = None

    def setUp(self):
        super().setUp()
        self.logout_url = reverse('logout')

    def test_logout_success(self):
        logout_response = self.client.post(self.logout_url, format='json')
        self.assertEqual(status.HTTP_200_OK, logout_response.status_code)
        self.assertEqual('Successfully logged out.', logout_response.data['detail'])

    def test_logout_with_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token wrong_token')
        logout_response = self.client.post(self.logout_url, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, logout_response.status_code)
        self.assertEqual('Invalid token.', logout_response.data['detail'])
