from rest_framework import serializers
from .models import Transaction, TransactionType
from accountsb.models import Currency


# Added by AI - Main Transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    # Added by AI - Read-only fields for display
    source_account_name = serializers.CharField(source='source_account.name', read_only=True)
    destination_account_name = serializers.CharField(source='destination_account.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'amount', 'currency', 
            'source_account_name', 'destination_account_name', 
            'description', 'created_at'
        ]
        read_only_fields = fields


# Added by AI - Serializer for creating IN transactions
class TransactionInCreateSerializer(serializers.Serializer):
    destination_account_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    currency = serializers.ChoiceField(choices=Currency.choices)
    description = serializers.CharField(required=False, allow_blank=True)


# Added by AI - Serializer for creating OUT transactions
class TransactionOutCreateSerializer(serializers.Serializer):
    source_account_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    currency = serializers.ChoiceField(choices=Currency.choices)
    description = serializers.CharField(required=False, allow_blank=True)


# Added by AI - Serializer for creating TRANSFER transactions
class TransactionTransferCreateSerializer(serializers.Serializer):
    source_account_name = serializers.CharField()
    destination_account_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)


# Added by AI - Serializer for listing transactions by account
class TransactionListByAccountSerializer(serializers.Serializer):
    account_name = serializers.CharField()
