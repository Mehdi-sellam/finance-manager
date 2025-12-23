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
                account = create_account(
                    user=request.user,
                    namespace_name=serializer.validated_data['namespace_name'],
                    name=serializer.validated_data['name'],
                    currency=serializer.validated_data['currency']
                )
                return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        accounts = list_accounts(request.user)
        return Response(AccountSerializer(accounts, many=True).data, status=status.HTTP_200_OK)


class RetrieveAccountByNameView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Retrieve account by name",
        operation_description="Get details of a specific account by its unique name within a namespace",
        request_body=AccountRetrieveByNameSerializer,
        responses={200: AccountSerializer},
        tags=["Accounts"],
        security=[{"Token": []}]
    )
    def post(self, request):
        serializer = AccountRetrieveByNameSerializer(data=request.data)
        if serializer.is_valid():
            try:
                account = get_account_by_name(
                    user=request.user,
                    namespace_name=serializer.validated_data['namespace_name'],
                    name=serializer.validated_data['account_name']
                )
                return Response(AccountSerializer(account).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Update account",
        operation_description="Update account details (e.g., rename) by current name and namespace",
        request_body=AccountUpdateSerializer,
        manual_parameters=[
            openapi.Parameter('namespace_name', openapi.IN_QUERY, description="Namespace Name", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('account_name', openapi.IN_QUERY, description="Current Account Name", type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: AccountSerializer},
        tags=["Accounts"],
        security=[{"Token": []}]
    )
    def patch(self, request):
        namespace_name = request.query_params.get('namespace_name')
        account_name = request.query_params.get('account_name')
        
        if not namespace_name:
            return Response({"error": "namespace_name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not account_name:
            return Response({"error": "account_name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AccountUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                account = update_account(
                    user=request.user,
                    namespace_name=namespace_name,
                    current_name=account_name,
                    new_name=serializer.validated_data.get('name')
                )
                return Response(AccountSerializer(account).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Delete account",
        operation_description="Permanently remove an account by name and namespace",
        manual_parameters=[
            openapi.Parameter('namespace_name', openapi.IN_QUERY, description="Namespace Name", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('account_name', openapi.IN_QUERY, description="Account Name", type=openapi.TYPE_STRING, required=True)
        ],
        responses={204: "No Content"},
        tags=["Accounts"],
        security=[{"Token": []}]
    )
    def delete(self, request):
        namespace_name = request.query_params.get('namespace_name')
        account_name = request.query_params.get('account_name')
        
        if not namespace_name:
            return Response({"error": "namespace_name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not account_name:
            return Response({"error": "account_name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            delete_account(request.user, namespace_name, account_name)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
                accounts = list_accounts_by_namespace(request.user, serializer.validated_data['namespace_name'])
                return Response(AccountSerializer(accounts, many=True).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
