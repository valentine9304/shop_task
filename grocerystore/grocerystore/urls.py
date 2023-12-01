from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static

urlpatterns = [
    path("", include("products.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    re_path(r"^chaining/", include("smart_selects.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
