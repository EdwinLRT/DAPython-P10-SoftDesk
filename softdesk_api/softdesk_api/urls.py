from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SoftDesk API",
        default_version='v0',
        description="API-SoftDesk est une API RESTful permettant de remonter et suivre des problèmes techniques"
                    " pour les trois plateformes (site web, applications Android et iOS)."
                    "L'application permet aux utilisateurs de créer divers projets, d'ajouter des utilisateurs"
                    " (contributeurs) à des projets spécifiques, de créer des problèmes au sein des projets et"
                    " d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('api-auth/', include('sd_accounts.urls')),

    # Support API
    path('api/', include('sd_support.urls')),

    # drf-yasg routes
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
