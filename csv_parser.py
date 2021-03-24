# This file parses the DeliveryInfo csv file to do the following:
# extract each individual delivery (row),
# convert each row into a delivery object,
# load the delivery objects onto their associated truck for delivery
# add the delivery object and it's unique key (tuple) to the hash table

import csv
from hashtable import HashTable

# parse the deliveries csv file (separating by comma)
with open('DeliveryInfo.csv') as f:
    readCSV = csv.reader(f, delimiter=',')

    # instantiate a Hash Table object
    insert_into_hash_table = HashTable()
    # create lists to hold the delivery items for each truck
    first_truck = []
    second_truck = []
    first_truck_second_trip = []

    # Loop through the parsed delivery data and create key/value pairs
    for row in readCSV:
        package_ID = row[0]
        address = row[1]
        city = row[2]
        state = row[3]
        zipcode = row[4]
        deadline = row[5]
        weight = row[6]
        delivery_note = row[7]
        delivery_status = ''
        delivery_start = ''
        address_location = ''
        delivery_info = [package_ID, address, city, state, zipcode, deadline, weight, delivery_note, delivery_start,
                         delivery_status, address_location]

        key = package_ID
        value = delivery_info

        # Conditionals to determine which packages are loaded onto which truck:

        # First truck: packages that have an earlier deadline (not EOD) and/or must be delivered together (Must)
        if value[5] != 'EOD':
            if 'Must' in value[7] or 'None' in value[7]:
                first_truck.append(value)
        # Second truck: packages with Delayed note or EOD deadline
        if 'Can only be' in value[7]:
            second_truck.append(value)
        if 'Delayed' in value[7]:
            second_truck.append(value)
        if 'East #104' in value[1]:
            second_truck.append(value)
        # Fix the wrong address package and add it to the first truck (second trip)
        if '84104' in value[4] and '10:30' not in value[5]:
            first_truck_second_trip.append(value)
        if 'Wrong address listed' in value[7]:
            value[1] = '410 S State St'
            value[4] = '84111'
            first_truck_second_trip.append(value)
        # Add any remaining packages to whichever truck has less packages (second truck or first truck (second trip))
        if value not in first_truck and value not in second_truck and value not in first_truck_second_trip:
            if len(second_truck) > len(first_truck_second_trip):
                first_truck_second_trip.append(value)
            else:
                second_truck.append(value)
        insert_into_hash_table.insert(key, value)

    # Getter to retrieve the full list of values at start of day
    def get_hash_table():
        return insert_into_hash_table

    # Getter to retrieve a list of the packages on the first truck
    def get_first_truck_packages():
        return first_truck

    # Getter to retrieve a list of the packages on the second truck
    def get_second_truck_packages():
        return second_truck

    # Getter to retrieve a list of the packages on the first truck (second trip)
    def get_first_truck_second_trip_packages():
        return first_truck_second_trip



