'''
Created on Jun 13, 2011

@author: scott.embler
'''
from crn import findDate, findStation, getData
from datetime import datetime as pydt, timedelta, tzinfo
from timezone import *
import calendar


class Period(object):
    '''
    An abstract representation for a period of time, defined by a starting and 
    ending date.  The Period is assumed to be continuous.
    '''
    def start(self):
        pass
    
    def end(self):
        pass

class Day(Period):
    '''
    Represents the Period between the start and end of a Calendar Day.  Days can also
    provide their neighboring Days via next().  Days are also specific to a timezone.
    Once created, the timezone for a Day should not be changed.  Any neighboring Days
    are shown with the same timezone as the called Day.
    '''
    def __init__ (self, year, month, day, tzinfo=Utc()):
        self.year = year
        self.month = month
        #Ordinal:  of or pertaining to order, rank, or position in a series
        self.ordinal = day
        self.tzinfo = tzinfo
        self._start_date = None
        self._end_date = None
    
    def next (self):
        tomorrow = self.start() + timedelta(days=1)
        return Day(tomorrow.year, tomorrow.month, tomorrow.day, tzinfo=self.tzinfo)
    
    def start(self):
        if self._start_date == None:
            self._start_date = pydt(self.year, self.month, self.ordinal, tzinfo=self.tzinfo)
        return self._start_date
    
    def end(self):
        if self._end_date == None:
            self._end_date = self.start() + timedelta(days=1)
        return self._end_date
    
    def __str__ (self):
        return str(self.year) + "-" + '%02d' % self.month + "-" + '%02d' % self.ordinal
    
    def __hash__ (self):
        return (self.year * 12 * 31) + (self.month * 31) + (self.ordinal - 1)
    
    def __eq__ (self, other):
        try:
            return self.year == other.year and self.month == other.month and self.ordinal == other.ordinal and self.tzinfo == other.tzinfo
        except:
            return False
    
    def __ne__ (self, other):
        return not self == other
    
    def __le__ (self, other):
        return self.start() <= other.start()
    
    def __lt__ (self, other):
        return self.start() < other.start()
    
    def __ge__ (self, other):
        return self.start() >= other.start()
    
    def __gt__ (self, other):
        return self.start() > other.start()
    

def days(por, localize=True):
    '''
    Iterates through each Day that overlaps the given period-of-record.  By default
    the Days are localized, using the timezone of the period-of-record's station. 
    This can be overridden to produce Days with a UTC timezone.
    '''
    if localize:
        station = findStation(por.getStationId())
        offset = station.offset
        tz = StationTz(station)
    else:
        offset = 0
        tz = Utc()
        
    #We first need a way to understand what the por integers mean.  To do that,
    #we'll get CRN Datetimes from the database.
    por_start = findDate(por.startDatetime)
    por_end = findDate(por.endDatetime)
    
    #Now we have CRN Datetimes, but they are in UTC.  Depending on the parameters
    #we might need to shift to a different CRN Datetime to find out what month it
    #is in local standard time.  We can find LST by applying the station offset
    #to the CRN Datetimes we have, and making another database select.
    start = findDate(por_start.getLstDatetime0_23(offset))
    end = findDate(por_end.getLstDatetime0_23(offset))
    
    #Now we have CRN Datetimes that should show the correct year, month, and day
    #integers. But keep in mind that the Datetime objects use Java calendars, which
    #uses a 0-11 indexing instead of the 1-12 indexing that python expects. Add 1 
    #to fix this.
    first = Day(start.year, start.month + 1, start.day, tzinfo=tz)
    last = Day(end.year, end.month + 1, end.day, tzinfo = tz)
    
    current = first
    while current <= last:
        yield current
        current = current.next()


