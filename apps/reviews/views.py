from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from .models import Listing, Review
from .serializers import ReviewSerializer
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Сохраняем пользователя в отзыве


@login_required
def create_review(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.listing = listing
            review.save()
            return redirect('listing_detail', listing_id=listing.id)  # Перенаправление на страницу объявления
    else:
        form = ReviewForm()
    return render(request, 'reviews/create_review.html', {'form': form, 'listing': listing})


@login_required
def listing_reviews(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    reviews = listing.reviews.all()
    return render(request, 'reviews/listing_reviews.html', {'listing': listing, 'reviews': reviews})