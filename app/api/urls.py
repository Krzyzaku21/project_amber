from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1.0',
        description="Panels",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),

    path('api.json/', schema_view.without_ui(cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
]
