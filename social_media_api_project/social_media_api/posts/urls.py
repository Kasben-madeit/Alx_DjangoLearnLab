"""
URL patterns for the posts app.

Defines routes for posts and nested comments using function-based
views to allow for custom patterns without requiring third‑party
packages for nested routers.  Also exposes endpoints for liking and
unliking posts and retrieving the feed of posts from followed users.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FeedView, LikePostView, PostViewSet, UnlikePostView


# Configure a router for posts.  Comments are handled via explicit
# paths instead of a nested router to avoid external dependencies.
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# Comments views – we explicitly create list and detail views bound to
# a specific post.  The ``post_pk`` argument is passed through the
# URL pattern to the viewset.
comment_list = CommentViewSet.as_view({'get': 'list', 'post': 'create'})
comment_detail = CommentViewSet.as_view(
    {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}
)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/comments/', comment_list, name='comment-list'),
    path('posts/<int:post_pk>/comments/<int:pk>/', comment_detail, name='comment-detail'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('feed/', FeedView.as_view(), name='feed'),
]