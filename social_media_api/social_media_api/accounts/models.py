"""
Models for the accounts app.

The ``CustomUser`` model extends Django’s built-in ``AbstractUser`` to
provide additional fields commonly required in social media platforms,
including a biography, profile picture and follower/following
relationships.  This model serves as the ``AUTH_USER_MODEL`` for the
project, enabling full customization of user behaviour and fields.
"""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model with additional social media fields.

    Attributes
    ----------
    bio : TextField
        A short biography provided by the user.
    profile_picture : ImageField
        Optional avatar image uploaded by the user.  Images are stored
        under ``profile_pictures/`` within ``MEDIA_ROOT``.
    followers : ManyToManyField
        Relationship representing which users follow this user.  This
        field is non‑symmetrical, so if A follows B, it does not
        automatically imply that B follows A.  The related name
        ``following`` enables queries like ``user.following.all()`` to
        retrieve the users that ``user`` follows.
    following : ManyToManyField
        Relationship representing which users this user follows.  The
        related name ``followers_set`` makes it possible to query
        ``user.followers_set.all()`` to retrieve users following ``user``.
    """

    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # Users who follow this user
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    # Users that this user follows
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers_set', blank=True)

    def __str__(self) -> str:
        return self.username