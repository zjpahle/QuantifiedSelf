# -*- coding: utf-8 -*-
"""
Created on Tue May 22 17:23:08 2018

@author: pahlza
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

#filePath = 'C:\\Users\pahlza\Desktop\School Stuff\SelfData\QuantifiedSelf\\'
filePath = 'C:\\Users\zjpah\Documents\GitHub\QuantifiedSelf\\'
fileName = 'Nutrition-Summary-2018-01-01-to-2018-06-05.xlsx'

mfpXLS = pd.ExcelFile(os.path.join(filePath, fileName))
mfpFoodData = pd.read_excel(mfpXLS)
mfpFoodData = mfpFoodData.drop('Meal', axis=1)

#combine meals per day
for loop1 in range(len(mfpFoodData.iloc[:,0])-2):
    if (mfpFoodData.iloc[loop1,0] == mfpFoodData.iloc[loop1+1,0]):
        mfpFoodData.iloc[loop1, 1:] = mfpFoodData.iloc[loop1,1:]+mfpFoodData.iloc[loop1+1,1:]
        #mfpFoodData.iloc[loop1+1, 1:] = mfpFoodData.iloc[loop1+1,1:]-mfpFoodData.iloc[loop1+1,1:]
    if (mfpFoodData.iloc[loop1,0] == mfpFoodData.iloc[loop1+2,0]):
        mfpFoodData.iloc[loop1, 1:] = mfpFoodData.iloc[loop1,1:]+mfpFoodData.iloc[loop1+2,1:]
        #mfpFoodData.iloc[loop1+2, 1:] = mfpFoodData.iloc[loop1+2,1:]-mfpFoodData.iloc[loop1+2,1:]
mfpFoodData = mfpFoodData.drop_duplicates(subset='Date', keep='first')
#mfpFoodData = mfpFoodData.reindex(index = range(len(mfpFoodData.iloc[:,0])))


#read in meas data
fileName = 'Exercise-Summary-2018-01-01-to-2018-06-05.xlsx'

mfpMeasXLS = pd.ExcelFile(os.path.join(filePath, fileName))
mfpMeasData = pd.read_excel(mfpMeasXLS)
mfpMeasData = mfpMeasData.drop(mfpMeasData.columns.tolist()[1], axis=1)
mfpMeasData = mfpMeasData.drop_duplicates( keep='first')

#repair weight data
mfpMeasData.loc[:,'Weight'] = mfpMeasData.loc[:,'Weight'].interpolate(method='polynomial', order=2)
mfpMeasData.loc[:,'Weight'] = mfpMeasData.loc[:,'Weight'].fillna(method='bfill')
mfpMeasData.loc[:,'Weight'] = mfpMeasData.loc[:,'Weight'].fillna(method='ffill')

#repair sleep data
mfpMeasData.loc[:,'FB sleep (min)'] = mfpMeasData.loc[:,'FB sleep (min)'].interpolate(method='polynomial', order=2)

mfpData = pd.merge(mfpFoodData, mfpMeasData, how='outer', on='Date', sort=True)
#mfpData.index = pd.to_datetime(mfpData.index)
#mfpData =  mfpData.reindex(mfpData.loc[:,'Date'], method='nearest')
#mfpData = mfpData.sort_values(by='Date')

mfpData = mfpData.fillna(method='bfill')
mfpData = mfpData.fillna(method='ffill')

fig, ax1 = plt.subplots()
color = 'tab:red'

ax1.set_xlabel('Date (Months)')
ax1.set_ylabel('Weight Change (lbs/month)', color=color)
#questionable math
plt.plot(mfpData.loc[:,'Date'], np.gradient(mfpData.loc[:,'Weight']), color=color)
plt.plot(mfpData.loc[:,'Date'], ((mfpData.loc[:,'Calories']-2484)/3600).rolling(14, win_type='blackmanharris').mean(), color='blue')
ax1.tick_params(axis='y', labelcolor=color)

#ax2 = ax1.twinx()
#color = 'tab:blue'
#
#ax2.set_xlabel('Date (Months)')
#ax2.set_ylabel('Steps', color=color)
#plt.plot(mfpData.loc[:,'Date'], mfpData.loc[:,'FB steps'].rolling(10, win_type='triang').mean(), color=color)
#ax2.tick_params(axis='y', labelcolor=color)

ax3 = ax1.twinx()
color = 'tab:green'

ax3.set_xlabel('Date (Months)')
ax3.set_ylabel('Calories', color=color)
plt.ylim([0,2500])
plt.plot(mfpData.loc[:,'Date'], mfpData.loc[:,'Calories'].rolling(7, win_type='blackmanharris').mean(), color=color)

plt.plot(mfpData.loc[:,'Date'], np.full(len(mfpData.loc[:,'Date']),1200), color=color)
plt.plot(mfpData.loc[:,'Date'], np.full(len(mfpData.loc[:,'Date']),1400), color=color)
plt.plot(mfpData.loc[:,'Date'], np.full(len(mfpData.loc[:,'Date']),1600), color=color)
ax3.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.show()