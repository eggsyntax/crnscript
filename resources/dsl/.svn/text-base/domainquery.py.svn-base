'''
Functions for finding the domain objects which define CRN data: Stations, Datetimes, and Elements.

Created on Jan 19, 2011

@author: egg.davis
'''
from crn import *

import gov.noaa.ncdc.crn.domain.Element as Element
import gov.noaa.ncdc.crn.domain.Station as Station
import gov.noaa.ncdc.crn.domain.Datetime as Datetime
import gov.noaa.ncdc.crn.domain.POR as POR

from datetime import datetime as python_datetime
from datetime import tzinfo
import parsedatetime.parsedatetime as pdt 
import parsedatetime.parsedatetime_consts as pdc
import java.util.Map as Map
import time,re
from ElementSubhourlyGroupManager import ElementSubhourlyGroupManager
# Maintain global variables for allstations and allelements, with an associated load time
allstations = None # loaded with the list of stations the 1st time it's needed
allelements = None
globalloadtime = 0

# Maintain a list of commonly-requested elements:
elaliases = {"wind":"WINDSPD", "solar":"SOLARAD", "infrared":"SUR_TEMP", "battery":"BV_DL",
             "precip":"P_OFFICIAL", "precipitation":"P_OFFICIAL", "temp":"T_OFFICIAL",
             "temperature":"T_OFFICIAL", "tmin":"T_MIN", "tmax":"T_MAX"}


# Create a parsedatetime calendar to handle complex date parsing
pdtConstants = pdc.Constants()
dateparser = pdt.Calendar(pdtConstants)

class _UTC(tzinfo):
    """UTC"""
    def __init__(self):
        from datetime import timedelta
        self.ZERO = timedelta(0)
 
    def utcoffset(self, dt):
        return self.ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return self.ZERO

def findStations(*params):
    ''' Finds a station or stations based on station id, name, WBAN, etc (anything that 
        appears in the resulting string), or a list of any of the above. Special case: if 
        you pass in a 4-digit number, findStations() only matches on the station id. Full 
        regex syntax is allowed. Uses smartcase, aka if the input string is all lowercase, 
        it does a case-insensitive search; otherwise case-sensitive.
        Returns a set of unique stations as a list.
        See also: http://docs.python.org/dev/howto/regex.html
    '''
    identifiers = _flatten(params)
    freshenGlobals() # Ensure that allstations and allelements are freshly loaded
    stations = []
    for identifier in identifiers: # separate cases follow for int, Station, other
        if isinstance(identifier,int):
            if identifier not in allstations.keySet(): raise KeyError(str(identifier)+" is not a valid station id")
            stations.append(allstations[identifier])
        elif isinstance(identifier,Station):
            stations.append(identifier)
        else:
            identstring = str(identifier)
            if (re.match("^\d\d\d\d$",identstring)): # Special case: 4-digit station id; surround with brackets to ensure 
                identstring = "\["+identstring+"\]"  # no other matches
            matches = [s for s in allstations.values() if re.search(identstring,str(s),_caseStrategy(identstring))]
            if not matches: raise KeyError("No stations matching "+identstring)
            stations.extend(matches)
    return list(set(stations)) # Convert to set for uniqueness, then back to list for convenience
        
def findStation(identifier):
    ''' Same as findStations(), but returns the first matching station it finds.    '''
    return findStations(identifier).pop()

def findElements(*params):
    ''' Returns elements by name search. There is a list of convenient aliases for the most 
        commonly requested elements, which can be seen with the showElements() command. If 
        the input parameter is not one of these aliases, it is treated as a search against 
        element names & descriptions. Full regex syntax is allowed. Uses smartcase (see 
        findStations()). Note that element names are in all caps, so searches in all caps 
        will match only on name, not on description (sometimes a desired behavior). A numeric 
        parameter (as number or string) is treated as an element id.
        Returns a set of unique elements as a list.
    '''
    identifiers = _flatten(params)
    freshenGlobals() # Ensure that allstations and allelements are freshly loaded
    elements = []
    for identifier in identifiers: # separate cases follow based on parameter type
        if identifier in elaliases: identifier = elaliases[identifier]
        if isinstance(identifier,int): # int parameters are treated as element ids
            if identifier not in allelements.keySet(): raise KeyError(str(identifier)+" is not a valid element id")
            elements.append(allelements[identifier])
        elif isinstance(identifier,Element): # Elements are left untouched
            elements.append(identifier)
        else: # all other cases: convert to string and try to match
            identstring = str(identifier)
            if (re.match("^\d+$",identstring)): # Special case: all digits. Cast to int and find again. 
                elements.append(findElement(int(identstring)))
            else:
                matches = [s for s in allelements.values() if re.search(identstring,str(s),_caseStrategy(identstring))]
                if not matches: raise KeyError("No elements matching "+identstring)
                elements.extend(matches)
    return list(set(elements)) # Convert to set for uniqueness, then back to list for user convenience
    
