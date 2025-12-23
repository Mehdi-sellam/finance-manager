from django.db import transaction
from accountsb.models import Account
from conversion_rates.models import ConversionRate
from .models import Transaction, TransactionType


# Added by AI - Create IN transaction (deposit)
def create_in_transaction(user, destination_account_name, amount, currency, description=""):
    # Added by AI - Validate inputs
    if not destination_account_name or not destination_account_name.strip():
        raise ValueError("Destination account name is required")
    if amount <= 0:
        raise ValueError("Amount must be positive")
        
    with transaction.atomic():
        try:
            destination_account = Account.objects.get(user=user, name=destination_account_name.strip())
        except Account.DoesNotExist:
            raise ValueError(f"Account '{destination_account_name}' not found.")
        
        # Added by AI - Validate currency match
        if destination_account.currency != currency:
            raise ValueError(f"Account currency {destination_account.currency} does not match transaction currency {currency}")
            
        # Added by AI - Update balance
        destination_account.balance += amount
        destination_account.save()
        
        # Added by AI - Record transaction
        return Transaction.objects.create(
            user=user,
            transaction_type=TransactionType.IN,
            amount=amount,
            currency=currency,
            destination_account=destination_account,
            description=description
        )


# Added by AI - Create OUT transaction (withdrawal)
def create_out_transaction(user, source_account_name, amount, currency, description=""):
    # Added by AI - Validate inputs
    if not source_account_name or not source_account_name.strip():
        raise ValueError("Source account name is required")
    if amount <= 0:
        raise ValueError("Amount must be positive")

    with transaction.atomic():
        try:
            source_account = Account.objects.get(user=user, name=source_account_name.strip())
        except Account.DoesNotExist:
            raise ValueError(f"Account '{source_account_name}' not found.")
        
        # Added by AI - Validate currency match
        if source_account.currency != currency:
            raise ValueError(f"Account currency {source_account.currency} does not match transaction currency {currency}")
            
        # Added by AI - Check sufficient funds
        if source_account.balance < amount:
            raise ValueError("Insufficient funds")
            
        # Added by AI - Update balance
        source_account.balance -= amount
        source_account.save()
        
        # Added by AI - Record transaction
        return Transaction.objects.create(
            user=user,
            transaction_type=TransactionType.OUT,
            amount=amount,
            currency=currency,
            source_account=source_account,
            description=description
        )


# Added by AI - Create TRANSFER transaction
def create_transfer_transaction(user, source_account_name, destination_account_name, amount, description=""):
    # Added by AI - Validate inputs
    if not source_account_name or not source_account_name.strip():
        raise ValueError("Source account name is required")
    if not destination_account_name or not destination_account_name.strip():
        raise ValueError("Destination account name is required")
    if amount <= 0:
        raise ValueError("Amount must be positive")

    with transaction.atomic():
        try:
            source_account = Account.objects.get(user=user, name=source_account_name.strip())
        except Account.DoesNotExist:
            raise ValueError(f"Account '{source_account_name}' not found.")
            
        try:
            destination_account = Account.objects.get(user=user, name=destination_account_name.strip())
        except Account.DoesNotExist:
            raise ValueError(f"Account '{destination_account_name}' not found.")
        
        # Added by AI - Check sufficient funds
        if source_account.balance < amount:
            raise ValueError("Insufficient funds in source account")
            
        # Added by AI - Determine conversion rate if currencies differ
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
        
        # Added by AI - Update balances
        source_account.balance -= amount
        source_account.save()
        
        destination_account.balance += converted_amount
        destination_account.save()
        
        # Added by AI - Record transaction
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


# Added by AI - List all transactions for user
def list_transactions(user):
    return Transaction.objects.filter(user=user)


# Added by AI - List transactions related to a specific account
def list_transactions_by_account(user, account_name):
    if not account_name or not account_name.strip():
        raise ValueError("Account name is required")

    try:
        account = Account.objects.get(user=user, name=account_name.strip())
    except Account.DoesNotExist:
        raise ValueError(f"Account '{account_name}' not found.")
        
    return Transaction.objects.filter(
        models.Q(source_account=account) | models.Q(destination_account=account)
    )


# Added by AI - List transactions by type
def list_transactions_by_type(user, transaction_type):
    return Transaction.objects.filter(user=user, transaction_type=transaction_type)
