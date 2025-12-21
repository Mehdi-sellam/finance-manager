# Added by AI - namespace/urls.py
from django.urls import path
from .views import (
    CreateNamespaceView,
    ListNamespacesView,
    RetrieveNamespaceView,
    RetrieveNamespaceByNameView,
    UpdateNamespaceView,
    DeleteNamespaceView
)

urlpatterns = [
    path("", ListNamespacesView.as_view(), name="list-namespaces"),
    path("create/", CreateNamespaceView.as_view(), name="create-namespace"),
    path("<int:pk>/", RetrieveNamespaceView.as_view(), name="retrieve-namespace-by-id"),
    path("retrieve-by-name/", RetrieveNamespaceByNameView.as_view(), name="retrieve-namespace-by-name"),
    path("update/", UpdateNamespaceView.as_view(), name="update-namespace"),
    path("delete/", DeleteNamespaceView.as_view(), name="delete-namespace"),
]

