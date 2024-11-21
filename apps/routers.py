# from django.urls import path, include
#
# urlpatterns = [
#     path('', include('apps.users.urls')),
#     path('', include('apps.bookings.urls')),
#     path('', include('apps.listings.urls')),
#     path('', include('apps.reviews.urls')),
#     path('', include('apps.search.urls')),
#     path('api-auth/', include('rest_framework.urls')),
# ]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # Маршруты для аутентификации
    # path('', include('apps.users.urls')),         # Маршруты из приложения users
    path('', include('apps.bookings.urls')),   # Маршруты из приложения bookings
    path('', include('apps.listings.urls')),   # Маршруты из приложения listings
    path('', include('apps.reviews.urls')),     # Маршруты из приложения reviews
    path('', include('apps.search.urls')),       # Маршруты из приложения search
]

