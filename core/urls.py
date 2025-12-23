from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions


# DRF router
router = routers.DefaultRouter()


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
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

    # API routes
    path("api/", include(router.urls)),

    # Auth / accounts
    path("api/auth/", include("accounts.urls")),
    
    # Namespace endpoints
    path("api/namespaces/", include("namespace.urls")),

    # New Financial Apps
    path("api/accountsb/", include("accountsb.urls")),
    path("api/conversion-rates/", include("conversion_rates.urls")),
    path("api/transactions/", include("transactions.urls")),



    # API documentation
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]
