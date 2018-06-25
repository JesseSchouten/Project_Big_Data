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
#%%
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
                                      'delay_time' : float('nan'),\
                                      'sleep_time' : float('nan')},\
                                      name=idx))
        return df
    
    columns = ['group','delay_nights','delay_time','sleep_time']
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
            #Negative delaytimes are considered as 0.
            if isBiggerThenZero(row[i]) == 1:
                delayTime += row[i]
            if not isnan(row[i]):
                days +=1
        if days != 0:
            dataresult = dataresult.set_value(index,'delay_time',int(round(delayTime/days)))
            
        sleepTime = 0.0
        days = 0
        for i in [8,18,28,38,48,58,68,78,88,98,108,118]:
            #if we encounter a negative sleeptime, consider it as a NaN, as it's a clear measurement failure
            if isBiggerThenZero(row[i]) == 1:
                sleepTime += row[i]
            if not isnan(row[i]) and isBiggerThenZero(row[i]) == 1:
                    days+=1
        if days != 0:
            dataresult = dataresult.set_value(index,'sleep_time',int(round(sleepTime/days)))        
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
    
def visualize():  
    #Histogram of delay nights
    delay_nights_0 = mergedData.query('group==0')['delay_nights'].astype(int)
    
    f = plt.figure(figsize=(10,6))
    plt.suptitle("Histograms of delay nights", fontsize = 16, fontweight = 'bold')
    
    ax1 = f.add_subplot(121)
    ax1.title.set_text("Control group")
    plt.hist(delay_nights_0, bins=range(0, max(delay_nights_0) + 1, 1), color = 'blue', label = 'Control group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Number of delay nights')
    plt.ylabel('Frequency')
    #plt.show()
    
    ax2 = f.add_subplot(122)
    ax2.title.set_text("Experimental group")
    delay_nights_1 = mergedData.query('group==1')['delay_nights'].astype(int)
    plt.hist(delay_nights_1, bins=range(0, max(delay_nights_1) + 1, 1), color = 'blue', label = 'Experimental group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Number of delay nights')
    plt.ylabel('Frequency')
    plt.show()
    
    print('mean delay_nights (control):', mergedData.query('group==0')['delay_nights'].mean())
    print('SD delay_nights (control):',np.std(mergedData.query('group==0')['delay_nights']))
    print('median delay_nights (control):', np.median(mergedData.query('group==0')['delay_nights']))
    
    print('mean delay_nights (experimental):', mergedData.query('group==1')['delay_nights'].mean())
    print('SD delay_nights (experimental):',np.std(mergedData.query('group==1')['delay_nights']))
    print('median delay_nights (experimental):',np.median(mergedData.query('group==1')['delay_nights']))
    
    
    sm.qqplot(delay_nights_0)
    plt.title("QQ-plot delay nights vs. N(0,1) (control group)")
    pylab.show()
    
    sm.qqplot(delay_nights_1)
    plt.title("QQ-plot delay nights vs. N(0,1) (experimental group)")
    pylab.show()
    
    print(ss.ranksums(delay_nights_0, delay_nights_1))
    
    #Histogram of time participants spent in bed each night
    
    sleep_time_0 = (mergedData.query('group==0')['sleep_time'].dropna()/3600).astype(float)
    
    f = plt.figure(figsize=(10,6))
    plt.suptitle("Histograms of sleep time", fontsize = 16, fontweight = 'bold')
    
    ax1 = f.add_subplot(121)
    ax1.title.set_text("Control group")   
    plt.hist(sleep_time_0, bins=[6,7,8,9,10], color = 'blue', label = 'Control group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Sleep time in hours')
    plt.ylabel('Frequency')
    #plt.show()
    
    ax2 = f.add_subplot(122)
    ax2.title.set_text("Experimental group")
    sleep_time_1 = (mergedData.query('group==1')['sleep_time'].dropna()/3600).astype(float) 
    plt.hist(sleep_time_1, bins=[6,7,8,9,10], color = 'blue', label = 'Experimental group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Sleep time in hours')
    plt.ylabel('Frequency')
    plt.show()
    
    print('mean sleep_time (control):',mergedData.query('group==0')['sleep_time'].mean())
    print('SD sleep_time (control):',np.std(mergedData.query('group==0')['sleep_time']))
    print('median sleep_time (control):',np.median(mergedData.query('group==0')['sleep_time']))
    
    print('mean sleep_time (experimental):',mergedData.query('group==1')['sleep_time'].mean())
    print('SD sleep_time (experimental):',np.std(mergedData.query('group==1')['sleep_time']))
    print('median sleep_time (experimental):',np.median(mergedData.query('group==1')['sleep_time']))
    
    sm.qqplot(sleep_time_0)
    plt.title("QQ-plot sleep time vs. N(0,1) (control group)")
    pylab.show()
    
    sm.qqplot(sleep_time_1)
    plt.title("QQ-plot sleep time vs. N(0,1) (experimental group)")
    pylab.show()
    
    print(ss.ranksums(sleep_time_0, sleep_time_1))
    
    
    #Histogram of mean time participants spent delaying their bedtime
    delay_time_0 = (mergedData.query('group==0')['delay_time'].dropna()).astype(int) 
    
    f = plt.figure(figsize=(10,6))
    plt.suptitle("Histograms of delay time", fontsize = 16, fontweight = 'bold')
    
    ax1 = f.add_subplot(121)
    ax1.title.set_text("Control group")
    plt.hist(delay_time_0, bins=range(0, max(delay_time_0) + 1000, 1000), color = 'blue', label = 'Control group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Delay time')
    plt.ylabel('Frequency')
    #plt.show()

    ax2 = f.add_subplot(122)
    ax2.title.set_text("Experimental group")
    delay_time_1 = (mergedData.query('group==1')['delay_time'].dropna()).astype(int) 
    plt.hist(delay_time_1, bins=range(0, max(delay_time_1) + 1000, 1000), color = 'lime', label = 'Experimental group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Number of delay nights')
    plt.ylabel('Frequency')
    plt.show()
    
    print('mean delay_time (control):',mergedData.query('group==0')['delay_time'].mean())
    print('SD delay_time (control):',np.std(mergedData.query('group==0')['delay_time']))
    print('median delay_time (control):',np.median(mergedData.query('group==0')['delay_time']))
    
    print('mean delay_time (experimental):',mergedData.query('group==1')['delay_time'].mean())
    print('SD delay_time (experimental):',np.std(mergedData.query('group==1')['delay_time']))
    print('median delay_time (experimental):',np.median(mergedData.query('group==1')['delay_time']))
    
    sm.qqplot(delay_time_0)
    plt.title("QQ-plot delay time vs. N(0,1) (control group)")
    pylab.show()
    
    sm.qqplot(delay_time_1)
    plt.title("QQ-plot delay time vs. N(0,1) (experimental group)")
    pylab.show()
    
    print(ss.ranksums(delay_time_0, delay_time_1))
    
    
