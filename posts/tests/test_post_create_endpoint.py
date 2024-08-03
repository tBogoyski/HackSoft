from django.urls import reverse
from rest_framework import status

from posts.models import Post
from tests.base_test_case import BaseAPITestCase


class TestCreatePost(BaseAPITestCase):
    post_create_url = None
    post_data = None

    def setUp(self):
        super().setUp()
        self.post_create_url = reverse('post_create')
        self.post_data = {
            'content': 'This is a test post'
        }

    def test_create_post_success(self):
        self.assertEqual(0, Post.objects.count())
        response = self.client.post(self.post_create_url, self.post_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn('content', response.data)
        self.assertEqual(self.post_data['content'], response.data['content'])
        self.assertIn('id', response.data)

        self.assertEqual(1, Post.objects.count())
        self.assertEqual(self.post_data['content'], Post.objects.first().content)
        self.assertEqual(self.user, Post.objects.first().author)
        self.assertIsNone(Post.objects.first().deleted_at)

    def test_create_post_unauthenticated(self):
        self.client.credentials()  # Unset the credentials
        response = self.client.post(self.post_create_url, self.post_data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
