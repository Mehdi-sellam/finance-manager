from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    ConversionRateSerializer,
    ConversionRateCreateSerializer,
    ConversionRateUpdateSerializer
)
from .services import (
    create_conversion_rate,
    list_conversion_rates,
    update_conversion_rate,
    delete_conversion_rate
)

class CreateConversionRateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create conversion rate",
        request_body=ConversionRateCreateSerializer,
        responses={201: ConversionRateSerializer},
        tags=["Conversion Rates"],
        security=[{"Token": []}]
    )
    def post(self, request):
        serializer = ConversionRateCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                rate = create_conversion_rate(
                    user=request.user,
                    **serializer.validated_data
                )
                return Response(ConversionRateSerializer(rate).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListConversionRatesView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List conversion rates",
        responses={200: ConversionRateSerializer(many=True)},
        tags=["Conversion Rates"],
        security=[{"Token": []}]
    )
    def get(self, request):
        rates = list_conversion_rates(request.user)
        return Response(ConversionRateSerializer(rates, many=True).data, status=status.HTTP_200_OK)

class UpdateConversionRateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Update conversion rate",
        request_body=ConversionRateUpdateSerializer,
        manual_parameters=[
            openapi.Parameter('from_currency', openapi.IN_QUERY, description="From Currency", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('to_currency', openapi.IN_QUERY, description="To Currency", type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: ConversionRateSerializer},
        tags=["Conversion Rates"],
        security=[{"Token": []}]
    )
    def patch(self, request):
        from_currency = request.query_params.get('from_currency')
        to_currency = request.query_params.get('to_currency')
        
        if not from_currency or not to_currency:
            return Response({"error": "from_currency and to_currency query parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = ConversionRateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                rate = update_conversion_rate(
                    user=request.user,
                    from_currency=from_currency,
                    to_currency=to_currency,
                    rate=serializer.validated_data['rate']
                )
                return Response(ConversionRateSerializer(rate).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteConversionRateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Delete conversion rate",
        manual_parameters=[
            openapi.Parameter('from_currency', openapi.IN_QUERY, description="From Currency", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('to_currency', openapi.IN_QUERY, description="To Currency", type=openapi.TYPE_STRING, required=True)
        ],
        responses={204: "No Content"},
        tags=["Conversion Rates"],
        security=[{"Token": []}]
    )
    def delete(self, request):
        from_currency = request.query_params.get('from_currency')
        to_currency = request.query_params.get('to_currency')
        
        if not from_currency or not to_currency:
            return Response({"error": "from_currency and to_currency query parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            delete_conversion_rate(request.user, from_currency, to_currency)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
