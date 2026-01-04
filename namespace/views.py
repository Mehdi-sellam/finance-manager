from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import create_namespace, get_namespace, list_namespaces, update_namespace, delete_namespace
from .serializers import (
    NamespaceCreateSerializer, 
    NamespaceUpdateSerializer, 
    NamespaceSerializer
)

class NamespaceListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List namespaces",
        operation_description="List all namespaces for the authenticated user.",
        responses={200: NamespaceSerializer(many=True)},
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def get(self, request):
        namespaces = list_namespaces(request.user)
        return Response(NamespaceSerializer(namespaces, many=True).data)

    @swagger_auto_schema(
        operation_summary="Create a namespace",
        operation_description="Create a new namespace for the authenticated user.",
        request_body=NamespaceCreateSerializer,
        responses={201: NamespaceSerializer},
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def post(self, request):
        serializer = NamespaceCreateSerializer(data=request.data)
        if serializer.is_valid():
            namespace = create_namespace(request.user, **serializer.validated_data)
            return Response(NamespaceSerializer(namespace).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NamespaceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a namespace",
        operation_description="Retrieve a namespace by its ID for the authenticated user.",
        responses={200: NamespaceSerializer},
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def get(self, request, pk):
        namespace = get_namespace(request.user, pk)
        return Response(NamespaceSerializer(namespace).data)

    @swagger_auto_schema(
        operation_summary="Update a namespace",
        operation_description="Update a namespace's details by ID for the authenticated user.",
        request_body=NamespaceUpdateSerializer,
        responses={200: NamespaceSerializer},
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def patch(self, request, pk):
        serializer = NamespaceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            namespace = update_namespace(request.user, pk, **serializer.validated_data)
            return Response(NamespaceSerializer(namespace).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a namespace",
        operation_description="Delete a namespace by its ID for the authenticated user.",
        responses={204: "No Content"},
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def delete(self, request, pk):
        delete_namespace(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
