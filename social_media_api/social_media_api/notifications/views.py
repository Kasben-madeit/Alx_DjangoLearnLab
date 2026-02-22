"""
Views for the notifications app.

Currently exposes a simple list endpoint for retrieving all
notifications for the authenticated user.  Pagination and filtering
are handled by the REST framework settings defined in the project
configuration.
"""

from __future__ import annotations

from rest_framework import generics, permissions

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """List all notifications for the current user."""

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)