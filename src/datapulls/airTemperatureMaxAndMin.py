'''
Created on Feb 3, 2012

Done for Jesse Bell, for comparison with soil temperatures.

Produces records of the form:
  station name , station id, date(YYYYMMDD), maximum temperature, minimum temperature.

@author: scott.embler
'''

from crn import *
from period import *
import csv

start = findDate("01/01/2001 0:00").datetimeId;
end = findDate("01/01/2012 0:00").datetimeId;

stations = getAllStations()
tmax = findElements('T_MAX')
tmin = findElements('T_MIN')
outputFile = open('air_temperatures_2001-2011.txt','w')
csvOutput = csv.writer(outputFile, lineterminator='\n')
csvOutput.writerow(['station name','station id','YYYYMMDD','maximum temperature','minimum temperature']);

for station in stations:
    #Query time-outs might occur if we ask for the full period of record.
    #quickly generate a period-of-record object and use existing functions
    #to break that period-of-record into local-months.
    por = POR()
    por.setStationId(station.getStationId())
    por.setStartDatetime(start)
    por.setEndDatetime(end)
    for month in months(por):
        #Now we are ready to fetch data from the database.
        monthlyValues = getDataForPeriod(station, month, (tmax,tmin))
        #Further refine the month's worth of data into local days so that we can easily
        #pick out the maximum and minimum temperatures.
        for localDay in monthlyValues.localDays:
            dailyValues = monthlyValues.forLocalDay(localDay)
            tmaxs = dailyValues.forElement(tmax)
            tmins = dailyValues.forElement(tmin)
            try:
                #The max() and min() functions will raise an error if there are no values for the day.
                #We'd prefer to skip to the next record in this situation.  So just catch and drop the 
                #error.
                maximum = max([f.value for f in tmaxs])
                minimum = min([f.value for f in tmins])
                print station.getNameString(), ',', station.getWbanno(), ',', localDay, ',', maximum, ',', minimum
                csvOutput.writerow([station.getNameString(), station.getWbanno(), localDay, maximum, minimum])
                outputFile.flush()
            except ValueError:
                pass

outputFile.close()
        