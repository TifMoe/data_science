#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 19:50:45 2017

@author: tmoeller

Using data published by NCMEC (National Center for Missing and Exploited Children)
on March 8, 2017 for the Cloudera childfinder hackaton at SXSW 
(https://childfinder.hackerearth.com/)

This dataset includes information from NCMEC related to active, media-ready 
cases for missing children in the United States

NCMEC dataset found on data.world:
(https://data.world/jamesgray/missing-children-in-the-us)
"""

import pandas as pd
import matplotlib.pyplot as plt


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
child_data['days_missing_prior_report'] = (child_data.missingreporteddate - \
		  child_data.missingfromdate).astype('timedelta64[D]')


# Create new column with the age of child at the date missing
child_data['age_at_missing'] = (child_data.missingfromdate - \
		   child_data.birthdate).astype('timedelta64[Y]')

# Investigate deltas and date columns to verify
print child_data[['birthdate','missingfromdate','age_at_missing']].head(10)
print child_data[['missingfromdate', 'missingreporteddate', \
				  'days_missing_prior_report']].head(10)


# Create dummy variable for gender with female as default 
print child_data['sex'].unique()
child_data['gender_female'] = child_data.sex.replace({'Male':0,'Female':1})

# Confirm that dummy variables correctly displayed
print child_data[['sex','gender_female']].head(10)


# Find number of months elapsed between date missing and current local date
local_date = pd.datetime.now().date()
child_data['months_missing'] = (local_date - child_data.missingfromdate).astype('timedelta64[M]')
print child_data[['missingfromdate','months_missing']].head(10)
print child_data[['missingfromdate','months_missing']].tail(10)


# Check out data 
print child_data.describe()
print child_data.dtypes



# Create box plots and descriptions for some columns

def BoxPlots(df):
	plot_cols = ['days_missing_prior_report','months_missing','age_at_missing']
	for x in df.columns:
		if x in plot_cols:
			print x 
			print df[x].describe()
			plt.figure()
			plt.boxplot(df[x])
			plt.show()

BoxPlots(child_data	)

# Investigate where days_missing_prior_report date is negative
print child_data.ix[child_data['days_missing_prior_report']< 0, \
		 ['missingfromdate', 'missingreporteddate', 'months_missing',\
		 'days_missing_prior_report']]

""" 

I believe these 7 rows include incorrect dates in either the missingfromdate
field or the missingreporteddate field because each of these rows indicate
that the child was reported missing before the date they actually went missing
(which could not happen in the real world)

"""


# Create bar graphs showing volume for frequency of values in columns with attributes of child

def BarGraphs(df):
	plot_cols = ['sex','race','age_at_missing','casetype','missingfromstate']
	for x in df.columns:
		if x in plot_cols:
			# create df with index as value and column as count
			print x.upper()
			counts = pd.DataFrame(df.groupby(x).size())
			counts.columns = ['count']
			print 'Top ' + str(len(counts) if len(counts) < 10 else 10) +  \
				' Most Frequently Occuring Values'
			print counts['count'].order(ascending = False).head(10)
			print counts.describe()
			
			# plot df with frequency counts for each value in column
			fig = plt.figure()
			axes = fig.add_subplot(1,1,1)
			axes.set_ylabel(x)
			axes.set_xlabel("Count")
			axes.set_title(x)
			counts.plot(kind='barh',ax=axes,legend=False)
			plt.show()

BarGraphs(child_data)



# Visualize count open cases missing by date reported missing

child_data['year_reported_missing'] = pd.DatetimeIndex(child_data['missingreporteddate']).year
child_data['month_reported_missing'] = pd.DatetimeIndex(child_data['missingreporteddate']).month
child_data[['year_reported_missing','month_reported_missing', 'missingreporteddate']]

count_by_date  = pd.DataFrame(child_data.groupby(['year_reported_missing']).size());
count_by_date.columns = ['count']
count_by_date['percent_total'] = count_by_date.div(count_by_date.sum(axis=0), axis=1)
print count_by_date

"""
It makes sense that the greatest number of open cases (32% of total media-ready open cases) 
were reported last year as cases from prior years have likely been resolved.
"""

# Plot count of active missing children cases by month/year reported (using year and month as index)


fig = plt.figure()
axes = fig.add_subplot(1,1,1)
axes.set_ylabel("Number of Children Reported Missing")
axes.set_xlabel("Year Reported Mising")
axes.set_title("Count of missing children by month/year reported")
count_by_date.plot(kind='line', ax = axes, legend=False)
plt.show()


# Reset index so year and month reported missing are listed as columns in dataframe to plot year over year monthly counts

count_by_date  = pd.DataFrame(child_data.groupby(['year_reported_missing', 'month_reported_missing']).size());
count_by_date.columns = ['count']
count_by_date = count_by_date.reset_index()[['year_reported_missing', 'month_reported_missing','count']]

ax = plt.subplot(111)
ax.set_title('Count of open cases by month reported each year')
test = count_by_date[count_by_date.year_reported_missing.isin([2014,2015,2016, 2017])].groupby('year_reported_missing').plot(y = 'count', x = 'month_reported_missing', kind = 'line', ax = ax)  
L = plt.legend()
_ = [plt.setp(item, 'text', T) for item, T in zip(L.texts, ['2014','2015','2016', '2017'])]
_ = ax.set_xticks(count_by_date.month_reported_missing.unique())
plt.show()





