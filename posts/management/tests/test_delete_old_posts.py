from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from posts.models import Post
from users.models import CustomUser


class TestDeleteOldPostsCommand(TestCase):
    def setUp(self):
        super().setUp()

        author = CustomUser.objects.create_user(email='test@example.com', password='123456')
        # Recently deleted post
        self.recent_post = Post.objects.create(
            author=author,
            content='Post content',
            deleted_at=timezone.now() - timedelta(days=1)
        )

        # Old deleted post
        self.old_post = Post.objects.create(
            author=author,
            content='Post content',
            deleted_at=timezone.now() - timedelta(days=11)
        )
        self.not_deleted_post = Post.objects.create(author=author, content='Post content')
        self.assertEqual(3, Post.objects.count())

    def test_command_hard_deletes_old_posts(self):
        out = StringIO()  # Used for asertion of log messages
        call_command('delete_old_posts', stdout=out)
        self.assertIn(f'Successfully deleted post with id {self.old_post.id}.', out.getvalue())
        self.assertIn('Successfully deleted a total of 1 posts.', out.getvalue())

        self.assertEqual(2, Post.objects.count())
        self.assertFalse(Post.objects.filter(id=self.old_post.id).exists())
        self.assertTrue(Post.objects.filter(id=self.recent_post.id).exists())
        self.assertTrue(Post.objects.filter(id=self.not_deleted_post.id).exists())

    def test_no_post_for_deletion(self):
        self.old_post.delete()
        self.assertEqual(2, Post.objects.count())

        out = StringIO()  # Used for asertion of log messages
        call_command('delete_old_posts', stdout=out)
        self.assertIn('No posts to delete.', out.getvalue())

        self.assertEqual(2, Post.objects.count())
        self.assertTrue(Post.objects.filter(id=self.recent_post.id).exists())
        self.assertTrue(Post.objects.filter(id=self.not_deleted_post.id).exists())
