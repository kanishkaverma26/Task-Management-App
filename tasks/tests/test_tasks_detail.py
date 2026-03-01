from django.contrib.auth.models import User

from .base import BaseTaskTestCase
from tasks.models import Task
from django.urls import reverse
from rest_framework import status

class TaskDetailTests(BaseTaskTestCase):
    """Test suite for Task detail API endpoints (retrieve, update, delete)."""

    def setUp(self):
        """Initialize test task and detail endpoint URL."""
        super().setUp()
        self.task = Task.objects.create(title="Detail Task", created_by=self.user)
        self.detail_url = reverse('task-detail', args=[self.task.id])

    def test_get_task(self):
        """Verify authenticated user can retrieve a task by ID."""
        self.authenticate_user()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        """Verify authenticated user can fully update a task."""
        self.authenticate_user()
        payload = {"title": "Updated", "description": "New", "completed": True}
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_task(self):
        """Verify authenticated user can partially update a task."""
        self.authenticate_user()
        response = self.client.patch(self.detail_url, {"completed": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        """"Verify authenticated user can delete a task."""
        self.authenticate_user()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Task deleted successfully.")

    def test_unauthorized_user_cannot_access_task(self):
        """Verify non-owner cannot access another user's task."""
        other_user = User.objects.create_user(username="stranger", password="password")
        self.client.force_authenticate(user=other_user)
        response = self.client.get(self.detail_url)
        self.assertIn(response.status_code, [403, 404])