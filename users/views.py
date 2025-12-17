from django.shortcuts import render
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import Employee
from accounts.models import BusinessOwner

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer




class AssignEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, "businessowner"):
            return Response(
                {"error": "Only BusinessOwners can assign employees"},
                status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get("user_id")
        role = request.data.get("role")
        monthly_salary = request.data.get("monthly_salary")

        if not user_id or not role or not monthly_salary:
            return Response(
                {"error": "user_id, role, monthly_salary are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if hasattr(user, "employee"):
            return Response(
                {"error": "User is already an Employee"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Employee.objects.create(
            user=user,
            owner=request.user.businessowner,
            name=" ".join(filter(None, [user.first_name, user.last_name])) or user.username,
            role=role,
            monthly_salary=monthly_salary
        )


        return Response(
            {"message": "Employee assigned successfully"},
            status=status.HTTP_201_CREATED
        )
