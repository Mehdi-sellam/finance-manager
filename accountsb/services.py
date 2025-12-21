from django.shortcuts import get_object_or_404
from namespace.models import Namespace
from .models import Account

def create_account(user, namespace_name, name, currency):
    # Resolve namespace by name and user
    namespace = get_object_or_404(Namespace, name=namespace_name, user=user)
    
    # Check if account name already exists for user
    if Account.objects.filter(user=user, name=name).exists():
        raise ValueError(f"Account with name '{name}' already exists.")
        
    account = Account.objects.create(
        user=user,
        namespace=namespace,
        name=name,
        currency=currency
    )
    return account

def list_accounts(user):
    return Account.objects.filter(user=user)

def get_account_by_name(user, name):
    return get_object_or_404(Account, user=user, name=name)

def update_account(user, current_name, new_name=None):
    account = get_object_or_404(Account, user=user, name=current_name)
    
    if new_name and new_name != current_name:
        if Account.objects.filter(user=user, name=new_name).exists():
            raise ValueError(f"Account with name '{new_name}' already exists.")
        account.name = new_name
        account.save()
        
    return account

def delete_account(user, name):
    account = get_object_or_404(Account, user=user, name=name)
    account.delete()

def list_accounts_by_namespace(user, namespace_name):
    namespace = get_object_or_404(Namespace, name=namespace_name, user=user)
    return Account.objects.filter(user=user, namespace=namespace)
