from django.shortcuts import get_object_or_404
from .models import ConversionRate

def create_conversion_rate(user, from_currency, to_currency, rate):
    if ConversionRate.objects.filter(user=user, from_currency=from_currency, to_currency=to_currency).exists():
        raise ValueError(f"Conversion rate from {from_currency} to {to_currency} already exists.")
    
    return ConversionRate.objects.create(
        user=user,
        from_currency=from_currency,
        to_currency=to_currency,
        rate=rate
    )

def list_conversion_rates(user):
    return ConversionRate.objects.filter(user=user)

def update_conversion_rate(user, from_currency, to_currency, rate):
    conversion_rate = get_object_or_404(ConversionRate, user=user, from_currency=from_currency, to_currency=to_currency)
    conversion_rate.rate = rate
    conversion_rate.save()
    return conversion_rate

def delete_conversion_rate(user, from_currency, to_currency):
    conversion_rate = get_object_or_404(ConversionRate, user=user, from_currency=from_currency, to_currency=to_currency)
    conversion_rate.delete()
