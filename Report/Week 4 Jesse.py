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
    
def visualize_delay_nights():  
    
    #Histogram of delay nights
    delay_nights_0 = mergedData.query('group==0')['delay_nights'].astype(int)
    delay_nights_1 = mergedData.query('group==1')['delay_nights'].astype(int)
    
    f = plt.figure(figsize=(10,6))
    plt.suptitle("Histograms of delay nights", fontsize = 16, fontweight = 'bold')
    
    ax1 = f.add_subplot(121)
    ax1.title.set_text("Control group")
    plt.hist(delay_nights_0, bins=range(0, max(delay_nights_0) + 1, 1), color = 'blue', edgecolor='black', linewidth=1.2, label = 'Control group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Number of delay nights')
    plt.ylabel('Frequency')
    #plt.show()
    
    ax2 = f.add_subplot(122)
    ax2.title.set_text("Experimental group")
    plt.hist(delay_nights_1, bins=range(0, max(delay_nights_1) + 1, 1), color = 'lime', edgecolor='black', linewidth=1.2, label = 'Experimental group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Number of delay nights')
    plt.ylabel('Frequency')
    #plt.savefig('delaynightsHist.pdf')
    plt.show()
    
    print('mean delay_nights (control):', delay_nights_0.mean())
    print('SD delay_nights (control):',np.std(delay_nights_0))
    print('median delay_nights (control):', np.median(delay_nights_0))
    
    print('mean delay_nights (experimental):', delay_nights_1.mean())
    print('SD delay_nights (experimental):',np.std(delay_nights_1))
    print('median delay_nights (experimental):',np.median(delay_nights_1))
    
    sm.qqplot(delay_nights_0)
    plt.title("QQ-plot delay nights vs. N(0,1) (control group)")
    pylab.show()
    
    sm.qqplot(delay_nights_1)
    plt.title("QQ-plot delay nights vs. N(0,1) (experimental group)")
    pylab.show()
    
    print(ss.ranksums(delay_nights_0, delay_nights_1))
    
def visualize_sleep_time():      
    #Histogram of time participants spent in bed each night
    #in hours:
    #sleep_time_0 = (mergedData.query('group==0')['sleep_time'].dropna()/3600).astype(float)
    #sleep_time_1 = (mergedData.query('group==1')['sleep_time'].dropna()/3600).astype(float) 
    
    #in seconds:
    sleep_time_0 = (mergedData.query('group==0')['sleep_time'].dropna()).astype(float)
    sleep_time_1 = (mergedData.query('group==1')['sleep_time'].dropna()).astype(float)
    
    f = plt.figure(figsize=(10,6))
    plt.suptitle("Histograms of sleep time", fontsize = 16, fontweight = 'bold')
    
    ax1 = f.add_subplot(121)
    ax1.title.set_text("Control group")   
    plt.hist(sleep_time_0,color = 'blue', label = 'Control group', edgecolor='black', linewidth=1.2)
    plt.legend(loc = 'upper right')
    plt.xlabel('Sleep time in seconds')
    plt.ylabel('Frequency')
    
    ax2 = f.add_subplot(122)
    ax2.title.set_text("Experimental group")
    plt.hist(sleep_time_1, color = 'lime', label = 'Experimental group', edgecolor='black', linewidth=1.2)
    plt.legend(loc = 'upper right')
    plt.xlabel('Sleep time in seconds')
    plt.ylabel('Frequency')
    #plt.savefig('sleeptimeHist.pdf')
    plt.show()
    
    print('mean sleep_time (control):',sleep_time_0.mean())
    print('SD sleep_time (control):',np.std(sleep_time_0))
    print('median sleep_time (control):',np.median(sleep_time_0))
    
    print('mean sleep_time (experimental):',sleep_time_1.mean())
    print('SD sleep_time (experimental):',np.std(sleep_time_1))
    print('median sleep_time (experimental):',np.median(sleep_time_1))
    
    sm.qqplot(sleep_time_0)
    plt.title("QQ-plot sleep time vs. N(0,1) (control group)")
    pylab.show()
    
    sm.qqplot(sleep_time_1)
    plt.title("QQ-plot sleep time vs. N(0,1) (experimental group)")
    pylab.show()
    
    print(ss.ranksums(sleep_time_0, sleep_time_1))
    
def visualize_delay_time():      
    #Histogram of mean time participants spent delaying their bedtime
    delay_time_0 = (mergedData.query('group==0')['delay_time'].dropna()).astype(int) 
    delay_time_1 = (mergedData.query('group==1')['delay_time'].dropna()).astype(int) 
    
    f = plt.figure(figsize=(10,6))
    plt.suptitle("Histograms of delay time", fontsize = 16, fontweight = 'bold')
    
    ax1 = f.add_subplot(121)
    ax1.title.set_text("Control group")
    plt.hist(delay_time_0, bins=range(0, max(delay_time_0) + 1000, 1000), color = 'blue', edgecolor='black', linewidth=1.2, label = 'Control group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Delay time')
    plt.ylabel('Frequency')
    #plt.show()

    ax2 = f.add_subplot(122)
    ax2.title.set_text("Experimental group")
    plt.hist(delay_time_1, bins=range(0, max(delay_time_1) + 1000, 1000), color = 'lime', edgecolor='black', linewidth=1.2, label = 'Experimental group')
    plt.legend(loc = 'upper right')
    plt.xlabel('Delay time')
    plt.ylabel('Frequency')
    plt.savefig('delaytimeHist.pdf')
    plt.show()
    
    print('mean delay_time (control):',delay_time_0.mean())
    print('SD delay_time (control):',np.std(delay_time_0))
    print('median delay_time (control):',np.median(delay_time_0))
    
    print('mean delay_time (experimental):',delay_time_1.mean())
    print('SD delay_time (experimental):',np.std(delay_time_1))
    print('median delay_time (experimental):',np.median(delay_time_1))
    
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
import seaborn as sns

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

