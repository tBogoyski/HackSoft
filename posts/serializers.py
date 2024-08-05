from rest_framework import serializers

from posts.models import Post
from users.models import CustomUser


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'short_description', 'profile_picture')


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    liked_by = serializers.SlugRelatedField(
        slug_field='email',
        many=True,
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'created_at', 'liked_by', 'get_likes_count')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('content',)
