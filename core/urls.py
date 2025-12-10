from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Import viewsets
from projects.views import ProjectViewSet
from finance.views import (
    ExpenseViewSet, SalaryPaymentViewSet,
    ResourceConsumptionViewSet, BudgetViewSet
)
from users.views import UserViewSet
from accounts.views import BusinessOwnerViewSet

# Routers setup
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'users', UserViewSet, basename='users')
router.register(r'owners', BusinessOwnerViewSet, basename='owners')

router.register(r'expenses', ExpenseViewSet, basename='expenses')
router.register(r'salaries', SalaryPaymentViewSet, basename='salaries')
router.register(r'resources', ResourceConsumptionViewSet, basename='resources')
router.register(r'budgets', BudgetViewSet, basename='budgets')

projects_router = nested_routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'expenses', ExpenseViewSet, basename='project-expenses')
projects_router.register(r'salaries', SalaryPaymentViewSet, basename='project-salaries')
projects_router.register(r'budgets', BudgetViewSet, basename='project-budgets')
projects_router.register(r'resources', ResourceConsumptionViewSet, basename='project-resources')

# Swagger setup
schema_view = get_schema_view(
    openapi.Info(
        title="Finance Manager API",
        default_version='v1',
        description="API documentation for Finance Manager",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),
    path('api/auth/', include('accounts.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
