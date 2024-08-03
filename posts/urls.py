from django.urls import path

from posts.views import PostCreateView, PostListView, PostLikeView, PostUnlikeView, PostDeleteView

urlpatterns = [
    path('list/', PostListView.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:post_id>/like/', PostLikeView.as_view(), name='post_like'),
    path('<int:post_id>/unlike/', PostUnlikeView.as_view(), name='post_unlike'),
    path('<int:post_id>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
