from django.urls import path, include
from rest_framework.routers import DefaultRouter

from testing import views

app_name = "testing"

router = DefaultRouter()
router.register('tests', views.Test, basename='test')
router.register('questions', views.Question, basename='question')
router.register('answers', views.Answer, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
    # Добавьте другие URL-маршруты, если это необходимо
]
