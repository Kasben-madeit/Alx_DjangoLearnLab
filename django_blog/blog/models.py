"""
Models for the blog application.

These define the data structures for posts, comments, tags and user profiles.
"""
from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Simple tag model used to categorise blog posts. Tags are identified by
    a unique name and can be associated with multiple posts.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """
    Blog post model. Each post has a title, rich text content, a publication
    timestamp and an author. Posts can also be associated with multiple tags.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    class Meta:
        ordering = ["-published_date"]

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """
    Model representing comments left on blog posts. Comments are linked to a
    specific post and authored by a user. Timestamps capture creation and
    last modification times.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author.username} on {self.post.title}"


class Profile(models.Model):
    """
    Extension of Django's built‑in User model to include additional user data
    such as a bio and an optional profile picture. This model is linked to
    User via a one-to-one relationship.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.user.username} Profile"