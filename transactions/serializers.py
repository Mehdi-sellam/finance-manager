from rest_framework import serializers
from .models import Transaction, TransactionType
from accountsb.models import Currency

class TransactionSerializer(serializers.ModelSerializer):
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

class TransactionInCreateSerializer(serializers.Serializer):
    destination_account_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    currency = serializers.ChoiceField(choices=Currency.choices)
    description = serializers.CharField(required=False, allow_blank=True)

class TransactionOutCreateSerializer(serializers.Serializer):
    source_account_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    currency = serializers.ChoiceField(choices=Currency.choices)
    description = serializers.CharField(required=False, allow_blank=True)

class TransactionTransferCreateSerializer(serializers.Serializer):
    source_account_name = serializers.CharField()
    destination_account_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)

class TransactionListByAccountSerializer(serializers.Serializer):
    account_name = serializers.CharField()
