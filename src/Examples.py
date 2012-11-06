'''
Created on Oct 19, 2010

@author: egg.davis

Provides some simple examples of how to use the crnscript utilites.  Feel free to fiddle with them 
and run them. If you're new to crnscript, a careful read through these examples will be well
worth your time.
'''

from crn import *

''' findStations examples:'''

print findStation("Crossville")
#Station[1121] TN Crossville 7 NW (04906C,63855,402210)Comm:Y, OpStat: Y

printlist(findStations("Asheville"))
#Station[1026] NC Asheville 8 SSW (0246CA,53877,310308)Comm:Y, OpStat: Y
#Station[1027] NC Asheville 13 S (0255BC,53878,310310)Comm:Y, OpStat: Y

stations = findStations("RI")
for s in stations:
    if Decimal(s.latitude) < 41.48: print s,s.latitude # Must cast to Decimal -- easy to trip up on!
#Station[1043] RI Kingston 1 W (0362DC,54797,374269)Comm:Y, OpStat: Y

''' Similarly, findElement and findDate: '''
printlist(findElements('solar radiation'))
#Element 14:SOLARAD:average solar radiation for the hour
#Element 15:SR_STD:solar radiation std dev for the hour
#Element 304:SOLRAD_MN:10sec minimum solar radiation for the hour
#Element 305:SOLRAD_MX:10sec maximum solar radiation for the hour

# Certain aliases retrieve elements of key importance (use showElements() to
# get a list of these)
print findElements('temp')
#[Element 343:T_OFFICIAL:calculated average temp for hour (calculated from three sensors' hourly averages)]

print findDate('3/21/10 8:00') # Most standard ways of writing the date are supported
#Datetime 82919:2010032108 UTC
print findDate('2010032108') # This is the canonical CRN form
#Datetime 82919:2010032108 UTC
print findDate('last tuesday') # You can do some funky things like this
#Datetime 90192:2011011809 UTC
print findDate('october 2009') # Note that this will return *some* date in Oct 09 --
#Datetime 79273:2009102010 UTC # don't count on a particular one.
print findDate('now') # 'now' is a special case which returns a recent hour
#Datetime 90413:2011012714 UTC # for which the CRN database has an observation.

'''getData examples: '''
# Simplest case:
printlist("Crossville","2009111917","temp") # args are station, datetime, element
#TN Crossville 7 NW, 2009111917, T_OFFICIAL: 6.8 (0)

# For a datetime range, use an ordered pair (in parentheses):
printlist("Crossville",("2009111917","2009111921"),"temp")

# Another example: find three hours' worth of all 5-minute calc temps for one of the Asheville stations. This time
# we use intermediate variables to store results (since we might want to reuse them)
station = findStation("Asheville 8 SSW")
start = findDate("01/02/2009 5:00")
end   = findDate("01/02/2009 7:00")
tempElements = findElements("T5")

data = getData(station,(start,end),tempElements)
printlist(data)
graph(data)

# As you can see, the printlist() function is handy; it handles lists and maps 
# of all kinds. It sorts its entries by default. To leave them unsorted, use 
# printlist(data,sortData=False). Or to sort them in some other way, use the following
# pattern:
stations = getAllStations()
stationsByVector = sorted(stations, key=lambda station: station.name.vector)
# the general pattern is sorted(listToSort, key=lambda listmember: listmember.property).
# In some cases you'll want to cast to Decimal. 
printlist(stationsByVector,sortData=False) # We prevent printlist from re-sorting them with their default sort.

# There are csv(),fixed(), printfile() and graph() functions which take the output 
# from getData() as their parameter.
d = getData('Asheville',('10/10/10','+12'),'temp')
printfile("tempdata.txt",fixed(d))

# Example: find flagged Geonor wire values at either of the Asheville stations 
# in February 2008. Note the use of the list comprehension to filter down to 
# just the flagged data. Python's list comprehension syntax is highly elegant
# and fits well with crnscript's capabilities.
# A good intro to list comprehensions is at 
# http://www.secnetix.de/olli/Python/list_comprehensions.hawk
data = getData("Asheville",
               ("2008020100","2008030100"),
               "D\d\d\d") # Geonor wire values are named D105,D205,D305,D110,D210, etc
flaggeddata = [fact for fact in data if fact.flag != 0]
printlist(flaggeddata)

# Example: grab all elements for the Barrow, AK station for the most recent datetime:
printlist(getData("barrow","now",getAllElements()))

# Example: what wind elements are observed (as of 2010) at the Champaign, IL station?
windels = findElements("wind+") # Note the '+' at the end. "wind" is a standard alias for hourly average wind;
                                # adding a '+' at the end of a search term bypasses those aliases.
