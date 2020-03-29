from restaurants.models import *
import csv
import re
import collections
import datetime


# parses time for the regular expression: [:0-9]+[ ]?[aApP][mM]
def parse_time(time_str):
    # if no minutes are found
    if time_str.find(':') == -1:
        hour, suffix = re.search('([0-9]+)[ ]?([aApP][mM])', time_str, re.IGNORECASE).groups()
        return datetime.datetime.strptime('{}:00 {}'.format(hour, suffix), "%I:%M %p")
    else:
        hour, minute, suffix = re.search('([0-9]+):([0-9]+)[ ]?([aApP][mM])', time_str, re.IGNORECASE).groups()
        return datetime.datetime.strptime('{}:{} {}'.format(hour, minute, suffix), "%I:%M %p")


def load_airtable(file_path='setup/data/Main View.csv'):
    # build a circular buffer to iterate through the days as some day ranges loop over the start of the week
    d = collections.deque(maxlen=7)
    for day in ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']:
        d.append(day)

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

            # set default state to Ohio
            state = 'OH'

            loc = Location.objects.create(
                street_address=entry['Street Address'],
                city=entry['City'],
                state=state,
                zipcode=entry['Zip'],
                phone_number=phone_number,
                restaurant=restaurant,
            )

            #TODO: Hours
            ##### START HOURS
            # catch when ranges are provided
            re_hours = re.finditer('([A-Za-z]{3,}day)-([A-Za-z]{3,}day)[ ]?([:0-9]+[ ]?[aApP][mM])-([:0-9]+[ ]?[aApP][mM])', entry['Hours of Operation'], re.IGNORECASE)
            for hours in re_hours:
                (start_day, end_day, start_hours, end_hours) = hours.groups()

                start_time = parse_time(start_hours)
                end_time = parse_time(end_hours)

                start_day = start_day.upper()
                end_day = end_day.upper()
                start_idx = d.index(start_day)
                while d[start_idx] != end_day:
                    OpeningHours.objects.create(
                        weekday=OpeningHours.Weekday[d[start_idx]],
                        from_hour=start_time,
                        to_hour=end_time,
                        location=loc
                    )
                    d.rotate(-1)
                OpeningHours.objects.create(
                    weekday=OpeningHours.Weekday[d[start_idx]],
                    from_hour=start_time,
                    to_hour=end_time,
                    location=loc
                )


            # catch when a single day is provided
            re_hours = re.finditer('[^-]([A-Z][a-z]+day)[ ]?([:0-9]+[ ]?[aApP][mM])-([:0-9]+[ ]?[aApP][mM])', entry['Hours of Operation'])
            for hours in re_hours:
                (day, start_hours, end_hours) = hours.groups()

                start_time = parse_time(start_hours)
                end_time = parse_time(end_hours)

                day = day.upper()
                OpeningHours.objects.create(
                    weekday=OpeningHours.Weekday[day],
                    from_hour=start_time,
                    to_hour=end_time,
                    location=loc
                )


            # catch when no days are provided
            re_hours = re.finditer('^([:0-9]+[ ]?[aApP][mM])-([:0-9]+[ ]?[aApP][mM])', entry['Hours of Operation'], re.IGNORECASE)
            for hours in re_hours:
                (start_hours, end_hours) = hours.groups()

                start_time = parse_time(start_hours)
                end_time = parse_time(end_hours)

                for day in d:
                    OpeningHours.objects.create(
                        weekday=OpeningHours.Weekday[day],
                        from_hour=start_time,
                        to_hour=end_time,
                        location=loc
                    )
            ##### END HOURS

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