'''
Functions for getting data as lists of Facts, for breaking data into a subhourly representation,
and for grouping data in several useful ways.

Created on Jan 19, 2011

@author: egg.davis
'''

from crn import *

from sets import Set

import java.util.HashMap as HashMap
import java.util.ArrayList as List
import socket
import sys
from dsl.domainquery import _parseDatetimeParam

import gov.noaa.ncdc.crn.domain.ElementValue as ElementValue

MAXQUERYSIZE = 120000 # Maximum number of facts which can be retrieved at once (unless overridden)

def getData(stations,datetimes,elements):
    '''Get facts (as a Collection of Fact domain objects). Pass a station or list of stations (as Station, string or int), a 
        datetime (as Datetime, string, or int) or a tuple containing a beginDatetime and endDatetime (as Datetime, 
        string, or int), and an element or list of elements (as Element, string or int), and get back a list of Facts. 
        That might sound complicated, but the upshot is that you can pass stations, datetimes, and elements in almost 
        any way that happens to be convenient at the time. One handy additional form for dates is to use "+n" for 
        the endDatetime, with n the number of hours' data you'd like, eg ("2009010100","+24")
        
        Limited to getting 120,000 pieces of data at once. If you're SURE that you need more, and you're aware of the
        impact on the database, and you can't break it into several separate queries, call the allowQuerySizeOverride()
        method before each large query. 
        
        The returned Facts have the following properties: station, datetime, element, value, flag, stationId, datetimeId,
        and elementId. The ids are sometimes useful as arguments to DAO methods. 
    '''
    global querySizeOverrideAllowed
    freshenGlobals()
    
    stations = [s.stationId for s in findStations(stations)]
    (begin,end) = _parseDatetimeParam(datetimes)

    # Ensure query is not too big
    if (querySizeOverrideAllowed):
        querySizeOverrideAllowed = False
    else:
        if _queryTooLarge(stations,begin,end,elements):
            raise Exception("Query size too large. Aborting. ("+str(_length(stations))+" stations, "+
                            str(end+1-begin)+" datetimes, "+str(_length(elements))+" elements).")

    # Create a map of parameters in the form that ElementDao wants
    elementIds = [s.elementId for s in findElements(elements)]
    params = HashMap()
    params["stationIds"] = stations
    params["begin"] = begin
    params["end"]   = end
    params["elementIds"] = elementIds
    
    # Done handling input parameters. Go ahead and make the query.
    queryResults = elementDao.getElementValues(params)
    
    factList = _asFactList(queryResults)
    return FactCollection(factList)

querySizeOverrideAllowed = False
def allowQuerySizeOverride():
    '''Overrides the limit on how much data can be requested at one time. Do not call this method unless you're SURE 
    you know what you're doing!'''
    global querySizeOverrideAllowed
    querySizeOverrideAllowed = True

