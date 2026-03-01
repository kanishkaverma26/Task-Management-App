# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    """
    Model representing a user-created task.

    Fields:
        title (str): The name of the task.
        description (str): Optional detailed information about the task.
        completed (bool): Indicates whether the task is finished.
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.
        created_by (User): Reference to the user who created the task.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title