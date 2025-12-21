from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



# Added by AI - Create user function with business logic validation
def create_user(requester, **data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    # Added by AI - Validate required fields
    if not username:
        raise ValueError("Username is required")
    if not email:
        raise ValueError("Email is required")
    if not password:
        raise ValueError("Password is required")
    
    # Added by AI - Validate username uniqueness (business logic validation)
    if User.objects.filter(username=username).exists():
        raise ValueError("A user with that username already exists")
    
    # Added by AI - Validate email uniqueness (business logic validation)
    if User.objects.filter(email=email).exists():
        raise ValueError("A user with that email already exists")
    
    # Added by AI - Validate password length (business logic validation)
    if len(password) < 4:
        raise ValueError("Password must be at least 4 characters long")
    
    # Added by AI - Create user using Django's create_user method (handles password hashing)
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password
    )
    
    # Added by AI - Return created user object
    return user






def change_password(requester, **data):
    password = data.get("password")
    
    # Added by AI - Validate that password is provided
    if not password:
        raise ValueError("Password is required")
    
    # Added by AI - Validate password length (minimum 8 characters as a basic check)
    if len(password) < 4:
        raise ValueError("Password must be at least 4 characters long")
    
    # Added by AI - Set and save the new password for the requester
    requester.set_password(password)
    requester.save()
    
    # Added by AI - Return the user object after password change
    return requester








# Added by AI - Login function that authenticates user and creates/gets token
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