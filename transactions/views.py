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
    TransactionTransferCreateSerializer
)
from .services import (
    create_in_transaction,
    create_out_transaction,
    create_transfer_transaction,
    list_transactions
)
from .models import TransactionType


class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List transactions",
        operation_description="List transactions for the authenticated user. Optional filters: type, account_id.",
        manual_parameters=[
            openapi.Parameter('type', openapi.IN_QUERY, description="Filter by Transaction Type (IN, OUT, TRANSFER)", type=openapi.TYPE_STRING),
            openapi.Parameter('account_id', openapi.IN_QUERY, description="Filter by Account ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: TransactionSerializer(many=True)},
        tags=["Transactions"],
        security=[{"Token": []}],
    )
    def get(self, request):
        transaction_type = request.query_params.get('type')
        account_id = request.query_params.get('account_id')
        transactions = list_transactions(request.user, transaction_type=transaction_type, account_id=account_id)
        return Response(TransactionSerializer(transactions, many=True).data)


class CreateInTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create IN transaction",
        operation_description="Create a deposit (IN) transaction for the authenticated user.",
        request_body=TransactionInCreateSerializer,
        responses={201: TransactionSerializer},
        tags=["Transactions"],
        security=[{"Token": []}],
    )
    def post(self, request):
        serializer = TransactionInCreateSerializer(data=request.data)
        if serializer.is_valid():
            transaction = create_in_transaction(
                requester=request.user,
                **serializer.validated_data
            )
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOutTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create OUT transaction",
        operation_description="Create a withdrawal (OUT) transaction for the authenticated user.",
        request_body=TransactionOutCreateSerializer,
        responses={201: TransactionSerializer},
        tags=["Transactions"],
        security=[{"Token": []}],
    )
    def post(self, request):
        serializer = TransactionOutCreateSerializer(data=request.data)
        if serializer.is_valid():
            transaction = create_out_transaction(
                requester=request.user,
                **serializer.validated_data
            )
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTransferTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create TRANSFER transaction",
        operation_description="Create a transfer transaction between accounts for the authenticated user.",
        request_body=TransactionTransferCreateSerializer,
        responses={201: TransactionSerializer},
        tags=["Transactions"],
        security=[{"Token": []}],
    )
    def post(self, request):
        serializer = TransactionTransferCreateSerializer(data=request.data)
        if serializer.is_valid():
            transaction = create_transfer_transaction(
                requester=request.user,
                **serializer.validated_data
            )
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
