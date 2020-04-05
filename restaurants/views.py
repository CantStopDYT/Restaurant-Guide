from rest_framework import viewsets
from rest_framework import permissions

from restaurants.models import Restaurant, Location
from restaurants.serializers import RestaurantSerializer, LocationGeoSerializer


class LocationList(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationGeoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