#%%   
#First, load the functions above as they are used in the main() program
def main():
    print('Open the file and run the code by hand!')
    
import pandas as pd
import numpy as np
import scipy.stats as ss
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt 
import pylab as pylab

sleepdatafile = 'hue_week_4_2017.csv'
surveydatafile = 'hue_questionnaire.csv'
week4Data = pd.read_csv(sleepdatafile,delimiter = ';')
questionnaireData = pd.read_csv(surveydatafile, delimiter = ',')

newDataframe = createNewDataframe(sleepdatafile,questionnaireData)

questionnaireData = questionnaireData.set_index('ID')
week4Data = week4Data.set_index('ID')
mergedData = mergeDataframes(questionnaireData,newDataframe)

#Correlation of sets of determinants, as suggested in the exercise
x = mergedData[['bp_scale','delay_time']].dropna()['bp_scale']
y = mergedData[['bp_scale','delay_time']].dropna()['delay_time']
print('pearson correlation bp_scale & delay_time: ',correlate(x,y,'pearson'))

x = mergedData[['age','delay_time']].dropna()['age']
y = mergedData[['age','delay_time']].dropna()['delay_time']
print('kendall correlation age & delay_time: ',correlate(x,y,'kendall'))

x = mergedData[['daytime_sleepiness','delay_time']].dropna()['daytime_sleepiness']
y = mergedData[['daytime_sleepiness','delay_time']].dropna()['delay_time']
print('pearson correlation daytime_sleepiness & delay_time: ',correlate(x,y,'pearson'))

visualize()

#Regression model:
lin_regr = mergedData[['delay_time','gender', 'chronotype', 'bp_scale', 'motivation','delay_nights']].dropna().astype(int)
mod = smf.ols(formula = 'delay_time ~ chronotype + bp_scale + delay_nights' , data=lin_regr)
res = mod.fit()
print(res.summary())

