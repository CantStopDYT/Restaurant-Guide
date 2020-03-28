from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class Restauant(models.Model):
    create = models.DateTimeField(auto_now_add=True)
    #region = models.CharField(max_length=128, blank=True)

    # status
    name = models.CharField(max_length=128)
    STATUS_OPTIONS = [
        ('O', _('Regular Hours')),
        ('L', _('Limited Hours')),
        ('C', _('Temporarily Closed')),
    ]
    status = models.CharField(max_length=1, choices=STATUS_OPTIONS)

    # online information
    website_url = models.CharField(max_length=64, blank=True, null=True)
    limited_menu = models.BooleanField(blank=True)
    menu_url = models.CharField(max_length=64, blank=True, null=True)
    email_address = models.CharField(max_length=64, blank=True, null=True)
    accepting_future_orders = models.BooleanField(blank=True)
    selling_gift_cards = models.BooleanField(blank=True)


class Location(models.Model):
    # address
    street_address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=32, blank=True)
    zipcode = models.PositiveSmallIntegerField(blank=True)
    phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Phone number must be entered in the format: '9371234567'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=17, validators=[phone_regex], blank=True)
    restaurant = models.ForeignKey('Restauant', on_delete=models.CASCADE)


class OpeningHours(models.Model):
    WEEKDAYS = [
      (1, _("Monday")),
      (2, _("Tuesday")),
      (3, _("Wednesday")),
      (4, _("Thursday")),
      (5, _("Friday")),
      (6, _("Saturday")),
      (7, _("Sunday")),
    ]
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    address = models.ForeignKey('Location', on_delete=models.CASCADE)

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __str__(self):
        self.get
        return '%s: %s - %s'.format(self.get_weekday_display(), self.from_hour, self.to_hour)


class OrderMethods(models.Model):
    ORDER_METHODS = [
        ('C', _('Direct Call')),
        ('A', _('Delivery Apps')),
        ('W', _('Website')),
        ('O', _('Other')),
    ]
    order_methods = models.CharField(max_length=1, choices=ORDER_METHODS, blank=True)
    restaurant = models.ForeignKey('Restauant', on_delete=models.CASCADE)


class DeliveryOptions(models.Model):
    DELIVERY_OPTIONS = [
        ('DR', _('Direct from Restaurant')),
        ('GH', _('GrubHub')),
        ('PM', _('Postmates')),
        ('DD', _('Door Dash')),
        ('UE', _('Uber Eats')),
        ('SL', _('Seamless')),
        ('OT', _('Other')),
    ]
    None
    delivery_options = models.CharField(max_length=2, choices=DELIVERY_OPTIONS, blank=True)
    restaurant = models.ForeignKey('Restauant', on_delete=models.CASCADE)


class PickupOptions(models.Model):
    PICKUP_OPTIONS = [
        ('CO', _('Carry Out')),
        ('CS', _('Curbside')),
    ]
    pickup_options = models.CharField(max_length=2, choices=PICKUP_OPTIONS, blank=True)
    restaurant = models.ForeignKey('Restauant', on_delete=models.CASCADE)


class DietaryOptions(models.Model):
    DIET_OPTIONS = [
        ('VT', ('Vegetarian')),
        ('VG', ('Vegan')),
        ('PF', ('Peanut Free')),
        ('DF', ('Dairy Free')),
        ('SF', ('Soy Free')),
        ('GF', ('Gluten Free')),
        ('OT', ('Other')),
    ]
    dietary_options = models.CharField(max_length=2, choices=DIET_OPTIONS, blank=True)
    restaurant = models.ForeignKey('Restauant', on_delete=models.CASCADE)