from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/", include("loans.api.urls", namespace="loans")),
    path("api/", include("referrals.api.urls", namespace="referrals")),
    path("api/", include("savings_wallets.api.urls", namespace="savings_wallets")),
    path("api/", include("wallets.urls", namespace="wallets")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-docs",
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    extrapatterns = [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += extrapatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
