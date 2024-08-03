from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from posts.serializers import PostCreateSerializer, PostSerializer


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class PostLikeView(APIView):
    """
    This logic should be handled from the frontend.
    If the post is not liked and the user clicks on the like button, the front end should send a like request.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check is the user already liked the post
        if request.user in post.liked_by.all():
            return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        post.liked_by.add(request.user)
        return Response({'detail': 'Post is liked successfully.'}, status=status.HTTP_200_OK)


class PostUnlikeView(APIView):
    """
    To unlike a post, the user must firstly have liked it.
    This logic should be handled from the frontend.
    If the post is liked and the user clicks on the like button again, the front end should send an unlike request.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check is the user not liked the post
        if request.user not in post.liked_by.all():
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        post.liked_by.remove(request.user)
        return Response({'detail': 'Post is unliked successfully.'}, status=status.HTTP_200_OK)
