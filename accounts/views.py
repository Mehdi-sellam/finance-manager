from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import change_password, create_user, login_user


# Create your views here.
# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .serializers import UserChangePasswordSerializer, UserChangePasswordResponseSerializer, UserCreateSerializer, UserSerializer, UserLoginSerializer, UserLoginResponseSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class CreateUserView(APIView):
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(
        operation_summary="Create a user",
        operation_description="Create a new user using email and password",
        request_body=UserCreateSerializer,
        responses={
            201: UserSerializer,  
      
           
        },
        tags=["Authentication"],
        security=[{"Token": []}],
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
        operation_summary="Change password",
        operation_description="Change password for the authenticated user",
        request_body=UserChangePasswordSerializer,
        responses={
            200: UserChangePasswordResponseSerializer, 
      
           
        },
        tags=["Authentication"],
        security=[{"Token": []}],
    )
    def patch(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = change_password(request.user, **serializer.validated_data)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = UserChangePasswordResponseSerializer(user).data
            
            return Response(
                {
                    "message": "Password changed successfully",
                    "username": data["username"],
                    "password": data["password"] 
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class LoginView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_summary="Login user",
        operation_description="Authenticate user with username and password and return token",
        request_body=UserLoginSerializer,
        responses={
            200: UserLoginResponseSerializer,
        },
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = login_user(**serializer.validated_data)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            response_data = {
                "token": result["token"],
                "username": result["user"].username
            }
            
            return Response(
                response_data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
