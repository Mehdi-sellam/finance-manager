from django.urls import path
from .views import (
    CreateConversionRateView,
    ListConversionRatesView,
    UpdateConversionRateView,
    DeleteConversionRateView
)

urlpatterns = [
    path('create/', CreateConversionRateView.as_view(), name='conversion-rate-create'),
    path('', ListConversionRatesView.as_view(), name='conversion-rate-list'),
    path('update/', UpdateConversionRateView.as_view(), name='conversion-rate-update'),
    path('delete/', DeleteConversionRateView.as_view(), name='conversion-rate-delete'),
]
