from django.conf import settings
from django.db import models
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from apps.listings.models import Listing
from apps.listings.serializers import ListingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()   # Получаем все объявления из базы данных
    serializer_class = ListingSerializer    # Указываем сериализатор, который будем использовать
    permission_classes = [AllowAny]    # Позволяет доступ пользователям
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = {
        'price': ['gte', 'lte'],  # Фильтрация по минимальной и максимальной цене
        'location': ['icontains'],  # Фильтрация по местоположению
        'num_rooms': ['gte', 'lte'],  # Фильтрация по количеству комнат
        'housing_type': ['exact'],  # Фильтрация по типу жилья
    }
    search_fields = ['title', 'description']  # Полнотекстовый поиск
    ordering_fields = ['price', 'created_at']  # Сортировка
    ordering = ['-created_at']  # Сортировка по умолчанию (новые объявления)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'landlord':
                return Listing.objects.filter(user=user)
            return Listing.objects.filter(status='active')
        return Listing.objects.filter(status='active')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"

class Meta:
    model = Review
    fields = ['id', 'user', 'listing', 'content', 'rating', 'created_at']
    read_only_fields = ['user', 'created_at']