class Month(Period):
    '''
    Represents the Period between the start and end of a Calendar Month.  Also provides
    helper functions which describe characteristics about this Month.  Months can also
    provide their neighboring Months via next().  Months are also specific to a timezone.
    Once created, the timezone for a Month should not be changed.  Any neighboring Months
    are shown with the same timezone as the called Month.
    '''
    def __init__ (self, year, ordinal, tzinfo=Utc()):
        #The year of this Month.
        self.year = year
        
        #Ordinal:  of or pertaining to order, rank, or position in a series.
        #In this case, a series of month indicators (1-12).
        self.ordinal = ordinal
        
        #The timezone that this Month applies to, which influences the start and end datetimes.
        self.tzinfo = tzinfo
        
        #Private storage for a list of Days that is lazily created by the days() function.
        #Represents all of the Day periods that fall within this Month.
        self._day_list = None
        
        #Private storage for a python datetime representing the start of this Month.
        #This value is filled in when the first call to start() is made.
        self._start_date = None
        
        #Private storage for a python datetime representing the end of this Month.
        #This value is filled in when the first call to start() is made.
        self._end_date = None
    
    def next (self):
        '''
        Returns the next Month following this Month.  Timezone information for the following
        Month will be identical to the timezone for this Month.
        '''
        year = self.year
        month  = self.ordinal
        if month == 12:
            year = year + 1
        month = (month % 12) + 1
        return Month(year, month, tzinfo=self.tzinfo)
    
    def start(self):
        '''
        Returns the python datetime at which this Month begins.  It is an inclusive datetime.
        '''
        if self._start_date == None:
            self._start_date = pydt(self.year, self.ordinal, 1, tzinfo=self.tzinfo)
        return self._start_date
    
    def end(self):
        '''
        Returns the python datetime before which this Month ends.  It is not inclusive.  Meaning 
        that the returned datetime is actually the beginning of the next Month.
        '''
        if self._end_date == None:
            self._end_date = self.next().start()
        return self._end_date
    
    def days(self):
        '''
        Returns a list of Days that exist within this Month.  The list is ordered by ascending day.
        '''
        if self._day_list == None:
            cal = calendar.Calendar()
            self._day_list = [Day(self.year, self.ordinal, day, tzinfo=self.tzinfo) for day in cal.itermonthdays(self.year, self.ordinal) if day != 0]
        return self._day_list
    
    def hours(self):
        '''
        Returns the number of hours included in this Month.
        '''
        return len(self.days()) * 24
    
    def __repr__ (self):
        return "Month(" + str(self.year) + "," + str(self.ordinal) +", tzinfo=" + self.tzinfo.__repr__() + ")"
    
    def __str__ (self):
        return str(self.year) + "-" + '%02d' % self.ordinal
    
    def __hash__ (self):
        return (self.year * 12) + (self.ordinal - 1)
    
    def __eq__ (self, other):
        try:
            return self.year == other.year and self.ordinal == other.ordinal and self.tzinfo == other.tzinfo
        except:
            return False
    
    def __ne__ (self, other):
        return not self == other
    
    def __le__ (self, other):
        return self.start() <= other.start()
        

def months(por, localize=True):
    '''
    Iterates through each Month that overlaps the given period-of-record.  By default
    the Months are localized, using the timezone of the period-of-record's station. 
    This can be overridden to produce Months with a UTC timezone.
    '''
    if localize:
        station = findStation(por.getStationId())
        offset = station.offset
        tz = StationTz(station)
    else:
        offset = 0
        tz = Utc()
    
    #We first need a way to understand what the por integers mean.  To do that,
    #we'll get CRN Datetimes from the database.
    por_start = findDate(por.startDatetime)
    por_end = findDate(por.endDatetime)
    
    #Now we have CRN Datetimes, but they are in UTC.  Depending on the parameters
    #we might need to shift to a different CRN Datetime to find out what month it
    #is in local standard time.  We can find LST by applying the station offset
    #to the CRN Datetimes we have, and making another database select.
    start = por_start.add(offset)
    end = por_end.add(offset)
    
    #Now we have CRN Datetimes that should show the correct year and month integers.
    #But keep in mind that the Datetime objects use Java calendars, which uses a 0-11
    #indexing instead of the 1-12 indexing that python expects. Add 1 to fix this.
    first = Month(start.year, start.month + 1, tzinfo=tz)
    last = Month(end.year, end.month + 1, tzinfo = tz)
    
    #Iterate through all Months which intercept the given period of record.
    current = first
    while current <= last:
        yield current
        current = current.next()

def getDataForPeriod(station, period, elements):
    '''
    Returns a collection of Facts which were produced by the specified stations,
    over the specified period, corresponding to the specified elements.
    '''
    utc = Utc()
    #We actually start from the ending of this hour when reading from the CRN database.
    first = (period.start() + timedelta(hours=1)).astimezone(utc)
    last = period.end().astimezone(utc)
    return getData(station, (first, last), elements)

def __doctests():
    ''' These doctests are automatically run if you run the module. You should get no output unless there's a 
    problem.
    
    >>> m = Month(2000, 12)
    
    >>> m == Month(2000, 12)
    True
    >>> m != Month(1999, 5)
    True
    >>> str(m)
    '2000-12'
    >>> m.next() == Month(2001, 1)
    True
    >>> m <= Month(2001, 1)
    True
    >>> m.start() == pydt(2000, 12, 1, tzinfo=Utc())
    True
    >>> m.end() == pydt(2001, 1, 1, tzinfo=Utc())
    True
    >>> len(m.days())
    31
    >>> m.hours()
    744
    '''
    
if __name__ == "__main__":
    import doctest #@UnresolvedImport
    doctest.testmod()