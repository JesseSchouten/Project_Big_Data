"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Name Student 1 email@vu.nl
Name Student 2 email@vu.nl
"""

         
        
#%%
    def isNoInformativeEvent(eventid):
        matches = re.search(r'(lamp_change|nudge_time|bedtime_tonight|risetime|rise_reason|adherence_importance|fitness)',eventid)     
        if matches:
            result = False
        else:
            result = True
        
        return result
#%%   
    def getEvent(eventid):
        
        matches = re.search(r'(lamp_change|nudge_time|bedtime_tonight|risetime|rise_reason|adherence_importance|fitness)',eventid)
            
        if matches:
            result = matches.group(0) 
        else: result = 'No event'
        
        return result         
        
#%%    
    def getDateTimeFromEventID(eventid):       
        import datetime
        
        monthDict = {'jan' : 1,'feb' : 2,'maart' : 3,'apr' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'sep' : 9, 'okt' : 10,'nov' : 11,'dec' : 12}
        
        matches = re.search(r'((\d{1,2})_(\D{1,12})_(\d{4}))+(_(\d{1,2})_(\d{1,2})_(\d{1,2}))*',eventid)
         
        if matches:           
            year = int(matches.group(0).split('_')[2])
            month = monthDict[matches.group(0).split('_')[1]]
            day = int(matches.group(0).split('_')[0])
                
            #isDatetime = re.search(r'(_(\d{1,2})_(\d{1,2})_(\d{1,2}))',line)
            #if isDatetime:
             #   hour = int(matches.group(0).split('_')[3])
              #  minute =int(matches.group(0).split('_')[4])
              # sec = int(matches.group(0).split('_')[5])
            hour = 0
            minute = 0
            sec = 0
            
            result = datetime.datetime(year,month,day,hour,minute,sec)
        else: 
            result = 'No datetime'           
        
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
    def convertValueToDateTime(time,dateLine,event):
        import datetime
        
        matchestime = re.search(r'((\d{1,2})(\d{2}))+',time)
        matchesdate = re.search(r'((\d{1,2})_(\D{1,12})_(\d{4}))+',dateLine)
        
        monthDict = {'jan' : 1,'feb' : 2,'maart' : 3,'apr' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'sep' : 9, 'okt' : 10,'nov' : 11,'dec' : 12}
        
        result = 'no datetime found'
        
        if matchesdate and matchestime:           
            year = int(matchesdate.group(0).split('_')[2])
            month = monthDict[matchesdate.group(0).split('_')[1]]
            day = int(matchesdate.group(0).split('_')[0])
            #Check if user starting sleeping in morning (wrong input)
            hour = int(matchestime.group(2))
            
            if event == 'bedtime_tonight':                
                if hour >=6 and hour <= 12:
                    hour += 12
                #Check if the time is set at 24:00, and change to 0:00
                if hour == 24:
                    hour = 0
                else:
                    hour = int(matchestime.group(2))         
                
            minute = int(matchestime.group(3))
            
            result = datetime.datetime(year,month,day,hour,minute)
        
        return result
    
    #%%
    def getTimeFromLampChange(event_id):
        import datetime        
        
        matches = re.search(r'(\d{1,2})_(\D{1,12})_(\d{4})+_(\d{1,2})_(\d{1,2})_(\d{1,2})_(\d{3})+', event_id)
        
        monthDict = {'jan' : 1,'feb' : 2,'maart' : 3,'apr' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'sep' : 9, 'okt' : 10,'nov' : 11,'dec' : 12}
        
        year = int(matches.group(3))
        month = int(monthDict[matches.group(2)])
        day = int(matches.group(1))
        hour = int(matches.group(4))
        minute = int(matches.group(5))
        second = int(matches.group(6))
        millisecond = int(matches.group(7))
        
        result = datetime.datetime(year, month, day, hour, minute, second, millisecond)
        
        return result
        
#%%
    import pandas as pd
    import re as re
    import numpy as np
    import datetime
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
                line_values = line.split(';')
                user_id = line_values[1]
                event_id =line_values[2]
                value = line_values[3]
                
                if isNoInformativeEvent(event_id):
                    continue
            
                event = getEvent(event_id)
                dtime = getDateTimeFromEventID(event_id)
                index = (dtime,user_id)
                
                if index not in dataresult:
                    dataresult = insert_if_new(dataresult,index)
                    
                if event == 'bedtime_tonight':
                    #Skip if the time in the string has 1,2 or larger then 5 number (taking the comma's into account!)
                    if (len(value) > 4) and (len(value) < 7):
                        intendedBedtime = convertValueToDateTime(value,event_id,event)
                        dataresult = dataresult.set_value(index,'intended_bedtime',intendedBedtime)
                  
                if event == 'risetime':
                    #Skip if the time in the string has 1,2 or larger then 5 number (taking the comma's into account!)
                    if (len(value) > 4) and (len(value) < 7):
                        risetime = convertValueToDateTime(value,event_id,event)
                        dataresult = dataresult.set_value(index,'risetime',risetime)
                        
                if(event == 'rise_reason'):
                    dataresult = dataresult.set_value(index, 'rise_reason', value) 
                    
                if(event == 'lamp_change' and value == '"OFF"'):
                    time = getTimeFromLampChange(event_id)  
                    if int(time.strftime('%H')) < 6:
                        dtime = dtime - datetime.timedelta(hours = 24)                      
                        index = (dtime,user_id)
                    if index not in dataresult:
                        dataresult = insert_if_new(dataresult,index)
                    
                    if()
                dataresult = dataresult.set_value(index, 'bedtime', time) 
                
                if(event == 'nudge_time'):
                    dataresult = dataresult.set_value(index, 'in_experimental_group', True)
                
                if(event == 'fitness'):
                    dataresult = dataresult.set_value(index, 'fitness', value) 
                                
                if(event == 'adherence_importance'):
                    dataresult = dataresult.set_value(index, 'adherence_importance', value) 
                    
    
    
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

