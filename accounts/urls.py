from django.urls import path
from . import views
from .views import TestView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessOwnerViewSet

urlpatterns = [
    # Example placeholder endpoint
    # path('owners/', views.BusinessOwnerList.as_view(), name='owner-list'),
    path('test/', TestView.as_view(), name='test-view'),
]




router = DefaultRouter()
router.register(r'owners', BusinessOwnerViewSet, basename='owner')

urlpatterns = [
    path('', include(router.urls)),
]

