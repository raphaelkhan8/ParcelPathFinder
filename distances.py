# This file handles distances between each delivery point and does the following:
# aggregate distance and destination info by parsing their respective csv files
# contains the greedy algorithm (calculate_shortest_path) to find the optimal route for deliveries

import csv
import datetime

# Read in csv file that is the mapping of distances between locations
with open('Distances.csv') as dist_f:
    distCSV = csv.reader(dist_f, delimiter=',')
    distCSV = list(distCSV)

# Read in csv file that is the names of all possible delivery locations
with open('Destinations.csv') as destination_f:
    destinationCSV = csv.reader(destination_f, delimiter=',')
    destinationCSV = list(destinationCSV)

    # Method that calculates the distance between two locations
    # Time Complexity: Constant or O(1) - the passed-in indexes allows for constant retrieval time
    # Space Complexity: Constant or O(1) - will always create the same number of variables and return 1 float value
    def get_distance(row_value, column_value):
        distance = distCSV[row_value][column_value]
        if distance == '':
            distance = distCSV[column_value][row_value]
        return float(distance)

    # Lists corresponding to the time trucks leave the hub
    first_time_list = ['8:00:00']
    second_time_list = ['9:10:00']
    third_time_list = ['11:00:00']

    # Method that gets the time it takes to make a delivery (trucks travel at a constant 18 mph)
    # Time Complexity: Linear or O(N) - looping though the time list results in a worst-case scenario of linear time
    # Space Complexity: Constant or O(1) - will always create the same number of variables and return one value
    def get_delivery_time(distance, truck_number):
        # Divide passed-in distance by speed (18 mph) and convert to a string timestamp
        new_time = distance / 18
        distance_in_minutes = '{0:02.0f}:{1:02.0f}'.format(*divmod(new_time * 60, 60))
        final_time = distance_in_minutes + ':00'
        # Convert the string timestamp to datetime.timedelta and add it to it's associated truck time list
        if truck_number == 1:
            first_time_list.append(final_time)
            sum = datetime.timedelta()
            for i in first_time_list:
                (h, m, s) = i.split(':')
                d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                sum += d
            return sum
        elif truck_number == 2:
            second_time_list.append(final_time)
            sum = datetime.timedelta()
            for i in second_time_list:
                (h, m, s) = i.split(':')
                d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                sum += d
            return sum
        else:
            third_time_list.append(final_time)
            sum = datetime.timedelta()
            for i in third_time_list:
                (h, m, s) = i.split(':')
                d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                sum += d
            return sum

    # Getter to retrieve the destination lists
    def get_addresses():
        return destinationCSV

    # Container lists that correspond to the sorted trucks returned from the greedy algorithm
    first_optimized_truck = []
    first_optimized_truck_index_list = []
    second_optimized_truck = []
    second_optimized_truck_index_list = []
    third_optimized_truck = []
    third_optimized_truck_index_list = []

    # Insert initializing tuples in the optimized index list
    first_optimized_truck_index_list.insert(0, '0')
    second_optimized_truck_index_list.insert(0, '0')
    third_optimized_truck_index_list.insert(0, '0')

    # Getters to retrieve the optimized list of distances
    def first_optimized_truck_index():
        return first_optimized_truck_index_list

    def second_optimized_truck_index():
        return second_optimized_truck_index_list

    def third_optimized_truck_index():
        return third_optimized_truck_index_list

    # Getters to retrieve the optimized list of deliveries
    # Time Complexity: Constant or O(1) - the list corresponding to the passed-in truck is retrieved almost immediately
    # Space Complexity: Linear or O(N) - returns a new list that grows at a linear rate as the number of deliveries grow
    def first_optimized_truck_list():
        return first_optimized_truck

    def second_optimized_truck_list():
        return second_optimized_truck

    def third_optimized_truck_list():
        return third_optimized_truck

    # Getter to retrieve the optimized delivery list corresponding to the passed-in truck number
    # Time Complexity: Constant or O(1) - the list corresponding to the passed-in truck is retrieved almost immediately
    # Space Complexity: Linear or O(N) - returns a new list that grows at a linear rate as the number of deliveries grow
    def optimized_truck_list(truck_number):
        if truck_number == 1:
            return first_optimized_truck
        elif truck_number == 2:
            return second_optimized_truck
        else:
            return third_optimized_truck

    # The following method is my greedy algorithm used to optimize the delivery route for each truck
    # Time Complexity: Quadratic or O(N^2) - the items traversed grows at a quadratic rate due to two for loops
    # Space Complexity: Quadratic or O(N^2) - the variables created grow at a quadratic rate due to two for loops
    def calculate_shortest_distance(truck_distance_list, truck_number, current_location):
        # Base case: stop recursive calls and return final value once input list's is empty
        if len(truck_distance_list) == 0:
            return truck_distance_list
        # While the input list in not empty:
        else:
            try:
                shortest_distance = 100.0
                # Initialize a location variable (this will correspond to the new shortest distance package)
                new_location = 0
                # Loop through the entire distance list and find the shortest distance
                for index in truck_distance_list:
                    if get_distance(current_location, int(index[10])) <= shortest_distance:
                        shortest_distance = get_distance(current_location, int(index[10]))  # section 3
                        new_location = int(index[10])
                # Add the delivery object corresponding to the shortest distance index to its associated truck
                # Then, pop off the just added value from the original passed-in list and recursively repeat the
                # process until the base case is hit
                for index in truck_distance_list:  # section 4
                    if get_distance(current_location, int(index[10])) == shortest_distance:
                        if truck_number == 1:
                            first_optimized_truck.append(index)
                            first_optimized_truck_index_list.append(index[10])
                            pop_value = truck_distance_list.index(index)
                            truck_distance_list.pop(pop_value)
                            current_location = new_location
                            calculate_shortest_distance(truck_distance_list, 1, current_location)
                        elif truck_number == 2:
                            second_optimized_truck.append(index)
                            second_optimized_truck_index_list.append(index[10])
                            pop_value = truck_distance_list.index(index)
                            truck_distance_list.pop(pop_value)
                            current_location = new_location
                            calculate_shortest_distance(truck_distance_list, 2, current_location)
                        elif truck_number == 3:
                            third_optimized_truck.append(index)
                            third_optimized_truck_index_list.append(index[10])
                            pop_value = truck_distance_list.index(index)
                            truck_distance_list.pop(pop_value)
                            current_location = new_location
                            calculate_shortest_distance(truck_distance_list, 3, current_location)
            except IndexError:
                pass




