# Haystax_Interview
Response to the Haystax interview data set

Run the script SG_DoorScans.py using the following command:
python SG_DoorScans.py anomaly_data.csv output

Where "output" is the name of a subdirectory where you'd like to save the output files.



TESTS:
Three main tests were done:
1) Badge out time standard deviations were calculated.  The idea is that suspect behavior will not follow standard badging times and will stand out having a higher standard deviation.

2) Lone wolf badging patterns - Operating under the assumption that bad activities will be done in off hours rather than when other employees are around, badging patterns were examined to look for the largest quiet times around badge events, indicating that an employee was in the office when others were not...

3) Friend networks - look at who scanned their badges at the same times.  Would bad actors travel with common friends?  The goal is to see what kind of friendship patterns were among employees who might badge out within the same minute if they were going to lunch or generally walking in or out of the office together.



RESULTS:
Employee 72 has the most random schedule of the 100 employees. 

a) Their end of the day badge scan times have the highest standard deviation causing me to pull and examine their badge scans by hand.
December 4th, 8th and 11th have the most unusual badge scan patterns.

b) When looking at which badge scans were done during the most quiet times in the office, when the employee would have the office to themselves, Employee 72 hold the largest share of traffic.

Employees 11 and 33 also do some late night work, but their unusual scanning patterns look like simple time shifting to take days off rather than plain random patterns.

c) An analysis was also done using a SQL generated cross tab (FriendFinderCrosstab.xlsx) using data generated in the OP_ProcessedData.csv file.

While employee 72 had a lower than average friend badging rate, there was not a lot of variance among the employees when it came to badging in or out at the same time as their co-workers.

-Steve Green
green.stephen.e@gmail.com
703 431-4446
