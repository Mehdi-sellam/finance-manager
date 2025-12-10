from django.db import models
from accounts.models import BusinessOwner

# Create your models here.


class Employee(models.Model):
    owner = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.owner.company_name})"
