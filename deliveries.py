# This file handles delivery info and does the following:
# Aggregates the delivery info from csv_parser
# Passes that info to the greedy algorithm in distances.py (to optimize delivery route)
# Calculates total distance traveled by all three trucks
# Prints this info to the console

from csv_parser import *
from distances import *

import datetime
import distances

total_delivery_distance = 0

# Lists corresponding to each delivery object in the truck
first_delivery = []
second_delivery = []
third_delivery = []

# Lists of the distances for each delivery
first_truck_distance_list = []
second_truck_distance_list = []
third_truck_distance_list = []

# Times that each truck leaves the hub
first_time = '8:00:00'
second_time = '9:10:00'
third_time = '11:00:00'

# Convert the string time into a datetime.timedelta
(h, m, s) = first_time.split(':')
convert_first_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
(h, m, s) = second_time.split(':')
convert_second_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
(h, m, s) = third_time.split(':')
convert_third_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))


# Getter to retrieve the total distance traveled of all three trucks
def get_total_distance():
    return total_delivery_distance


# Method to handle/optimize each truck route (aggregates required info and passes that info to greedy algorithm)
def handle_delivery(truck_number):

    # Initialize global variables (will change based on passed-in truck_number)
    global package_list
    global truck_packages
    global truck_distances
    global optimized_truck_index_list
    global start_time
    global total_delivery_distance

    # Assign the global variables to their corresponding truck value
    if truck_number == 1:
        start_time = first_time
        package_list = get_first_truck_packages()
        truck_packages = first_delivery
        truck_distances = first_truck_distance_list
        optimized_truck_index_list = first_optimized_truck_index()
    elif truck_number == 2:
        start_time = second_time
        package_list = get_second_truck_packages()
        truck_packages = second_delivery
        truck_distances = second_truck_distance_list
        optimized_truck_index_list = second_optimized_truck_index()
    else:
        start_time = third_time
        package_list = get_first_truck_second_trip_packages()
        truck_packages = third_delivery
        truck_distances = third_truck_distance_list
        optimized_truck_index_list = third_optimized_truck_index()

    # Loop through the list of packages and assign the package's start time
    i = 0
    for val in package_list:
        package_list[i][8] = start_time
        truck_packages.append(package_list[i])
        i += 1

    # Loop through the packages list and address list to find the corresponding address location id
    try:
        count = 0
        for k in truck_packages:
            for j in get_addresses():
                if k[1] == j[2]:
                    truck_distances.append(j[0])
                    truck_packages[count][10] = j[0]
            count += 1
    except IndexError:
        pass

    # Pass the packages list to the greedy algorithm to optimize the delivery order
    calculate_shortest_distance(truck_packages, truck_number, 0)

    # Counter variable for following loop
    truck_package_id = 0

    # Loop through and populate the optimized list with the newly optimized order from above call to greedy algorithm
    for index in range(len(optimized_truck_index_list)):
        try:
            # Calculate the total distance of the truck
            global total_delivery_distance
            truck_distance = get_distance(int(optimized_truck_index_list[index]),
                                                        int(optimized_truck_index_list[index + 1]))
            total_delivery_distance = total_delivery_distance + truck_distance
            # Get the delivered or estimated delivery time and update it in the associated delivery object
            delivery_time = get_delivery_time(get_distance(int(optimized_truck_index_list[index]),
                                                                      int(optimized_truck_index_list[index + 1])),
                                               truck_number)
            optimized_truck_list(truck_number)[truck_package_id][9] = (str(delivery_time))
            get_hash_table().update(int(optimized_truck_list(truck_number)[truck_package_id][0]), truck_packages)
            truck_package_id += 1
        except IndexError:
            pass


# Call the handler function passing in each of the three trucks
handle_delivery(1)
handle_delivery(2)
handle_delivery(3)


# Method to print required delivery information
def print_delivery_info(index, comparison_time):
    # Convert the string times to datetime.timedelta
    try:
        start_time = get_hash_table().get(str(index))[8]
        delivered_time = get_hash_table().get(str(index))[9]
        (h, m, s) = start_time.split(':')
        converted_start_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        (h, m, s) = delivered_time.split(':')
        converted_delivered_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    except ValueError:
        pass
    # After string->time conversions, check packages against the input time to determine if they have left the hub yet
    if converted_start_time >= comparison_time:
        get_hash_table().get(str(index))[9] = 'At the Hub'
    elif converted_start_time <= comparison_time:
        # Then check to see which packages have left the hub but have not been delivered yet
        if comparison_time < converted_delivered_time:
            get_hash_table().get(str(index))[9] = 'En Route'
        # Then checks all packages that have already been delivered and displays the delivered time
        else:
            get_hash_table().get(str(index))[9] = 'Delivered at ' + delivered_time
    # Finally, print the delivery info for all packages
    print('ID:', get_hash_table().get(str(index))[0], '  Address:', get_hash_table().get(str(index))[1],
          '  City:', get_hash_table().get(str(index))[2] + ',', get_hash_table().get(str(index))[3],
          '  Zipcode:', get_hash_table().get(str(index))[4], '  Weight:', get_hash_table().get(str(index))[6] + ' lbs',
          '  Deadline:', get_hash_table().get(str(index))[5], '  Delivery Status:', get_hash_table().get(str(index))[9])
