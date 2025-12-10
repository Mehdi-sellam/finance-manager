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




class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # remove the token
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)

