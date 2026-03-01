from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit/view it.
    """

    def has_object_permission(self, request, view, obj):
        # Admin users get full access
        if request.user.is_staff:
            return True

        # Regular users only get access if they own the task
        return obj.created_by == request.user