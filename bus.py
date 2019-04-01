'''
Created on Mar 19, 2016
Python 3.4
@author: Miguel
'''
import dbqueries as dbq
import processor as proc
from menu import controller
from init import init_table_col_names
from processor import get_client_id, log_info, scrub

def option_0():
    return

def option_1(record_type):
    tablename = record_type
    accepted_responses = ('client','session','admin')
    while record_type not in accepted_responses:    
    #Handle an unrecognized option
        print("[!] ",record_type,"is not an invalid option...")
        return controller(1)   
    client_id = proc.get_client_id()
#    record_exists = dbq.record_exists('client','client_id', client_id)
    if record_type == 'client':
        while dbq.record_exists('client','client_id', client_id):
        #print error if client already exists
            print("[!] Client {id} already exists".format(id=client_id))
        #Get a new client id
            client_id = proc.get_client_id()
        #After a new ID is given, start interated thru the col names and prompt for values
        query,values = proc.automate_INSERT(tablename, client_id)   #return the formatted query and values parameters
        dbq.add_record(tablename, query, values)    #Add the record into the table
        tablename = proc.convert_client_to_sessiontable(client_id)  #now shift to creating the client-session table
        while not dbq.check_table(tablename):
            tablename = proc.convert_client_to_sessiontable(client_id)
            col_names = init_table_col_names('session')
            try:
                dbq.create_table(tablename, col_names)  #Create the client-session table
            except:
                pass
    if record_type == 'session':
        while not dbq.record_exists('client','client_id', client_id):
        #print error if client already exists
            print("[!] Client {id} does not exists".format(id=client_id))
            client_id = proc.get_client_id()
        #convert tablename into a session tablename
        tablename = proc.convert_client_to_sessiontable(client_id)
        while not dbq.check_table(tablename):
        #Handle an existing client record with no session table
            print("[!] Oops, something happened. Attempting to fix...")
            col_names = init_table_col_names('session')
            dbq.create_table(tablename, col_names)       
        query,values = proc.automate_INSERT(tablename, client_id)
        dbq.add_record(tablename, query, values)    #Add the record into the table     
    return

def option_2(record_type):
    accepted_responses = ('client','session')
    while record_type not in accepted_responses:    
    #Handle an unrecognized option
        print("[!] ",record_type,"is not an invalid option...")
        return controller(2)
    client_id = get_client_id()
    while not proc.clientexists(client_id):
    #check if the client exists, if does not exists, prompt again
        print("[!] Client {id} does not exists".format(id=client_id))
        client_id = get_client_id()
    if record_type == 'client':
        tablename = 'client'
        uniq_id_name = 'client_id'
        id_value = client_id      
    elif record_type == 'session':
        tablename = proc.convert_client_to_sessiontable(client_id)
        proc.format_cols_to_choices(3, tablename)
        print("ALL")
        uniq_id_name = ''
        col_names = proc.format_cols_in_list(tablename)
        while uniq_id_name not in col_names:
        #The below functions convert an input response (selecting a choice that outputs from string_mod)
        #back into db format
            uniq_id_name = scrub(proc.reverse_string_mod(input("[!] Enter look up identifier: ")))
            if uniq_id_name == "all":
                proc.automate_data_recall_output(tablename,"ALL","ALL")
                return
            
            elif uniq_id_name not in col_names and uniq_id_name != "all":
#                print("Chose: ",uniq_id_name)
                print("[!] Invalid Option")
        id_value = input("[?] Enter {id} value: ".format(id=proc.string_mod(uniq_id_name)))       
    proc.automate_data_recall_output(tablename,uniq_id_name,id_value)
    return

def option_3():
#    clients = dbq.list_records('client_id', 'client')    
    proc.list_clients(dbq.show_table('client'))
    return

def option_4(record_type):
    accepted_responses = ('client','session')
    while record_type not in accepted_responses:    
    #Handle an unrecognized option
        print("[!] ",record_type,"is not an invalid option...")
        return controller(2)
    if record_type == 'client':
        tablename = record_type
        total = dbq.count_records(tablename)[0]
    if record_type == 'session':
        client_id = proc.get_client_id()
        tablename = proc.convert_client_to_sessiontable(client_id)
        total = dbq.count_records(tablename)[0]
    if int(total) > 1:
        print("[i] There are {tn} {rt}s".format(tn=total,rt=record_type))
    else:
        print("[i] There is {tn} {rt}".format(tn=total,rt=record_type))
    return

def option_5(record_type):
    accepted_responses = ('client','session')
    while record_type not in accepted_responses:    
    #Handle an unrecognized option
        print("[!] ",record_type,"is not an acceptable option...")
        return controller(5)
    client_id = get_client_id()
    
    while not dbq.record_exists('client','client_id', client_id):
    #if the client does not exist, get a new client id
        print("[!] Client {id} does not exists".format(id=client_id))
        client_id = get_client_id()
        
    if record_type == 'client':
        tablename = 'client'
    elif record_type == 'session':
        tablename = proc.convert_client_to_sessiontable(client_id)
    
    proc.automate_UPDATE(tablename,record_type,client_id)   

    return

def option_100():
#This option handles program exists
    log_info(0, 'SHUTDOWN (100) DETECTED')
    exit(0)
