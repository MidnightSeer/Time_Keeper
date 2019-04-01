'''
Created on Mar 9, 2016
Python 3.4
@author: Miguel
'''

import datetime
import time

def convert_to_sec(time_string):
    x = time.strptime(time_string.split(',')[0],'%H:%M')
    seconds = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
    print("Converted into seconds: ", seconds)
    return seconds

def calc_delta(time1, time2):
    total_time = time2 - time1
    print("Time delta: ", total_time)
    return total_time

def convert_to_clock(total_seconds):
    mins, sec = divmod(total_seconds, 60)
    hrs, mins = divmod(mins, 60)
#    formatted_time = str(datetime.timedelta(seconds=total_seconds))
#    print(formatted_time)
    time = str(hrs) + " hrs " + str(mins) + " min"
#    print(time)
#    total_time = str(hrs) + ":" + str(mins)
#    print("Total Time Elapsed: ", total_time)
    return time


    
#time1 = input("Time1: ")
#time2 = input("Time2: ")
#convert_to_clock(calc_delta(convert_to_sec(time1), convert_to_sec(time2)))
