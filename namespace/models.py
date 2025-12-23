from django.db import models
from django.contrib.auth.models import User


class Namespace(models.Model):
    name = models.CharField(max_length=255, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="namespaces")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [['name', 'user']]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (User: {self.user.username})"
