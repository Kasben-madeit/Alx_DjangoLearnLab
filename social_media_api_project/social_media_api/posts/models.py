"""
Models for the posts app.

Three core models define content on the social media platform:

* ``Post`` — authored by a user and consisting of a title and body
  content.
* ``Comment`` — attached to a post and authored by a user.  When a
  comment is created, a notification is sent to the post author.
* ``Like`` — represents a user liking a post.  Users can like a post
  only once; attempting to like the same post again will result in an
  error at the API level.  Liking a post generates a notification
  for the post author.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models


class Post(models.Model):
    """A post authored by a user."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """A comment authored by a user on a specific post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Comment by {self.author.username} on {self.post.title}"


class Like(models.Model):
    """Represents a user liking a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.post.title}"