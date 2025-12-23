from rest_framework import serializers
from .models import ConversionRate


class ConversionRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRate
        fields = ['id', 'from_currency', 'to_currency', 'rate', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversionRateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRate
        fields = ['from_currency', 'to_currency', 'rate']


class ConversionRateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRate
        fields = ['rate']
