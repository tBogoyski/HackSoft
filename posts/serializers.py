from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
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
