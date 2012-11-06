'''
Created on Feb 8, 2011

I want the last day that soil temperature is above, and stays above, 5 and 10 degrees C - 
before July.  This will mark the beginning of the growing season. Then, I want the first day 
that goes below 10 and 5 degrees C in the fall.  This would mark the end of the growing season.
Ideally, I would want these dates from all the sites that have soil temperature probes.  
Furthermore, I want to repeat this analysis on air temperature, but using 0 and 5 degrees C. 

@author: egg.davis
'''
from crn import *

soilStations = stationDao.getStationsCurrentlyWithSmSt().values()
startOfJuly = '20100701'
endOfYear = '20101231'

# start helper functions

def get5cmSoilTemps(station,year):
    startDate = findDate(str(year)  +"010100")
    endDate   = findDate(str(year+1)+"010200")
    el = findElement('soil temperature layer average at 5 cm for the hour')
    d = getData(station,(startDate,endDate),el)
    
def earliestDate(data):
    # Returns the earliest date present in a map of data (as returned by get5cmSoilTemps())
    sortedkeys = sorted(data.keys())
    try:
        return sortedkeys[0]
    except:
        return None

def isEarlierThan(date1,date2):
    # Compares dates in the form of YYYYMMDD strings
    return int(date1) < int(date2)

def incrementDate(datestring):
    # Takes a datestring in YYYYMMDD format; returns a string in the same format
    # representing the following day.
    date = findDate(str(datestring)+'12')
    nextdate = date.add(24)
    nextdatestring = (nextdate.getDatetime0_23())[0:8]
    return nextdatestring
    
# end helper functions

for station in soilStations:
    startOfGrowingSeason = None
    peakOfGrowingSeason = None
    endOfPeak = None
    endOfGrowingSeason = None
    
    soilTemps = get5cmSoilTemps(station,2010) # returned grouped by local day
    if not soilTemps: continue # ignore stations which don't yet have data
    date = earliestDate(soilTemps)
    if isEarlierThan(date,'20100401'): # If we don't have data before April, we don't try
        while date != startOfJuly:     # to calculate start/peak
            dailyTemps = soilTemps[date]
            if all(fact.value > 5 for fact in dailyTemps):
                #print "found:",date,dailyTemps
                startOfGrowingSeason = date
                break
            date = incrementDate(date)
    
        while date != startOfJuly:
            dailyTemps = soilTemps[date]
            if all(fact.value > 10 for fact in dailyTemps):
                #print "found:",date,dailyTemps
                peakOfGrowingSeason = date
                break
            date = incrementDate(date)
            
    if isEarlierThan(date,'20101001'): # If we don't have data before October, we don't try to 
        #                                calculate end of peak/end of growing season
        date = '20101001' # Jump to the beginning of October
        while date != endOfYear:
            dailyTemps = soilTemps[date]
            if any(fact.value < 10 and fact.value > -9999 for fact in dailyTemps):
                endOfPeak = date
                break
            date = incrementDate(date)
    
        while date != endOfYear:
            dailyTemps = soilTemps[date]
            if any(fact.value < 5 and fact.value > -9999 for fact in dailyTemps):
                endOfGrowingSeason = date
                break
            date = incrementDate(date)

    print station.name,",",startOfGrowingSeason,",",peakOfGrowingSeason,",",endOfPeak,",",endOfGrowingSeason
    
