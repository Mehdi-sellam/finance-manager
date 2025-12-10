from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestView, BusinessOwnerViewSet, LoginView, LogoutView

# Create the router and register viewsets first
router = DefaultRouter()
router.register(r'owners', BusinessOwnerViewSet, basename='owners')

# Now define urlpatterns
urlpatterns = [
    path('test/', TestView.as_view(), name='test-view'),
    path('', include(router.urls)),  # Include router URLs AFTER router is defined
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
