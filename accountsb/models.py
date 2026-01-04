from django.db import models
from django.contrib.auth.models import User
from namespace.models import Namespace
from common.models import TimeStampedModel


class Currency(models.TextChoices):
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    DZD = 'DZD', 'DZD'


class Account(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=50)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    balance = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['namespace', 'name'], name='unique_account_name_per_namespace')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.currency})"
