from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.reviews.views import ReviewViewSet, create_review, listing_reviews

router = DefaultRouter()
router.register(r'rewiews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('listings/<int:listing_id>/reviews/create/', create_review, name='create_review'),
    path('listings/<int:listing_id>/reviews/', listing_reviews, name='listing_reviews'),
]
