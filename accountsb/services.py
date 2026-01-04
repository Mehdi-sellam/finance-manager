from namespace.models import Namespace
from .models import Account
from common.exceptions import NotFoundError, ConflictError, DomainValidationError


def create_account(requester, namespace_id, name, currency):
    if not name or not name.strip():
        raise DomainValidationError("Account name is required")
    try:
        namespace = requester.namespaces.get(id=namespace_id)
    except Namespace.DoesNotExist:
        raise NotFoundError(f"Namespace with ID {namespace_id} not found.")
    if namespace.accounts.filter(name=name.strip()).exists():
        raise ConflictError(f"Account with name '{name}' already exists.")
        
    account = Account.objects.create(
        user=requester,
        namespace=namespace,
        name=name.strip(),
        currency=currency
    )
    return account


def list_accounts(requester, namespace_id=None):
    if namespace_id:
        try:
            namespace = requester.namespaces.get(id=namespace_id)
        except Namespace.DoesNotExist:
            raise NotFoundError(f"Namespace with ID {namespace_id} not found.")
        return namespace.accounts.all()
    return requester.accounts.all()


def get_account_by_id(requester, account_id):
    try:
        return requester.accounts.get(id=account_id)
    except Account.DoesNotExist:
        raise NotFoundError(f"Account with ID {account_id} not found.")


def update_account(requester, account_id, name=None):
    try:
        account = requester.accounts.get(id=account_id)
    except Account.DoesNotExist:
        raise NotFoundError(f"Account with ID {account_id} not found.")
    
    if name:
        if not name.strip():
            raise DomainValidationError("New account name cannot be empty")
        if name.strip() != account.name:
            if account.namespace.accounts.filter(name=name.strip()).exclude(id=account.id).exists():
                raise ConflictError(f"Account with name '{name}' already exists.")
            account.name = name.strip()
            account.save()
    return account


def delete_account(requester, account_id):
    try:
        account = requester.accounts.get(id=account_id)
        account.delete()
    except Account.DoesNotExist:
        raise NotFoundError(f"Account with ID {account_id} not found.")
