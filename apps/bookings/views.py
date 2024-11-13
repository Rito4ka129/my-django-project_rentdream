from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'tenant':
            return Booking.objects.filter(user=self.request.user)
        elif self.request.user.role == 'landlord':
            return Booking.objects.filter(listing__user=self.request.user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.user != request.user:
            return Response({'error': 'You can only cancel your own bookings.'}, status=status.HTTP_403_FORBIDDEN)
        booking.status = 'canceled'
        booking.save()
        return Response({'status': 'Booking canceled'})

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if request.user.role != 'landlord' or booking.listing.user != request.user:
            return Response({'error': 'Only the landlord can confirm the booking.'}, status=status.HTTP_403_FORBIDDEN)
        booking.status = 'confirmed'
        booking.save()
        return Response({'status': 'Booking confirmed'})
