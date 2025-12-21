from rest_framework import serializers
from .models import Account, Currency

class AccountSerializer(serializers.ModelSerializer):
    namespace_name = serializers.CharField(source='namespace.name', read_only=True)
    
    class Meta:
        model = Account
        fields = [
            'name',
            'namespace_name',
            'currency',
            'balance',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['balance', 'created_at', 'updated_at']

class AccountCreateSerializer(serializers.ModelSerializer):
    namespace_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Account
        fields = ['namespace_name', 'name', 'currency']

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['name']

class AccountRetrieveByNameSerializer(serializers.Serializer):
    account_name = serializers.CharField()

class AccountListByNamespaceSerializer(serializers.Serializer):
    namespace_name = serializers.CharField()
