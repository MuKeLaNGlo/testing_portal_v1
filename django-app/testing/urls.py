from django.urls import path

from testing.views import home, submit_test, test

app_name = "testing"

urlpatterns = [
    path("", home, name="home"),
    path("test/<int:test_id>/", test, name="test"),
    path("submit_test/<int:test_id>/", submit_test, name="submit_test"),
    # Добавьте другие URL-маршруты, если это необходимо
]
