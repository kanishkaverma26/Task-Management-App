from .base import BaseTaskTestCase
from rest_framework import status

from ..models import Task


class TaskListTests(BaseTaskTestCase):
    """Test suite for Task list and creation API endpoints."""

    def test_list_tasks_authenticated(self):
        """Verify authenticated user can retrieve task list."""
        self.authenticate_user()
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        """Verify authenticated user can create a task."""
        self.authenticate_user()
        data = {"title": "Base Test Task", "description": "Testing common setup"}
        response = self.client.post(self.tasks_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify the perform_create logic
        self.assertEqual(response.data['created_by']['id'], self.user.id)

    def test_task_string_representation(self):
        """Verify Task model string representation returns title."""
        task = Task.objects.create(title="String Test", created_by=self.user)
        self.assertEqual(str(task), "String Test")

    def test_admin_can_list_all_tasks(self):
        """Verify admin can retrieve all tasks."""
        self.authenticate_admin()
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 200)