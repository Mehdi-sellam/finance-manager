from rest_framework import serializers
from .models import Expense, ResourceConsumption, SalaryPayment, Budget

class ResourceConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceConsumption
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    resources = ResourceConsumptionSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'

class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
