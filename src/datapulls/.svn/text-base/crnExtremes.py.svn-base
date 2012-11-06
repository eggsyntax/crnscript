'''
Searches all CRN data for a given date range for extremes of temperature and precip.
Warning: takes a long time to run and consumes a large amount of data if run on a substantial 
date range.

Created on Aug 23, 2011

@author: egg.davis
'''
from crn import *
from sqlQueryExecutor import *
import dsl
from datetime import timedelta, datetime
import calendar
import urllib
import sys
from operator import lt,gt
from itertools import groupby

inchesPerMm = Decimal("25.4")

class UTC(tzinfo):
    ''' Helper class (Scott) '''

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)

class Month:
    ''' Helper class (Scott) '''

    def __init__ (self, year, month):
        self.start = datetime(year, month, 1, tzinfo=UTC())
        y = year
        m = month
        if m == 12:
            y = y + 1
        m = (m % 12) + 1
        self.end = datetime(y, m, 1, tzinfo=UTC())

    def next (self):
        year = self.start.year
        month = self.start.month
        if month == 12:
            year = year + 1
        month = (month % 12) + 1
        return Month(year, month)

    def days(self):
        cal = calendar.Calendar()
        list = []
        return max(cal.itermonthdays(self.start.year, self.start.month))

    def hours(self):
        return self.days() * 24

    def __str__ (self):
        return str(self.start.year) + '%02d' % (self.start.month)

    def __le__ (self, other):
        return self.start.__le__(other.start)

def findExtremes(startyear):
    ''' Finds the individual values for each month which represent highest and lowest air 
    temp and surface temp. '''
    now = findDate("now")
    extremeelements = [('T_MAX',max), ('T_MIN',min), ('ST_MX',max), ('ST_MN',min)]
    extremeelements = [('ST_MX',max), ('ST_MN',min)] # TODO: temp
    for elname,maxormin in extremeelements:
        month = Month(startyear,01)
        start = findDate(str(month)+"0101")
        while start < now:
            end = findDate(str(month.next()) + "0101").previous()
            allstations = getAllStations()
            excludedstations = findStations(["ME Old Town 2 W","NE Lincoln 8 ENE","WA Quinault 4 NE","GA Watkinsville 5 SSE","SD Aberdeen 35 WNW","LA Lafayette 13 SE","GA Brunswick 23 S"]) if (elname=='ST_MX' or elname=='ST_MN') else [] # per MP
            stations = [s for s in allstations if s not in excludedstations]
            allowQuerySizeOverride()
            d = getData(stations,(start,end),elname)
            extreme = maxormin(d,key=lambda f:f.value if not f.flag else 0) # 0 is a rather arbitrary value here, but we know it's < maxes and > mins.
            print "%s,%s,%s,%s,%s"%(str(month),elname,dsl.data._prettyDate(extreme.datetime),extreme.station.name,extreme.value)
            month = month.next()
            start = findDate(str(month)+"0101")

class FactSum:
    ''' Contains a list of Facts, generally a sequence representing consecutive times. '''
    def __init__(self,factlist):
        self.factlist = sorted(factlist)

    def total(self):
        return float(sum([f.value for f in self.factlist]))
        
    def duration(self):
        return len(self.factlist)
    
    def __str__(self):
        return "%s,%d periods,%.2f"%(self.factlist[0],self.duration(),self.total())
    
    def __repr__(self):
        return "%s,%d periods,%.2f"%(self.factlist[0],self.duration(),self.total())
    
    def __getitem__(self,k):
        #print "factlist:",self.factlist
        return self.factlist[k]

def findLargestSubsequenceSum(d,dur):
    ''' Given a sorted list of Facts d, returns a FactSum which contains 
    the dur-length subsequence whose sum is the highest. '''
    max = d[0].value
    factsum = FactSum([d[0]])
    for i in range(len(d)-dur):
        val = sum(d[i:i+dur])
        if val > max:
            max = val
            factsum = FactSum(d[i:i+dur])
            #print factsum,max
    return factsum

def findSubDailyPrecipMaxesForDur(startdate,dur):
    ''' For a particular duration dur (# of 5-minute periods), finds the highest-sum dur-length 
    subsequence for each station. '''
    maxList = [] # Holds a FactSum for each station
    now = findDate("now")
    
    for station in sorted(getAllStations()):
        month = Month(findDate(startdate).year,findDate(startdate).month+1)
        start = findDate(str(month)+"0101")
        d = FactCollection([])
        while start < now:
            #print month,
            end = findDate(str(month.next()) + "0101").previous()
            monthlyd = FactCollection(sorted(subhourly(getData(station,(start,end),'calculated geonor precip for 5 minutes'))))
            d.extend(monthlyd)
            month = month.next()
            start = findDate(str(month)+"0101")
        try:
            maxForDur = findLargestSubsequenceSum(d,dur)
            #print
            print maxForDur
            maxList.append(maxForDur)
        except:
            continue

    return maxList # 

def findSubDailyPrecipMaxes(startdate):
    durations = [1,3,6,12,288] # Number of 5-minute periods corresponding with each of the desired durations
    durations = [288] # TODO: temp
    ''' Get greatest 5-minute, 15-minute, 30-minute, and 60-minute precip totals for each
    station. Print a list for each, and then print the absolute max for each duration. '''
    absoluteMaxes = {}
    for dur in durations:
        maxList = findSubDailyPrecipMaxesForDur(startdate,dur)
        printfile("crn-extremes-%d.txt"%(dur),maxList,sortData=False)
        #printlist(maxList)
        print
        absoluteMaxes[dur] = max(maxList,key=lambda t:t.total)
        #printlist(sorted(maxList,key=lambda t:t.total),sortData=False)
    print
    output = []
    for dur in sorted(absoluteMaxes):
        output.append(absoluteMaxes[dur])
    printfile("crn-extremes-absolutemaxes.txt",output,sortData=False)

