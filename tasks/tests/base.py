from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse


class BaseTaskTestCase(APITestCase):
    """
    Common setup for all Task API tests.
    """

    def setUp(self):
        # Common Users
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="test@example.com"
        )

        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpassword",
            email="admin@example.com"
        )

        # Common URLs
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')
        self.tasks_url = reverse('task-list')
        self.stats_url = reverse('task-stats')

    def authenticate_user(self):
        """Helper to log in the regular user."""
        self.client.force_authenticate(user=self.user)

    def authenticate_admin(self):
        """Helper to log in the admin."""
        self.client.force_authenticate(user=self.admin_user)