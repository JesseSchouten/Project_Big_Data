"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Yannick Hogebrug  y.r.hogebrug@student.vu.nl
Jesse Schouten j7.schouten@student.vu.nl
"""
        
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
                #if someone expects to sleep between 6:00 and 13:00, he/she problably mean the evening
                if hour >=6 and hour <= 12:
                    hour += 12
                elif hour > 12 and hour < 13:
                    hour -= 12
                #Check if the time is set at 24:00, and change to 0:00
                elif hour == 24:
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
                
                if event == 'nudge_time':
                    dataresult = dataresult.set_value(index, 'in_experimental_group', True)
                
                if(event == 'fitness'):
                    dataresult = dataresult.set_value(index, 'fitness', value) 
                                
                if(event == 'adherence_importance'):
                    dataresult = dataresult.set_value(index, 'adherence_importance', value) 
                    
    return dataresult
    
#%%        
#Returns a filled mongodb (if we wouldn't do this it would only exist in the function)
def to_mongodb(df):
    import pymongo, datetime,pytz
    from pymongo import MongoClient
    
    tz= pytz.timezone('Europe/Amsterdam')
 
    client = pymongo.MongoClient("localhost", 27017)
    db = client['BigData'] 
    sleepdata = db['sleepdata']
    sleepdata.delete_many({})
    
    for i in range(0,len(df)):
       # if type(dataresult['risetime'][i]) != float and type(dataresult['bedtime'][i]) != float:
       #     #sleepDuration = df['risetime'][i] - df['bedtime'][i]
       #     sleepDuration = 
       # else: 
       #     sleepDuration = 0
        
        if isinstance(df['bedtime'][i],datetime.datetime) and \
            isinstance(df['risetime'][i], datetime.datetime):
            #time slept = time in a day - time awake
            sleepDuration = 86400 - round((df['bedtime'][i] - df['risetime'][i]).total_seconds(), 0) 
            
        else:
            sleepDuration = float('nan')
                        
        x = {}
        x['_id'] = {'date': df.index[i][0], 'user': df.index[i][1]}
        
        sleepdata.insert_one({'_id':x,\
                      'date':df.index[i][0],\
                      'user':df.index[i][1],\
                      'bedtime': df['bedtime'][i],\
                      'intended_bedtime' : df['intended_bedtime'][i],\
                      'risetime' : df['risetime'][i],\
                      'rise_reason' : df['rise_reason'][i],\
                      'fitness' : df['fitness'][i],\
                      'adherence_importance' : df['adherence_importance'][i],\
                      'in_experimental_group' : df['in_experimental_group'][i],\
                      'sleep_duration' : sleepDuration})
        
        #sleepdata.aggregate(query) [met dit volgt een error!]
    
    return sleepdata
         
"""           
            query = [{
                '$project': {
                        '_id': 1,
                        'sleep_duration': { 
                                '$divide': [
                                        {'$subtract': ['$risetime', '$bedtime']},
                                        1000
                                        ] 
                                        } 
                            }
            }]
                        
        else:                
            query = [{
                '$project': {
                        '_id': 1,
                        'sleep_duration': {
                                '$divide': [
                                        0, 
                                        1
                                        ]
                                        }
                            }
            }]
"""  
        
    #sleepdata.create_index([('date',pymongo.DESCENDING)
    #                           ,('user',pymongo.ASCENDING)]
    #                          ,unique=True)

#assumes the database is named sleepdata
def read_mongodb(filter,sort):
    import pymongo
    from pymongo import MongoClient
    import pprint
    import re as re
    import time
    
    def isNan(var):
        return isinstance(var,float)
    
    for doc in sleepdata.find():
        print(doc)
    
    query = sleepdata.find(filter)

    matches = re.search(r'(_id|date|user|bedtime|intended_bedtime|risetime|rise_reason|fitness|adherence_importance|in_experimental_group|sleep_duration)',sort)         

    if matches:
        printedQuery = query.sort(sort,pymongo.ASCENDING)
    else: 
        printedQuery = query      
        
    print('date\t'
          ,'user\t'
          ,'bedtime\t'
          ,'intended\t'
          ,'risetime\t'
          ,'reason\t'
          ,'fitness\t'
          ,'adh\t'
          ,'in_exp\t'
          ,'sleep_duration')
    
    for document in printedQuery:                          
        date = str(document['date'].date())
        user = str(document['user'])
        
        if isNan(document['bedtime']):       
            bedtime = str(document['bedtime'])
        else: 
             bedtime = str(document['bedtime'].time())
        
        if isNan(document['intended_bedtime']):
            int_bedtime = str(document['intended_bedtime'])
        else:    
            int_bedtime = str(document['intended_bedtime'].time()) 
            
        if isNan(document['risetime']):
            risetime = str(document['risetime'])
        else: 
            risetime = str(document['risetime'].time())     
        
        rise_reason = str(document['rise_reason'])
        fitness = str(document['fitness'])
        adh_importance = str(document['adherence_importance'])
        in_exp_group = str(document['in_experimental_group'] )
        sleep_duration = str(document['sleep_duration'])

        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" %
              (date
              ,user
              ,bedtime
              ,int_bedtime
              ,risetime
              ,rise_reason
              ,fitness
              ,adh_importance
              ,in_exp_group
              ,sleep_duration))

if __name__ == '__main__':
    # this code block is run if you run solution.py (instead of run_solution.py)
    # it is convenient for debugging

    df = read_csv_data(["hue_upload.csv","hue_upload2.csv"])
    # to_mongodb(df)
    # read_mongodb({},'_id')
