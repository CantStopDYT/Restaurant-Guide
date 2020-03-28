from restaurants.models import *
import csv


def load_airtable(file_path='setup/data/Main View.csv'):
    status_map = {status.label: status.value for status in Restaurant.StatusOptions}
    order_methods_map = {om.label: om.value for om in OrderMethods.OrderMethods}
    delivery_methods_map = {dm.label: dm.value for dm in DeliveryOptions.DeliveryMethods}

    with open(file_path, encoding='utf-8-sig') as csvfile:
        #reader = csv.reader(csvfile)
        reader = csv.DictReader(csvfile)
        for entry in reader:
            print(entry)

            # create entry for restaurant
            restaurant = Restauant.objects.create(
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
            Location.objects.create(
                street_address=entry['Street Address'],
                city=entry['City'],
                zipcode=entry['Zip'],
                #phone_number= #TODO
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

            # create associated delivery options
            if entry['How To Order'] != '':
                options = entry['How To Order'].split(',')
                for option in options:
                    DeliveryOptions.objects.create(
                        delivery_options=option,
                        restaurant=restaurant
                    )

            # create associated delivery options
            if entry['Delivery Options'] != '':
                options = entry['Delivery Options'].split(',')
                for option in options:
                    DeliveryOptions.objects.create(
                        delivery_options=option,
                        restaurant=restaurant
                    )