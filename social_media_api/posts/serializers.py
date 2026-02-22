"""
Serializers for the posts app.

Serializers translate between model instances and JSON representations
while encapsulating validation and nested representation logic.  The
``PostSerializer`` nests comments and calculates like counts; the
``CommentSerializer`` represents comments and associates the
authenticated user on creation; the ``LikeSerializer`` is used
internally and not exposed directly to clients.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment, Like, Post

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['post', 'author', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts with nested comments and like count."""

    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'likes_count'
        ]


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for post likes.  Primarily for internal use."""

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['created_at']