from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Listing
from .serializers import ListingSerializer
from rest_framework.permissions import IsAuthenticated

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'landlord':
            return Listing.objects.filter(user=self.request.user)
        return Listing.objects.filter(status='active')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
