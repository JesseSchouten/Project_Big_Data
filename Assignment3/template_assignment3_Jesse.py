#!/usr/bin/env python

"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Yannick Hogebrug  y.r.hogebrug@student.vu.nl
Jesse Schouten j7.schouten@student.vu.nl
"""

# Include these lines without modifications
# Call the script as follows: ./<scriptname> <csv_filename> <mapper function> <reducer function>
# So, for example: ./template_assignment3.py hue_week_3_2017.csv mapper1 reducer1
# This will call the mapper1 function for each line of the data, sort the output, and feed the sorted output into import sys
import sys
import numpy as np
from io import StringIO
import traceback
from queue import Queue
import requests
import json
import threading

# Implement these mapper and reducer functions

def mapper1(line):
    fitness = line.split(',')[5]
    
    if fitness:
        print(fitness)

def reducer1(line):
    global count
    
    if line:
        fitness = float(line)
        if (fitness > 50.0):
            count += 1
        
    if not line:
        print(count)
    
def mapper2(line):
    None
	
def reducer2(line):
    None

def mapper3(line):  
    def convertToDatetime(datestring):
        import datetime       
        import re as re
        
        matches = re.search(r'((\d{4})-(\d{2})-(\d{2}) (\d{1,2}):(\d{1,2}):(\d{1,2}).(\d{3}))+', datestring)
        
        year = int(matches.group(2))
        month = int(matches.group(3))
        day = int(matches.group(4))
        hour = int(matches.group(5))
        minute = int(matches.group(6))
        second = int(matches.group(7))
        millisecond = int(matches.group(8))
        
        result = datetime.datetime(year, month, day, hour, minute, second, millisecond)
        
        return result
    
    def convertTimeToSeconds(time):      
        import re as re
        
        matches = re.search(r'(\d{1,2}):(\d{1,2}):(\d{1,2}).(\d{3})+', time)
        
        hour = int(matches.group(1))
        minute = int(matches.group(2))
        second = int(matches.group(3))
        
        result = (hour*60*60)+(minute*60)+(second)
        
        return result
    
    def shiftHalfOfADay(timeInSeconds):
        #The goal is to shift a time in seconds to midday to calculate an average
        if timeInSeconds < 43200 and timeInSeconds > 0:
            #shift up if after midnight
            timeInSeconds += 43200
        elif timeInSeconds >= 43200 and timeInSeconds < 86400:
            #shift down if before midnight
            timeInSeconds -= 43200
        return timeInSeconds

    user = line.split(',')[1]
    
    bedtime = line.split(',')[2]
    
    if bedtime:   
        #bedtimeAsDatetime = convertToDatetime(bedtime)
        dayInSeconds = convertTimeToSeconds(bedtime)
        shiftedDayInSeconds = shiftHalfOfADay(dayInSeconds)
        
        print('{}\t{}'.format(user, shiftedDayInSeconds))
	
def reducer3(line):
    def ShiftSecondsBack(seconds):
        #The goal is to shift a time in seconds to midday to calculate an average
        if seconds < 43200:
            #shift up if after afternoon
            seconds += 43200
        elif seconds >= 43200:
            #shift down if before afternoon
            seconds -= 43200
        return seconds
    
    def secondsToTime(seconds):
        import datetime
        return str(datetime.timedelta(seconds=seconds))

    global sum_time, current_user, user, count                 
  
    if line:
        user, time = line.split('\t')
        time = float(time)
    
        if(current_user == user):
            sum_time += time
            count = count + 1
        else: 
            if current_user != None:
                mean_shifted_time = round(sum_time/count, 2)
                mean_time = ShiftSecondsBack(mean_shifted_time)
                print('{}\t{}'.format(current_user, secondsToTime(mean_time)))
            count = 1
            sum_time = time
            current_user = user
    else:
        mean_shifted_time = round(sum_time/count, 2)
        mean_time = ShiftSecondsBack(mean_shifted_time)
        print('{}\t{}'.format(current_user, secondsToTime(mean_time)))

    
def mapper4(line):
    None

def reducer4(line):
    None


def instantiate_queue():
    None
    
def consume_data_stream(queue):
    None
    
def process_queue(queue):
    None

def main():
    None	

global count
global sum_time
count, sum_time = 0, 0

global current_user
global user
global current_count
current_user, user = None, None
current_count = 0

import os
os.chdir("C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Pre-master/Project big data")

global count
count = 0

if(len(sys.argv) == 4):
    data = sys.argv[1]
    mapper = sys.argv[2]
    reducer = sys.argv[3]
else:
    data = 'hue_week_3_2017.csv'
    mapper = 'mapper3'
    reducer = 'reducer3'

# Include these lines without modifications
 
if 'old_stdout' not in globals():
    old_stdout = sys.stdout
mystdout = StringIO()
sys.stdout = mystdout

with open(data) as file:
    #lines = [line.rstrip('\n') for line in file]
    #for line in lines: 
     #   line_values = line.split(';')
    try:
        for index, line in enumerate(file):
            if index == 0:
                continue
            line = line.strip()
            
            locals()[mapper](line)
        locals()[mapper](',,,,,,,') 
    except:
        sys.stdout = old_stdout
        print('Error in ' + mapper)
        print('The mapper produced the following output before the error:')
        print(mystdout.getvalue())
        traceback.print_exc()

    sys.stdout = old_stdout
    mapper_lines = mystdout.getvalue().split("\n")

    for index, line in enumerate(sorted(mapper_lines)):
        if index == 0:
            continue
        locals()[reducer](line)
    locals()[reducer]('')

mystdout.close()
 
# End of MapReduce

# Run main
main()
