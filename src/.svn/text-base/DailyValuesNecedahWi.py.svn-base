'''
Created on Dec 10, 2010
@author: egg.davis

Could you take care of this request for daily values (list at end of e-mail)?  There are a few odd 
ones that are not typically in the daily01 files, including daily maximum solar (SOLARRADMAX) and 
daily maximum wind speed (WSMAX), that will need to come from hourly values in the database (I think
we have both hourly max solar and hourly max wind speed).
...
Nice to chat with you earlier today. I would like weather data from the station located on Necedah 
National Wildlife Refuge. I would like daily data for the variables listed below. I would like the 
data from October 1, 2004 to the present. If you are interested, I plan to use the weather data in 
datasets I am building to evaluate whooping crane nesting events and migration.
...
DAILY
TEMPMAX TEMPMIN RHMAX RHMIN WSMAX SOLARRADMAX PRECEP.

TEMPMAX TEMPMIN -- max of tmax values for day, min of tmin
RHMAX RHMIN -- max,min of 5-minute RH values for day
WSMAX -- max of WS_MAX, aka 10sec maximum wind speed for the hour
SOLARRADMAX -- max of SOLRAD_MX, aka 10sec maximum solar radiation for the hour
PRECIP -- sum of hourly calculated precip

'''

from crn import *
import re,sys

station = findStation("necedah")

tmax = findElement("tmax")
tmin = findElement("tmin")
rh5  = findElements("RH percent average for 5 minutes")
windmax = findElement("maximum 1.5m wind speed")
solarmax = findElement("maximum solar radiation")
precip = findElement("precip")
allEls = [tmax,tmin,rh5,windmax,solarmax,precip]

def getMax(curVal,newVal):
    return newVal if (curVal is None or newVal > curVal) else curVal

def getMin(curVal,newVal):
    return newVal if (curVal is None or newVal < curVal) else curVal

start = findDate("9/30/04 0:00").datetimeId - 7
start = findDate("12/1/10 0:00").datetimeId - 7 # Changed to make it faster to run as an example
end   = findDate("12/11/10 0:00").datetimeId - 7

allowQuerySizeOverride()
data = getData(station,(start,end),allEls)

output = []

print "day,tmax,tmin,rh5max,rh5min,windmax,solarmax,precip"

for day in data.localDays:
    tmaxmax = None
    tminmin = None
    rh5max = None
    rh5min = None
    windmaxmax = None
    solarmaxmax = None
    precipsum = Decimal("0")

    values = data.forLocalDay(day)
    for f in values:
        name = f.element.name
        value = f.value
        if name == "P_OFFICIAL":
            precipsum += f.value
        elif re.match("RH",f.element.name):
            rh5max = getMax(rh5max,value)
            rh5min = getMin(rh5min,value)
        elif name == "SOLRAD_MX":
            solarmaxmax = getMax(solarmaxmax,value)
        elif name == "T_MAX":
            tmaxmax = getMax(tmaxmax,value)
        elif name == "T_MIN":
            tminmin = getMin(tminmin,value)
        elif name == "WS_MAX":
            windmaxmax = getMax(windmaxmax,value)
        else:
            print "Uh oh. What's this? "+name
            sys.exit()

    # Missing values are replaced by -9999.0
    tmaxmax =     tmaxmax     or -9999.0
    tminmin =     tminmin     or -9999.0
    rh5max =      rh5max      or -9999.0
    rh5min =      rh5min      or -9999.0
    windmaxmax =  windmaxmax  or -9999.0
    solarmaxmax = solarmaxmax or -9999.0

    try:
        outline = "%s,%+05.1f,%+05.1f,%05.1f,%05.1f,%05.1f,%06.1f,%05.1f" % (day,float(tmaxmax),float(tminmin),float(rh5max),float(rh5min),float(windmaxmax),float(solarmaxmax),float(precipsum))
    except:
        print "Problem with these values:",day,tmaxmax,tminmin,rh5max,rh5min,windmaxmax,solarmaxmax,precipsum
        sys.exit()
    output.append(outline)
    print(outline)
    
printfile("NecedahDaily.txt",output)