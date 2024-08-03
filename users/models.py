import typing

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from posts.models import Post

if typing.TYPE_CHECKING:
    from django.db.models import QuerySet


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str = None, **extra_fields) -> 'CustomUser':
        if not email:
            raise ValueError('The Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields) -> 'CustomUser':
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.create_user(email, password, **extra_fields)
        user.is_valid = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=70, unique=True)
    name = models.CharField(max_length=100, help_text='All names of the user')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True)
    is_valid = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def get_posts(self) -> 'QuerySet':
        return Post.objects.filter(author=self, deleted_at__isnull=True)
