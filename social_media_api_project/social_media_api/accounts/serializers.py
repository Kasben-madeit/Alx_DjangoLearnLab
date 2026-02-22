"""
Serializers for the accounts app.

These classes translate between complex Python objects (model
instances) and simple representations suitable for rendering in JSON
and accepting validated input.  They also encapsulate logic for
creating and authenticating users.
"""

from __future__ import annotations

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for representing user profiles."""

    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count'
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration.

    Handles password hashing, user creation and token generation.  When
    a new user is created, a corresponding authentication token is
    automatically generated.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        # Create an auth token so that the user can authenticate immediately
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer used for logging in a user."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        attrs['user'] = user
        return attrs