# Added by AI - namespace/services.py
from .models import Namespace


# Added by AI - Create namespace function with business logic validation
def create_namespace(requester, **data):
    name = data.get("name")
    
    # Added by AI - Validate required fields
    if not name:
        raise ValueError("Name is required")
    
    # Added by AI - Validate name is not empty or whitespace
    if not name.strip():
        raise ValueError("Name cannot be empty")
    
    # Added by AI - Validate name length (matches serializer max_length=50)
    if len(name) > 50:
        raise ValueError("Name cannot exceed 50 characters")
    
    # Added by AI - Check if namespace with same name already exists for this user (business logic validation)
    # Use name.strip() to match what we save in the database
    if Namespace.objects.filter(name=name.strip(), user=requester).exists():
        raise ValueError("A namespace with that name already exists for this user")
    
    # Added by AI - Create namespace linked to the authenticated user
    namespace = Namespace.objects.create(
        name=name.strip(),
        user=requester
    )
    
    # Added by AI - Return created namespace
    return namespace


# Added by AI - Get namespace by ID with ownership validation
def get_namespace(requester, namespace_id):
    try:
        namespace = Namespace.objects.get(id=namespace_id)
    except Namespace.DoesNotExist:
        raise ValueError("Namespace not found")
    
    # Added by AI - Validate ownership (users can only access their own namespaces)
    if namespace.user != requester:
        raise ValueError("You do not have permission to access this namespace")
    
    # Added by AI - Return namespace
    return namespace


# Added by AI - Get namespace by name with ownership validation
def get_namespace_by_name(requester, name):
    # Added by AI - Validate that name is provided (business logic validation)
    if not name:
        raise ValueError("Name is required")
    
    # Added by AI - Validate name is not empty or whitespace
    if not name.strip():
        raise ValueError("Name cannot be empty")
    
    try:
        namespace = Namespace.objects.get(name=name.strip(), user=requester)
    except Namespace.DoesNotExist:
        raise ValueError("Namespace not found")
    
    # Added by AI - Return namespace (ownership already validated by filter)
    return namespace


# Added by AI - List all namespaces for the authenticated user
def list_namespaces(requester):
    # Added by AI - Return only namespaces belonging to the authenticated user
    return Namespace.objects.filter(user=requester)


# Added by AI - Update namespace function with business logic validation (uses name instead of ID)
def update_namespace(requester, current_name, **data):
    new_name = data.get("new_name")
    
    # Added by AI - Get namespace by name and validate ownership
    namespace = get_namespace_by_name(requester, current_name)
    
    # Added by AI - Validate required fields
    if not new_name:
        raise ValueError("New name is required")
    
    # Added by AI - Validate name is not empty or whitespace
    if not new_name.strip():
        raise ValueError("Name cannot be empty")
    
    # Added by AI - Validate name length (matches serializer max_length=50)
    if len(new_name) > 50:
        raise ValueError("Name cannot exceed 50 characters")
    
    # Added by AI - Check if another namespace with same name already exists for this user (excluding current namespace)
    # Use new_name.strip() to match what we save in the database
    if Namespace.objects.filter(name=new_name.strip(), user=requester).exclude(id=namespace.id).exists():
        raise ValueError("A namespace with that name already exists for this user")
    
    # Added by AI - Update namespace name
    namespace.name = new_name.strip()
    namespace.save()
    
    # Added by AI - Return updated namespace
    return namespace


# Added by AI - Delete namespace function with ownership validation (uses name instead of ID)
def delete_namespace(requester, name):
    # Added by AI - Get namespace by name and validate ownership
    namespace = get_namespace_by_name(requester, name)
    
    # Added by AI - Delete namespace
    namespace.delete()
    
    # Added by AI - Return success indicator
    return True

