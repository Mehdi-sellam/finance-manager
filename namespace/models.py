from django.db import models
from django.contrib.auth.models import User
from common.models import TimeStampedModel


class Namespace(TimeStampedModel):
    name = models.CharField(max_length=50, unique=False)  # Name can be duplicate across users
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="namespaces")
    
    class Meta:
        unique_together = [['name', 'user']]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (User: {self.user.username})"
