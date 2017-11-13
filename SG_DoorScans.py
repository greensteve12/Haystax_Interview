'''
Door Scans - bad actor detector

Assumption: a bad actor will keep a less predictable schedule than all other employees.

Test: look at the variance of scans, with an eye towards the last scans of the day.

Output rosters showing variance in last scan of the day, first scan of the day and total scans per day.

Human analyst will dig in from there

================

Out of curiosity, we will also develop a Friend metric
We will look at the distros of who badges in and out at the same times to see if an employee
has any friends or favorites.

Will the bad actor employee have a more Uniform distribution of same time scan partners? 

================
Usage:
------
    SG_DoorScans.py <anomaly_data.csv> <output_directory>

Misc:
-----
    
'''

import sys
import numpy as np
import csv
from datetime import datetime
from datetime import time
from datetime import timedelta
import operator
#import scipy.stats import kurtosis, skew
from collections import Counter


data_src = sys.argv[1]
output_directory = sys.argv[2]

rawData = []
rawDataRow = []

####################
#
# read the file into rawData variable
#
####################
with open(data_src, 'r') as csvfile:

	myReader = csv.reader(csvfile, delimiter=',', quotechar="'")
	
	for givenRow in myReader:
		rawData.append (givenRow)
		
		
		
		
# delete that header		
rawData.pop(0)

		
# Supplement the data with date conversions and add some extra classifiers

# And get a set of employees without duplicate EmployeeIDs
setOfEmployees = set()

for eachRow in rawData:
	# Append the ordinal day to the stack 
	eachRow.append ((datetime.strptime(eachRow [1], '%m/%d/%y %H:%M')).toordinal())
	
	# append number of minutes into the day that the scan happened
	eachRow.append ((datetime.strptime(eachRow [1], '%m/%d/%y %H:%M').hour)*60 + (datetime.strptime(eachRow [1], '%m/%d/%y %H:%M').minute))
	
	
	#####
	#  Also, create the unique list of employees
	#####
	
	setOfEmployees.add(eachRow[0])

	
	
	
	
	
#############################
#
#	DATA MUNGLING!
#	
# Lets mark up the first and last scans of the day
#   sort rawData by person, day and then time
#   then mark the first scan with a 1 and all others with a 2
#
#############################
	

print ("-------------------")



# sort by EmployeeID, OrdinalDate then #minutes
rawData = sorted(rawData, key = operator.itemgetter(0, 2, 3))

# seed the  tempEmployeeID var and tempDates with a guaranteed never seen value
tempEmpID = "100000"
tempDate = 9999

# loop through the data and mark the first badge swipes of the day
for eachRow in rawData:

	# if the name or the date are different, you have a new day or new person swipe event.  Mark it!
	# Append a 1 to the row
	if ((eachRow[0] != tempEmpID) or (eachRow[2] != tempDate)):
		
		eachRow.append(1) # because it's the first scan of day
		scanOfTheDayNumber = 1
	
	# Else, this is a later swipe.  Append a 2
	else:
		eachRow.append(2)  # 2s will represent all other scans for now
	
	
	eachRow.append(scanOfTheDayNumber)
	scanOfTheDayNumber = scanOfTheDayNumber + 1
	
	tempEmpID = eachRow[0]
	tempDate = eachRow[2]
	
	
	



	
#############################
#	
# Lets mark up the last scans of the day
#   Reverse the sort order by time of day
#   then mark the last scan of the day with a 3
#
#############################
	



rawData = sorted(rawData, key = operator.itemgetter(3), reverse=True)
rawData = sorted(rawData, key = operator.itemgetter(0, 2))



# reestablish fake current data flag
tempEmpID = 100000
tempDate = 9999

for eachRow in rawData:
	# if both the name and date are different, you have a new person and day combination
	# Append a 1 to the row
	if (eachRow[0] != tempEmpID) or (eachRow[2] != tempDate):
		
		eachRow[4] = 3

	
	tempEmpID = eachRow[0]
	tempDate = eachRow[2]
	










##################################
#
#	Pull metrics on the scan data
#
# Go through each employee in setOfEmployees
# Grab all type 1 data points  (first scans)
# 
# Write all of them into a tempList
# Find the count, mean, StD, Skew and kurtosis (if possible)
# Write that to a list (Type1Results): EmpID | Type1 | Count | Mean | StD | Skew | Kurtosis
#
# Repeat for type 3 - file name (Type3OP)
# 
#
###################################

setOfEmployees = sorted(setOfEmployees, key = operator.itemgetter(0))


tempType1Data = []
Type1Results = []
tempType3Data = []
Type3Results = []
tempTotalScansThatDay = []
TotalScansPerDay = []

