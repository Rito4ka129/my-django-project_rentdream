from django.urls import path, include

urlpatterns = [
    path('', include('apps.users.urls')),
    path('', include('apps.bookings.urls')),
    path('', include('apps.listings.urls')),
    path('', include('apps.reviews.urls')),
    path('', include('apps.search.urls')),
    #path('api-auth/', include('rest_framework.urls')),
]