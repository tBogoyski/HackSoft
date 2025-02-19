from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.author} - {self.content[:50]}'  # First 50 characters of the content

    @property
    def get_likes_count(self):
        return self.liked_by.count()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
