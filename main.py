# Student_Name: Raphael Khan
# Student_ID: 001546693

from csv_parser import get_hash_table
from deliveries import get_total_distance, print_delivery_info
import datetime


class Main:
    def __init__(self):
        pass

    # Round the total mileage to tenth place and bold text
    total_mileage = '\033[1m' + "{0:.1f}".format(get_total_distance()) + ' miles.' + '\033[0m'

    # Welcome message and display total mileage
    print('Welcome to the WGUPS package finder!\n')
    print('Total Mileage Traveled: ', total_mileage + "\n")

    # User input: to view all delivery statuses at a certain time (timestamp) or get info for a single package (lookup)
    print("Please enter one of the following to view the package delivery statuses for the day:\n"
          "View All Deliveries - Enter 'all' to view all the of delivery statuses at the input time\n"
          "Individual Delivery - Enter 'one' to view the delivery status for a particular package\n")
    view = input("Delivery View (enter exit to close the program): ").strip().lower()

    while view != 'exit':
        # Timestamp view: User types in their time. Delivery statuses for all packages at that time will be displayed.
        if view == 'all':
            try:
                input_time = input('Please enter a time (HH:MM:SS): ')
                (h, m, s) = input_time.split(':')
                converted_input_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                for i in range(1, 41):
                    print_delivery_info(i, converted_input_time)
            except IndexError:
                print(IndexError)
                exit()
        # Search view: User is asked to enter a package id followed by a timestamp. The delivery info is then displayed.
        elif view == 'one':
            try:
                i = input('Package ID: ')
                if int(i) < 1 or int(i) > 40:
                    print('That package ID does not exist. Please choose a value between 1 and 40')
                    i = input('Package ID: ')
                input_time = input('Please enter a time (HH:MM:SS): ')
                (h, m, s) = input_time.split(':')
                converted_input_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                print_delivery_info(i, converted_input_time)
            except ValueError as e:
                print(e)
                print('Please enter a valid input (all or one)')
                exit()
        elif view == 'exit':
            exit()
        else:
            print('Please enter a valid input (all or one)')
            view = input("\nDelivery View (enter exit to close the program): ").strip().lower()





