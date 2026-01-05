from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions


# DRF router
router = routers.DefaultRouter()


# Custom schema generator to include Token Authentication security scheme
class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # Add security definitions for Token Authentication
        schema.security_definitions = {
            'Token': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Token-based authentication. Format: Token <your-token-here>'
            }
        }
        return schema


# Swagger / OpenAPI schema
# Configure schema with custom generator for Token Authentication
schema_view = get_schema_view(
    openapi.Info(
        title="Finance Manager API",
        default_version="v1",
        description="API documentation for Finance Manager",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=CustomOpenAPISchemaGenerator,
)


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Added by AI - Fix Swagger login redirect
    path("accounts/login/", admin.site.login, name="login"),

    # API routes
    path("api/", include(router.urls)),

    # Auth / accounts
    path("api/auth/", include("accounts.urls")),
    
    # Added by AI - Namespace endpoints
    path("api/namespaces/", include("namespace.urls")),

    # Added by AI - New Financial Apps
    path("api/accounts/", include("accountsb.urls")),
    path("api/transactions/", include("transactions.urls")),



    # API documentation
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),



    # Web routes
    path('', include('web.urls')),
]
