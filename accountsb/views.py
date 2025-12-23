from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    AccountCreateSerializer,
    AccountSerializer,
    AccountUpdateSerializer,
    AccountRetrieveByNameSerializer,
    AccountListByNamespaceSerializer
)
from .services import (
    create_account,
    list_accounts,
    get_account_by_name,
    update_account,
    delete_account,
    list_accounts_by_namespace
)


# Added by AI - View for creating new accounts
class CreateAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create an account",
        operation_description="Create a new financial account within a namespace",
        request_body=AccountCreateSerializer,
        responses={201: AccountSerializer},
        tags=["Accounts"],
        security=[{"Token": []}]
    )
    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Added by AI - Call service to create account
                account = create_account(
                    user=request.user,
                    namespace_name=serializer.validated_data['namespace_name'],
                    name=serializer.validated_data['name'],
                    currency=serializer.validated_data['currency']
                )
                return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Added by AI - Handle business logic errors
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Added by AI - View for listing all accounts
class ListAccountsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List all user accounts",
        operation_description="Retrieve all financial accounts belonging to the authenticated user",
        responses={200: AccountSerializer(many=True)},
        tags=["Accounts"],
        security=[{"Token": []}]
    )
    def get(self, request):
        # Added by AI - Retrieve accounts via service
        accounts = list_accounts(request.user)
        return Response(AccountSerializer(accounts, many=True).data, status=status.HTTP_200_OK)


# Added by AI - View for retrieving a single account by name
class RetrieveAccountByNameView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Retrieve account by name",
        operation_description="Get details of a specific account by its unique name",
        request_body=AccountRetrieveByNameSerializer,
        responses={200: AccountSerializer},
        tags=["Accounts"],
        security=[{"Token": []}]
    )
    def post(self, request):
        serializer = AccountRetrieveByNameSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Added by AI - Get account details
                account = get_account_by_name(request.user, serializer.validated_data['account_name'])
                return Response(AccountSerializer(account).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Added by AI - View for updating an account
class UpdateAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Update account",
        operation_description="Update account details (e.g., rename) by current name",
        request_body=AccountUpdateSerializer,
        manual_parameters=[
            openapi.Parameter('account_name', openapi.IN_QUERY, description="Current Account Name", type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: AccountSerializer},
        tags=["Accounts"],
        security=[{"Token": []}]
    )
    def patch(self, request):
        account_name = request.query_params.get('account_name')
        if not account_name:
            return Response({"error": "account_name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AccountUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Added by AI - Update account logic
                account = update_account(
                    user=request.user,
                    current_name=account_name,
                    new_name=serializer.validated_data.get('name')
                )
                return Response(AccountSerializer(account).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Added by AI - View for deleting an account
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Delete account",
        operation_description="Permanently remove an account by name",
        manual_parameters=[
            openapi.Parameter('account_name', openapi.IN_QUERY, description="Account Name", type=openapi.TYPE_STRING, required=True)
        ],
        responses={204: "No Content"},
        tags=["Accounts"],
        security=[{"Token": []}]
    )
    def delete(self, request):
        account_name = request.query_params.get('account_name')
        if not account_name:
            return Response({"error": "account_name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Added by AI - Delete account via service
            delete_account(request.user, account_name)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Added by AI - View for listing accounts in a namespace
class ListAccountsByNamespaceView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List all accounts in a namespace",
        operation_description="Get all accounts belonging to a specific namespace",
        request_body=AccountListByNamespaceSerializer,
        responses={200: AccountSerializer(many=True)},
        tags=["Accounts"],
        security=[{"Token": []}]
    )
    def post(self, request):
        serializer = AccountListByNamespaceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Added by AI - List accounts in namespace
                accounts = list_accounts_by_namespace(request.user, serializer.validated_data['namespace_name'])
                return Response(AccountSerializer(accounts, many=True).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
