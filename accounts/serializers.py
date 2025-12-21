# accounts/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

# Added by AI - Serializer for creating users with validation
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password"]




# Added by AI - User serializer for response (excludes password for security)
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email"]  # Removed password field for security






class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["password"]



# Added by AI - Response serializer for change password endpoint
class UserChangePasswordResponseSerializer(serializers.ModelSerializer):
    # Added by AI - Include username and hashed password (password field contains the hash)
    password = serializers.CharField(read_only=True)  # This will show the hashed password
    
    class Meta:
        model = User
        fields = ["username", "password"]  


        


# Added by AI - Login serializer for user authentication (using Serializer not ModelSerializer to avoid unique username validation error)
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


# Added by AI - Login response serializer to return token and username (using Serializer since token is not a User model field)
class UserLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    username = serializers.CharField()