'''
Created on Jun 22, 2011

@author: scott.embler
'''
from crn import *
from period import *
import unittest


class Test(unittest.TestCase):

    def testMonths(self):
        '''
        Verify that the Months returned for a period-of-record correspond
        to the correct local, or UTC, periods.
        '''        
        s = findStation(1026)
        self.assertTrue(s != None)
        
        por = POR()
        por.setStationId(s.getStationId())
        por.setStartDatetime(10888) #Jan 1, 2002 01.00.00 UTC / Dec 31, 2001 20.00.00 EST
        por.setEndDatetime(10893)   #Jan 1, 2002 06.00.00 UTC / Jan 01, 2002 01.00.00 EST
                
        #Two different months are expected since the POR is close to a yearly 
        #boundary and localization will push it into the previous year.
        self.assertEquals([Month(2001,12, tzinfo=StationTz(s)), Month(2002,1,tzinfo=StationTz(s))], list(months(por)))
        
        #A single month is expected since no localization takes place.
        self.assertEquals([Month(2002,1)], list(months(por, localize=False)))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()