visualize_delay_nights()
visualize_sleep_time()
visualize_delay_time()

#Regression model:
mod = smf.ols(formula = 'delay_time ~ chronotype + bp_scale + group' , data=mergedData.dropna().astype(float))
res = mod.fit()
print(res.summary())

sns.set()
df = mergedData[['delay_time', 'age', 'bp_scale', 'daytime_sleepiness']]
pplot = sns.pairplot(df)
plt.subplots_adjust(top=0.95)
pplot.fig.suptitle('Pairwise scatterplots',fontsize=16,fontweight = 'bold')
plt.show(pplot)

#Line chart of chronotype
#source: https://seaborn.pydata.org/tutorial/categorical.html
visualisationdf = mergedData[['chronotype','group','delay_time']]
visualisationdf['Delay_time_in_hours'] = visualisationdf['delay_time'] / 3600
visualisationdf.dropna()
ax = sns.swarmplot(x="chronotype", y="Delay_time_in_hours", hue="group", data=visualisationdf).set_title("Delaytime vs chronotype (per group)");
plt.xlabel("Chronotype")
plt.ylabel("Delay time in hours")
plt.show(ax)

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


##Density plot of sleeptime for males and females:
#male = (mergedData.query('gender==1')['sleep_time'].dropna()/3600).astype(float)
#female = (mergedData.query('gender==2')['sleep_time'].dropna()/3600).astype(float)
# 
#male.plot(kind='density', color = 'blue',label = 'Male')
#female.plot(kind='density',color = 'deeppink',label = 'Female')
#plt.suptitle("Density plot of the sleeptimes", fontsize = 16, fontweight = 'bold')
#plt.legend(loc = 'upper right')
#plt.xlabel('Sleeptime in hours')
#plt.ylabel('Density')
#plt.show()
#
##Density plot of sleeptime for both groups:
#group0 = (mergedData.query('group==0')['sleep_time'].dropna()/3600).astype(float)
#group1 = (mergedData.query('group==1')['sleep_time'].dropna()/3600).astype(float)
# 
#group0.plot(kind='density', color = 'blue',label = 'Control')
#group1.plot(kind='density',color = 'deeppink',label = 'Experimental')
#plt.suptitle("Density plot of the sleeptimes", fontsize = 16, fontweight = 'bold')
#plt.legend(loc = 'upper right')
#plt.xlabel('Sleeptime in hours')
#plt.ylabel('Density')
#plt.show()

##correlation plot:
#
##https://stackoverflow.com/questions/29432629/correlation-matrix-using-pandas
#
#
##https://www.spss-tutorials.com/pearson-correlation-coefficient/ also suitable for dichtomious variables
#pearsondf =mergedData[['delay_time','sleep_time','gender','bp_scale',]].dropna().astype(int)
#
#f, ax = plt.subplots(figsize=(10, 8))
#corr = pearsondf.corr()
#sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool),annot=True, cmap=sns.diverging_palette(220, 10, as_cmap=True),
#            square=True, ax=ax,)
#ax.set_title('Heatmap of pearson correlation between variables in data',fontsize = 20)
#plt.show()
#
#kendalldf = mergedData[['delay_time','age','chronotype','motivation','daytime_sleepiness','self_reported_effectiveness','group','delay_nights']].dropna().astype(int)
#
#f, ax = plt.subplots(figsize=(10, 8))
#corr = kendalldf.corr()
#sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool),annot=True, cmap=sns.diverging_palette(220, 10, as_cmap=True),
#            square=True, ax=ax,)
#ax.set_title('Heatmap of kendall correlation between variables in data',fontsize = 20)
#plt.show()

#    #Probably usable (in hours)
#    delay_time_0 /= 3600 
#    delay_time_1 /= 3600 
#    
#    delay_time_0.plot(kind='density', color = 'blue',label = 'Control group')
#    delay_time_1.plot(kind='density',color = 'lime',label = 'Experimental group')
#    plt.suptitle("Density plot of the delay times", fontsize = 16, fontweight = 'bold')
#    plt.legend(loc = 'upper right')
#    plt.xlabel('Delay time in hours')
#    plt.ylabel('Density')
#    plt.show()

"""
Tip: create one function per visualization, and call those functions from the main visualize() function.
""


#Is executed when main() is called
if __name__ == '__main__':
    main()

    