#Regression model:
lin_regr = mergedData[['delay_time','gender','group', 'chronotype', 'bp_scale', 'motivation','delay_nights']].dropna().astype(int)
mod = smf.ols(formula = 'delay_time ~ group' , data=lin_regr)
res = mod.fit()
print(res.summary())

import seaborn as sns
sns.set()
df = mergedData[['delay_time', 'gender', 'age', 'chronotype', 'bp_scale', 'motivation', 'daytime_sleepiness', 'self_reported_effectiveness', 'group', 'delay_nights', 'sleep_time']]
sns.pairplot(df)

male = (mergedData.query('gender==1')['sleep_time'].dropna()/3600).astype(float)
female = (mergedData.query('gender==2')['sleep_time'].dropna()/3600).astype(float)
 
#Density plot:
male.plot(kind='density', color = 'blue',label = 'Male')
female.plot(kind='density',color = 'deeppink',label = 'Female')
plt.suptitle("Density plot of the sleeptimes of both males and females")
plt.legend(loc = 'upper right')
plt.xlabel('Sleeptime')
plt.ylabel('Density')
plt.show()

#correlation plot:

#https://stackoverflow.com/questions/29432629/correlation-matrix-using-pandas
import seaborn as sns

#https://www.spss-tutorials.com/pearson-correlation-coefficient/ also suitable for dichtomious variables
pearsondf =mergedData[['delay_time','sleep_time','gender','bp_scale',]].dropna().astype(int)

f, ax = plt.subplots(figsize=(10, 8))
corr = pearsondf.corr()
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool),annot=True, cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax,)
ax.set_title('Heatmap of pearson correlation between variables in data',fontsize = 20)
plt.show()

kendalldf = mergedData[['delay_time','age','chronotype','motivation','daytime_sleepiness','self_reported_effectiveness','group','delay_nights']].dropna().astype(int)

f, ax = plt.subplots(figsize=(10, 8))
corr = kendalldf.corr(method = 'kendall')
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool),annot=True, cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax,)
ax.set_title('Heatmap of kendall correlation between variables in data',fontsize = 20)
plt.show()




#%%


    #the condition column in week4Data is the 'group' in the mergedData file
#def getBedtimes(query):     
#    result = []    
#        #source:https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-in-python
#    def isnan(value):
#      try:
#          import math
#          return math.isnan(float(value))
#      except:
#          return False
#    
#    for row_index,row in query.iterrows():
#        for i in [7,17,27,37,47,57,67,77,87,97,107,117]:
#            if not isnan(row[i]):
#                result.append(row[i]) 
#           
#    return result
     
#    #Histogram of time participants spent in bed each night
#    queryGroup0 = week4Data.query('Condition==0')
#    sleeptimesGroup0 = pd.DataFrame(getBedtimes(queryGroup0))
#    sleeptimesGroup0.columns = ['Inbedtimes']
#    
#    sleeptime_0 = (sleeptimesGroup0['Inbedtimes'].dropna()/3600).astype(float)
#    plt.hist(sleeptime_0, bins=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5], color = 'blue', label = 'Control group')
#    plt.legend(loc = 'upper right')
#    plt.suptitle("Histogram of sleeptime (Control group)")
#    plt.xlabel('Sleep time')
#    plt.ylabel('Frequency')
#    plt.show()
#    
#    queryGroup1 = week4Data.query('Condition==1')
#    sleeptimesGroup1 = pd.DataFrame(getBedtimes(queryGroup1))
#    sleeptimesGroup1.columns = ['Inbedtimes']
#    
#    sleeptime_1 = (sleeptimesGroup1['Inbedtimes'].dropna()/3600).astype(float)
#    plt.hist(sleeptime_1, bins=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5], color = 'blue', label = 'Experimental group')
#    plt.legend(loc = 'upper right')
#    plt.suptitle("Histogram of sleeptime (Experimental group)")
#    plt.xlabel('Sleep time')
#    plt.ylabel('Frequency')
#    plt.show()
#    
#    print(sleeptimesGroup0.mean())
#    print(np.std(sleeptimesGroup0))
#    print(np.median(sleeptimesGroup0))
#    
#    print(sleeptimesGroup1.mean())
#    print(np.std(sleeptimesGroup1))
#    print(np.median(sleeptimesGroup1))



"""
Tip: create one function per visualization, and call those functions from the main visualize() function.
""


#Is executed when main() is called
if __name__ == '__main__':
    main()

    