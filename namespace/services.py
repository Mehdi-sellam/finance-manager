from .models import Namespace
from common.exceptions import NotFoundError, ConflictError, DomainValidationError


def create_namespace(requester, **data):
    name = data.get("name")
    if not name:
        raise DomainValidationError("Name is required")
    if not name.strip():
        raise DomainValidationError("Name cannot be empty")
    if len(name) > 50:
        raise DomainValidationError("Name cannot exceed 50 characters")
    if requester.namespaces.filter(name=name.strip()).exists():
        raise ConflictError("A namespace with that name already exists for this user")
    namespace = Namespace.objects.create(
        name=name.strip(),
        user=requester
    )
    return namespace


def get_namespace(requester, namespace_id):
    try:
        namespace = requester.namespaces.get(id=namespace_id)
    except Namespace.DoesNotExist:
        raise NotFoundError("Namespace not found")
    return namespace


def get_namespace_by_name(requester, name):
    if not name:
        raise DomainValidationError("Name is required")
    if not name.strip():
        raise DomainValidationError("Name cannot be empty")
    try:
        namespace = requester.namespaces.get(name=name.strip())
    except Namespace.DoesNotExist:
        raise NotFoundError("Namespace not found")
    return namespace


def list_namespaces(requester):
    return requester.namespaces.all()


def update_namespace(requester, namespace_id, **data):
    new_name = data.get("new_name")
    namespace = get_namespace(requester, namespace_id)
    if not new_name:
        raise DomainValidationError("New name is required")
    if not new_name.strip():
        raise DomainValidationError("Name cannot be empty")
    if len(new_name) > 50:
        raise DomainValidationError("Name cannot exceed 50 characters")
    if requester.namespaces.filter(name=new_name.strip()).exclude(id=namespace.id).exists():
        raise ConflictError("A namespace with that name already exists for this user")
    namespace.name = new_name.strip()
    namespace.save()
    return namespace


def delete_namespace(requester, namespace_id):
    namespace = get_namespace(requester, namespace_id)
    namespace.delete()
    return True
