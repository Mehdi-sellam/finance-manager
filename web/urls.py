from django.urls import path
from .views import index, login, namespaces, namespace_detail, change_password, logout, accounts, account_detail, transactions, transaction_in_create, transaction_out_create, transaction_transfer_create, transaction_transfer_wizard

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('change-password/', change_password, name='change-password'),
    path('namespaces/', namespaces, name='namespaces'),
    path('namespaces/<int:pk>/', namespace_detail, name='namespace-detail'),
    path('accounts/', accounts, name='accounts'),
    path('accounts/<int:pk>/', account_detail, name='account-detail'),
    path('transactions/', transactions, name='transactions'),
    path('transactions/in/', transaction_in_create, name='transaction-in-create'),
    path('transactions/out/', transaction_out_create, name='transaction-out-create'),
    path('transactions/transfer/', transaction_transfer_create, name='transaction-transfer-create'),
    path('transactions/transfer/wizard/', transaction_transfer_wizard, name='transaction-transfer-wizard'),
]
