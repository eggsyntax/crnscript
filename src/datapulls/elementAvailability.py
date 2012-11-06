'''
Replicates the most common use case for the element availability report (which sometimes
times out when run on a large number of stations). Shows % available of temp and precip
for each station for a one-month period.

Created on Nov 1, 2011

@author: egg.davis
'''

from crn import *

year = 2011
month = 10

stations = [s for s in getAllStations() if s.networkId == 3]
elements = findElements('temp','precip')

print "Station,Possible hours,% Temp,% Precip"

for station in sorted(stations):
    start = max(findDate('%d%02d0201' %(year,month)).datetimeId , getPor(station).startDatetime)
    end   = findDate('%d%02d0300' %(year,month+1)).datetimeId
    if end < start: continue
    possibleHours = (end - start) + 1

    d = getData(station,(start,end),elements)

    numTemp   = len(d.forElement('temp'))
    numPrecip = len(d.forElement('precip'))
       
    availableTemp   = 100.0 * numTemp   / possibleHours
    availablePrecip = 100.0 * numPrecip / possibleHours
    print '%s,%d,%.1f,%.1f' %(station.name,possibleHours,availableTemp,availablePrecip)
