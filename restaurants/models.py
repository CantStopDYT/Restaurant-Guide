from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class Restaurant(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    #region = models.CharField(max_length=128, blank=True)

    # status
    name = models.CharField(max_length=128)

    class StatusOptions(models.TextChoices):
        REGULAR_HOURS = 'O', _('Regular Hours')
        LIMITED_HOURS = 'L', _('Limited Hours')
        TEMPORARILY_CLOSED = 'C', _('Temporarily Closed')
    status = models.CharField(max_length=1, choices=StatusOptions.choices)

    # online information
    website_url = models.CharField(max_length=64, blank=True, null=True)
    limited_menu = models.BooleanField(blank=True, null=True)
    menu_url = models.CharField(max_length=64, blank=True, null=True)
    email_address = models.CharField(max_length=64, blank=True, null=True)
    accepting_future_orders = models.BooleanField(blank=True, null=True)
    selling_gift_cards = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    # address
    street_address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=32, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Phone number must be entered in the format: '9371234567'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=17, validators=[phone_regex], blank=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return self.restaurant.name


class OpeningHours(models.Model):

    class Weekday(models.TextChoices):
        MONDAY = 1, _('Monday')
        TUESDAY = 2, _('Tuesday')
        WEDNESDAY = 3, _('Wednesday')
        THURSDAY = 4, _('Thursday')
        FRIDAY = 5, _('Friday')
        SATURDAY = 6, _('Saturday')
        SUNDAY = 7, _('Sunday')
    weekday = models.IntegerField(choices=Weekday.choices)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='hours')

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __str__(self):
        self.get
        return '%s: %s - %s'.format(self.get_weekday_display(), self.from_hour, self.to_hour)


class OrderMethods(models.Model):

    class OrderMethods(models.TextChoices):
        CALL = 'C', _('Direct Call')
        APPS = 'A', _('Delivery Apps')
        WEBSITE = 'W', _('Website')
        OTHER = 'O', _('Other')
    order_methods = models.CharField(max_length=1, choices=OrderMethods.choices, blank=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='order_methods')

    def __str__(self):
        return '{} for {}'.format(self.OrderMethods(self.order_methods).label, self.restaurant)


class DeliveryOptions(models.Model):

    class DeliveryMethods(models.TextChoices):
        DIRECT = 'DR', _('Direct from Restaurant')
        GRUBHUB = 'GH', _('GrubHub')
        POSTMATES = 'PM', _('Postmates')
        DOOR_DASH = 'DD', _('Door Dash')
        UBER_EATS = 'UE', _('Uber Eats')
        SEAMLESS = 'SL', _('Seamless')
        OTHER = 'OT', _('Other')
    delivery_options = models.CharField(max_length=2, choices=DeliveryMethods.choices, blank=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='delivery_options')

    def __str__(self):
        return '{} for {}'.format(self.DeliveryMethods(self.delivery_options).label, self.restaurant)


class PickupOptions(models.Model):

    class PickupOptions(models.TextChoices):
        CARRY_OUT = 'CO', _('Carry Out')
        CURBSIDE = 'CS', _('Curbside')
    pickup_options = models.CharField(max_length=2, choices=PickupOptions.choices, blank=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='pickup_options')


class DietaryOptions(models.Model):

    class DietaryOptions(models.TextChoices):
        DIRECT = 'VT', _('Vegetarian')
        GRUBHUB = 'VG', _('Vegan')
        POSTMATES = 'PF', _('Peanut Free')
        DOOR_DASH = 'DF', _('Dairy Free')
        UBER_EATS = 'SF', _('Soy Free')
        SEAMLESS = 'GF', _('Gluten Free')
        OTHER = 'OT', _('Other')
    dietary_options = models.CharField(max_length=2, choices=DietaryOptions.choices, blank=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='dietary_options')

    def __str__(self):
        return '{} for {}'.format(self.DietaryOptions(self.dietary_options).label, self.restaurant)