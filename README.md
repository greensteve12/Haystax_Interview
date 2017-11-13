# Haystax_Interview
Response to the Haystax interview data set

Run the script SG_DoorScans.py using the following command:
python SG_DoorScans.py anomaly_data.csv output

Where "output" is the name of a subdirectory where you'd like to save the output files.
"output" can be run as a full path also.


RESULTS:
Employee 72 has the most random schedule of the 100 employees.  

Their end of the day badge scan times have the highest standard deviation causing me to pull and examine their badge scans by hand.
December 4th, 8th and 11th have the most unusual badge scan patterns.

When looking at which badge scans were done during the most quiet times in the office, when the employee would have the office to themselves, Employee 72 hold the largest share of traffic.

Employees 11 and 33 also do some late night work, but their unusual scanning patterns look like simple time shifting to take days off rather than plain random patterns.

An analysis was also done using a SQL generated cross tab (FriendFinderCrosstab.xlsx), looking to link patterns in who scanned out in the same minute as an employee.
The goal was to see what kind of friendship patterns were among employees who might badge out within the same minute if they were going to lunch or generally walking in or out of the office together.

While employee 72 had a lower than average friend badging rate, there was not a lot of variance among the employees when it came to badging in or out at the same time as their co-workers.

