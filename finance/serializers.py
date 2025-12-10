from rest_framework import serializers
from .models import Expense, ResourceConsumption, SalaryPayment, Budget

# ----------------------
# Expense Serializer
# ----------------------
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"

    def validate(self, data):
        project = data.get("project")
        if project and hasattr(project, "budget"):
            total_expense = sum(e.amount for e in project.expense_set.all())
            total_salaries = sum(s.amount for s in project.salarypayment_set.all())
            budget_amount = project.budget.total_amount

            if total_expense + total_salaries + data["amount"] > budget_amount:
                raise serializers.ValidationError("Adding this expense exceeds the project budget.")
        return data


# ----------------------
# SalaryPayment Serializer
# ----------------------
class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = "__all__"

    def validate(self, data):
        project = data.get("project")
        if project and hasattr(project, "budget"):
            total_expense = sum(e.amount for e in project.expense_set.all())
            total_salaries = sum(s.amount for s in project.salarypayment_set.all())
            budget_amount = project.budget.total_amount

            if total_expense + total_salaries + data["amount"] > budget_amount:
                raise serializers.ValidationError("Adding this salary exceeds the project budget.")
        return data


# ----------------------
# ResourceConsumption Serializer
# ----------------------
class ResourceConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceConsumption
        fields = "__all__"


# ----------------------
# Budget Serializer
# ----------------------
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"
