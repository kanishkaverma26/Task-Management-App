from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Task model.

    Features:
        - Displays key task details in the admin list view.
        - Enables filtering by:
            • completion status
            • task creator
            • creation date
        - Allows searching by title and description.

    Admin List View:
        Columns shown:
            - title
            - created_by
            - completed
            - created_at
    """
    list_display = ('title', 'created_by', 'completed', 'created_at')
    list_filter = ('completed', 'created_by', 'created_at')
    search_fields = ('title', 'description')