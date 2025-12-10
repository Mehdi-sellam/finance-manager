from django.db import models
from accounts.models import BusinessOwner
from users.models import Employee

# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.owner.company_name}"


class ProjectEmployee(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project', 'employee')

    def __str__(self):
        return f"{self.employee.name} on {self.project.name}"


class ResourceConsumption(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=255)
    quantity = models.FloatField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.resource_type} for {self.project.name}"
