from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    total_likes_on_posts = serializers.SerializerMethodField()
    total_posts = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'profile_picture', 'short_description', 'total_likes_on_posts', 'total_posts')
        extra_kwargs = {'email': {'read_only': True}}

    @staticmethod
    def get_total_likes_on_posts(obj: 'CustomUser') -> int:
        user_posts = obj.get_posts

        if not user_posts.exists():
            return 0

        total_likes = 0
        for post in user_posts:
            total_likes += post.get_likes_count
        return total_likes

    @staticmethod
    def get_total_posts(obj: 'CustomUser') -> int:
        return obj.get_posts.count()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'name', 'profile_picture', 'short_description')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict) -> 'CustomUser':
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            profile_picture=validated_data.get('profile_picture', None),
            short_description=validated_data.get('short_description', '')
        )
        return user
