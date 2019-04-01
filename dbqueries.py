'''
Created on Mar 18, 2016
Python 3.4
@author: Miguel
'''
from init import db,conn
from sqlite3 import OperationalError
from menu import controller
import sys
from processor import log_info

def get_col_names(tablename):
#Lists all the column names    
    try:
        db.execute("pragma table_info({tn})".format(tn=tablename))    
    except:
        cmd = "pragma table_info({tn})".format(tn=tablename)
        log_info(1, cmd, str(sys.exc_info()))
    return db.fetchall()
    
def update_record(tablename,col_name,col_value,id_col,id_value):
#Update an item based off the ID
    try:
        db.execute("UPDATE {tn} SET {cn}='{cv}' WHERE {colid}='{id}'".format(tn=tablename,cn=col_name,cv=col_value,colid=id_col,id=id_value))
        conn.commit()    
    except:
        cmd = "UPDATE {tn} SET {cn}='{cv}' WHERE {colid}='{id}'".format(tn=tablename,cn=col_name,cv=col_value,colid=id_col,id=id_value)
        log_info(1, cmd, str(sys.exc_info()))
#        print("[!] ERROR, Unable to update record, try again...")
    return db.fetchone()
        
def recall_record(col_name,tablename,id_col,id_value):
#Recall an item by ID to display
#use * for col_name to select all columns
    try:
        db.execute("SELECT {cn} FROM {tn} WHERE {colid}='{id}'".format(cn=col_name,tn=tablename,colid=id_col,id=id_value))
    except:
        cmd = "SELECT {cn} FROM {tn} WHERE {colid}='{id}'".format(cn=col_name,tn=tablename,colid=id_col,id=id_value)
        log_info(1, cmd, str(sys.exc_info()))
    return db.fetchone()

def record_exists(tablename,col_name,ID):
#Checks to see if a record exists.  Can be used to see if a client_id exists
#dbq.record_exists('client','client_id',client_id)
    try:
        db.execute("SELECT * FROM {tn} WHERE {col} = '{ci}'".format(tn=tablename,col=col_name,ci=ID))
    except:
        cmd = "SELECT * FROM {tn} WHERE {col} = '{ci}'".format(tn=tablename,col=col_name,ci=ID)
        log_info(1, cmd, str(sys.exc_info()))
        return controller(2)
    return db.fetchone()
      
def list_records(col_names,tablename):
#Select data to display.  Can be used to see if that column has any data; 'cns' can be a list of column names
    try:
        db.execute("SELECT {cns} FROM {tn}".format(cns=col_names,tn=tablename))
    except:
        cmd = "SELECT {cns} FROM {tn}".format(cns=col_names,tn=tablename)
        log_info(1, cmd, str(sys.exc_info()))
    return db.fetchall()
  
def create_table(tablename,col_names):
#Create a table with specified columns and value type; col_names needs to be in a list
#ie: (client_id INTEGER, first_name TEXT, last_name TEXT, age INTEGER)
    try:
        db.execute("CREATE table '{tn}' {cns}".format(tn=tablename,cns=col_names))
        conn.commit()
    except OperationalError:
        cmd = "CREATE table '{tn}' {cns}".format(tn=tablename,cns=col_names)
        log_info(1, cmd, str(sys.exc_info()))
    return db.fetchone()

def check_table (tablename):
#Display a table; can be used to determine if the table exists
    try:
        db.execute("SELECT * FROM sqlite_master WHERE name='{tn}' and type='table' ".format(tn=tablename))
#    print(db.fetchall())
    except:
        cmd = "SELECT * FROM sqlite_master WHERE name='{tn}' and type='table' ".format(tn=tablename)
        log_info(1, cmd, str(sys.exc_info()))
    return db.fetchall()

def add_record(tablename,col_names,col_values):
#Appends data to the table; INSERT INTO 'clients' col1,col2 values (1,2)
#    print("INSERT INTO '{tn}' {cns} values {vl}".format(tn=tablename,cns=col_names,vl=col_values))
    try:
        db.execute("INSERT INTO '{tn}' {cns} values {vl}".format(tn=tablename,cns=col_names,vl=col_values))
        conn.commit()
    except:
        cmd = "INSERT INTO '{tn}' {cns} values {vl}".format(tn=tablename,cns=col_names,vl=col_values)
        log_info(1, cmd, str(sys.exc_info()))
    return db.fetchone()
    
def show_table(tablename):
#Show everything in a table
    try:
        db.execute("SELECT * FROM '{tn}'".format(tn=tablename))
    except:
        cmd = "SELECT * FROM '{tn}'".format(tn=tablename)
        log_info(1, cmd, str(sys.exc_info()))
    return db.fetchall()

def count_records(tablename):
#Show the total # of records in a Table
    try:
        db.execute("SELECT Count(*) FROM {tn}".format(tn=tablename))
    except:
        cmd = "SELECT Count(*) FROM {tn}".format(tn=tablename)
        log_info(1, cmd, str(sys.exc_info()))
    return db.fetchone()