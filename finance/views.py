from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Expense, ResourceConsumption, SalaryPayment, Budget
from .serializers import (
    ExpenseSerializer,
    ResourceConsumptionSerializer,
    SalaryPaymentSerializer,
    BudgetSerializer
)
from .filters import ExpenseFilter, ResourceConsumptionFilter, SalaryPaymentFilter, BudgetFilter
from .permissions import IsOwnerOrAdmin, IsEmployeeOrAdmin, IsOwnerEmployeeOrAdmin

# ----------------------
# Finance ViewSets
# ----------------------

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExpenseFilter
    search_fields = ["title"]
    ordering_fields = ["date", "amount"]
    permission_classes = [IsOwnerEmployeeOrAdmin]


class ResourceConsumptionViewSet(viewsets.ModelViewSet):
    queryset = ResourceConsumption.objects.all()
    serializer_class = ResourceConsumptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ResourceConsumptionFilter
    search_fields = ["resource_name"]
    ordering_fields = ["quantity", "cost_per_unit"]
    permission_classes = [IsOwnerEmployeeOrAdmin]  # added


class SalaryPaymentViewSet(viewsets.ModelViewSet):
    queryset = SalaryPayment.objects.all()
    serializer_class = SalaryPaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SalaryPaymentFilter
    search_fields = ["employee__name"]
    ordering_fields = ["date", "amount"]
    permission_classes = [IsOwnerEmployeeOrAdmin]  # added


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BudgetFilter
    search_fields = ["project__name"]
    ordering_fields = ["total_amount", "created_at"]
    permission_classes = [IsOwnerOrAdmin]

