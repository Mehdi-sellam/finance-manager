from .models import ConversionRate


# Added by AI - Create conversion rate
def create_conversion_rate(user, from_currency, to_currency, rate):
    # Added by AI - Validate inputs
    if not from_currency:
        raise ValueError("From currency is required")
    if not to_currency:
        raise ValueError("To currency is required")
    if rate <= 0:
        raise ValueError("Rate must be positive")
    
    # Added by AI - Check existence
    if ConversionRate.objects.filter(user=user, from_currency=from_currency, to_currency=to_currency).exists():
        raise ValueError(f"Conversion rate from {from_currency} to {to_currency} already exists.")
    
    # Added by AI - Create record
    return ConversionRate.objects.create(
        user=user,
        from_currency=from_currency,
        to_currency=to_currency,
        rate=rate
    )


# Added by AI - List conversion rates for user
def list_conversion_rates(user):
    return ConversionRate.objects.filter(user=user)


# Added by AI - Update conversion rate
def update_conversion_rate(user, from_currency, to_currency, rate):
    if not from_currency:
        raise ValueError("From currency is required")
    if not to_currency:
        raise ValueError("To currency is required")
    if rate <= 0:
        raise ValueError("Rate must be positive")

    try:
        conversion_rate = ConversionRate.objects.get(user=user, from_currency=from_currency, to_currency=to_currency)
    except ConversionRate.DoesNotExist:
        raise ValueError(f"Conversion rate from {from_currency} to {to_currency} not found.")
    
    conversion_rate.rate = rate
    conversion_rate.save()
    return conversion_rate


# Added by AI - Delete conversion rate
def delete_conversion_rate(user, from_currency, to_currency):
    if not from_currency:
        raise ValueError("From currency is required")
    if not to_currency:
        raise ValueError("To currency is required")

    try:
        conversion_rate = ConversionRate.objects.get(user=user, from_currency=from_currency, to_currency=to_currency)
        conversion_rate.delete()
    except ConversionRate.DoesNotExist:
        raise ValueError(f"Conversion rate from {from_currency} to {to_currency} not found.")
