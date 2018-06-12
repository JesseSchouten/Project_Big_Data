"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Name Student 1 email@vu.nl
Name Student 2 email@vu.nl
"""

   
#%%  

    def readCSVFile(data):
        
        
#%%
    def isNoInformativeEvent(line):
        informativeEvent = ['lamp_change','nudge_time','bedtime_tonight','risetime','rise_reason','adherence_importance', 'fitness']     
        if informativeEvent:
            result = False
        else: result = True
        
        return result
#%%   
    def getEvent(line):
        
        matches = re.search(r'(lamp_change|nudge_time|bedtime_tonight|risetime|rise_reason|adherence_importance|fitness)',line)
            
        if matches:
            result = matches.group(0) 
        else: result = 'No event'
        
        return result         
        
#%%    
    def getDateTime(line):       
        import datetime
        
        monthDict = {'jan' : 1,'feb' : 2,'maart' : 3,'apr' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'sep' : 9, 'okt' : 10,'nov' : 11,'dec' : 12}
        
        matches = re.search(r'((\d{1,2})_(\D{1,12})_(\d{4}))+(_(\d{1,2})_(\d{1,2})_(\d{1,2}))*',line)
         
        if matches:           
            year = int(matches.group(0).split('_')[2])
            month = monthDict[matches.group(0).split('_')[1]]
            day = int(matches.group(0).split('_')[0])
                
            isDatetime = re.search(r'(_(\d{1,2})_(\d{1,2})_(\d{1,2}))',line)
            #if isDatetime:
             #   hour = int(matches.group(0).split('_')[3])
              #  minute =int(matches.group(0).split('_')[4])
              # sec = int(matches.group(0).split('_')[5])
            hour = 0
            minute = 0
            sec = 0
        else: result = 'No datetime'
            
        result = datetime.datetime(year,month,day,hour,minute,sec)
        
        return result
    
    #%%
    
    def createID(data):
        data = data2.set_index(['Datetime','user id'])
        return data
    
    #%%
    def insert_if_new(df,idx):
        if idx not in df.index:
            df = df.append(pd.Series({'bedtime' : float('nan'),\
                                      'intended_bedtime' : float('nan'),\
                                      'risetime' : float('nan'),\
                                      'rise_reason' : float('nan'),\
                                      'fitness' : float('nan'),\
                                      'adherence_importance' : float('nan'),\
                                      'in_experimental_group' : False},\
                                      name=idx))
        return df

#%%
    import pandas as pd
    import re as re
    import numpy as np
    from datetime import datetime, date, time
    import os
    os.chdir("C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Pre-master/Project big data/data-week-1")
    
    def read_csv_data(filenames):   
    
        #textfile='hue_upload.csv'
        
        #colnames = ['row id','user id','event id','value']
        
        #data = pd.read_csv(textfile,sep = ';'
        #                   ,header=None
        #                   ,names=colnames) 
        
        #data2=getInformativeEvents(data)
        
        #data2 = addEvent(data2)
        
        #data2 = addDateTime(data2)
   
        #data3= createID(data2)   
        
        columns = ['bedtime','intended_bedtime','risetime','rise_reason','fitness','adherence_importance','in_experimental_group']
        dataresult = pd.DataFrame(columns=columns)
        
        with open('hue_upload.csv') as f:
            lines = [line.rstrip('\n') for line in f]
            for line in lines: 
                if isNoInformativeEvent(line):
                    continue
                else: 
                    line_values = line.split(';')
                    event = getEvent(line)
                    datetime = getDateTime(line)
                    user_id = line_values[1]
                    index = (datetime,user_id)
                    if(event)
                        dataresult = insert_if_new(dataresult,index)

                
                
                
                
            
    
    
    
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

