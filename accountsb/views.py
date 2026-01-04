from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import create_account, list_accounts, get_account_by_id, update_account, delete_account
from .serializers import (
    AccountCreateSerializer,
    AccountSerializer,
    AccountUpdateSerializer
)

class AccountListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List all user accounts",
        operation_description="List all accounts for the authenticated user. Optionally filter by namespace_id.",
        manual_parameters=[
            openapi.Parameter('namespace_id', openapi.IN_QUERY, description="Filter by Namespace ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: AccountSerializer(many=True)},
        tags=["Accounts"],
        security=[{"Token": []}],
    )
    def get(self, request):
        namespace_id = request.query_params.get('namespace_id')
        accounts = list_accounts(request.user, namespace_id=namespace_id)
        return Response(AccountSerializer(accounts, many=True).data)

    @swagger_auto_schema(
        operation_summary="Create an account",
        operation_description="Create a new account in a namespace for the authenticated user.",
        request_body=AccountCreateSerializer,
        responses={201: AccountSerializer},
        tags=["Accounts"],
        security=[{"Token": []}],
    )
    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            account = create_account(
                requester=request.user,
                namespace_id=serializer.validated_data['namespace_id'],
                name=serializer.validated_data['name'],
                currency=serializer.validated_data['currency']
            )
            return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve account by ID",
        operation_description="Retrieve an account by its ID for the authenticated user.",
        responses={200: AccountSerializer},
        tags=["Accounts"],
        security=[{"Token": []}],
    )
    def get(self, request, pk):
        account = get_account_by_id(request.user, pk)
        return Response(AccountSerializer(account).data)

    @swagger_auto_schema(
        operation_summary="Update account",
        operation_description="Update an account's details by ID for the authenticated user.",
        request_body=AccountUpdateSerializer,
        responses={200: AccountSerializer},
        tags=["Accounts"],
        security=[{"Token": []}],
    )
    def patch(self, request, pk):
        serializer = AccountUpdateSerializer(data=request.data)
        if serializer.is_valid():
            account = update_account(request.user, pk, **serializer.validated_data)
            return Response(AccountSerializer(account).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete account",
        operation_description="Delete an account by its ID for the authenticated user.",
        responses={204: "No Content"},
        tags=["Accounts"],
        security=[{"Token": []}],
    )
    def delete(self, request, pk):
        delete_account(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
