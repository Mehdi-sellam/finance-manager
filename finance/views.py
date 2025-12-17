# finance/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Expense, ResourceConsumption, SalaryPayment, Budget
from .serializers import (
    ExpenseSerializer,
    ResourceConsumptionSerializer,
    SalaryPaymentSerializer,
    BudgetSerializer
)
from .filters import (
    ExpenseFilter,
    ResourceConsumptionFilter,
    SalaryPaymentFilter,
    BudgetFilter
)

from accounts.permissions import IsOwnerOrAdmin, IsOwnerEmployeeOrAdmin


# ------------------------
# Expense
# ------------------------
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExpenseFilter
    search_fields = ["title"]
    ordering_fields = ["date", "amount"]
    permission_classes = [IsOwnerEmployeeOrAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Expense.objects.all()

        if hasattr(user, "businessowner"):
            return Expense.objects.filter(
                project__owner=user.businessowner
            )

        if hasattr(user, "employee"):
            return Expense.objects.filter(
                project__owner=user.employee.owner
            )

        return Expense.objects.none()


# ------------------------
# Resource Consumption
# ------------------------
class ResourceConsumptionViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceConsumptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ResourceConsumptionFilter
    search_fields = ["resource_name"]
    ordering_fields = ["quantity", "cost_per_unit"]
    permission_classes = [IsOwnerEmployeeOrAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return ResourceConsumption.objects.all()

        if hasattr(user, "businessowner"):
            return ResourceConsumption.objects.filter(
                expense__project__owner=user.businessowner
            )

        if hasattr(user, "employee"):
            return ResourceConsumption.objects.filter(
                expense__project__owner=user.employee.owner
            )

        return ResourceConsumption.objects.none()


# ------------------------
# Salary Payment
# ------------------------
class SalaryPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = SalaryPaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SalaryPaymentFilter
    search_fields = ["employee__user__username"]
    ordering_fields = ["date", "amount"]
    permission_classes = [IsOwnerEmployeeOrAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return SalaryPayment.objects.all()

        if hasattr(user, "businessowner"):
            return SalaryPayment.objects.filter(
                employee__owner=user.businessowner
            )

        if hasattr(user, "employee"):
            return SalaryPayment.objects.filter(
                employee__owner=user.employee.owner
            )

        return SalaryPayment.objects.none()


# ------------------------
# Budget
# ------------------------
class BudgetViewSet(viewsets.ModelViewSet): 
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BudgetFilter
    search_fields = ["project__name"]
    ordering_fields = ["total_amount", "created_at"]
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Budget.objects.all()

        if hasattr(user, "businessowner"):
            return Budget.objects.filter(
                project__owner=user.businessowner
            )

        return Budget.objects.none()
