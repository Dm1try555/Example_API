from django.contrib import admin
from django.urls import path, include
from .views import hello_world, ProductViewSet, hello_dima, CarViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'car', CarViewSet)



schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Документация API",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hello_world),  # Для выведения "Hello, World!"
    path('api/hello', hello_dima),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
