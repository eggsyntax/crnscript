'''
Produces station.name,lat,lon,datestring,solar,solarmax,solarmin,solarstd for each station
for POR

Created on May 9, 2011
@author: egg.davis
'''
from __future__ import with_statement
from crn import *
import os
import dsl

solarels = findElements('SOLARAD','SR_STD','SOLRAD_MX','SOLRAD_MN')
header = ("Station,Latitude,Longitude,Datetime,SOLARAD,SR_STD,SOLRAD_MX,SOLRAD_MN\n")
stations = stationDao.getNontestStations()

for station in stations.values():
    stationname = str(station.name).replace(" ","_")
    headerwritten = False
    print stationname
    namelatlong = "%s,%s,%s"%(station.name,station.latitude,station.longitude)
    filename = "C:/Users/Jesse.Davis/Documents/Temp/solardata/"+stationname+".txt"
    if os.path.exists(filename): continue # For right now: don't refresh existing files TODO:
    with open(filename,"w") as file:
        for year in range(2001,2012):
#            raw = getData(station,("1/1/%d 0:00"%(year),"12/31/%d 23:00"%(year)),solarels)
            start = findDate("1/1/%d 0:00"%(year))
            mid = findDate("7/1/%d 0:00"%(year)).datetimeId
            end = findDate("1/1/%d 0:00"%(year+1))
            raw = FactCollection()
            for el in solarels:
                raw += getData(station,(start,mid-1),el)
                raw += getData(station,(mid,end),el)
            if not raw or not len(raw): continue
            if not headerwritten: # using this slightly awkward idiom to prevent files being written for stations with no data 
                file.write(header)
                headerwritten = True
            print "  retrieved data for",year
            fillMissing(raw)
            for hour in dateRange(start,end):
                datestring = dsl.data._prettyDate(hour)
                outlist = [namelatlong,datestring]
                try:
                    facts = raw.forDatetime(hour)
                    try:
                        outlist.append(str(facts.forElement('SOLARAD')[0].value))
                    except IndexError:
                        outlist.append("-999")
                    try:
                        outlist.append(str(facts.forElement('SR_STD')[0].value))
                    except IndexError:
                        outlist.append("-999")
                    try:
                        outlist.append(str(facts.forElement('SOLRAD_MX')[0].value))
                        outlist.append(str(facts.forElement('SOLRAD_MN')[0].value))
                    except IndexError:
                        outlist.extend(["-999","-999"])
                except:
                    outlist.extend(['-999','-999','-999','-999'])

                file.write(",".join(outlist) + "\n")
