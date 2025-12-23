from django.db import transaction
from accountsb.models import Account
from accountsb.services import get_account_by_name
from conversion_rates.models import ConversionRate
from .models import Transaction, TransactionType


def create_in_transaction(user, destination_namespace_name, destination_account_name, amount, currency, description=""):
    if not destination_namespace_name or not destination_namespace_name.strip():
        raise ValueError("Destination namespace name is required")
    if not destination_account_name or not destination_account_name.strip():
        raise ValueError("Destination account name is required")
    if amount <= 0:
        raise ValueError("Amount must be positive")
        
    with transaction.atomic():
        try:
            destination_account = get_account_by_name(user, destination_namespace_name, destination_account_name)
        except ValueError as e:
            raise ValueError(str(e))
        
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


def create_out_transaction(user, source_namespace_name, source_account_name, amount, currency, description=""):
    if not source_namespace_name or not source_namespace_name.strip():
        raise ValueError("Source namespace name is required")
    if not source_account_name or not source_account_name.strip():
        raise ValueError("Source account name is required")
    if amount <= 0:
        raise ValueError("Amount must be positive")

    with transaction.atomic():
        try:
            source_account = get_account_by_name(user, source_namespace_name, source_account_name)
        except ValueError as e:
            raise ValueError(str(e))
        
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


def create_transfer_transaction(user, source_namespace_name, source_account_name, destination_namespace_name, destination_account_name, amount, description=""):
    if not source_namespace_name or not source_namespace_name.strip():
        raise ValueError("Source namespace name is required")
    if not source_account_name or not source_account_name.strip():
        raise ValueError("Source account name is required")
    if not destination_namespace_name or not destination_namespace_name.strip():
        raise ValueError("Destination namespace name is required")
    if not destination_account_name or not destination_account_name.strip():
        raise ValueError("Destination account name is required")
    if amount <= 0:
        raise ValueError("Amount must be positive")

    with transaction.atomic():
        try:
            source_account = get_account_by_name(user, source_namespace_name, source_account_name)
        except ValueError as e:
            raise ValueError(str(e))
            
        try:
            destination_account = get_account_by_name(user, destination_namespace_name, destination_account_name)
        except ValueError as e:
            raise ValueError(str(e))
        
        if source_account.balance < amount:
            raise ValueError("Insufficient funds in source account")
            
        if source_account.currency == destination_account.currency:
            source_account.balance -= amount
            source_account.save()
            
            destination_account.balance += amount
            destination_account.save()
            
            return Transaction.objects.create(
                user=user,
                transaction_type=TransactionType.TRANSFER,
                amount=amount,
                currency=source_account.currency,
                source_account=source_account,
                destination_account=destination_account,
                description=description
            )
        else:
            try:
                rate = ConversionRate.objects.get(
                    user=user, 
                    from_currency=source_account.currency, 
                    to_currency=destination_account.currency
                )
            except ConversionRate.DoesNotExist:
                raise ValueError(f"No conversion rate found from {source_account.currency} to {destination_account.currency}")
                
            converted_amount = amount * rate.rate
            
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
                conversion_rate=rate,
                description=description
            )


def list_transactions(user):
    return Transaction.objects.filter(user=user)


def list_transactions_by_account(user, namespace_name, account_name):
    if not namespace_name or not namespace_name.strip():
        raise ValueError("Namespace name is required")
    if not account_name or not account_name.strip():
        raise ValueError("Account name is required")
        
    try:
        account = get_account_by_name(user, namespace_name, account_name)
    except ValueError as e:
        raise ValueError(str(e))
        
    return Transaction.objects.filter(
        user=user
    ).filter(
        models.Q(source_account=account) | models.Q(destination_account=account)
    )


def list_transactions_by_type(user, transaction_type):
    return Transaction.objects.filter(user=user, transaction_type=transaction_type)
