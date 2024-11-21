# search/serializers.py
from rest_framework import serializers

from apps.listings.models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'  # Или укажите конкретные поля, если нужно

class LogoutSerializer(serializers.Serializer):
    pass