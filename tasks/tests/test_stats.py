from django.contrib.auth.models import User

from .base import BaseTaskTestCase
from tasks.models import Task
from rest_framework import status


class TaskStatsTests(BaseTaskTestCase):
    """Test suite for Task statistics API endpoint."""

    def test_task_stats_calculation_success(self):
        """Verify stats calculation returns correct totals and completion rate."""
        self.authenticate_user()

        # Create 4 tasks: 3 completed, 1 pending (75%)
        Task.objects.create(title="T1", completed=True, created_by=self.user)
        Task.objects.create(title="T2", completed=True, created_by=self.user)
        Task.objects.create(title="T3", completed=True, created_by=self.user)
        Task.objects.create(title="T4", completed=False, created_by=self.user)

        response = self.client.get(self.stats_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tasks'], 4)
        self.assertEqual(response.data['completed_tasks'], 3)
        self.assertEqual(response.data['pending_tasks'], 1)
        self.assertEqual(response.data['completion_rate'], "75.0%")

    def test_stats_zero_tasks_edge_case(self):
        """Verify stats handles zero tasks without division error."""
        self.authenticate_user()
        # No tasks created for this user
        response = self.client.get(self.stats_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tasks'], 0)
        self.assertEqual(response.data['completion_rate'], "0%")

    def test_stats_unauthenticated(self):
        """Verify unauthenticated users cannot access stats."""
        # No self.authenticate_user() call here
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_stats_for_new_user_with_no_tasks(self):
        """Verify new user with no tasks gets 0% completion rate."""
        new_user = User.objects.create_user(username="newbie", password="pass")
        self.client.force_authenticate(user=new_user)
        response = self.client.get(self.stats_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total_tasks'], 0)
        self.assertEqual(response.data['completion_rate'], "0%")