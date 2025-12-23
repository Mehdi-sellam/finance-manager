from django.db import models
from django.contrib.auth.models import User
from accountsb.models import Account, Currency
from conversion_rates.models import ConversionRate


# Added by AI - Transaction type choices
class TransactionType(models.TextChoices):
    IN = 'IN', 'IN'
    OUT = 'OUT', 'OUT'
    TRANSFER = 'TRANSFER', 'TRANSFER'


# Added by AI - Transaction model definition
class Transaction(models.Model):
    # Added by AI - Owner of the transaction
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
    # Added by AI - Core transaction details
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    
    # Added by AI - Source account (for OUT and TRANSFER)
    source_account = models.ForeignKey(
        Account, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='outgoing_transactions'
    )
    
    # Added by AI - Destination account (for IN and TRANSFER)
    destination_account = models.ForeignKey(
        Account, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='incoming_transactions'
    )
    
    # Added by AI - Conversion rate applied (for TRANSFER between different currencies)
    conversion_rate = models.ForeignKey(
        ConversionRate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Added by AI - Additional metadata
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Added by AI - Default ordering by creation time
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} {self.amount} {self.currency}"
