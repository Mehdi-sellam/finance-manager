from django.shortcuts import render
from rest_framework import viewsets
from .models import Expense, ResourceConsumption, SalaryPayment, Budget
from .serializers import (
    ExpenseSerializer, ResourceConsumptionSerializer,
    SalaryPaymentSerializer, BudgetSerializer
)


# Create your views here.

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ResourceConsumptionViewSet(viewsets.ModelViewSet):
    queryset = ResourceConsumption.objects.all()
    serializer_class = ResourceConsumptionSerializer

class SalaryPaymentViewSet(viewsets.ModelViewSet):
    queryset = SalaryPayment.objects.all()
    serializer_class = SalaryPaymentSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
