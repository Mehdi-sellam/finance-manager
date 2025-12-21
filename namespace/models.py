from django.db import models
from django.contrib.auth.models import User


# Added by AI - Namespace model - defines database schema only (no business logic validation)
class Namespace(models.Model):
    # Added by AI - Field declarations (database schema definition)
    name = models.CharField(max_length=255, unique=False)  # Name can be duplicate across users
    # Added by AI - ForeignKey creates database relationship and enables user.namespaces.all()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="namespaces")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Added by AI - Database-level constraints (not validation logic)
        # unique_together: Database enforces uniqueness of (name, user) combination
        unique_together = [['name', 'user']]
        # Added by AI - Default ordering for queries (database/ORM configuration)
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (User: {self.user.username})"
