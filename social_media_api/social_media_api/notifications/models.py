"""
Models for the notifications app.

Notifications alert users to relevant activity on the platform such as
new followers, likes and comments.  Notifications use Django’s
generic relations to associate with any model type (e.g. posts,
comments or even other users).
"""

from __future__ import annotations

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(models.Model):
    """A notification sent to a user when relevant activity occurs."""

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text='The user who will receive this notification',
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actor_notifications',
        help_text='The user who performed the action generating this notification',
    )
    verb = models.CharField(
        max_length=50,
        help_text='A short description of the action (e.g. "liked", "followed", "commented")',
    )
    # Generic relation to the object that is the target of the notification
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    target_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self) -> str:
        return f"Notification for {self.recipient.username} from {self.actor.username}: {self.verb}"