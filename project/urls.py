from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', RedirectView.as_view(url='/backend/')),
    path('backend/', include('testing.urls', namespace='testing')),
    path('backend/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'backend/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path('backend/admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static('media', document_root=settings.MEDIA_ROOT)
