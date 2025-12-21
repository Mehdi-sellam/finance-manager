from django.db import transaction
from django.shortcuts import get_object_or_404
from accountsb.models import Account
from conversion_rates.models import ConversionRate
from .models import Transaction, TransactionType

def create_in_transaction(user, destination_account_name, amount, currency, description=""):
    with transaction.atomic():
        destination_account = get_object_or_404(Account, user=user, name=destination_account_name)
        
        if destination_account.currency != currency:
            raise ValueError(f"Account currency {destination_account.currency} does not match transaction currency {currency}")
            
        destination_account.balance += amount
        destination_account.save()
        
        return Transaction.objects.create(
            user=user,
            transaction_type=TransactionType.IN,
            amount=amount,
            currency=currency,
            destination_account=destination_account,
            description=description
        )

def create_out_transaction(user, source_account_name, amount, currency, description=""):
    with transaction.atomic():
        source_account = get_object_or_404(Account, user=user, name=source_account_name)
        
        if source_account.currency != currency:
            raise ValueError(f"Account currency {source_account.currency} does not match transaction currency {currency}")
            
        if source_account.balance < amount:
            raise ValueError("Insufficient funds")
            
        source_account.balance -= amount
        source_account.save()
        
        return Transaction.objects.create(
            user=user,
            transaction_type=TransactionType.OUT,
            amount=amount,
            currency=currency,
            source_account=source_account,
            description=description
        )

def create_transfer_transaction(user, source_account_name, destination_account_name, amount, description=""):
    with transaction.atomic():
        source_account = get_object_or_404(Account, user=user, name=source_account_name)
        destination_account = get_object_or_404(Account, user=user, name=destination_account_name)
        
        if source_account.balance < amount:
            raise ValueError("Insufficient funds in source account")
            
        # Determine conversion rate if currencies differ
        rate_obj = None
        converted_amount = amount
        
        if source_account.currency != destination_account.currency:
            try:
                rate_obj = ConversionRate.objects.get(
                    user=user,
                    from_currency=source_account.currency,
                    to_currency=destination_account.currency
                )
                converted_amount = amount * rate_obj.rate
            except ConversionRate.DoesNotExist:
                raise ValueError(f"No conversion rate found from {source_account.currency} to {destination_account.currency}")
        
        # Update balances
        source_account.balance -= amount
        source_account.save()
        
        destination_account.balance += converted_amount
        destination_account.save()
        
        return Transaction.objects.create(
            user=user,
            transaction_type=TransactionType.TRANSFER,
            amount=amount,
            currency=source_account.currency,
            source_account=source_account,
            destination_account=destination_account,
            conversion_rate=rate_obj,
            description=description
        )

def list_transactions(user):
    return Transaction.objects.filter(user=user)

def list_transactions_by_account(user, account_name):
    account = get_object_or_404(Account, user=user, name=account_name)
    return Transaction.objects.filter(
        models.Q(source_account=account) | models.Q(destination_account=account)
    )

def list_transactions_by_type(user, transaction_type):
    return Transaction.objects.filter(user=user, transaction_type=transaction_type)
