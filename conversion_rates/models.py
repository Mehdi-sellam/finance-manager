from django.db import models
from django.contrib.auth.models import User
from accountsb.models import Currency


# Added by AI - ConversionRate model definition
class ConversionRate(models.Model):
    # Added by AI - Owner of the rate configuration
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversion_rates')
    
    # Added by AI - Currency pair
    from_currency = models.CharField(max_length=3, choices=Currency.choices)
    to_currency = models.CharField(max_length=3, choices=Currency.choices)
    
    # Added by AI - Exchange rate
    rate = models.DecimalField(max_digits=19, decimal_places=6)
    
    # Added by AI - Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Added by AI - Ensure unique rate per currency pair per user
        constraints = [
            models.UniqueConstraint(fields=['user', 'from_currency', 'to_currency'], name='unique_rate_per_user')
        ]
        # Added by AI - Default ordering
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_currency} -> {self.to_currency}: {self.rate}"
