"""
Views for the accounts app.

These API endpoints handle registration, login, retrieving and
updating the authenticated user's profile, and managing follow
relationships.  Upon successful registration or login, an
authentication token is returned which must accompany subsequent
requests to protected endpoints.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer
from notifications.models import Notification

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Endpoint for creating a new user account."""

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(pk=response.data['id'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Authenticate a user and return their token."""

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user, context={'request': request}).data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FollowUserView(APIView):
    """Follow another user.

    This view updates both the current user's ``following`` relationship and
    the target user's ``followers`` relationship.  A notification is
    generated to inform the target that they have a new follower.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int, *args, **kwargs):
        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if target == request.user:
            return Response({'detail': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        # update following/followers relationships
        request.user.following.add(target)
        target.followers.add(request.user)
        # create a notification for the target user
        Notification.objects.create(
            recipient=target,
            actor=request.user,
            verb='followed',
            target_object=target,
        )
        return Response({'detail': 'Followed successfully'}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    """Unfollow another user."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int, *args, **kwargs):
        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        request.user.following.remove(target)
        target.followers.remove(request.user)
        return Response({'detail': 'Unfollowed successfully'}, status=status.HTTP_200_OK)