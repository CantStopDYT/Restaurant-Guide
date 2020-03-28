from rest_framework import serializers

from restaurants.models import *


class DietaryOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DietaryOptions
        fields = ['dietary_options']

    def to_representation(self, instance):
        return instance.get_dietary_options_display()


class PickupOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PickupOptions
        fields = ['pickup_options']

    def to_representation(self, instance):
        return instance.get_pickup_options_display()


class DeliveryOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryOptions
        fields = ['delivery_options']

    def to_representation(self, instance):
        return instance.get_delivery_options_display()


class OrderMethodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderMethods
        fields = ['order_methods']

    def to_representation(self, instance):
        return instance.get_order_methods_display()


class OpeningHoursSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpeningHours
        fields = ['weekday', 'from_hour', 'to_hour']


class LocationSerializer(serializers.ModelSerializer):
    hours = OpeningHoursSerializer(many=True)

    class Meta:
        model = Location
        fields = ['street_address', 'city', 'zipcode', 'phone_number', 'hours']


class RestaurantSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)
    order_methods = OrderMethodsSerializer(many=True)
    delivery_options = DeliveryOptionsSerializer(many=True)
    pickup_options = PickupOptionsSerializer(many=True)
    dietary_options = DietaryOptionsSerializer(many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['name', 'status', 'website_url', 'menu_url',
                  'locations', 'order_methods', 'delivery_options',
                  'pickup_options', 'dietary_options']

    def get_status(self, obj):
        return obj.get_status_display()