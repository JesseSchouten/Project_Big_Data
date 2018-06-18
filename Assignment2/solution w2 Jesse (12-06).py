"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Name Student 1 email@vu.nl
Name Student 2 email@vu.nl
"""

import pandas as pd
import re as re
import numpy as np
from datetime import datetime, date, time
import os
os.chdir("C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Pre-master/Project big data/data-week-1")


    #def read_csv_data(filenames):   
   
#%%  
    def getInformativeEvents(data):
        searchfor = ['lamp_change','nudge_time','bedtime_tonight','risetime','rise_reason','adherence_importance', 'fitness']     
        data = data[data['event id'].str.contains('|'.join(searchfor))]
        data = data.reset_index()
        
        return data
#%%   
    def addEvent(data):
        l = []
        
        for i in range(0,len(data)):
            string = data['event id'][i]
            matches = re.search(r'(lamp_change|nudge_time|bedtime_tonight|risetime|rise_reason|adherence_importance|fitness)',string)
            
            l.append(matches.group(0) if matches else l.append('No event'))
            
        df = pd.DataFrame(l)
        df.columns = ['event']
        
        return pd.merge(df,data,left_index=True,right_index=True)         
        
#%%    
    def addDateTime(data):       
        import datetime
        
        l = []
        
        monthDict = {'jan' : 1,'feb' : 2,'maart' : 3,'apr' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'sep' : 9, 'okt' : 10,'nov' : 11,'dec' : 12}
        
        for i in range(0,len(data)):
            string = data['event id'][i]
            matches = re.search(r'((\d{1,2})_(\D{1,12})_(\d{4}))+(_(\d{1,2})_(\d{1,2})_(\d{1,2}))*',string)
                    
            year = int(matches.group(0).split('_')[2])
            month = monthDict[matches.group(0).split('_')[1]]
            day = int(matches.group(0).split('_')[0])
            
            isDatetime = re.search(r'(_(\d{1,2})_(\d{1,2})_(\d{1,2}))',string)
            if isDatetime:
                hour = int(matches.group(0).split('_')[3])
                minute =int(matches.group(0).split('_')[4])
                sec = int(matches.group(0).split('_')[5])
            else:
                hour = 0
                minute = 0
                sec = 0
            
            dt = datetime.datetime(year,month,day,hour,minute,sec)
            l.append(dt if matches else l.append('No datetime'))
        
        df = pd.DataFrame(l)
        df.columns = ['Datetime']
        
        return pd.merge(df,data,left_index=True,right_index=True)
    
    #%%
    
    def createID(data):
        data = data.set_index(['Datetime', 'user id'])
        return data

#%%
    
    textfile='hue_upload.csv'
    colnames = ['row id','user id','event id','value']
    data = pd.read_csv(textfile,sep = ';'
                       ,header=None
                       ,names=colnames) 
    
    
    
    data2=getInformativeEvents(data)
    
    data2 = addEvent(data2)
    
    data2 = addDateTime(data2)

    data3 = createID(data2)

columns = ['bedtime']
test = pd.DataFrame(index = [0,1,2,3,4,5], columns = columns)


with open('hue_upload.csv') as f:   
    lines = [line.rstrip('\n') for line in f]
    for i in range(0,1):
        line_values = line.split(';')
        
        t = pd.Series([line_values[0], line_values[1], line_values[2], line_values[3]])
        print(t)
        string = line_values[2]
        matches = re.search('bedtime_tonight', string)
        if matches:
            test.set_value(i, 'bedtime', line_values[3])   
        else:
            test.set_value(i, 'bedtime', 123)
            
    
    
    
#%%    
    
def to_mongodb(df):
    None


def read_mongodb(filter,sort):
    None


if __name__ == '__main__':
    # this code block is run if you run solution.py (instead of run_solution.py)
    # it is convenient for debugging

    df = read_csv_data(["hue_upload.csv","hue_upload2.csv"])
    # to_mongodb(df)
    # read_mongodb({},'_id')