for eachEmployee in setOfEmployees:
	
	for eachRawDataRow in rawData:

		if ((eachRawDataRow[0] == eachEmployee) and (eachRawDataRow[4] == 1)): #each type1 data row

			tempType1Data.append(eachRawDataRow[3]) # collect all time of day scans for type 1 events
			
		elif ((eachRawDataRow[0] == eachEmployee) and (eachRawDataRow[4] == 3)): #each type3 data row

			tempType3Data.append(eachRawDataRow[3]) # collect all time of day scans for type 1 events
			tempTotalScansThatDay.append(eachRawDataRow[5])
			




	###############################################################
	#
	# now that you've gone through all data for a given employee,
	# calculate and write out the count, mean, std and possibly skew
	# get the count from len(tempType1Data)
	#
	# Data from these variables will be saved to disk at the end of the script
	#
	###############################################################
	
	
	Type1Results.append ([eachEmployee, 1, len(tempType1Data), np.mean(tempType1Data), np.std(tempType1Data, ddof=0)]) #skew(tempType1Data)
	Type3Results.append ([eachEmployee, 3, len(tempType3Data), np.mean(tempType3Data), np.std(tempType3Data, ddof=0)]) # , skew(tempType2Data)
	TotalScansPerDay.append ([eachEmployee, len(tempTotalScansThatDay), np.mean(tempTotalScansThatDay), np.std(tempTotalScansThatDay, ddof=0)]) #, skew(tempTotalScansThatDay)
	
	# and reset all the temp variables
	tempType1Data = []
	tempType3Data = []
	tempTotalScansThatDay = []


##################################
#
#	Join two copies of the final data on the scan DTG on a SQL database
#	Run a crosstab query to see who has shared each person's scan time
#	Look to see who has regular friends vs. who is a bit of a loner.  
#	Are there any changes in relationships over time?
#
##################################	
	
	

	
	
#######################
#
# Final thought - find all scans that had 2 hours dead time before and after them
#  
#	# first calc the number of minutes before previous scan
#	# then calc the minutes before the next scan
#	# cycle through the data where both numbers >120 and append an (1), else (0)
#
#
#######################

# First previous scan time calc
# ReSort rawData by date time stamps...
rawData = sorted(rawData, key = operator.itemgetter(2, 3))
	
	
#inialize the previous time variable
previoustime = (datetime.strptime(rawData[0][1], '%m/%d/%y %H:%M'))

# Calculate previous quiet times based on previoustime
for eachRawDataRow in rawData:	
	eachRawDataRow.append((((datetime.strptime(eachRawDataRow[1], '%m/%d/%y %H:%M')) - previoustime).seconds)/60)
	previoustime = (datetime.strptime(eachRawDataRow[1], '%m/%d/%y %H:%M'))

	
	
####################
#
# Calculate time until the next scan happened
#
####################

rawData = sorted(rawData, key = operator.itemgetter(3), reverse=True)
rawData = sorted(rawData, key = operator.itemgetter(2), reverse=True)


previoustime = (datetime.strptime(rawData[0][1], '%m/%d/%y %H:%M'))

for eachRawDataRow in rawData:	
	eachRawDataRow.append(((previoustime - (datetime.strptime(eachRawDataRow[1], '%m/%d/%y %H:%M')) ).seconds)/60)
	previoustime = (datetime.strptime(eachRawDataRow[1], '%m/%d/%y %H:%M'))



		
##############
# now mark the rows with > 120 minutes of dead time on both before and after
#
####################


for eachRawDataRow in rawData:	
	
	if (eachRawDataRow[6] >= 120) and (eachRawDataRow[7] >= 120):
		eachRawDataRow.append(1)
	else:
		eachRawDataRow.append(0)

	
	
	
	
	
###########################
#
# Output final data files
#
###########################
	
	
	
if not(output_directory.endswith("\\")): 
	# if output directory does not end with a slash - fix it!
	output_directory = output_directory + "\\"

	
	
# Final data write outs
	
with open(output_directory + "OP_FirstScansOfTheDay.csv", 'w', newline='') as outFile:
	writer = csv.writer(outFile)
	writer.writerow(["EmpID", "ScanType", "NumberObservations", "Mean", "Standard Deviation"])
	writer.writerows(Type1Results)

with open(output_directory + "OP_LastScansOfTheDay.csv", 'w', newline='') as outFile:
	writer = csv.writer(outFile)
	writer.writerow(["EmpID", "ScanType", "NumberObservations", "Mean", "Standard Deviation"])
	writer.writerows(Type3Results)

with open(output_directory + "OP_NumberOfScansInADay.csv", 'w', newline='') as outFile:
	writer = csv.writer(outFile)
	writer.writerow(["EmpID", "NumberObservations", "Mean", "Standard Deviation"])
	writer.writerows(TotalScansPerDay)


# and output the final data file
# ReSort rawData by person and then date time stamps...
rawData = sorted(rawData, key = operator.itemgetter(0, 2, 3))
#rawData = sorted(rawData, key = operator.itemgetter(2, 3))
with open(output_directory + "OP_ProcessedData.csv", 'w', newline='') as outFile:
	writer = csv.writer(outFile)
	writer.writerow(["EmpID", "DTG_String", "OrdinalDate", "TimeInSeconds", "FirstOrLast", "ScanOrder", "MinutesBeforePrevious", "MinutesBeforeNext", "FourHourQuietWindow"])
	writer.writerows(rawData)





# Closing message
print ("FileOutputComplete")





