from rest_framework import serializers
from .models import BusinessOwner

class BusinessOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessOwner
        fields = '__all__'  # or list the fields explicitly
