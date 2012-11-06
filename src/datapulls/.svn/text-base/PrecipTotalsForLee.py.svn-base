'''
In order to track Tropical Storm Lee, produce precip totals from 9/1/11 8 am EDT through
9/6/11 7 am EDT (aka 12pm/11am UTC) for all stations east of -97.6. Output
station name, lat/long, precip total.

Created on Sep 6, 2011
@author: egg.davis
'''
from crn import *

easternStations = [s for s in getAllStations() if float(s.longitude) >= -97.6]
daterange = ('8/25/11 12:00','9/8/11 11:00')
d = getData(easternStations,daterange,'precip')

for s in sorted(easternStations):
    stationdata = d.forStation(s)
    print "%s,%s,%s,%d,%f"%(str(s.name),s.latitude,s.longitude,len(stationdata),sum(stationdata))
    