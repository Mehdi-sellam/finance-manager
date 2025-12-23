# accounts/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password"]




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email"]  # Removed password field for security






class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["password"]



class UserChangePasswordResponseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)  # This will show the hashed password
    
    class Meta:
        model = User
        fields = ["username", "password"]  




class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class UserLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    username = serializers.CharField()