# Added by AI - namespace/serializers.py
from rest_framework import serializers
from .models import Namespace


# Added by AI - Serializer for creating namespaces
class NamespaceCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=50)
    
    class Meta:
        model = Namespace
        fields = ["name"]


# Added by AI - Serializer for updating namespaces (includes current_name to identify namespace and new_name to update)
class NamespaceUpdateSerializer(serializers.Serializer):
    current_name = serializers.CharField(required=True, max_length=50)
    new_name = serializers.CharField(required=True, max_length=50)


# Added by AI - Serializer for delete namespace by name
class NamespaceDeleteSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=50)


# Added by AI - Serializer for listing and retrieving namespaces
class NamespaceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Namespace
        fields = ["id", "name", "user", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

