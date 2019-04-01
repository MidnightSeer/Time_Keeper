'''
Created on Mar 18, 2016
Python 3.4
@author: Miguel
'''
import sqlite3
import dbqueries as dbq
from time import sleep
import os,re
from getpass import getuser,getpass
from processor import log_info,create_user,contains_invalid_chars
import securepass
def init_table_col_names(table_type):
    if table_type == 'client':
        clients_table_cols = """
                    (client_id INTEGER, first_name TEXT, last_name TEXT, age INTEGER,
                    gender TEXT, phone_number1 TEXT, phone_number2 TEXT, email_address TEXT,
                    contact_address TEXT, total_time_charged TEXT, total_amount_charged INTEGER,
                    notes TEXT, created_by TEXT, modified_by TEXT)
                        """
        return clients_table_cols

    if table_type == 'admin':                
        admin_table_cols = """
                            (user_id INTEGER, username TEXT, email_address TEXT, password TEXT, 
                            auth_level INTEGER, modified_by TEXT)
                            """
        return admin_table_cols
    if table_type == 'constants':        
        constants_table_cols = """
                                (row_id INTEGER, hourly_rate INTEGER, modified_by TEXT)
                                """
        return constants_table_cols
    if table_type == 'session':
        clientid_table_cols = """
                            (session_id INTEGER, case_id INTEGER, session_date TEXT, session_length INTEGER, 
                            session_type TEXT, session_cost INTEGER, notes TEXT, modified_by TEXT, 
                            created_by TEXT, modified_by TEXT)
                            """
        return clientid_table_cols
    if table_type == 'validation':
        validation_table_cols = """
                                (validation_name TEXT, validation_value TEXT)
                                """
        
        validation_table_names_values = (
                            'session_date', 'session_length', 'session_type',
                            'phone_number1', 'phone_number2', 'gender',
                            'email_address')
        validation_table_values_values = (
                                'YYYY-MM-DD', 'HH:MM', 'phone,walk-in,general research,court,disposition'
                              ,'###-###-####','###-###-####','Male,Female','email@address.domain')
        
        return validation_table_cols,validation_table_names_values,validation_table_values_values
    if table_type == 'auth_groups':
        auth_table_cols = """
                                (group_id INTEGER, auth_level INTEGER, allowed_cmds TEXT, group_name TEXT)
                                """
        
        auth_table_group_id_values = ('1','2','3')
        auth_table_level_values = ('0','1','2')
        auth_table_cmds_values = ('CREATE,UPDATE,SELECT,INSERT,DROP,ALTER','UPDATE,SELECT','SELECT')
        auth_table_group_name_values = ('Admin','Member','Visitor')
        return auth_table_cols,auth_table_group_id_values,auth_table_level_values,auth_table_cmds_values,auth_table_group_name_values
                            

def db_setup():
    setup = False
    init_log_file = False
    if logfile_setup():
    #determine if this is the first time the log file will be created
    #or if there is already a file
    #The presence of a file means the program ran before
        init_log_file = True
    if not dbq.check_table('client'):
        print("[!] Setup is establishing space for client records...")
        dbq.create_table('client',init_table_col_names('client'))
        sleep(1)
        log_info(0,'SETUP CLIENT TABLE')
        setup = True      
    if not dbq.check_table('admin'):
        print("[!] Setup is initializing the administration settings...") 
        dbq.create_table('admin',init_table_col_names('admin'))
        sleep(1)
        log_info(0,'SETUP ADMIN TABLE')
        setup = True
    if not dbq.check_table('auth_groups'):
        print("[!] Setup is initializing the permission groups...") 
        table_cols,group_ids,levels,allowed_cmds,group_names = init_table_col_names('auth_groups')
        dbq.create_table('auth_groups',table_cols)
        for a,b,c,d in zip(group_ids,levels,allowed_cmds,group_names):
            dbq.add_record('auth_groups','(group_id, auth_level, allowed_cmds, group_name)',"('{a}','{b}','{c}','{d}')".format(a=a,b=b,c=c,d=d))
        sleep(1)
        log_info(0,'SETUP PERM GROUPS')
        setup = True
    if not dbq.check_table('validation'):
        print("[!] Setup is setting up validation rules...")
        table_cols,table_names,table_values = init_table_col_names('validation')
        dbq.create_table('validation',table_cols)
        for x,y in zip(table_names,table_values):
            dbq.add_record('validation','(validation_name,validation_value)',"('{x}','{y}')".format(x=x,y=y))
        sleep(1)
        log_info(0,'SETUP VALIDATION TABLE')
        setup = True
    if not dbq.check_table('constants'):
        print("[!] Setup is wrapping up...") 
        dbq.create_table('constants',init_table_col_names('constants'))
        sleep(1)
        log_info(0,'SETUP CONSTANTS TABLE')
        setup = True
    if init_log_file:
        print("[!] Logging turned on")
        log_info(0,'INITIATION COMPLETE')
    else:
        log_info(0,"PROGRAM RE-STARTED SUCCESSFULLY")
    if setup == True:   
        print("[!] Setup complete")
    return

def login():
    global logged_in_user
#function to prompt a login screen and detect if first usage
    output = dbq.recall_record('username', 'admin', 'auth_level', '0')
    #find admin users; if no users prompt to create one
    if not output:
        print("[!] Setup cannot find a user with Admin permissions")
        print("""[i] Your first user must be in the Admin group
            You must create a user with Administrator Permissions""")
        create_user()
    print("***********************")
    print("*       WELCOME       *")
    print("*    PLEASE LOG IN:   *")
    print("***********************")
    username = input("[?] Username: ")
    user_pass = getpass("[?] Password: ")
    if contains_invalid_chars('username', username):
        return login()
    db_pass = dbq.recall_record('password', 'admin', 'username', username)
#    print("db_pass: ",db_pass)
#    print("db_pass[0]: ",db_pass[0])
    if (db_pass is None) or (not securepass.check_password(db_pass[0], user_pass)):
        print("[!] Access Denied; attempt logged. ")
        log_info(0, "ACCESS DENIED","Access denied to: {u}, OS Username:{osid}".format(osid=getuser(),u=username))
        return login()
    else:
        print("[i] Successful Login: Access is logged")
        logged_in_user = username       #store the username as a global so other functions can reference it
        log_info(0, "LOGIN","Access granted to: '{u}', OS Username:'{osid}'".format(osid=getuser(),u=username))
def logfile_setup():
    if not os.path.isfile('error.log'):
        file = open('error.log','w+')
        file.close()
        return True

def scan_for_file():
    match_found = False
    files = os.listdir(path='./')
    pattern = '.*\.cr$'
    matches_list = []
    for item in files:
        match = re.match(pattern,item)
        if match:
#            print(match.group(0))
            matches_list.append(str(match.group(0)))
            match_found = True
    if len(matches_list) > 1:
        print("[!] Found multiple possible database files")
        print(*matches_list, sep=',')
        filename = input("[?] Choose your file: ")
#        print(filename)
        return filename
    if match_found and len(matches_list) == 1:
#        print(matches_list[0])
        return matches_list[0]
    else:
        return ''

if __name__ != '__main__':
    filename = scan_for_file()
    if not filename:
        print("[!] Initialization could not find a suitable file")
        print("[i] Entering setup...")
        filename = input("[?] Enter your db name: ")
        filetype = '.*\.cr'
        if not re.match(filetype,filename):
            filename = filename + '.cr'
    conn = sqlite3.connect(filename)    
    db = conn.cursor()    