from django.db import models
from django.conf import settings
from apps.listings.models import Listing

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Подтверждено'),
        ('pending', 'Ожидает'),
        ('canceled', 'Отменено'),
        ('active', 'Активно'),
        ('inactive', 'Неактивно'),
        ('sold', 'Продано'),
        ('expired', 'Истекло'),
        ('under_offer', 'На предложении'),
        ('rejected', 'Отклонено'),
        ('draft', 'Черновик'),
        ('archived', 'Архивировано'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', null=True)

    def __str__(self):
        listing_title = self.listing.title if self.listing else 'Без названия'
        return f"{listing_title} - {self.start_date} to {self.end_date}"