def findElement(partialname):
    ''' Same as findElements(), but returns only one matching element '''
    return findElements(partialname).pop()

def findDate(date):
    ''' Returns a CRN datetime. Pass in a datestring (most any format, although yyyymmddhh is 
        native and guarantees a unique result), datetime id, python datetime, or "now". Quite 
        flexible about parsing date descriptions like "last Tuesday 8:00". 
    '''
    freshenGlobals()
    if type(date) == Datetime: # If the parameter's already a Datetime, just pass it back
        return date
    if date == "now": # special case. We'll grab the datetime of the most recent observation for a representative station
        return datetimeDao.getDatetime(porDao.getPor(1631).getEndDatetime())
    if type(date) == int:
        return datetimeDao.getDatetime(date)
    if type(date) == python_datetime:
        if date.tzinfo is not None: # must convert to UTC
            date = date.astimezone(_UTC())
        date = date.strftime("%Y%m%d%H")
    if type(date) in (str,unicode):
        try:
            dummyconversion = int(date) # Fail out of this method unless the param is a string of digits
            #                             (to spare the expense of the trip to the DB)
            return datetimeDao.getDatetime(date[0:10]) # Use just the 1st 10 chars -- if they passed in more, we don't care
        except: # standard forms have failed. Turn to 3rd-party parsing.
            timestruct = (dateparser.parse(date))[0]
            if timestruct == None:
                raise ValueError("Invalid argument to findDate. Use YYYYMMDDHH or one of these: http://www.feedparser.org/docs/date-parsing.html")
            timestring = time.strftime("%Y%m%d%H",timestruct)
            datetime =  datetimeDao.getDatetime(timestring)
            if isinstance(datetime,Datetime):
                return datetime
    raise ValueError("Error! Invalid argument to findDate():",date)

def dateRange(begin,end,step=1):
    ''' Allows iteration over a range of hours (inclusive beginning, exclusive end, to
        match Python convention). Typically used like 'for hour in 
        dateRange("1/1/10 8:00","1/2/10 8:00"):'. Takes an optional third argument 
        which lets you iterate over every nth hour.
    '''
    (begin,end) = _parseDatetimeParam((begin,end))
    if begin >= end:
        raise ValueError("Your dates are out of order! %s is >= %s"%(begin,end))
    return (findDate(datetimeid) for datetimeid in range(begin,end,step))
    
def getPor(station):
    ''' Returns a POR object which can be used as the date argument to other methods. Takes a 
        station, stationId, or string (any of the arguments to findStation() are equally 
        valid here).
    '''
    try:
        stationId = findStation(station).stationId
    except:
        raise Exception("Invalid station argument to getPor().")
    return porDao.getPor(stationId)

def getAllElements():
    ''' Provides a list of all CRN elements. '''
    freshenGlobals()
    return allelements.values()
def getAllStations():
    ''' Provides a list of all CRN/RUSHCN stations. '''
    freshenGlobals()
    return allstations.values()

def _parseDatetimeParam(datetimes):
    ''' For creating params to pass to DAO. Takes a datetime (as Datetime, YYYYMMDDHH, 
        datetime id, or "now") or a tuple of two datetimes. Returns a tuple containing the 
        "begin" param and the "end" param, each a datetime id. Also allowed is a parameter 
        of the form (d, "+24"): assuming d is any of the other valid parameter types, the 
        second parameter will be treated as a number of hours to add to d. '''
    if type(datetimes) in [list,tuple]:
        if isinstance(datetimes[0],int):
            begin = datetimes[0]
        else:
            begin = findDate(datetimes[0]).getDatetimeId()
        
        if isinstance(datetimes[1],int):
            end = datetimes[1]
        elif isinstance(datetimes[1],str) and re.match("\+",datetimes[1]): # special case: can pass a pair like ("2009010203","+10")
            end = begin + (int(re.sub("\+","",datetimes[1])))
        else:
            end   = findDate(datetimes[1]).getDatetimeId()
            
    elif type(datetimes) == POR:
        begin = datetimes.getStartDatetime()
        end   = datetimes.getEndDatetime()
    else:
        if isinstance(datetimes,int):
            begin = datetimes
        else:
            begin = findDate(datetimes).getDatetimeId() 
        end   = begin
    return (begin,end)

