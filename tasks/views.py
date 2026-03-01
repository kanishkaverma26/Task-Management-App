import django_filters
from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .permissions import IsOwnerOrAdmin
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

id_param = OpenApiParameter("id", type=int, location=OpenApiParameter.PATH, description="The unique ID of the task")

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for task listing.

    Attributes:
        page_size (int): Default number of items per page.
        page_size_query_param (str): Query param to allow client-defined page size.
        max_page_size (int): Maximum allowed page size.
        page_query_param (str): Custom query parameter for page number.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page_num'

class CreateUserView(generics.CreateAPIView):
    """
    API endpoint to register a new user.

    Permissions:
        AllowAny – Accessible without authentication.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class TaskFilter(django_filters.FilterSet):
    """
    Filter class for Task model.

    Allows filtering by:
        - completed status
        - creator user ID
    """
    created_by = django_filters.NumberFilter(field_name="created_by__id", lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['completed', 'created_by']

@extend_schema_view(
    list=extend_schema(
        summary="List all tasks",
        description="Retrieve a paginated list of tasks. Admins see all; users see only their own.",
        parameters=[
            # Customizing the Search Description
            OpenApiParameter(
                name='search',
                description='A search term to find tasks. We search within the **title** and **description** fields.',
                required=False,
                type=str,
            ),
            # Customizing the Ordering Description
            OpenApiParameter(
                name='ordering',
                description='Which field to use when ordering the results. Acceptable fields: **created_at**, **-created_at** (newest first).',
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='created_by',
                description='Filter by the ID of the user who created the task.',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='completed',
                description='Filter by completion status. Use **true** or **false**.',
                required=False,
                type=bool,
            ),
        ],
        tags=['Tasks Management']
    ),
    create=extend_schema(summary="Create task", tags=['Tasks Management']),
    retrieve=extend_schema(summary="Get task details", parameters=[id_param], tags=['Tasks Management']),
    update=extend_schema(summary="Update task", parameters=[id_param], tags=['Tasks Management']),
    partial_update=extend_schema(summary="Patch task", parameters=[id_param], tags=['Tasks Management']),
    destroy=extend_schema(summary="Delete task", parameters=[id_param], tags=['Tasks Management']),
)
class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Tasks.

    Features:
        - CRUD operations on tasks
        - Pagination
        - Search (title, description)
        - Filtering (completed, created_by)
        - Ordering (created_at)
        - Role-based data visibility

    Permissions:
        - Admins: Full access to all tasks
        - Users: Access only to their own tasks
    """
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    permission_classes = [IsOwnerOrAdmin]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Fields available for filtering
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        Returns task queryset based on user role.

        Admin Users:
            Can view all tasks.

        Regular Users:
            Can only view tasks created by themselves.
        """
        user = self.request.user
        if user.is_staff:
            return Task.objects.select_related('created_by').all()
        return Task.objects.select_related('created_by').filter(created_by=user)

    def perform_create(self, serializer):
        """
        Automatically assigns the logged-in user as the task creator.
        """
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a task and returns a custom success message.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_200_OK
        )


class TaskStatsView(APIView):
    """
    API endpoint to retrieve task statistics for the logged-in user.

    Endpoint:
        GET /tasks/stats/

    Returns:
        - total_tasks
        - completed_tasks
        - pending_tasks
        - completion_rate (percentage)
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: dict},
        description="Returns task counts and completion percentage for the logged-in user."
    )
    def get(self, request):
        """
        Calculates task statistics for the authenticated user.
        """
        user_tasks = Task.objects.filter(created_by=request.user)
        total = user_tasks.count()
        completed = user_tasks.filter(completed=True).count()
        stats = {
            'total_tasks': total,
            'completed_tasks': completed,
            'pending_tasks': total-completed,
            'completion_rate': f"{(completed / total * 100):.1f}%" if total > 0 else "0%"
        }
        return Response(stats)