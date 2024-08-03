import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from posts.models import Post
from tests.base_test_case import BaseAPITestCase


class TestPostListEndpoint(BaseAPITestCase):
    post_list_url = None
    post1 = None
    post2 = None

    def setUp(self):
        super().setUp()
        self.post_list_url = reverse('post_list')

        self.post1 = Post.objects.create(author=self.user, content='Post 1 content')
        # Add likes to this post
        self.post2 = Post.objects.create(author=self.user, content='Post 2 content')
        self.post2.liked_by.add(self.user)

        Post.objects.create(author=self.user, content='Post 3 content', deleted_at=timezone.now())
        self.assertEqual(3, Post.objects.count())

    def assert_created_at_field(self, post_created_at, response_created_at):
        response_created_at = datetime.datetime.fromisoformat(response_created_at)
        post2_created_at_str = post_created_at.astimezone(timezone.get_current_timezone()).isoformat()
        self.assertEqual(post2_created_at_str, response_created_at.isoformat())

    def test_list_posts(self):
        response = self.client.get(self.post_list_url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert the soft-deleted post is not returned
        self.assertEqual(2, len(response.data['results']))

        # Assert the posts are sorted by created_at in descending order
        self.assertEqual(self.post2.id, response.data['results'][0]['id'])
        self.assertEqual(self.post1.id, response.data['results'][1]['id'])

        # Assert the returned data is correct
        post2_response_data = response.data['results'][0]
        self.assertEqual(self.post2.id, post2_response_data['id'])
        self.assertEqual(self.post2.author.name, post2_response_data['author']['name'])
        self.assertEqual(self.post2.author.short_description, post2_response_data['author']['short_description'])
        self.assertEqual(self.post2.author.profile_picture, post2_response_data['author']['profile_picture'])
        self.assertEqual(self.post2.content, post2_response_data['content'])
        self.assert_created_at_field(self.post2.created_at, post2_response_data['created_at'])
        self.assertEqual(self.post2.liked_by.first().email, post2_response_data['liked_by'][0])
        self.assertEqual(self.post2.get_likes_count, post2_response_data['get_likes_count'])

    def test_unauthorized_user(self):
        self.client.credentials()  # Unset the credentials
        response = self.client.get(self.post_list_url, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_pagination(self):
        # Create more than 20 posts
        for i in range(30):
            Post.objects.create(author=self.user, content='Some Post content')

        response = self.client.get(self.post_list_url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert only 20 posts are returned
        self.assertEqual(20, len(response.data['results']))
        self.assertIn('next', response.data)
        # Assert there is a next page link
        self.assertTrue(response.data['next'])
        self.assertIn('previous', response.data)
        self.assertFalse(response.data['previous'])
