from .base import BaseTaskTestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthAPITests(BaseTaskTestCase):
    """Test suite for authentication and user registration APIs."""

    def test_user_registration_success(self):
        """Verify a new user can successfully register."""
        # Test registering a brand new user
        data = {
            "username": "new_explorer",
            "password": "secure_pass_123",
            "email": "explorer@example.com"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username="new_explorer").count(), 1)

    def test_jwt_token_generation_success(self):
        """Verify user can obtain JWT access and refresh tokens."""
        # Test getting access/refresh pair using credentials from base.py
        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_access_token_refresh_success(self):
        """Verify access token can be refreshed using refresh token."""
        # First, get a refresh token
        login_data = {"username": self.username, "password": self.password}
        login_res = self.client.post(self.token_url, login_data)
        refresh_token = login_res.data['refresh']

        # Use the refresh token to get a new access token
        response = self.client.post(self.token_refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)