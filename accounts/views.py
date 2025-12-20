from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import change_password, create_user


# Create your views here.
# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .serializers import UserChangePasswordSerializer, UserCreateSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create a user",
        operation_description="Create a new user using email and password",
        request_body=UserCreateSerializer,
        responses={
            201: UserSerializer,  
      
           
        },
        tags=["Authentication"],
    )
    def post(self, request):
        print(request.user)
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = create_user(request.user, **serializer.validated_data)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = UserSerializer(user).data
            print(type(user))
            print(type(data))
            
            return Response(
                data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









class ChangePasseordView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create a user",
        operation_description="Create a new user using email and password",
        request_body=UserChangePasswordSerializer,
        responses={
            200: openapi.Response(
                description="Password changed successfully"
            ), 
      
           
        },
        tags=["Authentication"],
    )
    def patch(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                change_password(request.user, **serializer.validated_data)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            return Response(
                messsage="Password changed successfully",
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
