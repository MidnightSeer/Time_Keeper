'''
Created on Mar 6, 2016
Python 3.4
@author: Miguel
'''
import sqlite3
def create_table(database, client_id):
#Check for a present table with the same client_id    
    db = sqlite3.connect(database)
    db.execute("SHOW TABLES LIKE '", client_id,'"')
    tablefetch_result = db.fetchone()
#if table is not in the database (client does not have a table)
    if not tablefetch_result:
        db.execute('create table ', client_id, '(session_date int, session_length int, session_type text)')
    else:
        pass