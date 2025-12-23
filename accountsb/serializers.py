from rest_framework import serializers
from .models import Account, Currency


# Added by AI - Main Account serializer
class AccountSerializer(serializers.ModelSerializer):
    # Added by AI - Read-only field for display convenience
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


# Added by AI - Serializer for account creation
class AccountCreateSerializer(serializers.ModelSerializer):
    # Added by AI - Input field to resolve namespace by name
    namespace_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Account
        fields = ['namespace_name', 'name', 'currency']


# Added by AI - Serializer for updating account (renaming)
class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['name']


# Added by AI - Serializer for retrieving account by name
class AccountRetrieveByNameSerializer(serializers.Serializer):
    account_name = serializers.CharField()


# Added by AI - Serializer for listing accounts in a namespace
class AccountListByNamespaceSerializer(serializers.Serializer):
    namespace_name = serializers.CharField()
