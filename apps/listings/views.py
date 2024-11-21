
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Listing
from .serializers import ListingSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()   # Получаем все объявления из базы данных
    serializer_class = ListingSerializer    # Указываем сериализатор, который будем использовать
    permission_classes = [IsAuthenticatedOrReadOnly]    # Позволяет доступ пользователям
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