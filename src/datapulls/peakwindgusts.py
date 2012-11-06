'''
MP requests peak wind speed over a 3-day period at each station

Created on Apr 27, 2011

@author: egg.davis
'''
from crn import *
import re
from dsl.data import _prettyDate

start = findDate("4/25/2011 0:00")
end   = findDate("4/30/2011 0:00")

firstdate = 92511
for i in range(4):
    start = findDate(firstdate + 24*i)
    end   = findDate(firstdate + 24*i + 23)
    print "--",start,"--"
    maxes = []
    for station in getAllStations():
        d = getData(station,start,"WS_MAX")
        if d:
            d = getData(station,(start,end),"WS_MAX")
            maxf = sorted(d,key=lambda f:f.value).pop()
            #print maxf
            maxes.append(maxf)
    
    maxes.sort(key=lambda f:f.value)
    maxes.reverse()
    
    for maxf in maxes:
            prettydate = _prettyDate(maxf.datetime.datetime0_23)
    
            print str(maxf.station.name) + ":"
            print "  "+prettydate
            print "  Max WSpd: ",maxf.value
            print
            
    print
    
    # Handle 10-meter stations separately, since they have 5-minute peak and direction
    for station in getAllStations():
        d = getData(station,start,"WMAX") # Grab 1 hour first to see if it's a station that measures WMAX
        if d:
            d = getData(station,(start,end),"WMAX")
            maxf = sorted(d,key=lambda f:f.value).pop()
            direction = getData(station,maxf.datetimeId,maxf.elementId + 12)[0]
            ds = subhourly([maxf])
            maxs = ds.factlist.pop()
            prettydate = _prettyDate(maxs.datetime.datetime0_23)
    
            print str(station.name) + ":"
            print "  "+prettydate
            print "  Max WSpd: ",maxf.value
            print "  Direction:",direction.value
            print
            