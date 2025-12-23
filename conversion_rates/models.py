from django.db import models
from django.contrib.auth.models import User
from accountsb.models import Currency


class ConversionRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversion_rates')
    
    from_currency = models.CharField(max_length=3, choices=Currency.choices)
    to_currency = models.CharField(max_length=3, choices=Currency.choices)
    
    rate = models.DecimalField(max_digits=19, decimal_places=6)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'from_currency', 'to_currency'], name='unique_rate_per_user')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_currency} -> {self.to_currency}: {self.rate}"
