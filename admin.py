'''
Created on Mar 9, 2016
Python 3.4
@author: Miguel
'''
import sqlite3


    



    

    





def scrub_values(element):
    return str(element).translate({ord(i):None for i in "\{}[]!@;:?!.#$"}) #same as scrub without the apostrophe or quote



def closedb():
    conn.commit()
    conn.close()
