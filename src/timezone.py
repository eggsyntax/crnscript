'''
Created on Jun 23, 2011

@author: scott.embler
'''
from datetime import datetime as pydt, timedelta, tzinfo

class Utc(tzinfo):
    '''
    A timezone representing UTC time, with zero offset and zero day-light savings time.
    '''
    def utcoffset(self, dt):
        return timedelta(0)
    
    def tzname(self, dt):
        return "UTC"
    
    # a fixed-offset class:  doesn't account for DST
    def dst(self, dt):
        return timedelta(0)
    
    def __eq__ (self, other):
        return type(other) == Utc
    
    
class StationTz(tzinfo):
    '''
    A timezone defined a CRN Station.
    '''
    def __init__(self, station):
        self.station = station
    
    def utcoffset(self, dt):
        return timedelta(hours = self.station.offset)
    
    def tzname(self, dt):
        return str(self.station.offset)
    
    # a fixed-offset class:  doesn't account for DST
    def dst(self, dt):
        return timedelta(0)
    
    def __eq__ (self, other):
        if type(other) == StationTz:
            return self.station == other.station
        return False;