'''
Created on Mar 6, 2016
Python 3.4
@author: Miguel
'''
import time_functions,sys,bus
import admin    #import admin after database initiation, otherwise
                #admin will try to find db without being created yet               
from init import db_setup,login
from sqlite3 import DatabaseError
from processor import log_info,scrub
def menu():
    print("******************************MENU******************************* ")
    print("* OPTIONS:                                                      * ")
    print("*  0 - Admin Panel              7 - Export the data             * ")
    print("*  1 - Add a record             8 - List columns                * ")         
    print("*  2 - Show a record                                            * ")
    print("*  3 - List clients             10 - List all client sessions   * ")
    print("*  4 - Print a record's sum     11 - Update constants           * ")
    print("*  5 - Update a record          12 - List all clients           * ")
    print("*                                                               * ")
    print("====================100 - Exit the program======================= ")
    option = input("[?] Choose an option #: ")
    accepted_responses = (0,1,2,3,4,5)
    try:
        int(option)
    except:
        log_info(2, "DETECTED STRING AS AN OPTION", sys.exc_info(),False)
        print("[!] Invalid Option")
        return
    if int(option) not in accepted_responses:
        log_info(2, "INVALID OPTION '{opt}'".format(opt=option), sys.exc_info(),False)
        print("[!] Invalid Option")
    else:
        controller(scrub(int(option)))
        

def controller(option):
    if option == 0:
        bus.option_0()
    if option == 1:
        print("""[i] Record Types:
                    client   session   admin""")
        record_type = input("[?] Enter the type of record to add: ")
        bus.option_1(scrub(record_type))
    if option == 2:
        print("""[i] Record Types:
                    client   session""")
        record_type = input("[?] Enter the type of record to view: ")
        bus.option_2(scrub(record_type))
    if option == 3:
        bus.option_3()
    if option == 4:
        print("""[i] Record Types:
                    client   session""")
        record_type = input("[?] Enter the record to summarize: ")
        bus.option_4(scrub(record_type))
    if option == 5:
        print("""[i] Record Types:
                    client   session""")
        record_type = input("[?] Enter the record to update: ")
        bus.option_5(scrub(record_type))
    if option == 100:
        print("[!] Escape sequence detected")
        bus.option_100()
if __name__ == '__main__':
#Setup tables
    try:
        db_setup()
    except DatabaseError:
        print("""[!] ERROR - POSSIBLE REASONS:
                1. You entered a duplicate file name
                2. The existing file is not an sqlite3 database
                3. The existing file is corrupt""")
        print("[i] Delete the file or consult an administrator")
        log_info(str(sys.exc_info()),'db_setup()')
        exit(0)

    login()
#    prompts = admin.format_cols_for_db(db_functions.get_columns('clients'),'query')
#    print(prompts)

    while True:
        menu()