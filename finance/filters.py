import django_filters
from .models import Expense, SalaryPayment, OwnerSalary, ResourceConsumption, Budget

class ExpenseFilter(django_filters.FilterSet):
    class Meta:
        model = Expense
        fields = {
            'title': ['icontains'],
            'amount': ['exact', 'gt', 'lt'],
            'date': ['exact', 'gte', 'lte'],
            'project': ['exact'],
        }

class SalaryPaymentFilter(django_filters.FilterSet):
    class Meta:
        model = SalaryPayment
        fields = {
            'employee': ['exact'],
            'amount': ['exact', 'gt', 'lt'],
            'date': ['exact', 'gte', 'lte'],
            'project': ['exact'],
        }

class OwnerSalaryFilter(django_filters.FilterSet):
    class Meta:
        model = OwnerSalary
        fields = {
            'owner': ['exact'],
            'amount': ['exact', 'gt', 'lt'],
            'date': ['exact', 'gte', 'lte'],
        }

class ResourceConsumptionFilter(django_filters.FilterSet):
    class Meta:
        model = ResourceConsumption
        fields = {
            'resource_name': ['icontains'],
            'quantity': ['exact', 'gt', 'lt'],
            'unit': ['exact'],
            'cost_per_unit': ['exact', 'gt', 'lt'],
            'expense': ['exact'],
        }

class BudgetFilter(django_filters.FilterSet):
    class Meta:
        model = Budget
        fields = {
            'project': ['exact'],
            'total_amount': ['exact', 'gt', 'lt'],
            'created_at': ['exact', 'gte', 'lte'],
        }
