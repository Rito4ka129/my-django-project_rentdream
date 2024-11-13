from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'tenant':
            return Review.objects.filter(user=self.request.user)
        elif self.request.user.role == 'landlord':
            return Review.objects.filter(listing__user=self.request.user)
        return Review.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
