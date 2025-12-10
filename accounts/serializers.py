from rest_framework import serializers
from .models import BusinessOwner
from django.contrib.auth.models import User

class BusinessOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessOwner
        fields = '__all__'  # or list the fields explicitly




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff", "is_superuser"]
