from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



def create_user(requester, **data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username:
        raise ValueError("Username is required")
    if not email:
        raise ValueError("Email is required")
    if not password:
        raise ValueError("Password is required")
    
    if User.objects.filter(username=username).exists():
        raise ValueError("A user with that username already exists")
    
    if User.objects.filter(email=email).exists():
        raise ValueError("A user with that email already exists")
    
    if len(password) < 4:
        raise ValueError("Password must be at least 4 characters long")
    
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password
    )
    
    return user






def change_password(requester, **data):
    password = data.get("password")
    
    if not password:
        raise ValueError("Password is required")
    
    if len(password) < 4:
        raise ValueError("Password must be at least 4 characters long")
    
    requester.set_password(password)
    requester.save()
    
    return requester









def login_user(**data):
    username = data.get("username")
    password = data.get("password")
    
    # Authenticate the user using Django's authentication system
    user = authenticate(username=username, password=password)
    
    # If authentication fails, raise an exception
    if user is None:
        raise ValueError("Invalid username or password")
    
    # Get or create a token for the authenticated user
    token, created = Token.objects.get_or_create(user=user)
    
    # Return the user and token
    return {
        "user": user,
        "token": token.key
    }