def findLargestSubsequenceSum2(d,dur):
    ''' Given a sorted list of tuples d, each containing a string date in YYYYMMDD and a value, 
    returns a tuple containing 1) the date of the first day in 
    the dur-length subsequence whose sum is the highest, and 2) the sum itself. '''
    print "data length:",len(d)
    maxtuple = (d[0][0],d[0][1])
    for i in range(len(d)-dur):
        val = sum([v[1] if v[1] > 0 else 0 for v in d[i:i+dur]])
        if val > maxtuple[1]: 
            maxtuple = ((d[i][0],val))
        print val,maxtuple[1]
    return maxtuple

def getDailyFile(station,year):
    stationname = str(station.name).replace(' ','_')
    url = 'http://www1.ncdc.noaa.gov/pub/data/uscrn/products/daily01/%s/CRND0102-%s-%s.txt' % (str(year),str(year),stationname)
    file = urllib.urlopen(url)
    return file

def findDailyPrecipMaxes(startyear,endyear):
    maxesByDur = {}
    durs = [1,5,7,30,365]
    for dur in durs:
        for station in sorted(getAllStations()): 
            stationvals = []
            for year in range(startyear,endyear+1):
                file = getDailyFile(station,year)
                try:
                    for line in file:
                        stationvals.append((line[6:14],float(line[70:77].replace(' ',''))))
                except: # slightly awkward idiom for breaking the nested loop
                    file.close()
                    continue
                file.close()
            largestSubsequence = findLargestSubsequenceSum2(stationvals, dur)
            out = "%s,%s,%d periods,%.1f"%(station.name,largestSubsequence[0],dur,largestSubsequence[1])
            print out
            maxesByDur.setdefault(dur,[]).append(out)
        
    for dur in durs:
        printfile("dailyPrecipMaxes-%2d.txt"%(dur),maxesByDur[dur],sortData=False)
        
    absoluteMaxes = {}
    for dur in durs:
        absoluteMaxes[dur] = max(maxesByDur[dur],key=lambda v:float(v.split(',')[3])) # records are strings so we split them back up
        print absoluteMaxes[dur]
    printfile("dailyPrecipAbsoluteMaxes.txt",absoluteMaxes)
        
def findWaterYears(startyear,endyear):
    for station in findStations('Quinault'):
        for year in range(startyear-1,endyear):
            start = findDate("%d100100"%(year)).datetimeId   + station.offset
            end   = findDate("%d093023"%(year+1)).datetimeId + station.offset
            d = getData(station,(start,end),'precip')
            vals = [f.value if f.value > 0 else 0 for f in d]
            total = sum(vals)
            print "%d,%.1f,%.2f"%(year+1,total,total/inchesPerMm)

def getStationVals(station,startyear,endyear,(startPosition,endPosition)):
    ''' returns tuples representing consecutive days, each containing a datestring and a value '''
    vals = []
    for year in range(startyear,endyear+1):
        stationFile = getDailyFile(station,year)
        for line in stationFile:
            vals.append((line[6:14],float(line[startPosition:endPosition].replace(' ',''))))
    #printlist(vals,sortData=False)
    return vals

def findLongestSequenceByKey(values,keys,comparisonOperator):
    ''' Returns the longest subsequence for each key (using a comparisonOperator, generally
    gt (for max) or lt (for min). values are expected to be a list containing tuples whose
    second member contains the actual value. '''
    results = {}
    for key in keys:
        subsequences = (list(it)
                        for satisfiesPredicate, it in groupby(values,lambda v: comparisonOperator(v[1],key))
                        if satisfiesPredicate)
        results[key] = max(subsequences,key=len)
    return results

def fToC(fVals):
    return [(f - 32.0) * 5 / 9 for f in fVals]
    
def cToF(cVal):
    return cVal * 9 / 5 + 32

def findLongestSequences(startyear,endyear):
    ''' Finds the longest hot spells and cold spells for the appropriate stations, for various
    values of 'hot spell' and 'cold spell' (namely a stretch of consecutive days which all have
    a daily max/min temperature above/below some particular temperature) '''
    print "Maximum temperature durations:"
    maxStation = findStation('stovepipe wells')
    maxLocation = (38,45)
    maxStationVals = getStationVals(maxStation,startyear,endyear,maxLocation)
    keyTemps = fToC([120,110,100,95,90])
    longestMaxSequences = findLongestSequenceByKey(maxStationVals, keyTemps, gt)
    for keyTemp,subsequence in sorted(longestMaxSequences.items()):
        print "%6.1f,%03d,%s,%s"%(cToF(keyTemp),len(subsequence),subsequence[0][0],subsequence[-1][0])
        
    print
    print "Minimum temperature durations:"
    minStation = findStation('barrow')
    minLocation = (46,53)
    minStationVals = getStationVals(minStation,startyear,endyear,minLocation)
    keyTemps = fToC([-50,-30,0,32])
    longestMinSequences = findLongestSequenceByKey(minStationVals, keyTemps, lt)
    for keyTemp,subsequence in sorted(longestMinSequences.items()):
        print "%6.1f,%03d,%s,%s"%(cToF(keyTemp),len(subsequence),subsequence[0][0],subsequence[-1][0])
 
 
    
''' Note: this script will take days to run (findSubDailyPrecipMaxes is by far the slowest part); you
may want to run the functions below one at a time. '''
findExtremes(2009)
#findSubDailyPrecipMaxes("2009010100")
#findDailyPrecipMaxes(2009,2011)
#findWaterYears(2007,2011)
#findLongestSequences(2009,2011)

