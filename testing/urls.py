from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "testing"

router = DefaultRouter()
router.register()

urlpatterns = [
    path('', include(router.urls)),
    # Добавьте другие URL-маршруты, если это необходимо
]
