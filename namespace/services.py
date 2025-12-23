from .models import Namespace


def create_namespace(requester, **data):
    name = data.get("name")
    
    if not name:
        raise ValueError("Name is required")
    
    if not name.strip():
        raise ValueError("Name cannot be empty")
    
    if len(name) > 50:
        raise ValueError("Name cannot exceed 50 characters")
    
    if Namespace.objects.filter(name=name.strip(), user=requester).exists():
        raise ValueError("A namespace with that name already exists for this user")
    
    namespace = Namespace.objects.create(
        name=name.strip(),
        user=requester
    )
    
    return namespace


def get_namespace(requester, namespace_id):
    try:
        namespace = Namespace.objects.get(id=namespace_id)
    except Namespace.DoesNotExist:
        raise ValueError("Namespace not found")
    
    if namespace.user != requester:
        raise ValueError("You do not have permission to access this namespace")
    
    return namespace


def get_namespace_by_name(requester, name):
    if not name:
        raise ValueError("Name is required")
    
    if not name.strip():
        raise ValueError("Name cannot be empty")
    
    try:
        namespace = Namespace.objects.get(name=name.strip(), user=requester)
    except Namespace.DoesNotExist:
        raise ValueError("Namespace not found")
    
    return namespace


def list_namespaces(requester):
    return Namespace.objects.filter(user=requester)


def update_namespace(requester, current_name, **data):
    new_name = data.get("new_name")
    
    namespace = get_namespace_by_name(requester, current_name)
    
    if not new_name:
        raise ValueError("New name is required")
    
    if not new_name.strip():
        raise ValueError("Name cannot be empty")
    
    if len(new_name) > 50:
        raise ValueError("Name cannot exceed 50 characters")
    
    if Namespace.objects.filter(name=new_name.strip(), user=requester).exclude(id=namespace.id).exists():
        raise ValueError("A namespace with that name already exists for this user")
    
    namespace.name = new_name.strip()
    namespace.save()
    
    return namespace


def delete_namespace(requester, name):
    namespace = get_namespace_by_name(requester, name)
    namespace.delete()

