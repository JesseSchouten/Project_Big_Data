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
import datetime as dt
import os
os.chdir("C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Pre-master/Project big data/data-week-1")


def read_csv_data(filenames):
    
    
    textfile='hue_upload.csv'
    colnames = ['row id','user id','event id','value']
    data = pd.read_csv(textfile,sep = ';'
                       ,header=None
                       ,names=colnames)
    
    def find_event(string):
        return re.findall(r'[a-zA-Z]+[_]*[a-zA-Z]+',string)
    
    x=pd.Series(index=[i for i in range(0,len(data))])
    

    
#%%  
    def getInformativeEvents(data):
        searchfor = ['lamp_change','nudge_time','bedtime_tonight','risetime','rise_reason','adherence_importance', 'fitness']     
        data = data[data['event id'].str.contains('|'.join(searchfor))]
        data = data.reset_index()
        
        return data
#%%   
    def addEvent(data):
        l = []
        
        searchfor = ['lamp_change','nudge_time','bedtime_tonight','risetime','rise_reason','adherence_importance', 'fitness']           
        for i in data2.index:
            if(searchfor[0] in data2['event id'][i]):
                data2['event'] == 'lamp_change'
            elif(searchfor[1] in data2['event id'][i]):
                data2['event'] == 'nudge_time'                         
            else: 'no event'
                    ]
        
#%%    
    def addDateTime(data):       
        l = []
        for i in range(0,len(data)):
            string = data['event id'][i]
            matches = re.search(r'\d{1,2}_\D{1,12}_\d{4}',string)
            if matches:
                l.append(matches.group(0))
            else: l.append('No date')
        
        df = pd.DataFrame(v)
        df.columns = ['Datetime']
        
        return pd.merge(df,data,left_index=True,right_index=True)
#%%    
    k = addDateTime(data2)
    
    ##Line per line
    import re as re
    #read line of file
    with open(textfile) as f:
        flines = f.readlines()
        
    for line in flines:
        match = re.search(r'',line)
        if match:
            coordinateList.append(readCoordinate(match.group(1)))
            pieceList.append(match.group(3))
        else:next         
    
    
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





