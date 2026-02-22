"""
URL patterns for the accounts app.

Expose endpoints for registering users, logging in, retrieving/updating
the current user's profile and managing follow/unfollow actions.
"""

from django.urls import path

from .views import FollowUserView, LoginView, ProfileView, RegisterView, UnfollowUserView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]