def subhourly(*data):
    ''' Calling subhourly(data) returns a new list of Facts in which all subhourly variables 
        (eg 5-minute precip) are given a single name and their time is changed to the previous 
        hour with a subhourly period appended (eg 15:00 might become 14:35). The output of 
        subhourly is suitable for passing to any of the print methods or to graph(). If you have 
        some other use for data organized in this way, let me know and I'll see if it can be 
        accommodated. Takes the output from getData() or the same list of parameters that
        getData() does. Note that the last subhourly period of the hour is labeled with :60 rather
        than :00 of the next hour. This practice (part of the CRN schema) serves to emphasize
        that the observation period is in the earlier hour, and keeps the 5-minute observations
        distinct from the hourly (which are labeled with :00).
    '''
    ''' This last bit (using :05 to :60) is an open design question. Should crnscript honor this 
        convention or recast the final period as :00 of the following hour? It's an unusual 
        convention, and it means that the time for those subhourly data (say, 13:60) won't 
        match the time for the hourly data (say, 14:00), which could arguably be a desirable
        or undesirable behavior. For the moment I'm sticking with the 
        convention and recasting only where it doesn't work (in the graphing methods).
    '''

    # Were we passed a dataset or parameters for obtaining a dataset?
    if len(data) == 3:
        station,date,element = data
        return subhourly(getData(station,date,element))
    else:
        data = data[0] # unwrap from tuple

    from copy import copy
    newdata = []
    for fact in data:
        newfact = copy(fact)
        if fact.subhourlyName is not None:
            newfact.subhourlyTime # Calling this ensures it's populated *before* the element id is overwritten 
            newfact.element  = Element(fact.subhourlyId,fact.subhourlyName,
                                       fact.subhourlyDescription)
            newfact.datetime = Datetime(fact.datetimeId-1,
                                        fact.datetime.previous().datetime0_23+
                                        fact.subhourlyTime)
            newfact.elementId = fact.subhourlyId
            newfact.datetimeId = newfact.datetime.datetimeId
            ''' If I want to replace 60 with 00 here, use this instead:
            if fact.subhourlyTime == "60": # DB represents as 60 of prev hour but we represent as 00 of current hour
                newfact.datetime = Datetime(fact.datetimeId,fact.datetime.datetime0_23+"00")
            else:
                newfact.datetime = Datetime(fact.datetimeId,fact.datetime.previous().datetime0_23+fact.subhourlyTime)
            '''
        newdata.append(newfact)
    return FactCollection(newdata)

def fillMissing(factCollection):
    factCollection._fillMissing()
    
def _prettyDate(d):
    ''' Takes a datetime or datetime id or CRN datestring (yyyymmddhh) and reformats it as mm/dd/yy hh:mm UTC
    '''
    if isinstance(d,int): d = findDate(d)
    if isinstance(d,Datetime): d = d.getDatetime0_23()
    minutes = d[10:12] if len(d) > 10 else "00"
    return str("%s/%s/%s %s:%s UTC" % (d[4:6],d[6:8],d[2:4],d[8:10],minutes))
 
def _length(x):
    ''' private utility method for getting the length of an arbitrary object which may or may not be a list '''
    try:
        l = len(x)
    except:
        l = 1
    return l

def _asFactList(data):
    ''' takes a list of ElementValue, or a map/dict whose values are ElementValue, and returns a list of Facts. '''
    try:
        data = data.values() # handles maps and dicts
    except:
        pass # no problem if not
    return [Fact(r) for r in data]

def _queryTooLarge(stations,begin,end,elements):
    ''' Returns True if number of facts requested is too large. '''
    elementlength = 1 if isinstance(elements,str) else _length(elements) # Slightly fancier handling because getData hasn't called findElements (because it has to separate out soil elements). Can change this once soil els are in the DB.
    querysize = _length(stations) * (end+1 - begin) * elementlength
    return querysize > MAXQUERYSIZE

