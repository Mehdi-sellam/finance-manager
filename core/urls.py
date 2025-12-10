"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

# Import viewsets
from projects.views import ProjectViewSet
from finance.views import (
    ExpenseViewSet, SalaryPaymentViewSet,
    ResourceConsumptionViewSet, BudgetViewSet
)
from users.views import UserViewSet
from accounts.views import BusinessOwnerViewSet

# Base Router
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'users', UserViewSet, basename='users')
router.register(r'owners', BusinessOwnerViewSet, basename='owners')

# Nested Router → /projects/<id>/
projects_router = nested_routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'expenses', ExpenseViewSet, basename='project-expenses')
projects_router.register(r'salaries', SalaryPaymentViewSet, basename='project-salaries')
projects_router.register(r'budgets', BudgetViewSet, basename='project-budget')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),

    # Swagger
    path('', include('swagger.urls')),
]
