'''
Created on Jun 22, 2011

@author: scott.embler
'''
from period import *
from decimal import Decimal, ROUND_HALF_UP

def byLocalDay(fact):
    '''
    Returns a Day that the given Fact exists within.  This Day can be used as 
    a key for grouping/sorting/filtering collections.  The Day returned is always
    in the local-time of the station which produced the Fact.
    '''
    #To get the date in local time, we offset by the time difference, and then offset
    #by -1 because crn datetimes refers to the *end* of the observation hour, whereas
    #python datetimes use the beginning of the hour.
    localdate = fact.getDatetime().add(fact.station.getOffset()).add(-1)
    #Keep in mind that the Datetime objects use Java calendars, which uses a 0-11
    #indexing instead of the 1-12 indexing that python expects. Add 1 to fix this.
    return Day(localdate.getYear(), localdate.getMonth() + 1, localdate.getDay(), tzinfo=StationTz(fact.getStation()))

def byLocalMonth(fact):
    '''
    Returns a Month that the given Fact exists within.  This Month can be used as 
    a key for grouping/sorting/filtering collections.  The Month returned is always
    in the local-time of the station which produced the Fact.
    '''
    #To get the date in local time, we offset by the time difference, and then offset
    #by -1 because crn datetimes refers to the *end* of the observation hour, whereas
    #python datetimes use the beginning of the hour.
    localdate = fact.getDatetime().add(fact.station.getOffset()).add(-1)
    #Keep in mind that the Datetime objects use Java calendars, which uses a 0-11
    #indexing instead of the 1-12 indexing that python expects. Add 1 to fix this.
    return Month(localdate.getYear(), localdate.getMonth() + 1, tzinfo=StationTz(fact.getStation()))


class SOD:
    '''
    Summary of Day.  Summarizes temperature and precipitation for the period of a Day,
    assuming the data provided constitutes a valid Day of Facts.  Summaries are not
    computed if the necessary number of Facts are unavailable.
    
    Validation:
      Temperature, Precipitation (between 22 and 24 hours in a day)
      
    Elements Required:
      Temperature Maximum (T_MAX)
      Temperature Minimum (T_MIN)
      Temperature Mean    (T_MAX, T_MIN)
      Temperature Average (T_OFFICIAL)
      Precipitation Sum   (P_OFFICIAL)
    '''
    def __init__(self, day, station, data):
        self.day = day
        self.station = station
        self.temp_avg = None
        self.temp_max = None           
        self.temp_min = None     
        self.temp_mean = None        
        self.precip_sum = None
            
        if day in data:
            facts = data.get(day).forStation(station)
            
            t_avg = calc(average, validHoursInDay, extract("T_OFFICIAL", facts))
            t_max = calc(maximum, validHoursInDay, extract("T_MAX", facts))
            t_min = calc(minimum, validHoursInDay, extract("T_MIN", facts))
            
            self.temp_avg = round(t_avg, '0.1')
            self.temp_max = round(t_max, '0.1')
            self.temp_min = round(t_min, '0.1')
            self.temp_mean = round(mean(t_max, t_min), '0.1')
            
            precip = extract("P_OFFICIAL", facts)
            self.precip_sum = round(calc(sum, validHoursInDay, precip), '0.1')
    
    def __str__(self):
        return "SOD: " + str(self.day) + ", " + str(self.station)
    
    def __hash__ (self):
        return self.day.__hash__() * self.station.getStationId()
    
    def __eq__ (self, other):
        try:
            return self.day == other.day and self.station == other.station
        except:
            return False
    
    def __ne__ (self, other):
        return not self == other
    
    def __le__ (self, other):
        return self.day <= other.day
    
    def __lt__(self, other):
        return self.day < other.day
    
    def __ge__ (self, other):
        return self.day >= other.day
    
    def __gt__(self, other):
        return self.day > other.day