def __doctests():
    ''' These doctests are automatically run if you run the module. You should get no output unless there's a 
    problem.
    

    getData() is the central method of pythonutilities. Takes a station or stations, a date or tuple of begin/end 
    dates, and an element or elements, each in any reasonable form.
    >>> station = findStation("Barrow")
    >>> el = findElements("OFFICIAL")
    >>> date = findDate("2009010100")
    >>> data = getData(station,date,el)
    >>> printlist(data)
    AK Barrow 4 ENE, 2009010100, P_OFFICIAL: 0 (0)
    AK Barrow 4 ENE, 2009010100, T_OFFICIAL: -22 (0)

    All soil data are now in the DB so they should function like any other elements:
    >>> e = findElements("soil")
    >>> d = getData("crossville","10/1/10 8:00",e)
    >>> printlist(d)
    TN Crossville 7 NW, 2010100108, SM1005: 16.19 (0)
    TN Crossville 7 NW, 2010100108, SM1010: 18.70 (0)
    TN Crossville 7 NW, 2010100108, SM1020: 19.23 (0)
    TN Crossville 7 NW, 2010100108, SM1050: 25.62 (0)
    TN Crossville 7 NW, 2010100108, SM1100: 25.03 (0)
    TN Crossville 7 NW, 2010100108, SM2005: 20.71 (0)
    TN Crossville 7 NW, 2010100108, SM2010: 20.79 (0)
    TN Crossville 7 NW, 2010100108, SM2020: 23.85 (0)
    TN Crossville 7 NW, 2010100108, SM2050: 28.13 (0)
    TN Crossville 7 NW, 2010100108, SM2100: 22.11 (0)
    TN Crossville 7 NW, 2010100108, SM3005: 11.51 (0)
    TN Crossville 7 NW, 2010100108, SM3010: 16.04 (0)
    TN Crossville 7 NW, 2010100108, SM3020: 19.74 (0)
    TN Crossville 7 NW, 2010100108, SM3050: 24.18 (0)
    TN Crossville 7 NW, 2010100108, SM3100: 20.48 (0)
    TN Crossville 7 NW, 2010100108, SMV005: 25.60 (0)
    TN Crossville 7 NW, 2010100108, SMV010: 28.90 (0)
    TN Crossville 7 NW, 2010100108, SMV020: 31.90 (0)
    TN Crossville 7 NW, 2010100108, SMV050: 37.60 (0)
    TN Crossville 7 NW, 2010100108, SMV100: 33.80 (0)
    TN Crossville 7 NW, 2010100108, SMV1005: 26.0 (0)
    TN Crossville 7 NW, 2010100108, SMV1010: 29.2 (0)
    TN Crossville 7 NW, 2010100108, SMV1020: 29.9 (0)
    TN Crossville 7 NW, 2010100108, SMV1050: 37.3 (0)
    TN Crossville 7 NW, 2010100108, SMV1100: 36.6 (0)
    TN Crossville 7 NW, 2010100108, SMV2005: 31.7 (0)
    TN Crossville 7 NW, 2010100108, SMV2010: 31.8 (0)
    TN Crossville 7 NW, 2010100108, SMV2020: 35.3 (0)
    TN Crossville 7 NW, 2010100108, SMV2050: 39.9 (0)
    TN Crossville 7 NW, 2010100108, SMV2100: 33.4 (0)
    TN Crossville 7 NW, 2010100108, SMV3005: 19.1 (0)
    TN Crossville 7 NW, 2010100108, SMV3010: 25.8 (0)
    TN Crossville 7 NW, 2010100108, SMV3020: 30.5 (0)
    TN Crossville 7 NW, 2010100108, SMV3050: 35.7 (0)
    TN Crossville 7 NW, 2010100108, SMV3100: 31.4 (0)
    TN Crossville 7 NW, 2010100108, ST005: 18.10 (0)
    TN Crossville 7 NW, 2010100108, ST010: 18.80 (0)
    TN Crossville 7 NW, 2010100108, ST020: 19.20 (0)
    TN Crossville 7 NW, 2010100108, ST050: 19.60 (0)
    TN Crossville 7 NW, 2010100108, ST100: 19.90 (0)
    TN Crossville 7 NW, 2010100108, ST1005: 17.85 (0)
    TN Crossville 7 NW, 2010100108, ST1010: 18.00 (0)
    TN Crossville 7 NW, 2010100108, ST1020: 18.80 (0)
    TN Crossville 7 NW, 2010100108, ST1050: 19.39 (0)
    TN Crossville 7 NW, 2010100108, ST1100: 19.70 (0)
    TN Crossville 7 NW, 2010100108, ST2005: 18.30 (0)
    TN Crossville 7 NW, 2010100108, ST2010: 18.95 (0)
    TN Crossville 7 NW, 2010100108, ST2020: 19.34 (0)
    TN Crossville 7 NW, 2010100108, ST2050: 19.70 (0)
    TN Crossville 7 NW, 2010100108, ST2100: 19.94 (0)
    TN Crossville 7 NW, 2010100108, ST3005: 18.15 (0)
    TN Crossville 7 NW, 2010100108, ST3010: 19.40 (0)
    TN Crossville 7 NW, 2010100108, ST3020: 19.35 (0)
    TN Crossville 7 NW, 2010100108, ST3050: 19.70 (0)
    TN Crossville 7 NW, 2010100108, ST3100: 20.10 (0)

    >>> d = getData("stillwater",("10/10/10 10:00","+2"),("temp","precip"))
    >>> printlist(d.groupedByStation())
    (Station[1005] OK Stillwater 2 W (00D65C,53926)Comm:Y, OpStat: Y, OK Stillwater 2 W, 2010101010, P_OFFICIAL: 0 (0), OK Stillwater 2 W, 2010101010, T_OFFICIAL: 12.2 (0), OK Stillwater 2 W, 2010101011, P_OFFICIAL: 0 (0), OK Stillwater 2 W, 2010101011, T_OFFICIAL: 12.3 (0), OK Stillwater 2 W, 2010101012, P_OFFICIAL: 0 (0), OK Stillwater 2 W, 2010101012, T_OFFICIAL: 13.3 (0))
    (Station[1006] OK Stillwater 5 WNW (00E3C6,53927)Comm:Y, OpStat: Y, OK Stillwater 5 WNW, 2010101010, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101010, T_OFFICIAL: 10.5 (0), OK Stillwater 5 WNW, 2010101011, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101011, T_OFFICIAL: 10.5 (0), OK Stillwater 5 WNW, 2010101012, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101012, T_OFFICIAL: 12 (0))

    >>> d = getData("stillwater 5",("10/10/10 1:00","+35"),("temp","precip"))
    >>> printlist(d.groupedByLocalDay())
    ('20101009', OK Stillwater 5 WNW, 2010101001, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101001, T_OFFICIAL: 20.1 (0), OK Stillwater 5 WNW, 2010101002, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101002, T_OFFICIAL: 17 (0), OK Stillwater 5 WNW, 2010101003, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101003, T_OFFICIAL: 15.3 (0), OK Stillwater 5 WNW, 2010101004, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101004, T_OFFICIAL: 14.2 (0), OK Stillwater 5 WNW, 2010101005, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101005, T_OFFICIAL: 13 (0), OK Stillwater 5 WNW, 2010101006, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101006, T_OFFICIAL: 12.3 (0))
    ('20101010', OK Stillwater 5 WNW, 2010101007, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101007, T_OFFICIAL: 11.7 (0), OK Stillwater 5 WNW, 2010101008, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101008, T_OFFICIAL: 11.3 (0), OK Stillwater 5 WNW, 2010101009, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101009, T_OFFICIAL: 11 (0), OK Stillwater 5 WNW, 2010101010, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101010, T_OFFICIAL: 10.5 (0), OK Stillwater 5 WNW, 2010101011, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101011, T_OFFICIAL: 10.5 (0), OK Stillwater 5 WNW, 2010101012, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101012, T_OFFICIAL: 12 (0), OK Stillwater 5 WNW, 2010101013, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101013, T_OFFICIAL: 14.1 (0), OK Stillwater 5 WNW, 2010101014, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101014, T_OFFICIAL: 15.8 (0), OK Stillwater 5 WNW, 2010101015, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101015, T_OFFICIAL: 18.5 (0), OK Stillwater 5 WNW, 2010101016, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101016, T_OFFICIAL: 20.1 (0), OK Stillwater 5 WNW, 2010101017, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101017, T_OFFICIAL: 24 (0), OK Stillwater 5 WNW, 2010101018, P_OFFICIAL: 0.2 (0), OK Stillwater 5 WNW, 2010101018, T_OFFICIAL: 23.1 (0), OK Stillwater 5 WNW, 2010101019, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101019, T_OFFICIAL: 21.6 (0), OK Stillwater 5 WNW, 2010101020, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101020, T_OFFICIAL: 22.9 (0), OK Stillwater 5 WNW, 2010101021, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101021, T_OFFICIAL: 23.1 (0), OK Stillwater 5 WNW, 2010101022, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101022, T_OFFICIAL: 24 (0), OK Stillwater 5 WNW, 2010101023, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101023, T_OFFICIAL: 23.4 (0), OK Stillwater 5 WNW, 2010101100, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101100, T_OFFICIAL: 21.6 (0), OK Stillwater 5 WNW, 2010101101, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101101, T_OFFICIAL: 19.6 (0), OK Stillwater 5 WNW, 2010101102, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101102, T_OFFICIAL: 18.2 (0), OK Stillwater 5 WNW, 2010101103, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101103, T_OFFICIAL: 17.5 (0), OK Stillwater 5 WNW, 2010101104, P_OFFICIAL: 1.2 (0), OK Stillwater 5 WNW, 2010101104, T_OFFICIAL: 16.1 (0), OK Stillwater 5 WNW, 2010101105, P_OFFICIAL: 1.2 (0), OK Stillwater 5 WNW, 2010101105, T_OFFICIAL: 15.8 (0), OK Stillwater 5 WNW, 2010101106, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101106, T_OFFICIAL: 15.3 (0))
    ('20101011', OK Stillwater 5 WNW, 2010101107, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101107, T_OFFICIAL: 14.6 (0), OK Stillwater 5 WNW, 2010101108, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101108, T_OFFICIAL: 14.5 (0), OK Stillwater 5 WNW, 2010101109, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101109, T_OFFICIAL: 13.5 (0), OK Stillwater 5 WNW, 2010101110, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101110, T_OFFICIAL: 12.6 (0), OK Stillwater 5 WNW, 2010101111, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101111, T_OFFICIAL: 11.9 (0), OK Stillwater 5 WNW, 2010101112, P_OFFICIAL: 0 (0), OK Stillwater 5 WNW, 2010101112, T_OFFICIAL: 11.1 (0))

    >>> data = getData("Asheville 8 SSW",("2009010100","+2"),("temp","precip"))
    >>> printlist(data.groupedByObservation())
    ((NC Asheville 8 SSW, '01/01/09 00:00 UTC'), P_OFFICIAL: 0 (0), T_OFFICIAL: -0.2 (0))
    ((NC Asheville 8 SSW, '01/01/09 01:00 UTC'), P_OFFICIAL: 0 (0), T_OFFICIAL: -0.6 (0))
    ((NC Asheville 8 SSW, '01/01/09 02:00 UTC'), P_OFFICIAL: 0 (0), T_OFFICIAL: -1.5 (0))

    >>> data = subhourly('asheville 8',('2009123108'),('calculated average temp for 5 minutes','RH percent average for 5 minutes'))
    >>> printlist(data.groupedByObservation())
    ((NC Asheville 8 SSW, '12/31/09 07:05 UTC'), RH: 94.40 (0), T5: 1.4 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:10 UTC'), RH: 95.20 (0), T5: 1.1 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:15 UTC'), RH: 95.60 (0), T5: 1.6 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:20 UTC'), RH: 92.40 (0), T5: 1.9 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:25 UTC'), RH: 94.80 (0), T5: 1.5 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:30 UTC'), RH: 94.90 (0), T5: 1.6 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:35 UTC'), RH: 95.60 (0), T5: 1.3 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:40 UTC'), RH: 97.10 (0), T5: 1.1 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:45 UTC'), RH: 97.00 (0), T5: 1.3 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:50 UTC'), RH: 97.40 (0), T5: 0.8 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:55 UTC'), RH: 97.90 (0), T5: 0.6 (0))
    ((NC Asheville 8 SSW, '12/31/09 07:60 UTC'), RH: 98.30 (0), T5: 0.6 (0))

    >>> data = getData('AK',('10/10/10 8:00','+3'),('temp','precip'))
    >>> printlist(data.forStation('barrow').forElement('temp'))
    AK Barrow 4 ENE, 2010101008, T_OFFICIAL: -6.6 (0)
    AK Barrow 4 ENE, 2010101009, T_OFFICIAL: -6.3 (0)
    AK Barrow 4 ENE, 2010101010, T_OFFICIAL: -6.5 (0)
    AK Barrow 4 ENE, 2010101011, T_OFFICIAL: -6.3 (0)
        
'''

if __name__ == "__main__":
    import doctest #@UnresolvedImport
    doctest.testmod()

