from rest_framework import serializers
from .models import Expense, SalaryPayment, OwnerSalary, ResourceConsumption, Budget

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = '__all__'


class OwnerSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerSalary
        fields = '__all__'


class ResourceConsumptionSerializer(serializers.ModelSerializer):
    total_cost = serializers.ReadOnlyField()

    class Meta:
        model = ResourceConsumption
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    remaining_balance = serializers.ReadOnlyField()

    class Meta:
        model = Budget
        fields = '__all__'
