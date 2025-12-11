from rest_framework import permissions
from users.models import Employee
from accounts.models import BusinessOwner

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows access only to business owners or admin.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or hasattr(request.user, 'businessowner'))

class IsEmployeeOrAdmin(permissions.BasePermission):
    """
    Allows access only to employees or admin.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or hasattr(request.user, 'employee'))

class IsOwnerEmployeeOrAdmin(permissions.BasePermission):
    """
    Allows access to employees, owners, or admin.
    """

    def has_permission(self, request, view):
        return request.user and (
            request.user.is_superuser or hasattr(request.user, 'employee') or hasattr(request.user, 'businessowner')
        )
