'''
Pulls calculated precip for POR for a station (as daily totals, from Daily01) and finds the 365-day 
period with the highest precip total. Returns the start and end date and the total precip. Missing data are treated as
0 precip. Note: naively takes 365-element sublists of the total data record on the assumption
that Daily01 has a line for every date even if the data are missing. I verified that this is 
true for Quinault, but before using this on another station it should be verified as 
universally true.

Created on May 31, 2011
@author: egg.davis
'''
from crn import *
import urllib

def readWeb(url):
    filehandle = urllib.urlopen(url)
    lines = filehandle.readlines()
    filehandle.close()
    return lines

def getDaily01(station):
    ''' Returns a list containing a Daily01 line for each date in the POR found in Daily01 ''' 
    lines = []
    por = getPor(station)
    startYear = findDate(por.startDatetime).year
    endYear   = findDate(por.endDatetime).year
    for year in range(startYear,endYear+1):
        stationName = str(station.name).replace(' ','_')
        url = 'http://www1.ncdc.noaa.gov/pub/data/uscrn/products/daily01/%d/CRND0102-%d-%s.txt' % (year,year,stationName)
        #print url
        lines.extend(readWeb(url))
    return lines

def extractData(raw):
    ''' Returns a tuple of (date,dailyprecip) with missing values replaced by 0 '''
    dailyValues = []
    for line in raw:
        fields = line.split()
        date = fields[1]
        precip = fields[9]
        if precip == '-9999.0': precip = '0.0'
        dailyValues.append((date,precip))
    return dailyValues

highestYearlyTotal = 0.0

station = findStation('quinault')
rawDailyData = getDaily01(station)
#printlist(rawDailyData,noSort=True)
dailyData = extractData(rawDailyData)
for i in range(len(dailyData)-364):
    yearOfDailyData = dailyData[i:i+365]
    totalForYear = sum(float(day[1]) for day in yearOfDailyData)
    print "%s,%6.1f" % (yearOfDailyData[0][0],totalForYear)
    if totalForYear > highestYearlyTotal:
        highestYearlyTotal = totalForYear
        startDateForHighestYearlyTotal = yearOfDailyData[0][0]
        endDateForHighestYearlyTotal   = yearOfDailyData[-1][0]
    
print "Highest yearly total:",highestYearlyTotal
print "  %s - %s" % (startDateForHighestYearlyTotal,endDateForHighestYearlyTotal)
#printlist(dailyData,noSort=True)
#print len(dailyData)
#por = getPor(station)
#print por
#for (startDtId,endDtId) in (por):
#    pass