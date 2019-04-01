'''
Created on Mar 18, 2016
Python 3.4
@author: Miguel
'''
import dbqueries as dbq

from collections import OrderedDict
from random import randrange
from datetime import datetime
import copy,securepass
from os import system,name

def get_client_id():
#If the client ID is blank, repeat prompt until value is given
    client_id = ''
    while not client_id:
        client_id = scrub(input("[?] Enter a (new) client ID: "))
    return client_id

def clientexists(client_id):
#Check is a client_id exists in the client table
    exists = dbq.record_exists('client', 'client_id', client_id)
    if exists is not None:
        return True
    else:
        return False

def convert_client_to_sessiontable(client_id):
    return "client_" + client_id #from "12" to "client_12"

def format_cols_for_dbquery(li,query_type):
    i = 0    
    if query_type == 'INSERT':
        query = '('
        endchar = ')'
    if query_type == 'SELECT':
        query = ''
        endchar = ''
    while i < len(li):
        if i < len(li)-1:
            query = query + li[i] + ", "   #This stores values to INSERT or SELECT the columns
        else:
            query = query + li[i] + endchar
        i = i + 1
    return query

def format_cols_for_dbvalues(li,value_li,client_id):
#puts into this format: ('4','first','last','33'), made for values to be inserted
    i = 0
#    values = "(" + client_id + ","
    values = "({id},".format(id=client_id)
    while i < len(value_li):    
        if i < len(value_li)-1:
            values = "{v}'{vl}',".format(v=values,vl=value_li[i])
#            values + "'" + value_li[i] + "',"  
        else:
            values = "{v}'{vl}')".format(v=values,vl=value_li[i])
#            values + "'" + value_li[i] + "')"
        i = i + 1
    return values

def format_cols_for_dboutput(li,obj):
#formats values as {'[i] Col Name: ',' Value'} as a dictionary type
#li - col names list; value_li - data list in those columns
#checks if a tuple is passed (1 record set) or a list of tuples (multiple record sets)
    listofdicts = []      #This will be the list of dicts
#    t = 0
    i = 0
#    print("length: ",len(obj))
#    print(type(li))
#    print("Object: ",obj)
    answers = OrderedDict()
#===============================================================================
# #    print(value_li)
#     if isinstance(value_li, tuple):
#         for element in value_li:
#             i = 0
#     #        print(element)
#             for item in li:
#                 output = "[i] " + item + ": "
#                 answers[output] = element[i]
#     #            print(i)
#     #            print(item)
#                 i = i + 1
# #        print(i)
# #    print(answers)
#     elif isinstance(value_li, list):
#         for element in value_li:
#             i = 0
#             print(element)
#             for item in li: #load value pairs into a dict
#                 output = "[i] " + item + ": "
#                 answers[output] = element[i]
#     #            print(i)
#     #            print(item)
#                 i = i + 1
#     #        print(i)
#             out[t] = answers    #load a dict into a tuple
#             t = t + 1
#     return answers
#===============================================================================
    if isinstance(obj, tuple):
#        print('Length: ',len(obj))
        for item in obj:
#            print(item)
            output = "[i] " + li[i] + ": "
            answers[output] = item       #this creates dict of output prompts to answers
#            print(answers)
            i = i + 1
        return answers
    elif isinstance(obj, list):
#        print(obj)        
        for tup in obj:     #each item in the list is actually a tuple
#            print("tuple: ",tup)
            i = 0
            for item in tup:    #each element in the tuple is 'item'
#                print("item: ",item)
                output = "[i] " + li[i] + ": "
                answers[output] = item   #this creates dict of output prompts to answers
                i = i + 1
#            print("Dict: ",answers)
            listofdicts.append(copy.deepcopy(answers))      #Add the dict to the list
#            print("Appended List: ",listofdicts)
#    exit(0)      
        return listofdicts

def format_cols_for_dbprompts(li):
#Accepts a list and sets up prompts for each value in the list
#Add a validation key to each item that matches a result in the validation table
    prompts = []
    validation = {}
    validation_name_tuple = dbq.show_table('validation')
#    print(validation_name_tuple)
    for item in validation_name_tuple:
        validation[item[0]] = item[1]
