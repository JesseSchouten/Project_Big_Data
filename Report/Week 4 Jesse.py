# -*- coding: utf-8 -*-
"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Yannick Hogebrug  y.r.hogebrug@student.vu.nl
Jesse Schouten j7.schouten@student.vu.nl
"""

"""
This template is meant as a guideline. Feel free to alter existing functions and add new functions.
Remember to use descriptive variable names and to keep functions concise and readable.
"""

"""
The main() function is called when template_week_4.py is run from the command line.
It is a good place to define the logic of the data flow (for example, reading, transforming, analyzing, visualizing).
"""
import os
os.chdir("C:/Users/Jesse/Documents/Github/Project_Big_Data/Report")

import pandas as pd
import numpy as np
import scipy.stats as ss
import statsmodels.api as sm
import matplotlib.pyplot as plt 

def createNewDataframe(sleepdatafile, surveydatafile): 
    def isBiggerThenZero(x):
        if x > 0:
            return 1
        else:
            return 0
    
    #source:https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-in-python
    def isnan(value):
      try:
          import math
          return math.isnan(float(value))
      except:
          return False
    
    def insert_if_new(df,idx):
        if idx not in df.index:
            df = df.append(pd.Series({'group' : float('nan'),\
                                      'delay_nights' : float('nan'),\
                                      'delay_time' : float('nan')},\
                                      name=idx))
        return df
    
    columns = ['group','delay_nights','delay_time']
    dataresult = pd.DataFrame(columns=columns)
    
    for row_index,row in week4Data.iterrows():
        index = row["ID"] 
        
        if index not in dataresult:
            dataresult = insert_if_new(dataresult,index)
        condition = row[1]
        dataresult = dataresult.set_value(index,'group',condition)
        
        delayNights=0
        for i in [5,15,25,35,45,55,65,75,85,95,105,115]:
            delayNights += isBiggerThenZero(row[i]) 
        dataresult = dataresult.set_value(index,'delay_nights',delayNights)
        
        delayTime = 0.0
        days = 0
        for i in [5,15,25,35,45,55,65,75,85,95,105,115]:
            if isBiggerThenZero(row[i]) == 1:
                delayTime += row[i]
            if not isnan(row[i]):
                days +=1
        if days != 0:
            dataresult = dataresult.set_value(index,'delay_time',int(round(delayTime/days)))
        
    return dataresult

def mergeDataframes(frame1,frame2):
    import pandas as pd
    
    return pd.merge(frame1,frame2, how = 'inner',left_index = True,right_index=True)
    
def correlate(x, y, test_type):
    x = np.array(x)
    y=np.array(y)

    if test_type == 'pearson':
        r,p = ss.pearsonr(x,y)
    elif test_type == 'kendall':
        r,p = ss.kendalltau(x,y)
    else: 
        return 'Choose valid test method'
    
    return [r,p]

def compare(x, y, test_type = 'ttest'):
    None

def regress(target, predictors):
    None
    
#def visualize():
    

    
sleepdatafile = 'hue_week_4_2017.csv'
surveydatafile = 'hue_questionnaire.csv'
week4Data = pd.read_csv(sleepdatafile,delimiter = ';')
questionnaireData = pd.read_csv(surveydatafile, delimiter = ',')

newDataframe = createNewDataframe(sleepdatafile,questionnaireData)

questionnaireData = questionnaireData.set_index('ID')
week4Data = week4Data.set_index('ID')
mergedData = mergeDataframes(questionnaireData,newDataframe)

x = mergedData[['bp_scale','delay_time']].dropna()['bp_scale']
y = mergedData[['bp_scale','delay_time']].dropna()['delay_time']
correlate(x,y,'pearson')

x = mergedData[['age','delay_time']].dropna()['age']
y = mergedData[['age','delay_time']].dropna()['delay_time']
correlate(x,y,'kendall')

x = mergedData[['daytime_sleepiness','delay_time']].dropna()['daytime_sleepiness']
y = mergedData[['daytime_sleepiness','delay_time']].dropna()['delay_time']
correlate(x,y,'pearson')


#Histogram of delay nights
print(mergedData.query('group==1')['delay_nights'].mean())
print(np.std(mergedData.query('group==1')['delay_nights']))
print(np.median(mergedData.query('group==1')['delay_nights']))

print(mergedData.query('group==0')['delay_nights'].mean())
print(np.std(mergedData.query('group==0')['delay_nights']))
print(np.median(mergedData.query('group==0')['delay_nights']))

x=mergedData['delay_nights'].dropna().astype(int)
plt.hist(x, label = 'Delay nights')
plt.legend(loc = 'upper right')
plt.suptitle("Histogram of delay nights")
plt.xlabel('Number of delay nights')
plt.ylabel('Frequency')
plt.show()

#Histogram of time participants spent in bed each night
    #the condition column in week4Data is the 'group' in the mergedData file
def getBedtimes(query):     
    result = []    
        #source:https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-in-python
    def isnan(value):
      try:
          import math
          return math.isnan(float(value))
      except:
          return False
    
    for row_index,row in query.iterrows():
        for i in [7,17,27,37,47,57,67,77,87,97,107,117]:
            if not isnan(row[i]):
                result.append(row[i]) 
           
    return result
        

queryGroup0 = week4Data.query('Condition==0')
queryGroup1 = week4Data.query('Condition==1')

sleeptimesGroup0 = pd.DataFrame(getBedtimes(queryGroup0))
sleeptimesGroup0.columns = ['Inbedtimes']
sleeptimesGroup1 = pd.DataFrame(getBedtimes(queryGroup1))
sleeptimesGroup1.columns = ['Inbedtimes']

print(sleeptimesGroup0.mean())
print(np.std(sleeptimesGroup0))
print(np.median(sleeptimesGroup0))

print(sleeptimesGroup1.mean())
print(np.std(sleeptimesGroup1))
print(np.median(sleeptimesGroup1))


#Histogram of mean time participants spent delaying their bedtime
print(mergedData.query('group==1')['delay_time'].mean())
print(np.std(mergedData.query('group==1')['delay_time']))
print(np.median(mergedData.query('group==1')['delay_time']))

print(mergedData.query('group==0')['delay_time'].mean())
print(np.std(mergedData.query('group==0')['delay_time']))
print(np.median(mergedData.query('group==0')['delay_time']))

y= mergedData['delay_time'].dropna().astype(int)
plt.hist(y, label = 'Delay time')
plt.legend(loc = 'upper right')
plt.suptitle("Histogram of delay time")
plt.xlabel('Delay time in seconds')
plt.ylabel('Frequency')
plt.show()

results = smf.ols('delay_time ~ age + chronotype + motivation', data=mergedData).fit()
    
group1data = mergedData.groupby(['group'])



def calculateDifferenceInGroups(df):
    

"""
Tip: create one function per visualization, and call those functions from the main visualize() function.
"""


def main():


#Is executed when main() is called
if __name__ == '__main__':
    main()

    