'''
Created on Oct 7, 2010

@author: egg.davis

Sample python script based on the following request:

Could you extract by tomorrow morning the monthly temperature max for the 2 stations 
in new Hampshire and the 2 stations in Rhode Island? Please stick them in a spread
sheet with columns of year, month, max. I need to do an analysis for Sharon
LeDuc by Wednesday. Thanks!
'''
from crn import *
import java.util.TreeMap as TreeMap
import gov.noaa.ncdc.crn.util.TimeUtils as TimeUtils
import java.util.Calendar as Calendar
from pprint import pprint #@UnresolvedImport # Pydev bug http://klaith.wordpress.com/2009/06/12/pydev-unresolved-import-errors/

class monthlyMaxTemps:
    ''' 
    This class represents the multidimensional data structure storing the results, and
    is actually the most complicated part of this script. Feel free to skip past it;
    the complication is not about python or about the CRN-specific code.
    '''
    
    def __init__(self):
        self.stations = {}
        
    def get(self,station,year,month):
        try:
            return self.stations[station][year][month]
        except KeyError:
            return None
    
    def put(self,station,year,month,value):
        # This use of setdefault grabs the current value, creating the nested dicts along the way if necessary
        oldMax = self.stations.setdefault(station,{}).setdefault(year,{}).setdefault(month,-9999)
        if value > oldMax:
            self.stations[station][year][month] = value
    
    def printContents(self):
        for station in self.stations:
            print station
            for year in sorted(self.stations[station]):
                print"  Year: "+str(year)
                for month in sorted(self.stations[station][year]):
                    print "     %02d: %3.1f"%(month,self.stations[station][year][month])
        #pprint(self.stations) # Alternate strategy which would print the monthlyMaxTemps somewhat less nicely
    
        
stations = findStations("RI","NH")
elements = findElements("calculated average temp for 5 minutes")
monthlyMaxTemps = monthlyMaxTemps()
monthlyMaxTemps.get(stations[0],2001,01)
for station in stations:
    print "Getting data for",station
    data = getData(station, ("11/30/08 7:00", "1/10/09 22:00"), elements)
    print "  Retrieved",len(data),"values."
    for fact in data:
        calendar = TimeUtils.computeCalendarDate(fact.datetime.getDatetimeId())
        monthlyMaxTemps.put(fact.station,calendar.get(Calendar.YEAR),
                                calendar.get(Calendar.MONTH),fact.value)
        
monthlyMaxTemps.printContents()