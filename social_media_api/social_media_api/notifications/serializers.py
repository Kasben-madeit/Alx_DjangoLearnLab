"""
Serializers for the notifications app.

The ``NotificationSerializer`` provides a concise representation of
notifications, including the usernames of the actor and recipient
and a string representation of the target object.
"""

from __future__ import annotations

from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""

    actor = serializers.ReadOnlyField(source='actor.username')
    recipient = serializers.ReadOnlyField(source='recipient.username')
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 'target', 'timestamp', 'read'
        ]

    def get_target(self, obj: Notification) -> str | None:
        """Return a human‑readable representation of the notification target."""
        return str(obj.target_object) if obj.target_object else None