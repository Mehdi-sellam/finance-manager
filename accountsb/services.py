from namespace.models import Namespace
from .models import Account


# Added by AI - Create account service with validation
def create_account(user, namespace_name, name, currency):
    # Added by AI - Validate required fields
    if not namespace_name or not namespace_name.strip():
        raise ValueError("Namespace name is required")
    if not name or not name.strip():
        raise ValueError("Account name is required")
        
    # Added by AI - Resolve namespace by name and user
    try:
        namespace = Namespace.objects.get(name=namespace_name.strip(), user=user)
    except Namespace.DoesNotExist:
        raise ValueError(f"Namespace '{namespace_name}' not found.")
    
    # Added by AI - Check if account name already exists for user
    if Account.objects.filter(user=user, name=name.strip()).exists():
        raise ValueError(f"Account with name '{name}' already exists.")
        
    # Added by AI - Create the account
    account = Account.objects.create(
        user=user,
        namespace=namespace,
        name=name.strip(),
        currency=currency
    )
    return account


# Added by AI - List all accounts for user
def list_accounts(user):
    return Account.objects.filter(user=user)


# Added by AI - Get account by name
def get_account_by_name(user, name):
    if not name or not name.strip():
        raise ValueError("Account name is required")
        
    try:
        return Account.objects.get(user=user, name=name.strip())
    except Account.DoesNotExist:
        raise ValueError(f"Account '{name}' not found.")


# Added by AI - Update account (rename)
def update_account(user, current_name, new_name=None):
    if not current_name or not current_name.strip():
        raise ValueError("Current account name is required")

    try:
        account = Account.objects.get(user=user, name=current_name.strip())
    except Account.DoesNotExist:
        raise ValueError(f"Account '{current_name}' not found.")
    
    # Added by AI - Handle renaming
    if new_name:
        if not new_name.strip():
            raise ValueError("New account name cannot be empty")
            
        if new_name.strip() != current_name.strip():
            if Account.objects.filter(user=user, name=new_name.strip()).exists():
                raise ValueError(f"Account with name '{new_name}' already exists.")
            account.name = new_name.strip()
            account.save()
        
    return account


# Added by AI - Delete account
def delete_account(user, name):
    if not name or not name.strip():
        raise ValueError("Account name is required")
        
    try:
        account = Account.objects.get(user=user, name=name.strip())
        account.delete()
    except Account.DoesNotExist:
        raise ValueError(f"Account '{name}' not found.")


# Added by AI - List accounts within a specific namespace
def list_accounts_by_namespace(user, namespace_name):
    if not namespace_name or not namespace_name.strip():
        raise ValueError("Namespace name is required")
        
    try:
        namespace = Namespace.objects.get(name=namespace_name.strip(), user=user)
    except Namespace.DoesNotExist:
        raise ValueError(f"Namespace '{namespace_name}' not found.")
        
    return Account.objects.filter(user=user, namespace=namespace)
