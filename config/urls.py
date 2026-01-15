"""
URLs principales du projet
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Transport API - Architecture Modulaire",
        default_version='v1',
        description="""
        API backend pour l'application de gestion de transport.
        
        ## Architecture Modulaire
        - **Authentication**: Gestion utilisateurs et JWT
        - **Geography**: Pays, Villes, Gares
        - **Transport**: Trajets, Réservations, Bus
        - **Delivery**: Colis, Livraisons
        - **Payment**: Paiements, Rapports
        - **Shop**: Articles, Promotions
        - **Notifications**: Notifications push
        
        ## Authentification
        Utilisez le token JWT obtenu via `/api/auth/login/`:
        ```
        Authorization: Bearer <votre_token>
        ```
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@transport.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API Apps
    path('api/auth/', include('apps.authentication.urls')),
    path('api/geography/', include('apps.geography.urls')),
    path('api/transport/', include('apps.transport.urls')),
    # path('api/geography/', include('apps.geography.urls')),
    # path('api/transport/', include('apps.transport.urls')),
    # path('api/delivery/', include('apps.delivery.urls')),
    # path('api/payment/', include('apps.payment.urls')),
    # path('api/shop/', include('apps.shop.urls')),
    # path('api/notifications/', include('apps.notifications.urls')),
]

# Servir les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
