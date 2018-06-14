"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Name Student 1 email@vu.nl
Name Student 2 email@vu.nl
"""

         
        

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
        
        monthDict = {'januari' : 1,'februari' : 2,'maart' : 3,'april' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'september' : 9, 'oktober' : 10,'november' : 11,'december' : 12}
          
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
        
        monthDict = {'januari' : 1,'februari' : 2,'maart' : 3,'april' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'september' : 9, 'oktober' : 10,'november' : 11,'december' : 12}
        
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
        
        monthDict = {'januari' : 1,'februari' : 2,'maart' : 3,'april' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'september' : 9, 'oktober' : 10,'november' : 11,'december' : 12}
        
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
    import os
    os.chdir("C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Pre-master/Project big data/data-week-1")
    
    filenames = ["hue_upload.csv","hue_upload2.csv"]
    def read_csv_data(filenames):
        import pandas as pd
        import re as re
        import numpy as np
        import datetime
        
        def isNoInformativeEvent(eventid):
            matches = re.search(r'(lamp_change|nudge_time|bedtime_tonight|risetime|rise_reason|adherence_importance|fitness)',eventid)     
            if matches:
                result = False
            else:
                result = True
        
            return result
    
        def getEvent(eventid):
            
            matches = re.search(r'(lamp_change|nudge_time|bedtime_tonight|risetime|rise_reason|adherence_importance|fitness)',eventid)
                
            if matches:
                result = matches.group(0) 
            else: result = 'No event'
            
            return result         
  
        def getDateTimeFromEventID(eventid):       
            import datetime
            
            monthDict = {'januari' : 1,'februari' : 2,'maart' : 3,'april' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'september' : 9, 'oktober' : 10,'november' : 11,'december' : 12}
              
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
        
        def convertValueToDateTime(time,dateLine,event):
            import datetime
            
            matchestime = re.search(r'((\d{1,2})(\d{2}))+',time)
            matchesdate = re.search(r'((\d{1,2})_(\D{1,12})_(\d{4}))+',dateLine)
            
            monthDict = {'januari' : 1,'februari' : 2,'maart' : 3,'april' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'september' : 9, 'oktober' : 10,'november' : 11,'december' : 12}
            
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
    
        def getTimeFromLampChange(event_id):
            import datetime        
            
            matches = re.search(r'(\d{1,2})_(\D{1,12})_(\d{4})+_(\d{1,2})_(\d{1,2})_(\d{1,2})_(\d{3})+', event_id)
            
            monthDict = {'januari' : 1,'februari' : 2,'maart' : 3,'april' : 4,'mei' : 5,'juni' : 6,'juli' : 7,'augustus' : 8,'september' : 9, 'oktober' : 10,'november' : 11,'december' : 12}
            
            year = int(matches.group(3))
            month = int(monthDict[matches.group(2)])
            day = int(matches.group(1))
            hour = int(matches.group(4))
            minute = int(matches.group(5))
            second = int(matches.group(6))
            millisecond = int(matches.group(7))
            
            result = datetime.datetime(year, month, day, hour, minute, second, millisecond)
            
            return result
        
        
        columns = ['bedtime','intended_bedtime','risetime','rise_reason','fitness','adherence_importance','in_experimental_group']
        dataresult = pd.DataFrame(columns=columns)
        
        for file in filenames:    
            with open(file) as f:
                lines = [line.rstrip('\n') for line in f]
                for line in lines: 
                    line_values = line.split(';')
                    user_id = int(re.search(r'\d+',line_values[1]).group())
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
                            
                    if event == 'rise_reason':
                        dataresult = dataresult.set_value(index, 'rise_reason', value) 
                        
                    if(event == 'lamp_change' and value == '"OFF"'):
                        time = getTimeFromLampChange(event_id)
                        #Check whether the bedtime doesn't belong to the day before
                        if int(time.strftime('%H')) < 6:
                            dtime = dtime - datetime.timedelta(hours = 24)                      
                            index = (dtime,user_id)
                        #Checker whether the (possibly) changed index was already created for the user_id
                        if index not in dataresult:
                            dataresult = insert_if_new(dataresult,index)
                        
                        dateAtIndex = dataresult.ix[index,'bedtime']
                        #Just replace 'bedtime' when the time is later then a current registered time! 
                        #OR no time at all yet in cell!
                        if type(dateAtIndex) == float:
                            dataresult = dataresult.set_value(index, 'bedtime', time) 
                        elif(time<dateAtIndex):
                            dataresult = dataresult.set_value(index, 'bedtime', time) 
                    
                    if event == 'nudge_time':
                        dataresult = dataresult.set_value(index, 'in_experimental_group', True)
                    
                    if(event == 'fitness'):
                        dataresult = dataresult.set_value(index, 'fitness', value) 
                                    
                    if(event == 'adherence_importance'):
                        dataresult = dataresult.set_value(index, 'adherence_importance', value) 
                        
        return dataresult
    
#%%    
    
import pymongo, datetime
 
    client = pymongo.MongoClient("localhost", 27017)
    db = client['BigData'] 
    sleepdata = db['sleepdata'] 
    
    sleepdatatest = db['sleepdatatest']
    
    #Convert tuple index to dict (doesn't work as expected, namely less indexes)
    #converted_index = dict((x, y) for x, y in dataresult.index.values)
    
    for i in range(0,len(dataresult)):
        
    
    #Convert tuple to string:
    dataresult.index=dataresult.index.map(str)
    
    
    #Storing (i think this works, only the part of the index doesn't work)
    for i in range(0,len(dataresult)):
        sleepdatatest.insert_one({'date':str(dataresult.index[i][0]),\
                                  'user':str(dataresult.index[i][1]),\
                          'bedtime': dataresult['bedtime'][i],\
                          'intended_bedtime' : dataresult['intended_bedtime'][i],\
                          'risetime' : dataresult['risetime'][i],\
                          'rise_reason' : dataresult['rise_reason'][i],\
                          'fitness' : dataresult['fitness'][i],\
                          'adherence_importance' : dataresult['adherence_importance'][i],\
                          'in_experimental_group' : dataresult['in_experimental_group'][i]})
    sleepdatatest.create_index([('date',pymongo.DESCENDING)
                                ,('user',pymongo.ASCENDING)]
                                ,unique=True)
        #sleepdatatest.create_index([converted_index[i][0], converted_index[i][1]])
   
    #Clearing a database, but doesn't work always i think
    sleepdata = sleepdata.dropDatabase
    
    for doc in sleepdatatest.find():
        print(doc)
        
    sleepdatatest.get_id()
       
    sleepDuration = dataresult['risetime'][2] - dataresult['bedtime'][2]
    
def to_mongodb(df):
    import pymongo, datetime
    from pymongo import MongoClient
 
    client = pymongo.MongoClient("localhost", 27017)
    db = client['BigData'] 
    sleepdata = db['sleepdata']
    sleepdata.delete_many({})
    
    for i in range(0,len(dataresult)):
        if type(dataresult['risetime'][i]) != float and type(dataresult['bedtime'][i]) != float:
            #sleepDuration = df['risetime'][i] - df['bedtime'][i]
            sleepDuration = 
        else: 
            sleepDuration = 0
        
        x['_id'] = {'date': dataresult.index[i][0], 'user': dataresult.index[i][1]}
        
        sleepdata.insert_one({'id':x,\
                                'date':str(dataresult.index[i][0]),\
                                  'user':str(dataresult.index[i][1]),\
                              'bedtime': dataresult['bedtime'][i],\
                              'intended_bedtime' : dataresult['intended_bedtime'][i],\
                              'risetime' : dataresult['risetime'][i],\
                              'rise_reason' : dataresult['rise_reason'][i],\
                              'fitness' : dataresult['fitness'][i],\
                              'adherence_importance' : dataresult['adherence_importance'][i],\
                              'in_experimental_group' : dataresult['in_experimental_group'][i],\
                              'sleep_duration' : sleepDuration})
        
    
    sleepdata.create_index([('date',pymongo.DESCENDING)
                                ,('user',pymongo.ASCENDING)]
                                ,unique=True)
    
def read_mongodb(filter,sort):
    for doc in sleepdata.find():
        print(doc)


if __name__ == '__main__':
    # this code block is run if you run solution.py (instead of run_solution.py)
    # it is convenient for debugging

    df = read_csv_data(["hue_upload.csv","hue_upload2.csv"])
    # to_mongodb(df)
    # read_mongodb({},'_id')
