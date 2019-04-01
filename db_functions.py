'''
Created on Mar 6, 2016
Python 3.4
@author: Miguel
'''
import admin
import time_functions
from time import sleep

def clientexists(client_id):
    admin.db.execute("SELECT * FROM clients WHERE client_id = {ci}".format(ci=client_id))
    exists = admin.db.fetchone()
    if exists is not None:
        return True
    else:
        return False
    
def add_record(record_type): 
    if record_type == "client":
        client_id = admin.get_client_id()
        if clientexists(client_id):
            print("[!] Client ID already exists")
            show_client_info(client_id)
            input("[!] Press enter to continue...")
            list_clients()
            return
        else:    
            create_table(client_id,'session')
            tablename = "clients"
    elif record_type == 'session':
        client_id = admin.get_client_id()
        if not clientexists(client_id):
            print("[!] Client ID does not exist")
            if input("[?] Display a list of clients (Y/N)") == 'Y':
                list_clients('clients')
            return 
        else:
            tablename = admin.convert_client_to_sessiontable(client_id)
    col_names = get_column_names(tablename) #column names returned in a list format    
    prompts = admin.format_cols_for_dbprompts(col_names)#This returns the col names in a prompt format    
    input_from_prompts = admin.autoprompt(prompts)  #prompt the user for input for all column names
    query = admin.format_cols_for_dbquery(col_names,'INSERT')
    formatted_values = admin.format_cols_for_dbvalues(col_names,input_from_prompts,client_id)
#    print("INSERT INTO {tn} {q} values {v}".format(tn=tablename,q=query,v=formatted_values))
    admin.db.execute("INSERT INTO {tn} {q} values {v}".format(tn=tablename,q=query,v=formatted_values))
    input("[!] Info added - Press enter to commit changes...")
    admin.conn.commit()
#creates a client table to track sessions
        
def list_clients(tablename):
    cols_string = pick_cols(3, tablename)
    admin.db.execute("SELECT {cns} FROM {tn}".format(cns=cols_string,tn=tablename))
    cols = admin.db.fetchall()
    if not cols:
        print("[!] You have not entered any clients yet")    
    else:
        for col in cols:
            print_client_info(col)
    input("[!] Press enter to continue...")
        
def show_client_info(client_id):
    print("*******************")
    for col in admin.db.execute("SELECT * FROM clients WHERE client_id=(?)", [client_id]):
        print_client_info(col)
#    input("[!] Press enter to continue...")
        
def sum_clients():
    admin.db.execute("SELECT Count(*) FROM clients")
    for row in admin.db:
        print("[i] There are", row[0], "client(s)" )
    input("[!] Press enter to continue...")

#the print_info function is called from either show_clients or list_clients        
def print_client_info(col):
    print("[i] Client ID: ",col[0])
    print("[i] First Name: ",col[1])
    print("[i] Last Name: ",col[2])
    print("*******************")

def print_session_info(col):
    print("[i] Session Date: ", col[0])
    print("[i] Session Length: ", col[1])
    print("[i] Session Type: ", col[2])
    print("[i] Session Cost: ", col[3])

def add_session(client_id, session_date, session_length, session_type):
    command = "INSERT INTO '" + admin.scrub(client_id) + "' (session_date, session_length, session_type) values ('" + admin.scrub(session_date) + "', '" + admin.scrub(session_length) + "', '" + admin.scrub(session_type) + "')"
#    print(command)
    admin.db.execute(command)
    admin.conn.commit()
    
def show_session_info(client_id, session_date):
#    cmd = "SELECT session_date, session_length, session_type FROM '" + admin.scrub(client_id) + "' WHERE session_date = (?)"
#    print(command)
    print("[i] Client ID: ", client_id)
    
    for col in admin.db.execute("SELECT session_date, session_length, session_type FROM '{ci}' WHERE session_date = {sd}".format(ci=client_id,sd=session_date)):
        print_session_info(col)
#    input("Press enter to continue...")

def list_table_entries(tablename,date=''):
    if date == '':
        try:
            admin.db.execute("SELECT * FROM '{tn}'".format(tn=tablename))
        except:
            print("[!] Unable to find any sessions")
    else:
        admin.db.execute("SELECT * FROM '{tn}' WHERE session_date='{d}'".format(tn=tablename,d=date))
    results = admin.db.fetchall()
#    print(results)
    col_names = get_column_names(tablename)
#    print(cols)
    for ans in results:
        print("*********************")  
#        print(ans)
        output = admin.format_cols_for_dboutput(col_names, 'output', '' ,ans)
#        print(output)
        for key,value in output.items():
            if key == '[i] session_length: ':     #convert seconds to hrs:min output when outputting the length of a session
                time = time_functions.convert_to_clock(value)
                print(key,time)
            else:
                print(key,value)
            
        print("*********************") 
def find_table(tablename):
    admin.db.execute("SELECT * FROM sqlite_master WHERE name='{tn}' and type='table' ".format(tn=tablename))
#    cmd = "SELECT * FROM sqlite_master WHERE name='" + admin.scrub(tablename) +"' and type='table' "
#    admin.db.execute(cmd)
    client_table_exists = admin.db.fetchone()
    if client_table_exists:
        return True
    else:
        return False

def create_table(tablename,table_type):
    table_exists = find_table(tablename)
    if tablename == 'clients' and not table_exists:
        print("[!] Setup detected this is your first use")
        print("[!] Please standby while we initialize the databases")
        sleep(3)
    if not table_exists:
        admin.db.execute("CREATE table '{tn}' {cns}".format(tn=tablename,cns=admin.init_table_col_names(table_type)))
        admin.conn.commit()
#        input(print("[i] Created ", tablename, " Table - Press enter to continue..."))
    else:
#        print("[!] Table already exists")
        pass        
    
def find_data(col_name, table_name):
    cmd = "SELECT " + col_name + " FROM " + table_name
    admin.db.execute(cmd)
    data_exists = admin.db.fetchone()
    if data_exists:
        print("[i] Data found! ", data_exists)
        return True
    else:
        print("[i] Data not found")
        return False

def recall_data(tablename,col_name1,col_name2,row_value):
    admin.db.execute("SELECT {cn} FROM {tn} WHERE {rn}={rv}".format(cn=col_name1,tn=tablename,rn=col_name2,rv=row_value))
    data = admin.db.fetchone()
    return data[0]

def update_data(tablename, col_name, col_value, row_name, row_value):
#    print("UPDATE {tn} SET {cn}='{cv}' WHERE {rn}='{rv}'".format(tn=tablename,cn=col_name,cv=admin.scrub(col_value),rn=row_name,rv=admin.scrub(row_value)))
    admin.db.execute("UPDATE {tn} SET {cn}='{cv}' WHERE {rn}='{rv}'".format(tn=tablename,cn=col_name,cv=admin.scrub(col_value),rn=row_name,rv=admin.scrub(row_value)))
    admin.conn.commit()

def get_column_names(tablename):
    table_returns = admin.db.execute("pragma table_info({tn})".format(tn=tablename))
    rlist = []
#    return result_list[1]  #result_list[1] are the column names
    for r in table_returns:
        rlist.append(r[1])
#        print(r[1])
#    print(rlist)
    return rlist

def pick_cols(num,tablename):
    admin.db.execute("pragma table_info({tn})".format(tn=tablename))
    col_names = admin.db.fetchall()
    cols = []
    for r in col_names:
        cols.append(r[1])
    i = 0
    col_string = ''
    while i <= num:
        if i == num:
            col_string = col_string + cols[i]
        else:
            col_string = col_string + cols[i] + ','
        i = i + 1
    return col_string
    
