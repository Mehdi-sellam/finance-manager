from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from common.exceptions import DomainValidationError, ConflictError, NotFoundError



# Create user function with business logic validation
def create_user(requester, **data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username:
        raise DomainValidationError("Username is required")
    if not email:
        raise DomainValidationError("Email is required")
    if not password:
        raise DomainValidationError("Password is required")
    if User.objects.filter(username=username).exists():
        raise ConflictError("A user with that username already exists")
    if User.objects.filter(email=email).exists():
        raise ConflictError("A user with that email already exists")
    if len(password) < 4:
        raise DomainValidationError("Password must be at least 4 characters long")
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password
    )
    return user






def change_password(requester, **data):
    password = data.get("password")
    if not password:
        raise DomainValidationError("Password is required")
    if len(password) < 4:
        raise DomainValidationError("Password must be at least 4 characters long")
    requester.set_password(password)
    requester.save()
    return requester








# Login function that authenticates user and creates/gets token
def login_user(**data):
    username = data.get("username")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if user is None:
        raise DomainValidationError("Invalid username or password")
    token, created = Token.objects.get_or_create(user=user)
    return {
        "user": user,
        "token": token.key
    }
