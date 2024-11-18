from django.urls import path
from .views import ListingSearchView

urlpatterns = [
    path('search/', ListingSearchView.as_view({'get': 'list'}), name='listing-search'), # Можно переработать (?)
]
