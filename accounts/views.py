from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets
from .models import BusinessOwner
from .serializers import BusinessOwnerSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class TestView(APIView):

    @swagger_auto_schema(
        operation_description="Test endpoint for Accounts app",
        responses={200: openapi.Response('OK')}
    )
    def get(self, request):
        """
        Returns a simple test message
        """
        return Response({"message": "Accounts app works!"})




class BusinessOwnerViewSet(viewsets.ModelViewSet):
    queryset = BusinessOwner.objects.all()
    serializer_class = BusinessOwnerSerializer




class LoginView(APIView):
    """
    POST username & password → returns auth token
    """
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": {"id": user.id, "username": user.username}})
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    """
    POST with token → deletes token
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"success": "Logged out"}, status=status.HTTP_200_OK)