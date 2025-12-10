# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessOwnerViewSet, LoginView, LogoutView, RegisterView

router = DefaultRouter()
router.register(r'owners', BusinessOwnerViewSet, basename='owners')

urlpatterns = [


    # auth endpoints
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # viewsets (owners)
    path('', include(router.urls)),
]
