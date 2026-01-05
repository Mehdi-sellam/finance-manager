from rest_framework import serializers
from .models import Namespace


class NamespaceCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=50)
    
    class Meta:
        model = Namespace
        fields = ["name"]


class NamespaceUpdateSerializer(serializers.Serializer):
    new_name = serializers.CharField(required=True, max_length=50)


class NamespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Namespace
        fields = ["id", "name", "user", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class NamespaceDeleteSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=50)
