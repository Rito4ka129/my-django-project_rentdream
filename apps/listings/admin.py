from apps.listings.models import Listing  # Import the Listing model
from django.contrib import admin

# Register your models here.
@admin.register(Listing)  # Register the Listing model
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'num_rooms', 'housing_type', 'created_at')

    def num_rooms(self, obj):
        return obj.num_rooms

    def created_at(self, obj):
        return obj.created_at

    num_rooms.short_description = 'Number of Rooms'
    created_at.short_description = 'Creation Date'