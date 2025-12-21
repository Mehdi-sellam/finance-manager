from django.urls import path
from .views import (
    CreateAccountView,
    ListAccountsView,
    RetrieveAccountByNameView,
    UpdateAccountView,
    DeleteAccountView,
    ListAccountsByNamespaceView
)

urlpatterns = [
    path('create/', CreateAccountView.as_view(), name='account-create'),
    path('', ListAccountsView.as_view(), name='account-list'),
    path('retrieve-by-name/', RetrieveAccountByNameView.as_view(), name='account-retrieve-by-name'),
    path('update/', UpdateAccountView.as_view(), name='account-update'),
    path('delete/', DeleteAccountView.as_view(), name='account-delete'),
    path('list-by-namespace/', ListAccountsByNamespaceView.as_view(), name='account-list-by-namespace'),
]
