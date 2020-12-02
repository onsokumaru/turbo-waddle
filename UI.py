from database import *
import sqlite3

# create database, connection, and cursor
conn = sqlite3.connect('appDB.db')
c = conn.cursor()

# --- text based user interface for project --- #
# --- SWITCH CASE FUNCTIONS --- #


# --- Main Menu switch case --- #
def main_switch():
    print("""
    1) Create Service Request
    2) Query Service Requests
    3) Exit this Program
    """)
    try:
        option = int(input("Please enter your option : "))
    except ValueError:
        print("Invalid input provided... exiting")
        #exit(1)
    else:
        # based on option chosen take the appropriate action
        if option == 1:
            request_menu()
        elif option == 2:
            query_switch()
        elif option == 3:
            exit_program()
        else:
            print("Invalid option entered.... exiting.")
            #exit(1)


# --- Request Menu switch case --- #
def request_switch():
    print("--- Please choose from the options below ---")
    print("""
    1) Create a New Service Request
    2) Back to Main Menu
    3) Exit this Program
    """)
    try:
        option = int(input("Please enter your option : "))
    except ValueError:
        print("Invalid input provided... exiting")
        #exit(1)
    else:
        # based on option chosen take the appropriate action
        keep_going = True
        if option == 1:
            create_new_request()
            # while(keep_going):
            #     keep_going = create_new_request()
        elif option == 2:
            main_menu()
        elif option == 3:
            exit_program()
        else:
            print("Invalid option entered.... exiting.")
            #exit(1)


# --- Query Menu switch case --- #
def query_switch():
    print("--- Please choose from the options below ---")
    print("""
    1) Display Open Service Tickets by Technician
    2) Display Closed Service Tickets by Technician
    3) Back to Main Menu
    4) Exit this Program
    """)
    try:
        option = int(input("Please enter your option : "))
    except ValueError:
        print("Invalid input provided... exiting")
        #exit(1)
    else:
        # based on option chosen take the appropriate action
        if option == 1:
            display_open_requests(c)
        elif option == 2:
            display_closed_requests(c)
        elif option == 3:
            main_menu()
        elif option == 4:
            exit_program()
        else:
            print("Invalid option entered.... exiting.")
            exit(1)

# --- MENU FUNCTIONS --- #
# --- Main Menu --- #
def main_menu():
    print("""
    #================================#
    # WELCOME TO THE SERVICE REQUEST #
    #       TRACKING SYSTEM          #
    #================================#
    
    * Please choose from the one of the
    options below.
    """)
    main_switch()


# --- Request Menu --- #
def request_menu():
    print("""
    *** CREATE A NEW SERVICE REQUEST MENU ***
    """)
    request_switch()


# --- MAIN MENU FUNCTIONS --- #
# --- create_new_request --- #
def create_new_request():
    create_another_request = False
    try:
        emp_first_name = input("Please enter your first name : ")
        emp_last_name = input("Please enter your last name : ")
        emp_dept = input("Please enter your department [ Accounting, Admin, HR, IT, Marketing, Sales ] : ")
        request_desc = input("Please enter a brief description of your service request : ")
    except ValueError:
        print("Invalid input provided... exiting")
        exit(1)
    else:
        print(" ")
        print("Creating requests... ")
        # function provided by the database.py module
        create_request(c, conn, emp_last_name, emp_first_name, emp_dept, request_desc)
        print("---Service Request Created.---")
        print("A technician will contact you shortly.")
        print()
        try:
            new_request = input("Would you like to create another request[Y/N]?: ")
        except ValueError:
            print("Invalid input provided... exiting")
            #exit(1)
        else:
            # based on option chosen take the appropriate action
            if new_request.upper() == 'Y':
                create_new_request()
            elif new_request.upper() == 'N':
                main_menu()
            else:
                print("Invalid option entered.... exiting.")
                #exit(1)


# the functions to query the database and display the output are provided by the database.py module
def display_open_requests(cursor):
    display_something_else = False  # variable to determine whether user wants to perform another action
    format_query_results(fetch_open_requests(c))
    print()
    try:
        display_something_else = input("Would you like to display something else[Y/N]?: ")
    except ValueError:
        print("Invalid input provided... exiting")
        #exit(1)
    else:
        # based on option chosen take the appropriate action
        if display_something_else.upper() == 'Y':
            query_switch()
        elif display_something_else.upper() == 'N':
            main_menu()
        else:
            print("Invalid option entered.... exiting.")
            #exit(1)


def display_closed_requests(cursor):
    display_something_else = False  # variable to determine whether user wants to perform another action
    format_query_results(fetch_closed_requests(c))
    print()
    try:
        display_something_else = input("Would you like to display something else[Y/N]?: ")
    except ValueError:
        print("Invalid input provided... exiting")
        #exit(1)
    else:
        # based on option chosen take the appropriate action
        if display_something_else.upper() == 'Y':
            query_switch()
        elif display_something_else.upper() == 'N':
            main_menu()
        else:
            print("Invalid option entered.... exiting.")
            #exit(1)


def format_query_results(results):
    print("=" * 101)
    print("%-15s\t%-15s\t%-15s\t%-30s\t%-15s\t%-15s" % ("TECH L NAME", "TECH F NAME", "REQUEST DATE", "DESCRIPTION", "COMPLETE DATE", "NOTES"))
    print("=" * 101)
    for i in results:
        print("%-15s\t%-15s\t%-15s\t%-30s\t%-15s\t%-15s" % (i[0], i[1], i[2], i[3], i[4], i[5]))


# exit program
def exit_program():
    clear_database(c, conn) 
    print("Program Exiting ... ")
    print()
    print("Goodbye ^_^ ")
    #exit(0)
