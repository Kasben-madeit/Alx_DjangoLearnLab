"""
URL patterns for the notifications app.

Currently only exposes a single endpoint to retrieve notifications.
Further actions such as marking notifications as read could be added
here as the application evolves.
"""

from django.urls import path

from .views import NotificationListView


urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
]