'''
We have received a data request for our wind data from nichole gueck whose email is: 
ngueck@agrilogic.com. I told her that we would provide period of record files for stations 
with the hourly records in a fixed format of: station name, lat, lon, date, hour, hourly 
average wind speed, hourly wind max. This seems pretty straightforward .... I hope you can do 
this with your scripting approach very quickly. Would this be feasible sometime by mid-Friday?

And the catch .... she needs this for all our stations in Arkansas, Louisiana, Mississippi, Missouri, and Texas.

Created on Sep 1, 2011

@author: egg.davis
'''
from crn import *
import dsl,sys

stations = findStations('TX','AR','LA','MS','MO')
for station in sorted(stations):
    por = porDao.getPor(station.stationId)
    output = []
    start = por.startDatetime
    porend = por.endDatetime
    while start < (porend+3000):
#        allowQuerySizeOverride()
        print "retrieving data...",
        
        # I was getting timeout errors, so I'm retrying calls that time out. This is *only*
        # a reasonable solution since this is a one-time script which I'm monitoring as it runs.
        d = None
        while d is None:
            try:
                d = getData(station,(start,start+3000),('WINDSPD','WS_MAX'))
            except:
                print "Error:",sys.exc_info()[0]
        print "got %d for %s"%(len(d),station.name)
        
        fillMissing(d)
        print "   now %d"%(len(d))
        for ob in sorted(d.observations,key=lambda o:findDate(o[1]).datetimeId):
#            print ob
            try:
                (f,f2) = d.forObservation(ob)
            except ValueError:
                continue
            
            outputfields = (station.latitude,
                            station.longitude,
                            f.datetime.month+1,
                            f.datetime.day,
                            f.datetime.year,
                            f.datetime.hour,
                            f.value,  # WINDSPD
                            f2.value) # WS_MAX
            outputformat = "%10s %10s %02d/%02d/%4d %02d %09.2f %09.2f"
            outputline = outputformat % outputfields
            output.append(outputline)
        start += 3001
    filename = "C:/Documents and Settings/jesse.davis/My Documents/Temp/windspeed/windspeed-%s.txt"%( str(station.name).replace(' ','_'))
    printfile(filename,output,sortData=False)
    #printlist(output,sortData=False)
