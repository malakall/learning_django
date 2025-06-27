from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# Для сваггера
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="yatube API",
        default_version='v1',
        description="автосгенерированная документация к API Yatube",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="artemu@example.com"),
        license=openapi.License(name="права защищены жи есть"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('yatube.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('captcha/', include('captcha.urls')),
    path('posts/', include('posts.urls')),

    # Swagger и Redoc
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

handler404 = 'core.views.page_not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
