from django.db import models
from projects.models import Project
from users.models import Employee
from accounts.models import BusinessOwner

# Create your models here.


class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.project.name}"


class SalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Salary {self.amount} to {self.employee.name}"


class OwnerSalary(models.Model):
    owner = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Owner Salary {self.amount} - {self.owner.company_name}"


class ResourceConsumption(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="resources")
    resource_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    cost_per_unit = models.DecimalField(max_digits=12, decimal_places=2)

    def total_cost(self):
        return self.quantity * self.cost_per_unit

    def __str__(self):
        return f"{self.resource_name} for {self.expense.title}"

class Budget(models.Model):
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='project_budget'  # ✅ avoids clash
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    def remaining_balance(self):
        expense_total = sum(exp.amount for exp in self.project.expenses.all())
        salary_total = sum(s.amount for s in self.project.salary_payments.all())
        owner_salary_total = sum(os.amount for os in getattr(self.project, 'owner_salaries', []))
        return self.total_amount - expense_total - salary_total - owner_salary_total

    def __str__(self):
        return f"Budget for {self.project.name}: {self.total_amount}"
