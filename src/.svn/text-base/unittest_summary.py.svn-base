'''
Created on Aug 15, 2011

@author: scott.embler
'''
from crn import *
from period import *
from summary import *
import unittest


class Test(unittest.TestCase):

    def testCompleteSummaryOfDay(self):
        station = findStation(1026)
        day = Day(2008,6,1,StationTz(station))
        elements = findElements("T_MAX", "T_MIN", "T_OFFICIAL", "P_OFFICIAL")
        data = getDataForPeriod(station, day, elements)._grouped(byLocalDay)
        sod = SOD(day, station, data)
        
        #All values are present for this day.
        self.assertEquals(1, len(data))
        self.assertEquals(96, data.get(day).forStation(station).count());
        self.assertEquals(Decimal("25.6"), sod.temp_max)
        self.assertEquals(Decimal("13.5"), sod.temp_min)
        self.assertEquals(Decimal("19.6"), sod.temp_mean)
        self.assertEquals(Decimal("18.9"), sod.temp_avg)
        self.assertEquals(Decimal("1.5"), sod.precip_sum)
        
    def testPartialSummaryOfDay(self):
        station = findStation(1026)
        day = Day(2008,10,30,StationTz(station))
        elements = findElements("T_MAX", "T_MIN", "T_OFFICIAL", "P_OFFICIAL")
        data = getDataForPeriod(station, day, elements)._grouped(byLocalDay)
        sod = SOD(day, station, data)
        
        #There are less than 21 values for each element during this day.
        self.assertEquals(1, len(data))
        self.assertEquals(78, data.get(day).forStation(station).count());
        self.assertEquals(None, sod.temp_max)
        self.assertEquals(None, sod.temp_min)
        self.assertEquals(None, sod.temp_mean)
        self.assertEquals(None, sod.temp_avg)
        self.assertEquals(None, sod.precip_sum)
    
    def testSummaryOfMonth(self):
        station = findStation(1026)
        month = Month(2008, 6, StationTz(station))
        elements = findElements("T_MAX", "T_MIN", "T_OFFICIAL", "P_OFFICIAL")
        data = getDataForPeriod(station, month, elements)._grouped(byLocalMonth)
        som = SOM(month, station, data)
        
        #All values are present for this day.
        self.assertEquals(1, len(data))
        self.assertEquals(Decimal("28.7"), som.temp_max)
        self.assertEquals(Decimal("13.0"), som.temp_min)
        self.assertEquals(Decimal("20.9"), som.temp_mean)
        self.assertEquals(Decimal("20.3"), som.temp_avg)
        self.assertEquals(Decimal("166.2"), som.precip_sum)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSummaryOfDay']
    unittest.main()