#    print(validation)
    i = 1   #this skips the prompt for a client_id; previously asked, it handles a duplicate client_id
    while i < len(li):
        if li[i] in validation:
            #appending the format string to columns in the 'validation' table
            validation_value = validation[li[i]].upper() #puts the validation strings in uppercase (YYYY-MM-DD)
#            print(validation_value)
            string = "[?] Enter A Value For {cn} ({v}): ".format(cn=string_mod(li[i]),v=validation_value)
        else:
            string = "[?] Enter A Value For {cn}: ".format(cn=string_mod(li[i])) #This stores a prompt for each column name
        prompts.append(string)
        i = i + 1
    return prompts

def format_cols_in_list(tablename):
#gets all column names and parses the tuple to store col names in a list
    col_names = dbq.get_col_names(tablename)
    cols = []
    for i in col_names:
        cols.append(i[1])
    return cols    
    
def coltuple_to_list(ctuple):
#accepts a tuple of column names and orders the col names (index 1) into a list
    tlist = []
    for t in ctuple:
        if len(t) == 1:
            e = 0
        else: 
            e = 1
        tlist.append(t[e])
    return tlist        #returns the col names from the tuple

def list_clients(cols):
    ans = 'N'
    total = dbq.count_records('client')
    if int(total[0]) > 10:
        ans = scrub(input("[i] More than 10 records; Continue? (Y)"))
    print("*******************")
    if ans == 'Y' or len(total) < 10:
        i = 0
        for c in cols:
            print("[i] Client ID: ",c[0])
            print("[i] First Name: ",c[1])
            print("[i] Last Name: ",c[2])
            print("*******************")
            i = i + 1
            if i % 10 == 0:
                input("[i] Press enter to continue...")

def autoprompt(prompts):    
#This automates the prompts and returns the user entered inputs
#Must be run after the prompts are loaded into a list
    
    ans_list = [] 
    for p in prompts:
        value = ''
        while not value:        #prompt until given a value
            value = input(p) #value 1 is the column name in the list
        ans_list.append(value) #stores the answers to the prompts in list, data_list
    return ans_list

# def list_in_cols(cols,li):
#     i = 1
#     while i <= len(li):
#         if (i % cols == 0):
#             print(li[i-1])      
#         else:
#             print(li[i-1]+"  ",end="")
#         i = i + 1
#     print()

def format_cols_to_choices(num,obj):
#Gets the list of column names and outputs them in columns for choices
#num = number of columns; tablename
    if not isinstance(obj, list):
        col_names = dbq.get_col_names(obj)
    else:
        col_names = tuple(obj)
    i = 0
#    print(list(col_names))
    for r in col_names:
        if len(r) == 1:
            e = 0
        else: 
            e = 1
        formatted_string = string_mod(r[e])
        if (i/num) != 1:
            print(formatted_string + "   ",end="")
        else:
            print(formatted_string)
        i = i + 1
    print()

def automate_data_recall_output(tablename,uniq_id,id_value):
#This recalls data and outputs it.  the client_id parameter is optional; use if record_type is 'client'
#uniq id and id value must both be set to ALL to show all records
    if uniq_id == "ALL" and id_value == "ALL":
        results = dbq.show_table(tablename)
        print("*******************")    #This is a divider between entries
    else:
        results = dbq.recall_record('*', tablename, uniq_id, id_value)
#    print(results)
    col_names = coltuple_to_list(dbq.get_col_names(tablename))
#    print(col_names)   
    output = format_cols_for_dboutput(string_mod(col_names), results)
#    print(type(output))
#    print(output)
    
    if output and isinstance(output, OrderedDict):
        for dic in output.items():
#            print(type(dic))
#            print("Dict: ",dic)
            for key in dic:
                print(key,end='')
            print()
    elif output and isinstance(output, list):
        for dic in list(output):
#            print(type(dic))
#            print("Dict: ",dic)
#            print("Items: ",dic.items())
#            print("Enumerated: ",enumerate(dic))
            for key,value in dic.items():
                print(key,value)
#                print(vars().keys())
#                print(values(i))
            print()
    else:
        print("[!] Unable to look up the given identifier")
        log_info(0, "NO DATA RECEIVED")
    return

