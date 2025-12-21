# Added by AI - namespace/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import create_namespace, get_namespace, get_namespace_by_name, list_namespaces, update_namespace, delete_namespace
from .serializers import (
    NamespaceCreateSerializer, 
    NamespaceUpdateSerializer, 
    NamespaceSerializer,
    NamespaceDeleteSerializer
)


# Added by AI - Create namespace view
class CreateNamespaceView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create a namespace",
        operation_description="Create a new namespace for the authenticated user",
        request_body=NamespaceCreateSerializer,
        responses={
            201: NamespaceSerializer,
        },
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def post(self, request):
        # Added by AI - Validate input data using serializer
        serializer = NamespaceCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Added by AI - Call service to create namespace (business logic in services.py)
                namespace = create_namespace(request.user, **serializer.validated_data)
            except Exception as e:
                # Added by AI - Handle business logic errors from service layer
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Added by AI - Serialize response data
            data = NamespaceSerializer(namespace).data
            
            # Added by AI - Return successful response
            return Response(
                data,
                status=status.HTTP_201_CREATED
            )
        # Added by AI - Return validation errors from serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Added by AI - List namespaces view
class ListNamespacesView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List namespaces",
        operation_description="Get all namespaces for the authenticated user",
        responses={
            200: NamespaceSerializer(many=True),
        },
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def get(self, request):
        try:
            # Added by AI - Call service to list namespaces (business logic in services.py)
            namespaces = list_namespaces(request.user)
        except Exception as e:
            # Added by AI - Handle business logic errors from service layer
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Added by AI - Serialize response data
        data = NamespaceSerializer(namespaces, many=True).data
        
        # Added by AI - Return successful response
        return Response(
            data,
            status=status.HTTP_200_OK
        )


# Added by AI - Retrieve namespace view by ID
class RetrieveNamespaceView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Retrieve a namespace by ID",
        operation_description="Get a specific namespace by ID (only if owned by authenticated user)",
        responses={
            200: NamespaceSerializer,
        },
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def get(self, request, pk):
        try:
            # Added by AI - Call service to get namespace (business logic in services.py)
            namespace = get_namespace(request.user, pk)
        except Exception as e:
            # Added by AI - Handle business logic errors from service layer
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        # Added by AI - Serialize response data
        data = NamespaceSerializer(namespace).data
        
        # Added by AI - Return successful response
        return Response(
            data,
            status=status.HTTP_200_OK
        )


# Added by AI - Retrieve namespace view by name
class RetrieveNamespaceByNameView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Retrieve a namespace by name",
        operation_description="Get a specific namespace by name (only if owned by authenticated user). Provide name as query parameter: ?name=namespace-name",
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="Namespace name",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: NamespaceSerializer,
        },
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def get(self, request):
        # Added by AI - Get name from query parameters
        name = request.query_params.get("name")
        
        # Added by AI - Validate that name is provided (query parameter validation)
        if not name:
            return Response(
                {"error": "Name query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Added by AI - Call service to get namespace by name (business logic in services.py)
            namespace = get_namespace_by_name(request.user, name)
        except Exception as e:
            # Added by AI - Handle business logic errors from service layer
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        # Added by AI - Serialize response data
        data = NamespaceSerializer(namespace).data
        
        # Added by AI - Return successful response
        return Response(
            data,
            status=status.HTTP_200_OK
        )


# Added by AI - Update namespace view (uses name instead of ID)
class UpdateNamespaceView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Update a namespace",
        operation_description="Update a namespace by name (only if owned by authenticated user). Provide current_name and new_name in request body.",
        request_body=NamespaceUpdateSerializer,
        responses={
            200: NamespaceSerializer,
        },
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def patch(self, request):
        # Added by AI - Validate input data using serializer
        serializer = NamespaceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Added by AI - Call service to update namespace (business logic in services.py)
                # Pass current_name as parameter and new_name in data
                namespace = update_namespace(
                    request.user, 
                    serializer.validated_data["current_name"],
                    new_name=serializer.validated_data["new_name"]
                )
            except Exception as e:
                # Added by AI - Handle business logic errors from service layer
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Added by AI - Serialize response data
            data = NamespaceSerializer(namespace).data
            
            # Added by AI - Return successful response
            return Response(
                data,
                status=status.HTTP_200_OK
            )
        # Added by AI - Return validation errors from serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Added by AI - Delete namespace view (uses name instead of ID)
class DeleteNamespaceView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Delete a namespace",
        operation_description="Delete a namespace by name (only if owned by authenticated user). Provide name in request body.",
        request_body=NamespaceDeleteSerializer,
        responses={
            200: openapi.Response(
                description="Namespace deleted successfully"
            ),
        },
        tags=["Namespaces"],
        security=[{"Token": []}],
    )
    def delete(self, request):
        # Added by AI - Validate input data using serializer
        serializer = NamespaceDeleteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Added by AI - Call service to delete namespace (business logic in services.py)
                delete_namespace(request.user, serializer.validated_data["name"])
            except Exception as e:
                # Added by AI - Handle business logic errors from service layer
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Added by AI - Return successful response
            return Response(
                {"message": "Namespace deleted successfully"},
                status=status.HTTP_200_OK
            )
        # Added by AI - Return validation errors from serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
