from django.shortcuts import render

# Create your views here.
# from rest_framework import generics
# from listings.models import Listing
# from listings.serializers import ListingSerializer
# from django.db.models import Q
#
#
# class ListingSearchView(generics.ListAPIView):
#     serializer_class = ListingSerializer
#
#     def get_queryset(self):
#         queryset = Listing.objects.all()
#         keywords = self.request.query_params.get('keywords', None)
#         min_price = self.request.query_params.get('min_price', None)
#         max_price = self.request.query_params.get('max_price', None)
#         location = self.request.query_params.get('location', None)
#         min_rooms = self.request.query_params.get('min_rooms', None)
#         max_rooms = self.request.query_params.get('max_rooms', None)
#         housing_type = self.request.query_params.get('housing_type', None)
#         sort_by = self.request.query_params.get('sort_by', None)
#
#         if keywords:
#             queryset = queryset.filter(Q(title__icontains=keywords) | Q(description__icontains=keywords))
#         if min_price:
#             queryset = queryset.filter(price__gte=min_price)
#         if max_price:
#             queryset = queryset.filter(price__lte=max_price)
#         if location:
#             queryset = queryset.filter(location__icontains=location)
#         if min_rooms:
#             queryset = queryset.filter(rooms__gte=min_rooms)
#         if max_rooms:
#             queryset = queryset.filter(rooms__lte=max_rooms)
#         if housing_type:
#             queryset = queryset.filter(housing_type=housing_type)
#
#         if sort_by:
#             if sort_by == 'price_asc':
#                 queryset = queryset.order_by('price')
#             elif sort_by == 'price_desc':
#                 queryset = queryset.order_by('-price')
#             elif sort_by == 'date_newest':
#                 queryset = queryset.order_by('-id')  # assuming 'id' is auto-incrementing
#             elif sort_by == 'date_oldest':
#                 queryset = queryset.order_by('id')
#
#         return queryset
# search/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ListingSerializer  # Импортируйте ваш сериализатор
from ..listings.models import Listing


class ListingSearchView(viewsets.ViewSet):
    def list(self, request):
        # Реализуйте логику поиска здесь
        search_query = request.query_params.get('search', None)
        if search_query:
            listings = Listing.objects.filter(name__icontains=search_query)  # Пример фильтрации
        else:
            listings = Listing.objects.all()  # Если нет запроса, возвращаем все
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)