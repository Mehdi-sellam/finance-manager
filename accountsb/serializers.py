from rest_framework import serializers
from .models import Account, Currency

class AccountSerializer(serializers.ModelSerializer):
    namespace_name = serializers.CharField(source='namespace.name', read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'name', 'namespace', 'namespace_name', 'currency', 'balance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'balance', 'created_at', 'updated_at', 'namespace_name']

class AccountCreateSerializer(serializers.ModelSerializer):
    namespace_id = serializers.IntegerField(write_only=True)
    name = serializers.CharField(max_length=50)
    
    class Meta:
        model = Account
        fields = ['namespace_id', 'name', 'currency']

class AccountUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=50)
    
    class Meta:
        model = Account
        fields = ['name']
