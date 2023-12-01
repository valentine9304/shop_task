from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from .views import CategoryViewSet, ProductViewSet, ShoppingCartViewSet


router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("cart", ShoppingCartViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Shop Task API",
        default_version="v1",
        description="Документация для тестового приложения",
        contact=openapi.Contact(email="admin@admin.ru"),
        license=openapi.License(name="Test Task"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
