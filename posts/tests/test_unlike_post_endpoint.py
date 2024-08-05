from django.urls import reverse
from rest_framework import status

from posts.models import Post
from tests.base_test_case import BaseAPITestCase


class TestUnlikePostEndpoint(BaseAPITestCase):
    post = None
    unlike_post_url = None

    def setUp(self):
        super().setUp()

        self.post = Post.objects.create(author=self.user, content='Post content')
        self.post.liked_by.add(self.user)
        self.assertEqual(1, self.post.get_likes_count)
        self.unlike_post_url = reverse('post_unlike', kwargs={'post_id': self.post.id})

    def test_success_unlike_post(self):
        response = self.client.post(self.unlike_post_url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Post is unliked successfully.', response.data['detail'])

        self.assertEqual(0, self.post.get_likes_count)
        self.assertNotIn(self.user, self.post.liked_by.all())

    def test_unlike_already_unliked_post(self):
        self.post.liked_by.remove(self.user)
        response = self.client.post(self.unlike_post_url, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('You have not liked this post.', response.data['error'])

    def test_post_not_found(self):
        response = self.client.post(reverse('post_unlike', kwargs={'post_id': 9999}), format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('Post not found.', response.data['error'])

    def test_unauthorized_user(self):
        self.client.credentials()  # Unset the credentials
        response = self.client.post(self.unlike_post_url, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