def automate_INSERT(tablename,client_id):
    col_names = dbq.get_col_names(tablename)    #returns a tuple
    col_names_list = coltuple_to_list(col_names)#formats into a list with col names
    col_names_prompts = format_cols_for_dbprompts(col_names_list)   #formats the col names into a prompt list
    answers = autoprompt(col_names_prompts)  #shifts through the prompt list and records input in a list
    formatted_values = format_cols_for_dbvalues(col_names_list,answers,client_id)    #formats for an INSERT cmd
    query = format_cols_for_dbquery(col_names_list, 'INSERT') #formats for an INSERT cmd
    return (query,formatted_values)

def automate_UPDATE(tablename,record_type,client_id):
#Prompt for values to update the table with
#Inititiate constants
    
    col_to_update = ''
    id_value = ''
    id_col = ''
    
    format_cols_to_choices(3, tablename)    #display possible columns to update
    if record_type == 'client':
        
        tablename = record_type
        id_col = 'client_id'
        id_value = client_id
        
        col_names = format_cols_in_list(tablename)
        
    if record_type == 'session':
        
        col_names = format_cols_in_list(tablename)
        while id_col not in col_names:
            id_col = scrub(reverse_string_mod(input("[?] Enter lookup identifier: ")))
            if id_col not in col_names:
                print("[!] ",col_to_update,"is an invalid lookup method...")
        while not id_value:
            id_value = scrub(input("[?] Enter identifier's value: "))
    #The below code is independent of the record type
    
    while col_to_update not in col_names:
        col_to_update = scrub(reverse_string_mod(input("[?] Enter item to update: ")))
        if col_to_update not in col_names:
            print("[!] ",col_to_update,"is an invalid option...")
        current_value = dbq.recall_record(col_to_update, tablename, id_col, id_value)
        print("[i] Current value: {cv}".format(cv=current_value[0]))
        col_update_value = scrub(input("[?] Enter a new value: "))
    #UPDATE client SET first_name='TEST' WHERE client_id=1
    dbq.update_record(tablename, col_to_update, col_update_value, id_col, id_value)
    
    
    pass
def export_client_table(path):
    import csv
    try:
        with open(path,'w',newline='') as file:
            writer = csv.writer(file,delimiter=',')
            col_names = [
#Need to use the "title" case function
                'Client ID', 'First Name', 'Last Name', 'Age', 'Gender',
                'Phone Number1', 'Phone Number2', 'Email Address',
                'Contact Address', 'Total Session Time', 'Total Amt Charged']
            
            writer.writerow(col_names)
            data = dbq.show_table('clients')
            writer.writerows(data) 
        input("[i] Exported Data - Press enter to continue...")   
    except:
        import sys
        print(sys.exc_info())
        input("[!] Error during CSV export - Press enter to continue...")

def create_user():
#prompt to create a username and password
#this function will auto store the inputs 
#Checks for illegal characters in the username and hashes the password before storing
#     tablename = 'admin'
#     user_id = gen_user_id()
# #    print("user ID: ",user_id )
#     exists = dbq.recall_record('user_id', 'admin', 'user_id', user_id)
# #    print(exists)
#     if exists is not None:
#     #gen a new user_id if there is a duplicate
#         while user_id in exists:
#             user_id = gen_user_id()
# #    print("New User ID:", user_id)
#     query,values = automate_INSERT(tablename, user_id)   #return the formatted query and values parameters
#     dbq.add_record(tablename, query, values)
    user_id = gen_user_id()
#     print("user ID: ",user_id )
    exists = dbq.recall_record('user_id', 'admin', 'user_id', user_id)
#    print(exists)
    if exists is not None:
    #gen a new user_id if there is a duplicate
        while user_id in exists:
            user_id = gen_user_id()
    choice = ''
    user_name = input("[?] Enter a Username: ")
    exists = dbq.record_exists('admin', 'username', user_name)
    if exists is not None:
        print("[!] Username already exists.  Username must be unique")
        return create_user()
    elif contains_invalid_chars('username',user_name):
        return create_user()
    
    #prompt for email and desired auth level
    email = input("[?] Enter an Email: ")
    print("[?] Enter a Password: ")
    password = securepass.MaskInput('*')
    print(password)
    clear_screen()
    hash_pass = securepass.hash_password(password)
    print("[i] Available Groups: ")
    groups = dbq.list_records('group_name', 'auth_groups')
