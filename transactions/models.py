from django.db import models
from django.contrib.auth.models import User
from accountsb.models import Account, Currency
from common.models import TimeStampedModel


# Transaction type choices
class TransactionType(models.TextChoices):
    IN = 'IN', 'IN'
    OUT = 'OUT', 'OUT'
    TRANSFER = 'TRANSFER', 'TRANSFER'


# Transaction model definition
class Transaction(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    source_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='outgoing_transactions'
    )
    destination_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incoming_transactions'
    )
    destination_amount = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    source_currency_rate = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True)
    destination_currency_rate = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} {self.amount} {self.currency}"
