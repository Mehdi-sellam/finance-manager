# accounts/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .models import BusinessOwner
from .serializers import BusinessOwnerSerializer  # adapt path/name if different

class RegisterView(APIView):
    """
    POST /api/auth/register/  -> create user and return token
    Request JSON: {"username": "...", "password": "...", "email": "..."} (email optional)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if not username or not password:
            return Response({"error": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "user already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    POST /api/auth/login/ -> returns token on success
    Request JSON: {"username": "...", "password": "..."}
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Missing credentials"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})


class LogoutView(APIView):
    """
    POST /api/auth/logout/ - delete token (user must send Authorization header)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # delete user's token
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)


# ---- Example BusinessOwner viewset (if you already had it, keep it) ----
class BusinessOwnerViewSet(viewsets.ModelViewSet):
    queryset = BusinessOwner.objects.all()
    serializer_class = BusinessOwnerSerializer
    # Add appropriate permission_classes as needed (e.g., IsAdminUser or custom)
