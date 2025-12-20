from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# DRF router
router = routers.DefaultRouter()


# Swagger / OpenAPI schema
schema_view = get_schema_view(
    openapi.Info(
        title="Finance Manager API",
        default_version="v1",
        description="API documentation for Finance Manager",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API routes
    path("api/", include(router.urls)),

    # Auth / accounts
    path("api/auth/", include("accounts.urls")),



    # API documentation
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]
