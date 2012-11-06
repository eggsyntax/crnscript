'''
Created on Feb 7, 2012

Done for Jesse Bell, for comparison with air temperatures.

Produces records of the form:
  station name , station id, date(YYYYMMDD), maximum temperature, minimum temperature.

@author: scott.embler
'''

from crn import *
from period import *
import csv

start = findDate("01/01/2009 0:00").datetimeId;
end = findDate("01/01/2012 0:00").datetimeId;

stations = stationDao.getStationsCurrentlyWithSmSt().values()
depth = "100"

#Get the soil-layer average for the hour at the appropriate depth.
#If we used findElements here we'd get multiple elements when we should have only one.
soilTemp = [element for element in getAllElements() if element.name == ("ST" + depth)]

outputFile = open('soil_temperatures_' + depth + 'cm_2009-2011.txt','w')
csvOutput = csv.writer(outputFile, lineterminator='\n')
csvOutput.writerow(['station name','station id','YYYYMMDD','maximum temperature','minimum temperature']);

for station in stations:
#    print station
    allowQuerySizeOverride()
    porValues = getData(station, (start,end), soilTemp)
    #Further refine the period-of-record's worth of data into local days so that we can easily
    #pick out the maximum and minimum temperatures.
    for localDay in porValues.localDays:
        dailyValues = porValues.forLocalDay(localDay)
        try:
            #The max() and min() functions will raise an error if there are no values for the day.
            #We'd prefer to skip to the next record in this situation.  So just catch and drop the 
            #error.
            maximum = max([f.value for f in dailyValues if f.value > -100]) # filter out missing values too.
            minimum = min([f.value for f in dailyValues if f.value > -100]) # filter out missing values too.
#            print station.getNameString(), ',', station.getWbanno(), ',', localDay, ',', maximum, ',', minimum
            csvOutput.writerow([station.getNameString(), station.getWbanno(), localDay, maximum, minimum])
            outputFile.flush()
        except ValueError, ve:
            pass

outputFile.close()
        