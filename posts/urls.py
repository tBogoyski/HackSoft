from django.urls import path

from posts.views import PostCreateView, PostListView, PostLikeView, PostUnlikeView

urlpatterns = [
    path('list/', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),
    path('<int:post_id>/unlike/', PostUnlikeView.as_view(), name='post-unlike'),
]