data = getData("Champaign","2010010100",windels)
for fact in data:
    print fact.element.description

'''getObservations example: '''
stations = findStations("MS")
datetime = findDate("9/9/2009 9:00")
observations = getObservations(stations,datetime)
printlist(observations)

''' Some more examples of working with returned data and using list comprehensions: '''

# Say we want to know what states contain stations whose latitude is greater than 40:
highStations = [s.name.state for s in getAllStations() if Decimal(s.latitude) > 40]
printlist(set(highStations)) # We use 'set' to filter down to a set of unique values

# You'll note that we cast the latitude to a Decimal -- that's one of the less 
# obvious aspects of crnscript. The latitude, like many other values, is 
# returned by the database as a string and must be cast to Decimal. 
# Unfortunately, there's no easy way around this. Note, though, that
# the value field in Facts returned by getData is already a Decimal.

# Get the total current precipitation for Alabama stations. Note that sum sums
# the *values* of a list of facts. Similarly, using the arithmetic operators 
# (+,-,*,/) on Facts will operate on the values. 
data = getData("AL",
               "now",
               "precip")
print sum(data)

# Sometimes we want the entire period of record for a station -- if so we can 
# pass that as the date (use with caution!)
station = findStation("Gila Bend")
por = getPor(station)
graph(station,por,"temp")

# Graphing data example:
stations = findStations("HI")
dates   = ("2009010100","+48")
elements = findElements("official")
data = getData(stations,dates,elements)
graph(data)

# similarly,
histogram(data,numBins=8)

# Working with scatter plots and regression:
d = getData("AK",("11/29/10 4:00","+72"),("wind","solar"))
scatter(d,regress=True)

# Use data.forElement(), data.forStation(), data.forLocalDay(), data.forDatetime(), and 
# data.forObservation() to retrieve subsets of returned data. They can be chained freely:
d = getData("AK",("11/29/10 4:00","+72"),("tmin","tmax"))
printlist(d.forStation('barrow').forElement('tmin'))
printlist(d.forLocalDay("20101130").forStation('Sitka'))

# Use data.elements, data.stations, data.localDays, data.datetimes, and data.observations to 
# iterate over subsets of the data:
d = getData("AK",("11/29/10 4:00","+2"),("tmin","tmax"))
for station in d.stations:
    print station
    for element in d.elements:
        printlist(d.forStation(station).forElement(element))
        print
    print
    
# Use data.groupedByElement(), data.groupedByStation(), data.groupedByLocalDay(), 
# data.groupedByDatetime(), and data.groupedByObservation() to return all subsets at once
# (this idiom is slightly outdated; better to use the techniques shown in the last example
# when possible):
d = getData("AK",("11/29/10 4:00","+2"),("tmin","tmax"))
gd = d.groupedByStation()
for station in gd:
    print station
    printlist(gd[station])
    print

# There is still one good use for data.groupedByObservation(). It puts all the observations for one 
# station-datetime in one group, suitable for output with printlist etc. You can also pass
# data grouped in this way to csv. This is a good strategy for creating data which you 
# intend to paste into Excel or the like, especially if you call fillMissing().
d = getData("Jamestown 38",("11/11/10 4:00","+72"),"volumetric layer average")
fillMissing(d)
printlist(csv(d.groupedByObservation()))

# Similarly you can pass a list of facts to data.groupedByLocalDay() or data.groupedByStation()

# CRN treats 5-minute and 15-minute variables as a set of 12 or 4 hourly variables with different
# names. Sometimes, however, as when creating a time series graph, we wish to treat them as a 
# single variable with a subhourly time. Calling the subhourly() function recasts the data in 
# this way.
graph(subhourly(getData('asheville',('2010010100','+24'),'calculated average temp for 5 minutes')))

# Using forStation() and forLocalDay() to find daily precip totals at each NC station:
d = getData('NC',('10/12/10 6:00','+71'),'precip')
for station in d.stations:
    print station
    for day in sorted(d.localDays):
        print "%s %4.1f mm" % (day, sum(d.forStation(station).forLocalDay(day)))
    print
# Occasionally you may hit the limits of the DAOs. If you need to run an 
# arbitrary SQL query, you can do it as follows (please use with caution!):
from sqlQueryExecutor import *
azStations = executeQuery("select loc_state,location,vector from crn_station_data where loc_state like 'AZ'")
printlist(azStations)


# Want more examples? Some of the scripts in the src directory were written
# for just that purpose:
# SoilInAz.py
# spokane.py
# MonthlyStats.py
# And really all the scripts in src make at least some attempt to be clear examples.

# 