def freshenGlobals():
    ''' Refreshes the lists of stations and elements. You shouldn't generally need to call 
        this directly; it's automagically called when needed. '''
    global globalloadtime
    global allstations
    global allelements

    if (time.time() - globalloadtime > 1800): # reload every 1/2 hour 
        #print "Refreshing global variables (allstations,allelements)."
        globalloadtime = time.time()                                                          
        allstations = stationDao.getStations() # only load the list of stations once 
        allelements = elementDao.getElements() # only load the list of elements once
        
        # Add the artificial subhourly elements to the allelements list
        esgManager = ElementSubhourlyGroupManager.getManager()
        for curid in esgManager.getAllIds():
            allelements.put(curid,esgManager.generateElement(curid))
        
def showElements():
    ''' Prints a list of the special convenient aliases for CRN elements (e.g. "temp" for 
        hourly average temperature). '''
    for alias in elaliases:
        print alias


def _flatten(*in_tuple):
    ''' Returns a flat list of parameters, regardless of what's passed in. Any map is
        replaced with its values '''
    
    flatlist = []
    for cur in in_tuple:
        if type(cur) in [Map,dict]: cur = cur.values()
        if isinstance(cur,str): # Deal with strings separately; they're the only iterable over
            flatlist.append(cur)# which we don't want to iterate
        else:
            try: # Is it iterable?
                for member in cur:
                    flatlist.extend(_flatten(member))
            except TypeError: # not iterable
                flatlist.append(cur)
    return flatlist

def _caseStrategy(identstring):
    ''' Returns the case-handling strategy appropriate for a particular string
        (case insensitive if all lower-case, otherwise case sensitive). The
        result is appropriate for using as a parameter to re.search().
    '''
    return re.IGNORECASE if (identstring == identstring.lower()) else 0
    
def __doctests():
    ''' These doctests are automatically run if you run the module. You should get no output 
        unless there's a problem.
    
    the findStation() and findStations() methods will search the string you see in the output. 
    >>> findStations("Asheville")
    [Station[1027] NC Asheville 13 S (0255BC,53878)Comm:Y, OpStat: Y, Station[1026] NC Asheville 8 SSW (0246CA,53877)Comm:Y, OpStat: Y]
    >>> findStation("Barrow")
    Station[1007] AK Barrow 4 ENE (00F0B0,27516)Comm:E, OpStat: Y
        
    findElement() and findElements() parallel findStations() closely.
    >>> e = findElements(["official","17"],(findElement(3),"T5_6"))
    >>> printlist(e)
    Element 3:ZTIME:utc hour of observation (end of hour, range: 100-2400)
    Element 17:ST_STD:ir surface temp std dev for the hour
    Element 318:P_OFFICIAL:calculated Geonor precip total for hour
    Element 336:T5_6:calculated average temp for 5 minutes ending at :30
    Element 343:T_OFFICIAL:calculated average temp for hour (calculated from three sensors' hourly averages)

    findDate() takes a datetime id, a YYYYMMDDHH string, most other date representations, or "now".
    >>> findDate(80000)
    Datetime 80000:2009111917 UTC
    >>> findDate("2009010100")
    Datetime 72255:2009010100 UTC

    getPor gets the period of record for a station as an object:
    >>> s = findStation("barrow")
    >>> por = getPor(s)
    >>> type(por)
    <type 'gov.noaa.ncdc.crn.domain.POR'>

    >>> from datetime import timedelta, tzinfo
    >>> from datetime import datetime as python_datetime
    >>> class Eastern(tzinfo):
    ...     def utcoffset(self, dt):
    ...         return timedelta(hours=-5)
    ...     def tzname(self, dt):
    ...         return "US/Eastern"
    ...     def dst(self, dt):
    ...         return timedelta(hours=-4)
    
    >>> dt = python_datetime(2010,10,10,10,10,0,0,Eastern())
    >>> print dt
    2010-10-10 10:10:00-05:00
    >>> print findDate(dt)
    Datetime 87798:2010101015 UTC
    >>> dt = python_datetime(2010,10,10,10,10,0,0)
    >>> print dt
    2010-10-10 10:10:00
    >>> print findDate(dt)
    Datetime 87793:2010101010 UTC

'''
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

