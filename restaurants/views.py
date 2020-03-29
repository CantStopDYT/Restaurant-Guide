import json
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework import permissions

from restaurants.models import Restaurant, Location
from restaurants.serializers import RestaurantSerializer

from django.core.serializers import serialize


def restaurants_geojson(request):
    geojson = serialize('geojson', Location.objects.all(), geometry_field='coordinates',
                        fields=('restaurant', 'street_address', 'city', 'state', 'zip'))
    return JsonResponse(json.loads(geojson), safe=False)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
