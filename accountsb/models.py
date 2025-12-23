from django.db import models
from django.contrib.auth.models import User
from namespace.models import Namespace


# Added by AI - Currency choices enum
class Currency(models.TextChoices):
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    DZD = 'DZD', 'DZD'


# Added by AI - Account model definition
class Account(models.Model):
    # Added by AI - Relationship to User (owner)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_accounts')
    
    # Added by AI - Relationship to Namespace (organization)
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE, related_name='accounts')
    
    # Added by AI - Account details
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    balance = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    
    # Added by AI - Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Added by AI - Ensure unique account names per user
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_account_name_per_user')
        ]
        # Added by AI - Default ordering
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.currency})"
