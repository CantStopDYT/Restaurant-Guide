from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from restaurants.models import Restauant
from restaurants.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restauant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
