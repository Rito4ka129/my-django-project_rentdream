from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

# Определение типов жилья
HOUSING_TYPE_CHOICES = (
    ('apartment', 'Квартира'),
    ('house', 'Дом'),
    ('duplex', 'Дуплекс'),
    ('studio', 'Студия'),
    ('cottage', 'Коттедж'),
)

# Статусы объявления
STATUS_CHOICES = (
    ('active', 'Активно'),
    ('inactive', 'Неактивно'),
)

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_rooms = models.IntegerField()
    housing_type = models.CharField(max_length=50, choices=HOUSING_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}" if self.title and self.location else 'Без названия'

    def clean(self):
        if self.price < 0:
            raise ValidationError('Цена не может быть отрицательной.')

        if self.num_rooms < 0:
            raise ValidationError('Количество комнат не может быть отрицательным.')
