# -*- coding: utf-8 -*-
"""
Created on Tue May 22 17:23:08 2018

@author: pahlza
"""

import pandas as pd
import os

filePath = 'C:\\Users\pahlza\Desktop\School Stuff'
fileName = 'fitbit_export_20180523.xls'

fitbitXLS = pd.ExcelFile(os.path.join(filePath, fileName))
fbDataBody = pd.read_excel(fitbitXLS, 'Body')
fbDataFoods = pd.read_excel(fitbitXLS, 'Foods')
fbDataActivities = pd.read_excel(fitbitXLS, 'Activities')
fbDataSleep = pd.read_excel(fitbitXLS, 'Sleep')



fbData = pd.concat([fbDataBody.iloc[:,0:2], fbDataFoods['Calories In']], axis=1)