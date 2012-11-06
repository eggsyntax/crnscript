'''
Provides functions for managing observations.

Created on Jan 19, 2011

@author: egg.davis
'''

from crn import *

import java.util.ArrayList as List
from dsl.domainquery import _parseDatetimeParam

def getObservations(stations,datetimes):
    ''' Returns a list of Observations. These do *not* contain data, but are essentially metadata for the measurements for a 
        particular station-datetime: whether it exists, when it was loaded into the database, etc. Takes a station
        (as Station or station id) or list of stations, and a datetime or tuple of datetimes. Note that as of now
        it is possible to get multiple datetimes for one station or multiple stations for one datetime but *not*
        multiple stations for multiple datetimes.
    '''

    freshenGlobals()
    stationIds = List([s.stationId for s in findStations(stations)])
    (begin,end) = _parseDatetimeParam(datetimes)

    if len(stationIds) > 1 and begin != end:
        raise Exception("Can get observations for multiple stations or multiple datetimes, but NOT both simultaneously.")
    elif len(stationIds) > 1 and begin == end:
        return list(observationDao.getObservations(begin,stationIds).values())
    else:
        return list(observationDao.getObservations(begin,end,stationIds.get(0)).values())

def __doctests():
    ''' These doctests are automatically run if you run the module. 
        You should get no output unless there's a problem.
    
    >>> printlist(getObservations("barrow",("2/2/10 2:00","+2")))
    Observation 1007:81785:2 source: 1:7:Crn_201002012112.lrgs
    Observation 1007:81786:2 source: 1:7:Crn_201002012212.lrgs
    Observation 1007:81787:2 source: 1:7:Crn_201002012312.lrgs
    >>> printlist(getObservations("NC","2/2/10 2:00"))
    Observation 1026:81785:8 source: 1:2:Crn_201002012202.lrgs
    Observation 1027:81785:8 source: 1:4:Crn_201002012202.lrgs
    Observation 1347:81785:8 source: 1:43:Crn_201002012122.lrgs

    '''
    
if __name__ == "__main__":
    import doctest #@UnresolvedImport
    doctest.testmod()

