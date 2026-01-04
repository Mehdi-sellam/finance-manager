from rest_framework import serializers
from .models import Transaction, TransactionType
from accountsb.models import Currency, Account


class TransactionSerializer(serializers.ModelSerializer):
    source_account_name = serializers.CharField(source='source_account.name', read_only=True)
    destination_account_name = serializers.CharField(source='destination_account.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'amount', 'destination_amount', 
            'currency', 'source_currency_rate', 'destination_currency_rate',
            'source_account', 'destination_account',
            'source_account_name', 'destination_account_name', 
            'description', 'created_at'
        ]
        read_only_fields = fields


class TransactionInCreateSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    currency = serializers.ChoiceField(choices=Currency.choices)
    description = serializers.CharField(required=False, allow_blank=True)


class TransactionOutCreateSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    currency = serializers.ChoiceField(choices=Currency.choices)
    description = serializers.CharField(required=False, allow_blank=True)


class TransactionTransferCreateSerializer(serializers.Serializer):
    source_account_id = serializers.IntegerField()
    destination_account_id = serializers.IntegerField()
    source_amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    destination_amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)