#    print(groups)
#    print(type(groups[0]))
    format_cols_to_choices(3, groups)
    while choice.title() not in coltuple_to_list(groups):
        choice = input("[?] Enter a permission group: ")
        if choice.title() not in coltuple_to_list(groups):
            print("{gr} is an invalid group".format(gr=choice))
    auth_level = dbq.recall_record('auth_level', 'auth_groups', 'group_name', choice.title())
    col_names = dbq.get_col_names('admin')
    col_names_list = coltuple_to_list(col_names)
    answers = (user_name,email,hash_pass,auth_level[0])
#    print("answers: ",answers)
    formatted_values = format_cols_for_dbvalues(col_names_list,answers,user_id)    #formats for an INSERT cmd
    query = format_cols_for_dbquery(col_names_list, 'INSERT')  
    res = input("[?] Commit User Creation (Y/N): ").upper()
    print(res)
    while res !='Y' or res !='N':
        res = input("[?] Commit User Creation (Y/N): ").upper()
        if res == 'Y':                                  
            dbq.add_record('admin', query, formatted_values)
            return
        elif res == 'N':
            return    

def gen_user_id():
#generate a pseudo random userid
    num = randrange(1000,10000000,1)
    return num
        
def clear_screen():
    system('cls' if name=='nt' else 'clear')
       
def scrub(element):
    return str(element).translate({ord(i):None for i in "\"'{}[]!@;:?!.%#$"})

def contains_invalid_chars(str_type,obj):
#This function checks if a password has invalid characters
#Returns True if invalid characters are detected, else False
#accepted options: 'username','email_address'
    if str_type == 'username':
        notpermitted_values = "/\/\"'!@;:?!="
        
    elif str_type == 'email_address':
        notpermitted_values = "/\/\"'{}[]!;:?!%#$="

    for i in obj:
        if i in notpermitted_values:            
            print("[!] You're {t} contains invalid characters ({i})".format(t=string_mod(str_type).title(),i=notpermitted_values))
            log_info(2, "{s}: {o}".format(s=str_type,o=obj), 'INVALID CHARACTERS')
            return True
    return False
def string_mod(obj):
#Works with strings or lists at this time
    if isinstance(obj,str):
    #if the obj is a string 
        obj = obj.replace('_',' ')
        return obj.title()
    elif isinstance(obj, list):
        i = 0
        for element in obj:
            obj[i] = element.replace('_',' ').title()
            i = i+1
        return obj

def reverse_string_mod(obj):
#Takes a col name choice and converts it to db col format
#i.e. Choice: Case Id; Converts to: case_id    
    if isinstance(obj,str):
        obj = obj.replace(" ","_")
        obj = obj.lower()
        return obj

def modified_by():
#Determine the current logged in user, get the user_id, append the timestamp to it.
    pass
    
#
#Error Checking functions
#
def log_info(error_code,cmd,error="N/A",p=True,error_file='error.log'):
#error_codes: 0 --> informational; 1 --> critical; 2 --> minor
#cmd --> "NO ERROR" if informational or if unable to give a command, 
#explain why you are calling this function
#[2016-04-03 10:26:42.816868][ERROR]:Unable to verify record -->(<class 'sqlite3.OperationalError'>
#[DATETIME][ERRORTYPE]:[ERRORMESSAGE]-->[SYSTEMERRORMESSAGE]
#[DATETIME][ERRORTYPE]:COMMAND: [COMMAND]
    error_code = int(error_code)
    if error_code == 2:
        error_type = 'MINOR'
        error_msg = "SUCCESSFULLY CAUGHT EXCEPTION"
        
    if error_code == 1:
        error_type = 'CRITICAL'
        error_msg = "Unable to process request"
        
    elif error_code == 0:
        error_type = 'INFO'
        error_msg = 'NO ERROR'
        p = False

    with open(error_file,'a') as f:
        #print in this format: [2016-04-10 11:07:48]
        form = "%Y-%m-%d %H:%M:%S"
        t = datetime.now()
        stime = t.strftime(form)
        f.write("[{t}][{et}] COMMAND: {c}".format(t=stime,et=error_type,c=cmd)+'\n')
        f.write("[{t}][{et}]:[{msg}] --> {sys}".format(t=stime,et=error_type,msg=error_msg,sys=error)+'\n')
        
        if p == True:
            print("[!] Error, Unable to process request, try again...")
            print("[i] Logged to {logfile}".format(logfile=error_file))