from rest_framework import serializers
from .models import ConversionRate


# Added by AI - Main ConversionRate serializer
class ConversionRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRate
        fields = ['id', 'from_currency', 'to_currency', 'rate', 'created_at']
        read_only_fields = ['id', 'created_at']


# Added by AI - Serializer for creating conversion rates
class ConversionRateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRate
        fields = ['from_currency', 'to_currency', 'rate']


# Added by AI - Serializer for updating conversion rates
class ConversionRateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRate
        fields = ['rate']
