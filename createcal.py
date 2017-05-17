#######holidayapi.com 627ebd6f-d8a7-4217-b99e-9b378e5c88bd

import urllib
import re
import json
import datetime
import csv

##open the full diabetes data set
diabetes_data= open('diabetes_concatenated.txt', 'rU')

##use regex to identify select values from each record in the diabetes data set; these will
##be added to dictionaries in the my_diabetes_list
month = re.compile(r'^[0-9][0-9]')
day = re.compile(r'-([0-9][0-9])-')
year =re.compile(r'[0-9][0-9][0-9][0-9]')
time = re.compile(r'[0-9]:[0-9][0-9]')
code = re.compile(r'\t([0-9][0-9])\t')
measure = re.compile(r'\t([\w.]+)(?=\n)')


##create a list (called my_diabetes_list) to which the previously created variables (month, day, year, time, code, measure)
##may be added as dictionary entries
my_diabetes_list=[]

## count and special counters are here to ensure that the subsequent loop covers
## all data in the diabetes data set. they will count both the successfully created dictionaries
## and the rows that the loop ignores (because the measure data is not always correctly formatted)
count = 0
special = 0

## for every line in diabetes_data (the original diabetes data set), try to create a dictionary assigning the regex
## objects as values. append each newly created dictionary to the list, my_diabetes_list. if the regex can't find a match,
## pass the line (this is due to some measures data being non-numbers)
##use datetime to find out what weekday each date corresponds to (where numbers 0-6 correspond to Monday thru Sunday).
##then use if/else to assign values (Monday/Tuesday/Wednesday/Thursday/Friday/Saturday/Sunday) to 'weekday' key

for line in diabetes_data:
    try:
        row = {'month':re.findall(month,line)[0],
               'day':re.findall(day,line)[0],
               'year':re.findall(year,line)[0],
               'time':re.findall(time,line)[0],
               'code':re.findall(code,line)[0],
               'measure':re.findall(measure,line)[0]}
        if datetime.datetime(int(row['year']), int(row['month']), int(row['day']), 0, 0, 0,0).weekday() == 0:
            row['weekday'] = 'Monday'
        elif datetime.datetime(int(row['year']), int(row['month']), int(row['day']), 0, 0, 0,0).weekday() == 1:
            row['weekday'] = 'Tuesday'
        elif datetime.datetime(int(row['year']), int(row['month']), int(row['day']), 0, 0, 0,0).weekday() == 2:
            row['weekday'] = 'Wednesday'
        elif datetime.datetime(int(row['year']), int(row['month']), int(row['day']), 0, 0, 0,0).weekday() == 3:
            row['weekday'] = 'Thursday'
        elif datetime.datetime(int(row['year']), int(row['month']), int(row['day']), 0, 0, 0,0).weekday() == 4:
            row['weekday'] = 'Friday'
        elif datetime.datetime(int(row['year']), int(row['month']), int(row['day']), 0, 0, 0,0).weekday() == 5:
            row['weekday'] = 'Saturday'
        else:
            row['weekday'] = 'Sunday'
        my_diabetes_list.append(row)
        count = count + 1
        #print "working"
    except:
        special = special + 1
        #print "working"
        pass

## print out each dictionary added to my_diabetes_list (to roughly judge success)
# for line in my_diabetes_list:
#     print line

## print out the special (70) and count counters (29260). 70 + 29260 = 29330, which was confirmed as the diabetes data
## set's number of rows
# print special # 70
# print count # 29260

##create a list to which api call information may be appended
api_list=[]

## create dictionaries that will include necessary data for HolidayAPI request by looping through the dictionaries
## in my_diabetes_list . Dictionaries are to include the constants country (US) and the provided key.
## The other three values will depend on the my_diabetes_list dictionaries being looped through (and what they contain for their
## day, month and year). Then use the urllib method 'urlencode' to create a string that can be given to the API request

status = 0
for my_dict in my_diabetes_list:
    d = {'country': 'US',
         'key': '627ebd6f-d8a7-4217-b99e-9b378e5c88bd',
         'day': my_dict['day'],
         'month' : my_dict['month'],
         'year': my_dict['year']}
    if d not in api_list:
        api_list.append(d)
    #print urllib.urlencode(d)

for pieces in api_list:
    pieces['results']=json.loads(urllib.urlopen('https://holidayapi.com/v1/holidays?'+urllib.urlencode(pieces)).read())


##add a key (results) to each dictionary in my_diabetes_list, which will include the results of the API request. If there
## is no holiday, the value will take on the form {u'status': 200, u'holidays': []} (where status just indicates whether
## the request was successful) or {u'status': 200, u'holidays': [{u'date': u'1991-06-27', u'observed': u'1991-06-27', u'name': u'Helen Keller Day', u'public': False}]}
## where there is a holiday.


counter = 0
for my_dict in my_diabetes_list:
    counter = counter + 1
    print counter
    for pieces in api_list:
        if pieces['year'] == my_dict['year'] and pieces['month']==my_dict['month'] and pieces['day'] == my_dict['day']:
            my_dict['results'] = pieces['results']
             ##add another key to each my_dict in my_diabetes_list called 'holiday', which will simply indicate whether there is a holiday
             ## that day (TRUE) or not (FALSE)
            if my_dict['results']['holidays']:
                my_dict['holiday'] = 'TRUE'
            else:
                my_dict['holiday'] = 'FALSE'
            ##add another key to each my_dict in my_diabetes_list called 'weekend', which will simply indicate whether the date is a weekend
            ## (TRUE) or not (FALSE)
            if my_dict['weekday'] == 'Saturday' or my_dict['weekday'] =='Sunday':
                my_dict['weekend'] = 'TRUE'
            else: my_dict['weekend'] = 'FALSE'
            print my_dict




##write my_diabetes_list dictionaries to a csv called test2.csv
fieldnames = ['day', 'weekday', 'month','year','time','code','measure','holiday','weekend','results']    #####http://www.gadzmo.com/python/reading-and-writing-csv-files-with-python-dictreader-and-dictwriter/
test_file = open('test2.csv','wb')
csvwriter = csv.DictWriter(test_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in my_diabetes_list:
     csvwriter.writerow(row)
test_file.close()


