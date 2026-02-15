"""
URL routing for the blog application.

This file defines URL patterns for posts, comments, authentication and user
profile management. Patterns are named to simplify reverse URL lookups.
"""
from django.urls import path

from . import views


urlpatterns = [
    path("", views.PostListView.as_view(), name="blog-home"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("post/<int:pk>/comment/", views.add_comment, name="add-comment"),
    path(
        "post/<int:pk>/comment/<int:comment_id>/edit/",
        views.edit_comment,
        name="edit-comment",
    ),
    path(
        "post/<int:pk>/comment/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete-comment",
    ),
    path("tag/<str:tag_name>/", views.TagListView.as_view(), name="tag-posts"),
    path("search/", views.search, name="search"),
]