from restaurants.models import *
import csv
import re


def load_airtable(file_path='setup/data/Main View.csv'):
    status_map = {status.label: status.value for status in Restaurant.StatusOptions}
    order_methods_map = {om.label: om.value for om in OrderMethods.OrderMethods}
    delivery_methods_map = {dm.label: dm.value for dm in DeliveryOptions.DeliveryMethods}
    pickup_options_map = {po.label: po.value for po in PickupOptions.PickupOptions}
    dietery_options_map = {do.label: do.value for do in DietaryOptions.DietaryOptions}

    with open(file_path, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for entry in reader:
            print(entry)

            # create entry for restaurant
            restaurant = Restaurant.objects.create(
                name=entry['Business Name'],
                status=status_map[entry['Status']],
                website_url=entry['Website'],
                #limited_menu=,
                menu_url=entry['Menu'],
                #email_address=,
                #accepting_future_orders=,
                selling_gift_cards=entry['Selling Gift Cards?']!=''
            )

            # create entry for each restaurant location
            re_phone_number = re.search('[(]([0-9]{3})[)]\s?([0-9]{3})-([0-9]{4})', entry['Phone Number'], re.IGNORECASE)
            phone_number = '{}{}{}'.format(re_phone_number.group(1),re_phone_number.group(2),re_phone_number.group(3))
            Location.objects.create(
                street_address=entry['Street Address'],
                city=entry['City'],
                zipcode=entry['Zip'],
                phone_number=phone_number,
                restaurant=restaurant,
            )

            #TODO: Hours
            """
            OpeningHours.objects.create(
                weekday=,
                from_hour=,
                to_hour=,
            )
            """

            # create associated ordering options
            if entry['How To Order'] != '':
                options = entry['How To Order'].split(',')
                for option in options:
                    option = option.replace(' (details below)', '').strip()
                    OrderMethods.objects.create(
                        order_methods=order_methods_map[option],
                        restaurant=restaurant
                    )

            # create associated delivery options
            if entry['Delivery Options'] != '':
                options = entry['Delivery Options'].split(',')
                for option in options:
                    option = option.strip()
                    DeliveryOptions.objects.create(
                        delivery_options=delivery_methods_map[option],
                        restaurant=restaurant
                    )

            # create associated pickup options
            if entry['Pickup Options'] != '':
                options = entry['Pickup Options'].split(',')
                for option in options:
                    option = option.strip()
                    PickupOptions.objects.create(
                        pickup_options=pickup_options_map[option],
                        restaurant=restaurant
                    )

            # create associated dietary options
            if entry['Dietary Accommodations'] != '':
                options = entry['Dietary Accommodations'].split(',')
                for option in options:
                    option = option.strip()
                    DietaryOptions.objects.create(
                        dietary_options=dietery_options_map[option],
                        restaurant=restaurant
                    )