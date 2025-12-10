from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Expense, ResourceConsumption, SalaryPayment, Budget
from .serializers import (
    ExpenseSerializer, ResourceConsumptionSerializer,
    SalaryPaymentSerializer, BudgetSerializer
)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["project", "date", "amount"]
    search_fields = ["title"]
    ordering_fields = ["date", "amount"]

class ResourceConsumptionViewSet(viewsets.ModelViewSet):
    queryset = ResourceConsumption.objects.all()
    serializer_class = ResourceConsumptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["project", "date", "resource_type", "amount"]
    search_fields = ["resource_type"]
    ordering_fields = ["date", "amount"]

class SalaryPaymentViewSet(viewsets.ModelViewSet):
    queryset = SalaryPayment.objects.all()
    serializer_class = SalaryPaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["project", "employee", "date", "amount"]
    search_fields = ["employee"]
    ordering_fields = ["date", "amount"]

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["project", "total_amount", "created_at"]
    search_fields = ["project__name"]
    ordering_fields = ["total_amount", "created_at"]
