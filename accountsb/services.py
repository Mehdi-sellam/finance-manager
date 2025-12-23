from namespace.models import Namespace
from .models import Account


def create_account(user, namespace_name, name, currency):
    if not namespace_name or not namespace_name.strip():
        raise ValueError("Namespace name is required")
    if not name or not name.strip():
        raise ValueError("Account name is required")
        
    try:
        namespace = Namespace.objects.get(name=namespace_name.strip(), user=user)
    except Namespace.DoesNotExist:
        raise ValueError(f"Namespace '{namespace_name}' not found.")
    
    if Account.objects.filter(namespace=namespace, name=name.strip()).exists():
        raise ValueError(f"Account with name '{name}' already exists in namespace '{namespace_name}'.")
        
    account = Account.objects.create(
        user=user,
        namespace=namespace,
        name=name.strip(),
        currency=currency
    )
    return account


def list_accounts(user):
    return Account.objects.filter(user=user)


def get_account_by_name(user, namespace_name, name):
    if not namespace_name or not namespace_name.strip():
        raise ValueError("Namespace name is required")
    if not name or not name.strip():
        raise ValueError("Account name is required")
        
    try:
        namespace = Namespace.objects.get(name=namespace_name.strip(), user=user)
    except Namespace.DoesNotExist:
        raise ValueError(f"Namespace '{namespace_name}' not found.")

    try:
        return Account.objects.get(namespace=namespace, name=name.strip())
    except Account.DoesNotExist:
        raise ValueError(f"Account '{name}' not found in namespace '{namespace_name}'.")


def update_account(user, namespace_name, current_name, new_name=None):
    if not namespace_name or not namespace_name.strip():
        raise ValueError("Namespace name is required")
    if not current_name or not current_name.strip():
        raise ValueError("Current account name is required")

    try:
        namespace = Namespace.objects.get(name=namespace_name.strip(), user=user)
    except Namespace.DoesNotExist:
        raise ValueError(f"Namespace '{namespace_name}' not found.")

    try:
        account = Account.objects.get(namespace=namespace, name=current_name.strip())
    except Account.DoesNotExist:
        raise ValueError(f"Account '{current_name}' not found in namespace '{namespace_name}'.")
    
    if new_name:
        if not new_name.strip():
            raise ValueError("New account name cannot be empty")
            
        if new_name.strip() != current_name.strip():
            if Account.objects.filter(namespace=namespace, name=new_name.strip()).exists():
                raise ValueError(f"Account with name '{new_name}' already exists in namespace '{namespace_name}'.")
            account.name = new_name.strip()
            account.save()
        
    return account


def delete_account(user, namespace_name, name):
    if not namespace_name or not namespace_name.strip():
        raise ValueError("Namespace name is required")
    if not name or not name.strip():
        raise ValueError("Account name is required")
        
    try:
        namespace = Namespace.objects.get(name=namespace_name.strip(), user=user)
    except Namespace.DoesNotExist:
        raise ValueError(f"Namespace '{namespace_name}' not found.")

    try:
        account = Account.objects.get(namespace=namespace, name=name.strip())
        account.delete()
    except Account.DoesNotExist:
        raise ValueError(f"Account '{name}' not found in namespace '{namespace_name}'.")


def list_accounts_by_namespace(user, namespace_name):
    if not namespace_name or not namespace_name.strip():
        raise ValueError("Namespace name is required")
        
    try:
        namespace = Namespace.objects.get(name=namespace_name.strip(), user=user)
    except Namespace.DoesNotExist:
        raise ValueError(f"Namespace '{namespace_name}' not found.")
        
    return Account.objects.filter(user=user, namespace=namespace)
