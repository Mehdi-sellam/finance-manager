from django.urls import path
from .views import (
    TransactionListView,
    CreateInTransactionView,
    CreateOutTransactionView,
    CreateTransferTransactionView
)

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('in/', CreateInTransactionView.as_view(), name='transaction-in-create'),
    path('out/', CreateOutTransactionView.as_view(), name='transaction-out-create'),
    path('transfer/', CreateTransferTransactionView.as_view(), name='transaction-transfer-create'),
]
