'''
Egg,
Can you extract windspeed for the 7 texas stations tagged with a date and time.  Tim Wilson needs 
this and we really can't find a way to effeciently do this.
Thanks,
Bruce 

oops that was for 2010 to present
THanks,
Bruce 

Created on Sep 1, 2011

@author: egg.davis
'''
from crn import *
import dsl

stations = findStations('TX')
for station in sorted(stations):
    print station.name
    d = getData(station,('2010010100','now'),'WINDSPD')
    output = ["%s,%s" % (dsl.data._prettyDate(f.datetime),f.value) for f in sorted(d.forStation(station))]
    output = ["%d,%02d,%02d,%02d00,%s" % (f.datetime.year,
                                          f.datetime.month+1,
                                          f.datetime.day,
                                          f.datetime.hour,
                                          f.value) for f in sorted(d.forStation(station))]
    filename = "windspeed-%s.txt"%( str(station.name).replace(' ','_'))
    printfile(filename,output,sortData=False)
