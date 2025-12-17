from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project, ProjectEmployee
from .serializers import ProjectSerializer
from users.models import Employee


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Project.objects.all()

        if hasattr(user, "businessowner"):
            return Project.objects.filter(owner=user.businessowner)

        return Project.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, "businessowner"):
            raise PermissionError("Only BusinessOwners can create projects")

        serializer.save(owner=user.businessowner)

    # 🔥 CUSTOM ACTION
    @action(detail=True, methods=["post"], url_path="assign-employee")
    def assign_employee(self, request, pk=None):
        user = request.user

        if not hasattr(user, "businessowner"):
            return Response(
                {"error": "Only BusinessOwners can assign employees"},
                status=status.HTTP_403_FORBIDDEN
            )

        employee_id = request.data.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            project = Project.objects.get(
                id=pk,
                owner=user.businessowner
            )
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or not yours"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            employee = Employee.objects.get(
                id=employee_id,
                owner=user.businessowner
            )
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found or not yours"},
                status=status.HTTP_404_NOT_FOUND
            )

        obj, created = ProjectEmployee.objects.get_or_create(
            project=project,
            employee=employee
        )

        if not created:
            return Response(
                {"error": "Employee already assigned to this project"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Employee assigned successfully"},
            status=status.HTTP_201_CREATED
        )