class SOM:
    '''
    Summary of Month.  Summarizes temperature and precipitation for the period of a Month,
    assuming the data provided constitutes a valid Month of Facts.  Summaries are not
    computed if the necessary number of Facts are unavailable.
    
    Validation:
      Temperature   ( <= 3 consecutive days missing or <= 5 total days missing)
      Precipitation ( >= 95% hours available)
      
    Elements Required:
      Temperature Maximum (T_MAX)
      Temperature Minimum (T_MIN)
      Temperature Mean    (T_MAX, T_MIN)
      Temperature Average (T_OFFICIAL)
      Precipitation Sum   (P_OFFICIAL)
    '''
    def __init__(self, month, station, data):
        self.month = month
        self.station = station
        self.temp_avg = None
        self.temp_max = None
        self.temp_min = None
        self.temp_mean = None
        self.precip_sum = None
            
        if month in data:
            month_facts = data.get(month).forStation(station)
            day_facts = month_facts._grouped(byLocalDay)
            summaries_of_days = sorted([SOD(day, station, day_facts) for day in self.month.days()])
                        
            daily_maximums = [s.temp_max for s in summaries_of_days]
            daily_minimums = [s.temp_min for s in summaries_of_days]
            daily_averages = [s.temp_avg for s in summaries_of_days]
            
            t_max = calc(avg, validDaysInMonth, daily_maximums)
            t_min = calc(avg, validDaysInMonth, daily_minimums)
            t_avg = calc(avg, validDaysInMonth, daily_averages)
            
            self.temp_max = round(t_max, '0.1')
            self.temp_min = round(t_min, '0.1')
            self.temp_avg = round(t_avg, '0.1')
            self.temp_mean = round(mean(t_max, t_min), '0.1')
                        
            #We don't use the Summary Of Day precipitation because monthly
            #precipitation has different requirements.  There must be at least 97%
            #of the hourly precipitation measurements available for the month.
            precip = extract("P_OFFICIAL", month_facts)
            hours_of_precip = count(precip)
            if percentage(hours_of_precip, self.month.hours()) >= 0.97 :
                self.precip_sum = round(sum(precip), '0.1')

    def __str__ (self):
        '''
        Produces a String representation of this Summary of Month.
        '''
        return "SOM: " + str(self.month) + ", " + str(self.station)


def validHoursInDay(data):
    '''
    Returns whether or not the given collection has enough data for calculating a
    day summary.
    '''
    return len(data) >= 22 and len(data) < 25


def validDaysInMonth(data):
    '''
    Determines whether or not there is sufficient information to compute monthly
    summaries from the given daily data.  If there is enough information then True 
    will be returned, otherwise False.  The determination is made according to the number
    of valid days in the month.  Where there can be at most 3 consecutive days missing,
    or 5 total days missing.
    '''
    return max(consecutive(data, None)) <= 3 and data.count(None) <= 5

def extract(named, facts):
    try:
        return facts.forElement(named)
    except:
        return None
    
def calc(function, validation, decimals):
    try:
        if validation(decimals):
            return function(decimals)
        else:
            return None
    except:
        return None

    
def round(decimal, precision):
    '''
    Returns the given decimal rounded to the desired precision.  The rounding 
    technique used is ROUND_HALF_UP.
    '''
    if decimal != None and precision != None:
        return decimal.quantize(Decimal(precision), ROUND_HALF_UP)
    return None

def consecutive(lst, value):
    '''
    Iterates through a list, counting the number of times a value was consecutively 
    encountered.  Zero will be used when a non-matching element is encountered.
    
    Example:
      consecutive(True, [True, False, True, True, True, False, True])
      yields
      [1, 0, 1, 2, 3, 0, 1]
    '''
    count = 0
    for i in lst:
        if i == value:
            count += 1
        else:
            count = 0
        yield count
        
def maximum(data):
    if data != None:
        return max([f.value for f in data])
    else:
        return None

def minimum(data):
    if data != None:
        return min([f.value for f in data])
    else:
        return None

def average(data):
    if data != None:
        try:
            return sum(data) / data.count()
        except Exception, e:
            print e
    else:
        return None
    
def avg(data):
    if data != None:
        try:
            return sum(filter(None, data)) / (len(data) - data.count(None))
        except Exception, e:
            print e
    else:
        return None

def mean(max, min):
    if max != None and min != None:
        return (max + min)/2
    else:
        return None

def percentage(available, expected):
    return float(available) / float(expected)

def count(data):
    if data != None:
        return len(data)
    else:
        return 0
    
def __doctests():
    ''' These doctests are automatically run if you run the module. You should get no output unless there's a 
    problem.
    >>> from crn import FactCollection
    
    >>> summary = SOM(Month(2000,01), None, FactCollection([]))
    
    >>> str(summary)
    'SOM: 2000-01, None'
    
    >>> list(consecutive([1, None, 2, None, None, 3, None, None, None], None))
    [0, 1, 0, 1, 2, 0, 1, 2, 3]
    
    >>> avg([None, 1, 2, 3])
    2
    
    >>> validHoursInDay(range(0,24))
    True
    
    >>> validHoursInDay(range(0,21))
    False
    
    >>> validHoursInDay(range(0,25))
    False
    
    >>> validDaysInMonth([None, 1, 2, None, 3, 4, None, None])
    True
    
    >>> validDaysInMonth([1, None, None, None, None, 2, 3, 4])
    False
    
    >>> validDaysInMonth([None, 1, None, 2, None, 3, None, 4, None, 5, None])
    False
    
    >>> round(None, "0.01")
    
    
    >>> round(Decimal("5.987654"), None)
    
    
    >>> round(Decimal("5.987654"), '0.01')
    Decimal("5.99")
    
    >>> mean(5.5, 6.5)
    6.0
    
    >>> percentage(24, 100)
    0.24
    
    >>> count(None)
    0
    
    >>> count(FactCollection([]))
    0
    
    >>> count(FactCollection([0,1,2]))
    3
    '''
    
if __name__ == "__main__":
    import doctest #@UnresolvedImport
    doctest.testmod()