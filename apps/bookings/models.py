# Create your models here.
from django.db import models
from django.conf import settings
from apps.listings.models import Listing


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Подтверждено'),
        ('pending', 'Ожидает'),
        ('canceled', 'Отменено'),
        ('active', 'Активно'),  # Объявление активно и доступно для просмотра
        ('inactive', 'Неактивно'),  # Объявление неактивно, но не удалено
        ('sold', 'Продано'),  # Объявление было продано
        ('expired', 'Истекло'),  # Объявление истекло и больше не актуально
        ('under_offer', 'На предложении'),  # Объявление на стадии предложения
        ('rejected', 'Отклонено'),  # Объявление было отклонено
        ('draft', 'Черновик'),  # Объявление в стадии разработки, еще не опубликовано
        ('archived', 'Архивировано'),  # Объявление перемещено в архив)
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.listing.title} - {self.start_date} to {self.end_date}"
