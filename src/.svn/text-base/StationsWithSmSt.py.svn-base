'''
Created on Oct 27, 2010

@author: egg.davis

Script to be run monthly: lists all stations which currently observe soil moisture/soil temp, 
along with the date they started observing SM/ST, and the dates 60 and 240 days from that date.
'''

from crn import *
from java.util import Calendar
import time
from operator import itemgetter
from dsl.domainquery import getAllStations

datetimeOfFirstSm = 72255
datetimeOfNow = findDate("now").datetimeId

chunkOfObs = 1000 # Retrieve only 1000 obs at a time

soilStreams = [s.streamId for s in streamDao.getStreams().values() if s.getMeasuresSoil()]

results = []
smStations = list(s for s in stationDao.getStationsCurrentlyWithSmSt().values() if s in getAllStations())

for smStation in smStations:
    print "Searching",smStation.name
    foundSoilOb = False
    for datetime in range(datetimeOfFirstSm,datetimeOfNow,chunkOfObs):
        if foundSoilOb: break
        print "  ",datetime
        obs = getObservations(smStation,(datetime,datetime+chunkOfObs))
        for ob in sorted(obs):         
            if ob.streamId in soilStreams:
                foundSoilOb = True
                results.append((smStation,findDate(ob.datetimeId)))
                break

# Manual adjustments to results (per MP)
results.append((findStation("UT Torrey 7 E"),findDate("2010042000")))

results.sort(key=itemgetter(1)) # sort by 2nd field of tuple, aka date

oneDay = 60 * 60 * 24
sixtyDays = 60 * oneDay
twofortyDays = 240 * oneDay

print "State,Name,Vector,Date of changeover,t+60 days,t+240 days"
for station,date in results:
    name = station.name
    
    sSinceEpoch = date.utcCal.getTime().getTime() / 1000 # Java counts in ms, python in s
    dateInitial  = time.strftime("%m/%d/%y",time.gmtime(sSinceEpoch))
    dateSixty    = time.strftime("%m/%d/%y",time.gmtime(sSinceEpoch + sixtyDays))
    dateTwoforty = time.strftime("%m/%d/%y",time.gmtime(sSinceEpoch + twofortyDays))
    
    print("%s,%s,%s,%s,%s,%s" % (name.state, name.location, name.vector, dateInitial, dateSixty, dateTwoforty))
            