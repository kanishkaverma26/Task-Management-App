from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and representing User objects.

    Features:
        - Handles user creation with hashed password.
        - Ensures password is write-only for security.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        """
        Creates a new user with a properly hashed password.
        """
        return User.objects.create_user(**validated_data)

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.

    Features:
        - Includes nested read-only user details for the creator.
        - Used for task CRUD operations.
    """
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'