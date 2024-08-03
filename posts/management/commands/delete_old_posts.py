from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from posts.models import Post


class Command(BaseCommand):
    help = 'Hard deletes posts that were soft-deleted more than 10 days ago.'

    def handle(self, *args, **kwargs):
        ten_days_ago = timezone.now() - timedelta(days=10)
        posts_to_delete = Post.objects.filter(deleted_at__lt=ten_days_ago)

        if posts_to_delete.exists() is False:
            self.stdout.write(self.style.SUCCESS('No posts to delete.'))
            return

        count = posts_to_delete.count()
        for post in posts_to_delete:
            post_id = post.id
            post.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted post with id {post_id}.'))

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted a total of {count} posts.'))
