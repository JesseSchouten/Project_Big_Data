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
    def convertTimeToSeconds(time):      
        import re as re
        
        matches = re.search(r'(\d{1,2}):(\d{1,2}):(\d{1,2})', time)
        
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
        #The goal is to shift a time in seconds back to midnight to calculate an average
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

    global sum_time_Ex3, current_user_Ex3, count_Ex3                
  
    if line:
        user_Ex3, time = line.split('\t')
        time = float(time)
    
        if(current_user_Ex3 == user_Ex3):
            sum_time_Ex3 += time
            count_Ex3 = count_Ex3 + 1
        else: 
            if current_user_Ex3 != None:
                mean_shifted_time = round(sum_time_Ex3/count_Ex3, 2)
                mean_time = ShiftSecondsBack(mean_shifted_time)
                print('{}\t{}'.format(current_user_Ex3, secondsToTime(mean_time)))
            count_Ex3 = 1
            sum_time_Ex3 = time
            current_user_Ex3 = user_Ex3
    else:
        mean_shifted_time = round(sum_time_Ex3/count_Ex3, 2)
        mean_time = ShiftSecondsBack(mean_shifted_time)
        print('{}\t{}'.format(current_user_Ex3, secondsToTime(mean_time)))

    
def mapper4(line):
    def convertToDatetime(datestring):
        import datetime       
        import re as re
        
        matches = re.search(r'((\d{4})-(\d{2})-(\d{2}) (\d{1,2}):(\d{1,2}):(\d{1,2}))+', datestring)
        
        year = int(matches.group(2))
        month = int(matches.group(3))
        day = int(matches.group(4))
        hour = int(matches.group(5))
        minute = int(matches.group(6))
        second = int(matches.group(7))
        
        result = datetime.datetime(year, month, day, hour, minute, second)
        
        return result

    def timeDiffInSeconds(time1,time2):
        import datetime 
        
        diff = time1-time2
        
        return int(diff.total_seconds())
        
    user = line.split(',')[1]
    
    bedtime = line.split(',')[2]
    
    intendedBedtime = line.split(',')[4]
       
    if bedtime and intendedBedtime: 
        diff = timeDiffInSeconds(convertToDatetime(bedtime),convertToDatetime(intendedBedtime))
        if diff > 0:
            print('{}\t{}'.format(user, diff))
	

def reducer4(line):
    #source: http://python3.codes/popular-sorting-algorithms/
    def insertion_sort(l):
        for i in range(1, len(l)):
            j = i-1
            key = l[i][1]
            keyhelp = l[i]
            while (l[j][1] > key) and (j >= 0):
               l[j+1] = l[j]
               j -= 1
            l[j+1] = keyhelp  
    
    if line:
        user_Ex5, diff_Ex5 = line.split('\t')
    
        if len(top5_Ex5) < 5:
            top5_Ex5.append([user_Ex5, int(diff_Ex5)])
        else: 
            if int(diff_Ex5) > top5_Ex5[0][1]:
                top5_Ex5[0] = [user_Ex5,int(diff_Ex5)]
    else:
        for item in top5_Ex5:
            print('{}\t{}'.format(item[0],item[1]))
    
    insertion_sort(top5_Ex5)
    


def instantiate_queue():
    None
    
def consume_data_stream(queue):
    None
    
def process_queue(queue):
    None

def main():
    None	

global count_Ex3
global sum_time_Ex3
count_Ex3, sum_time_Ex3 = 0, 0
global current_user_Ex3
current_user_Ex3 = None

global top5_Ex5
top5_Ex5 = []

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
