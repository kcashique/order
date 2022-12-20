from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("users.urls", namespace="users")),
        path("", include("products.urls", namespace="products")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
