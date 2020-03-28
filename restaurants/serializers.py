from rest_framework import serializers

from restaurants.models import Restauant


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restauant
        fields = '__all__'
