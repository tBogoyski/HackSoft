import typing

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from posts.paginators import PostCursorPagination
from posts.serializers import PostCreateSerializer, PostSerializer

if typing.TYPE_CHECKING:
    from rest_framework.request import Request


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: 'PostCreateSerializer') -> None:
        serializer.save(author=self.request.user)

    def create(self, request: 'Request', *args, **kwargs) -> 'Response':
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Add the ID field to the response data
        response_data = serializer.data
        response_data['id'] = serializer.instance.id

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class PostListView(ListAPIView):
    queryset = Post.objects.filter(deleted_at__isnull=True)
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination
    permission_classes = [IsAuthenticated]


class PostLikeView(APIView):
    """
    This logic should be handled from the frontend.
    If the post is not liked and the user clicks on the like button, the front end should send a like request.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request: 'Request', post_id: int) -> 'Response':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check is the user already liked the post
        if request.user in post.liked_by.all():
            return Response({'error': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        post.liked_by.add(request.user)
        return Response({'detail': 'Post is liked successfully.'}, status=status.HTTP_200_OK)


class PostUnlikeView(APIView):
    """
    To unlike a post, the user must firstly have liked it.
    This logic should be handled from the frontend.
    If the post is liked and the user clicks on the like button again, the front end should send an unlike request.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request: 'Request', post_id: int) -> 'Response':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check is the user not liked the post
        if request.user not in post.liked_by.all():
            return Response({'error': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        post.liked_by.remove(request.user)
        return Response({'detail': 'Post is unliked successfully.'}, status=status.HTTP_200_OK)


class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: 'Request', post_id: int) -> 'Response':
        try:
            post = Post.objects.get(id=post_id, deleted_at__isnull=True)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        if post.author != request.user:
            return Response({'error': 'You do not have permission to delete this post.'},
                            status=status.HTTP_403_FORBIDDEN)

        post.soft_delete()
        return Response({'detail': 'The post has been deleted.'}, status=status.HTTP_200_OK)
