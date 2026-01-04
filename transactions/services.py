from django.db import transaction
from decimal import Decimal, ROUND_HALF_UP
from accountsb.models import Account, Currency
from .models import Transaction, TransactionType
from common.exceptions import DomainValidationError, NotFoundError


def create_in_transaction(requester, account_id, amount, currency, description=""):
    if amount <= 0:
        raise DomainValidationError("Amount must be positive")
        
    with transaction.atomic():
        try:
            destination_account = requester.accounts.get(id=account_id)
        except Account.DoesNotExist:
            raise NotFoundError(f"Account with ID {account_id} not found.")
        
        if destination_account.currency != currency:
            raise DomainValidationError(f"Account currency {destination_account.currency} does not match transaction currency {currency}")
            
        destination_account.balance += amount
        destination_account.save()
        
        return Transaction.objects.create(
            user=requester,
            transaction_type=TransactionType.IN,
            amount=amount,
            currency=currency,
            destination_account=destination_account,
            description=description
        )


def create_out_transaction(requester, account_id, amount, currency, description=""):
    if amount <= 0:
        raise DomainValidationError("Amount must be positive")

    with transaction.atomic():
        try:
            source_account = requester.accounts.get(id=account_id)
        except Account.DoesNotExist:
            raise NotFoundError(f"Account with ID {account_id} not found.")
        
        if source_account.currency != currency:
            raise DomainValidationError(f"Account currency {source_account.currency} does not match transaction currency {currency}")
            
        if source_account.balance < amount:
            raise DomainValidationError("Insufficient funds")
            
        source_account.balance -= amount
        source_account.save()
        
        return Transaction.objects.create(
            user=requester,
            transaction_type=TransactionType.OUT,
            amount=amount,
            currency=currency,
            source_account=source_account,
            description=description
        )


def create_transfer_transaction(requester, source_account_id, destination_account_id, source_amount, destination_amount, description=""):
    if source_amount <= 0 or destination_amount <= 0:
        raise DomainValidationError("Amounts must be positive")
    
    if source_account_id == destination_account_id:
        raise DomainValidationError("Source and destination accounts must be different.")

    with transaction.atomic():
        try:
            source_account = requester.accounts.get(id=source_account_id)
        except Account.DoesNotExist:
            raise NotFoundError(f"Source account with ID {source_account_id} not found.")
            
        try:
            destination_account = requester.accounts.get(id=destination_account_id)
        except Account.DoesNotExist:
            raise NotFoundError(f"Destination account with ID {destination_account_id} not found.")
        
        if source_account.balance < source_amount:
            raise DomainValidationError("Insufficient funds in source account")
            
        source_currency_rate = 1
        destination_currency_rate = 1
        
        if source_account.currency == destination_account.currency:
            if source_amount != destination_amount:
                raise DomainValidationError("Source and destination amounts must be equal for same-currency transfers")
        else:
            source_currency_rate = Decimal(source_amount) / Decimal(destination_amount)
            destination_currency_rate = Decimal(destination_amount) / Decimal(source_amount)

            if source_account.currency in {Currency.USD, Currency.EUR} or destination_account.currency in {Currency.USD, Currency.EUR}:
                source_currency_rate = source_currency_rate.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
                destination_currency_rate = destination_currency_rate.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
            
        source_account.balance -= source_amount
        source_account.save()
        
        destination_account.balance += destination_amount
        destination_account.save()
        
        return Transaction.objects.create(
            user=requester,
            transaction_type=TransactionType.TRANSFER,
            amount=source_amount,
            destination_amount=destination_amount,
            currency=source_account.currency, # Transaction currency is typically source currency
            source_currency_rate=source_currency_rate,
            destination_currency_rate=destination_currency_rate,
            source_account=source_account,
            destination_account=destination_account,
            description=description
        )

def list_transactions(requester, transaction_type=None, account_id=None):
    qs = requester.transactions.all()
    if transaction_type:
        qs = qs.filter(transaction_type=transaction_type)
    if account_id:
        # Filter where account is source OR destination
        from django.db.models import Q
        qs = qs.filter(Q(source_account_id=account_id) | Q(destination_account_id=account_id))
    return qs.order_by('-created_at')
