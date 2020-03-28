from django.contrib import admin
from restaurants.models import *

admin.site.register(Restaurant)
admin.site.register(Location)
admin.site.register(OpeningHours)
admin.site.register(OrderMethods)
admin.site.register(DeliveryOptions)
admin.site.register(PickupOptions)
admin.site.register(DietaryOptions)