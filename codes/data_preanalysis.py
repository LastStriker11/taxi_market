# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:30:36 2022

@author: Qing-Long Lu
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from os import listdir
#%%
path = '../data/fhvhv/'
files = listdir(path)
data_all = pd.DataFrame()
for i in files:
    data = pd.read_csv(path+i)
    data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'])
    data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime'])
    #%%
    data['day_year'] = data['pickup_datetime'].dt.dayofyear
    data['day_week'] = data['pickup_datetime'].dt.dayofweek
    data['hour_day'] = data['pickup_datetime'].dt.hour
    data['trip_duration'] = data['dropoff_datetime'] - data['pickup_datetime']
    data['trip_duration'] = data['trip_duration'].dt.total_seconds().div(60)
    #%%
    data_day = pd.DataFrame()
    data_day['num_trips'] = data.groupby(['day_year'])['day_week'].count()
    data_day['duration'] = data.groupby(['day_year'])['trip_duration'].mean()
    data_day['duration_std'] = data.groupby(['day_year'])['trip_duration'].std()
    data_day['year'] = int(i.split('-')[0][-4:])
    data_day.reset_index(drop=False, inplace=True)
    del data
    data_all = pd.concat([data_all, data_day], axis=0)
    #%%
data_all .reset_index(drop=True, inplace=True)
fig, ax = plt.subplots(1,1,figsize=(10,3))
ax.plot(data_all['num_trips'])
#%%
fig, ax = plt.subplots(1,1,figsize=(10,3))
ax.plot(data_all['duration'])
#%%
fig, ax = plt.subplots(1,1,figsize=(10,3))
ax.plot(data_all['duration_std'])
#%%
data_all.to_csv('results/data_daily.csv', index=False)
#%%
data = pd.read_csv('../data/fhv/fhv_tripdata_2016-01.csv')
