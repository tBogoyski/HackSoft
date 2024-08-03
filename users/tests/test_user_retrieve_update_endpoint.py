from django.urls import reverse
from rest_framework import status

from posts.models import Post
from tests.base_test_case import BaseAPITestCase
from users.models import CustomUser


class TestUserRetrieveEndpoint(BaseAPITestCase):
    retrieve_url = None

    def setUp(self):
        super().setUp()
        self.retrieve_url = reverse('user_profile')

        # Create a post and like it
        post = Post.objects.create(author=self.user, content='Post content')
        post.liked_by.add(self.user)

        # Create another user which will also like the post
        user = CustomUser.objects.create_user(
            email='new@example.com',
            password='123456',
        )
        user.is_valid = True
        user.save()
        post.liked_by.add(user)

    def test_retrieve_user_profile_data(self):
        response = self.client.get(self.retrieve_url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.email, response.data['email'])
        self.assertEqual(self.user.name, response.data['name'])
        self.assertEqual(self.user.profile_picture, response.data['profile_picture'])
        self.assertEqual(self.user.short_description, response.data['short_description'])
        self.assertEqual(2, response.data['total_likes_on_posts'])
        self.assertEqual(1, response.data['total_posts'])

    def test_retrieve_user_profile_when_unauthenticated(self):
        self.client.post(reverse('logout'), format='json')
        self.client.credentials()

        response = self.client.get(self.retrieve_url, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class TestUserUpdateEndpoint(BaseAPITestCase):
    update_url = None

    def setUp(self):
        super().setUp()
        self.update_url = reverse('user_profile')

    def test_successfully_update_user_profile(self):
        data = {
            'name': 'Updated Name',
            'profile_picture': None,
            'short_description': 'Updated Short Description'
        }
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user.refresh_from_db()
        self.assertEqual(data['name'], self.user.name)
        self.assertEqual('', self.user.profile_picture)
        self.assertEqual(data['short_description'], self.user.short_description)

    def test_email_cannot_be_updated(self):
        data = {
            'email': 'new@example.com'
        }
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, data['email'])
        self.assertEqual(self.user.email, 'test@example.com')

    def test_update_user_profile_when_unauthenticated(self):
        self.client.post(reverse('logout'), format='json')
        self.client.credentials()

        data = {
            'name': 'Updated Name',
            'profile_picture': None,
            'short_description': 'Updated Short Description'
        }
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
