#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 19:50:45 2017

@author: tmoeller

Using data published by NCMEC on March 8, 2017 for the Cloudera childfinder 
hackaton at SXSW 
https://childfinder.hackerearth.com/
"""

import numpy as np
import pandas as pd


# Import missing child data from NCMEC dataset
child_data = pd.read_csv('MediaReadyActiveCases_03082017.csv')

# Explore dataset
print child_data.head(20)
print list(child_data)

# Convert data type from series to datetime like values
child_data["missingreporteddate"] = pd.to_datetime(child_data.missingreporteddate)
child_data["missingfromdate"] = pd.to_datetime(child_data.missingfromdate)
child_data["birthdate"] = pd.to_datetime(child_data.birthdate)


# Create new column with the amount of days elapsing between the date missing and the date reported missing
child_data['days_missing_prior_report'] = (child_data.missingreporteddate - child_data.missingfromdate).astype('timedelta64[D]')

# Create new column with the age of child at the date missing
child_data['age_at_missing'] = (child_data.missingfromdate - child_data.birthdate).astype('timedelta64[Y]')

# Investigate deltas and date columns to verify
print child_data[['birthdate','missingfromdate','age_at_missing']]
print child_data[['missingfromdate', 'missingreporteddate', 'days_missing_prior_report']]

# Create dummy variable for gender with female as default 
print child_data['sex'].unique()
child_data['gender_female'] = child_data.sex.replace({'Male':0,'Female':1})

# Confirm that dummy variables correctly displayed
print child_data[['sex','gender_female']]


# Find months elapsed between date missing and current local date
local_date = pd.datetime.now().date()
child_data['months_missing'] = (local_date - child_data.missingfromdate).astype('timedelta64[Y]')
print child_data[['missingfromdate','months_missing']]

# Check out data 
print child_data.describe()

# Investigate where days_missing_prior_report date is negative
print child_data.ix[child_data['days_missing_prior_report']< 0]