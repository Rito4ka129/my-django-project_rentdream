# Create your models here.
from django.db import models
from django.conf import settings

from apps.listings.models import Listing


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Рейтинг от 1 до 5

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.listing.title} by {self.user.username}"
