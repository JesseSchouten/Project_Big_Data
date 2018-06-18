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
# This will call the mapper1 function for each line of the data, sort the output, and feed the sorted output into reducer1
import sys
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
    
    if not line:
        print(count)
    else:    
        fitness = float(line)
        if (fitness > 50.0):
            count += 1
          
def mapper2(line):
    fitness = line.split(',')[5]
    user = line.split(',')[1]
    
    if fitness:
        print(user, fitness)
	
def reducer2(line):
    global sum_fitness, current_user, user, count
    
    if line:
        user, fitness = line.split(' ')
        fitness = float(fitness)
        
        if(current_user == user):
            sum_fitness += fitness
            count = count + 1
        else: 
            if current_user != None:
                mean_fitness = round(sum_fitness/count, 2)
                print('{}\t{}'.format(current_user, mean_fitness))
            count = 1
            sum_fitness = fitness
            current_user = user
    else:
        mean_fitness = round(sum_fitness/count, 2)
        print('{}\t{}'.format(current_user, mean_fitness))
        
def mapper3(line):
    None
	
def reducer3(line):
    None

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
global sum_fitness
count, sum_fitness = 0, 0

global current_user
global user
global current_count
current_user, user = None, None
current_count = 0

if(len(sys.argv) == 4):
    data = sys.argv[1]
    mapper = sys.argv[2]
    reducer = sys.argv[3]
else:
    data = 'hue_week_3_2017.csv'
    mapper = 'mapper2'
    reducer = 'reducer2'

# Include these lines without modifications
 
if 'old_stdout' not in globals():
    old_stdout = sys.stdout
mystdout = StringIO()
sys.stdout = mystdout


with open(data) as file:
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
