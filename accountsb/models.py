from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
from namespace.models import Namespace

class Currency(models.TextChoices):
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    DZD = 'DZD', 'DZD'

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_accounts')
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    balance = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_account_name_per_user')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.currency})"
