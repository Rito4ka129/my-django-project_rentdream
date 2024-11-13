
# Create your models here.
from django.contrib.auth import get_user_model

from django.db import models
from django.conf import settings

class Listing(models.Model):
    HOUSING_TYPE_CHOICES = (
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('townhouse', 'Таунхаус'),
        ('land', 'Земля'),
        ('duplex', 'Дуплекс'),
        ('studio', 'Студия'),
        ('penthouse', 'Пентхаус'),
        ('villa', 'Вилла'),
        ('cottage', 'Коттедж'),
        ('chalet', 'Шале'),

    )

    STATUS_CHOICES = (
        ('active', 'Активно'),
        ('inactive', 'Неактивно'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField()
    housing_type = models.CharField(max_length=20, choices=HOUSING_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
