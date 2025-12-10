from rest_framework import viewsets
from .models import Expense, SalaryPayment, ResourceConsumption, Budget
from .serializers import ExpenseSerializer, SalaryPaymentSerializer, ResourceConsumptionSerializer, BudgetSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        if project_id:
            return Expense.objects.filter(project_id=project_id)
        return Expense.objects.all()

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        if project_id:
            serializer.save(project_id=project_id)
        else:
            serializer.save()


class SalaryPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = SalaryPaymentSerializer

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        if project_id:
            return SalaryPayment.objects.filter(project_id=project_id)
        return SalaryPayment.objects.all()

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        if project_id:
            serializer.save(project_id=project_id)
        else:
            serializer.save()


class ResourceConsumptionViewSet(viewsets.ModelViewSet):
    queryset = ResourceConsumption.objects.all()
    serializer_class = ResourceConsumptionSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        if project_id:
            return Budget.objects.filter(project_id=project_id)
        return Budget.objects.all()

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        if project_id:
            serializer.save(project_id=project_id)
        else:
            serializer.save()
