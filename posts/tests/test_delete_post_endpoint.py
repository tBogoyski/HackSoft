from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from posts.models import Post
from tests.base_test_case import BaseAPITestCase
from users.models import CustomUser


class TestDeletePostEndpoint(BaseAPITestCase):
    post = None
    delete_post_url = None
    other_user = None

    def setUp(self):
        super().setUp()

        self.post = Post.objects.create(author=self.user, content='Post content')
        self.assertIsNone(self.post.deleted_at)
        self.delete_post_url = reverse('post_delete', kwargs={'post_id': self.post.id})

    def test_success_delete_post(self):
        response = self.client.delete(self.delete_post_url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('The post has been deleted.', response.data['detail'])
        self.post.refresh_from_db()
        self.assertTrue(self.post)
        self.assertIsNotNone(self.post.deleted_at)

    def test_delete_already_deleted_post(self):
        self.post.deleted_at = timezone.now()
        self.post.save()
        response = self.client.delete(self.delete_post_url, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('Post not found.', response.data['error'])

    def test_post_not_found(self):
        response = self.client.delete(reverse('post_delete', kwargs={'post_id': 9999}), format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('Post not found.', response.data['error'])

    def test_other_user_delete_post(self):
        # Logout the current user
        self.client.post(reverse('logout'), format='json')
        self.client.credentials()

        # Create and login another user
        other_user = CustomUser.objects.create_user(email='other@example.com', password='123456')
        other_user.is_valid = True
        other_user.save()

        login_response = self.client.post(
            reverse('login'),
            {'username': other_user.email, 'password': '123456'},
            format='json'
        )
        self.assertEqual(status.HTTP_200_OK, login_response.status_code)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {login_response.data["token"]}')

        response = self.client.delete(self.delete_post_url, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual('You do not have permission to delete this post.', response.data['error'])

    def test_unauthorized_user(self):
        self.client.credentials()  # Unset the credentials
        response = self.client.delete(self.delete_post_url, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
