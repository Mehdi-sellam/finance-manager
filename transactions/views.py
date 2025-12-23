from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    TransactionSerializer,
    TransactionInCreateSerializer,
    TransactionOutCreateSerializer,
    TransactionTransferCreateSerializer,
    TransactionListByAccountSerializer
)
from .services import (
    create_in_transaction,
    create_out_transaction,
    create_transfer_transaction,
    list_transactions,
    list_transactions_by_account,
    list_transactions_by_type
)
from .models import TransactionType


class CreateInTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create IN transaction",
        operation_description="Add funds to an account (Deposit)",
        request_body=TransactionInCreateSerializer,
        responses={201: TransactionSerializer},
        tags=["Transactions"],
        security=[{"Token": []}]
    )
    def post(self, request):
        serializer = TransactionInCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                transaction = create_in_transaction(
                    user=request.user,
                    **serializer.validated_data
                )
                return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOutTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create OUT transaction",
        operation_description="Deduct funds from an account (Withdrawal)",
        request_body=TransactionOutCreateSerializer,
        responses={201: TransactionSerializer},
        tags=["Transactions"],
        security=[{"Token": []}]
    )
    def post(self, request):
        serializer = TransactionOutCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                transaction = create_out_transaction(
                    user=request.user,
                    **serializer.validated_data
                )
                return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTransferTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create TRANSFER transaction",
        operation_description="Transfer funds between two accounts, applying conversion rates if needed",
        request_body=TransactionTransferCreateSerializer,
        responses={201: TransactionSerializer},
        tags=["Transactions"],
        security=[{"Token": []}]
    )
    def post(self, request):
        serializer = TransactionTransferCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                transaction = create_transfer_transaction(
                    user=request.user,
                    **serializer.validated_data
                )
                return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTransactionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List transactions",
        operation_description="List all transactions for the user",
        responses={200: TransactionSerializer(many=True)},
        tags=["Transactions"],
        security=[{"Token": []}]
    )
    def get(self, request):
        transactions = list_transactions(request.user)
        return Response(TransactionSerializer(transactions, many=True).data, status=status.HTTP_200_OK)


class ListTransactionsByAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List transactions by account",
        operation_description="List all transactions involving a specific account",
        request_body=TransactionListByAccountSerializer,
        responses={200: TransactionSerializer(many=True)},
        tags=["Transactions"],
        security=[{"Token": []}]
    )
    def post(self, request):
        serializer = TransactionListByAccountSerializer(data=request.data)
        if serializer.is_valid():
            try:
                transactions = list_transactions_by_account(
                    user=request.user, 
                    namespace_name=serializer.validated_data['namespace_name'],
                    account_name=serializer.validated_data['account_name']
                )
                return Response(TransactionSerializer(transactions, many=True).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListInTransactionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List IN transactions",
        operation_description="List all IN transactions (deposits) for the user",
        responses={200: TransactionSerializer(many=True)},
        tags=["Transactions"],
        security=[{"Token": []}]
    )
    def get(self, request):
        transactions = list_transactions_by_type(request.user, TransactionType.IN)
        return Response(TransactionSerializer(transactions, many=True).data, status=status.HTTP_200_OK)


class ListOutTransactionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List OUT transactions",
        operation_description="List all OUT transactions (withdrawals) for the user",
        responses={200: TransactionSerializer(many=True)},
        tags=["Transactions"],
        security=[{"Token": []}]
    )
    def get(self, request):
        transactions = list_transactions_by_type(request.user, TransactionType.OUT)
        return Response(TransactionSerializer(transactions, many=True).data, status=status.HTTP_200_OK)


class ListTransferTransactionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List TRANSFER transactions",
        operation_description="List all TRANSFER transactions for the user",
        responses={200: TransactionSerializer(many=True)},
        tags=["Transactions"],
        security=[{"Token": []}]
    )
    def get(self, request):
        transactions = list_transactions_by_type(request.user, TransactionType.TRANSFER)
        return Response(TransactionSerializer(transactions, many=True).data, status=status.HTTP_200_OK)
