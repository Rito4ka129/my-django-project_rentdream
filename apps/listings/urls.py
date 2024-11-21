from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet
from django.urls import path
from . import views

# Создаём роутер для автоматической генерации URL-ов для viewset-ов
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listings')

urlpatterns = [
    path('', include(router.urls)),   # Включаем маршруты, сгенерированные роутером

]
