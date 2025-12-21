from django.urls import path
from .views import (
    CreateInTransactionView,
    CreateOutTransactionView,
    CreateTransferTransactionView,
    ListTransactionsView,
    ListTransactionsByAccountView,
    ListInTransactionsView,
    ListOutTransactionsView,
    ListTransferTransactionsView
)

urlpatterns = [
    path('in/create/', CreateInTransactionView.as_view(), name='transaction-in-create'),
    path('out/create/', CreateOutTransactionView.as_view(), name='transaction-out-create'),
    path('transfer/create/', CreateTransferTransactionView.as_view(), name='transaction-transfer-create'),
    path('', ListTransactionsView.as_view(), name='transaction-list'),
    path('list-by-account/', ListTransactionsByAccountView.as_view(), name='transaction-list-by-account'),
    path('list-in/', ListInTransactionsView.as_view(), name='transaction-list-in'),
    path('list-out/', ListOutTransactionsView.as_view(), name='transaction-list-out'),
    path('list-transfers/', ListTransferTransactionsView.as_view(), name='transaction-list-transfers'),
]
