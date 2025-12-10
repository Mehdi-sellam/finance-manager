from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BusinessOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"
