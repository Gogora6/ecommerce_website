from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Graey E-Commerce API",
        default_version='v1',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="lashagogorishvili1999@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('cart.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
