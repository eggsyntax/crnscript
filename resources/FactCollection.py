'''
Created on Mar 1, 2011

@author: egg.davis
'''

import dsl.domainquery

from sets import Set
from Fact import Fact

import gov.noaa.ncdc.crn.domain.Datetime as Datetime
import gov.noaa.ncdc.crn.domain.ElementValue as ElementValue
from decimal import Decimal
from gov.noaa.ncdc.crn.domain import Observation

missingValue1 = Decimal("-9999.0")
missingValue2 = Decimal("-999.0")
missingValues = [missingValue1,missingValue2]

class FactCollection(object):
    '''
    FactCollection is a wrapper around a list of Facts. It also contains lazily-created
    dictionaries of Facts.
    '''
    ''' TODO: Arguably if there are only a few Facts in a FactCollection, the dictionaries
        should not be created; the list should just be searched on demand. This reduces overhead
        at the cost of more complex internal logic.
    '''

    def __init__(self,factlist=[]):

        #factlist is the underlying list of Facts
        self.factlist = factlist
        
        #These dictionaries are created by the _groupByStation() etc functions when needed.
        self._dictByStation = None
        self._dictByLocalDay = None
        self._dictByObservation = None
        self._dictByElement = None # Maybe?
        self._dictByDatetime = None
        
    @property
    def stations(self):
        if self._dictByStation is None:
            self._dictByStation = self._groupByStation(self.factlist)
        return sorted(self._dictByStation.keys())

    @property
    def localDays(self):
        if self._dictByLocalDay is None:
            self._dictByLocalDay = self._groupByLocalDay(self.factlist)
        return sorted(self._dictByLocalDay.keys())

    @property
    def elements(self):
        if self._dictByElement is None:
            self._dictByElement = self._groupByElement(self.factlist)
        return sorted(self._dictByElement.keys())

    @property
    def observations(self):
        if self._dictByObservation is None:
            self._dictByObservation = self._groupByObservation(self.factlist)
        return sorted(self._dictByObservation.keys())

    @property
    def datetimes(self):
        if self._dictByDatetime is None:
            self._dictByDatetime = self._groupByDatetime(self.factlist)
        return sorted(self._dictByDatetime.keys())

    ''' Methods which return the dictionaries (equivalent to the old groupBy... functions) '''
    
    def groupedByLocalDay(self):
        ''' Returns a dictionary of the data from LocalDay to a collection of data for each
            localDay. Use is somewhat discouraged in favor of data.localDays and data.forLocalDay()
        ''' 
        if self._dictByLocalDay is None:
            self._dictByLocalDay = self._groupByLocalDay(self.factlist)
        return self._dictByLocalDay

    def groupedByObservation(self,fillMissing=False):
        ''' Returns a dictionary of the data from Observation to a collection of data for each
            observation. Use is somewhat discouraged in favor of data.observations and data.forObservation()
        ''' 
        if self._dictByObservation is None:
            self._dictByObservation = self._groupByObservation(self.factlist,fillMissing=fillMissing)
        return self._dictByObservation

    def groupedByStation(self):
        ''' Returns a dictionary of the data from Station to a collection of data for each
            station. Use is somewhat discouraged in favor of data.stations and data.forStation()
        ''' 
        if self._dictByStation is None:
            self._dictByStation = self._groupByStation(self.factlist)
        return self._dictByStation

    def groupedByElement(self):
        ''' Returns a dictionary of the data from Element to a collection of data for each
            element. Use is somewhat discouraged in favor of data.elements and data.forElement()
        ''' 
        if self._dictByElement is None:
            self._dictByElement = self._groupByElement(self.factlist)
        return self._dictByElement

    def groupedByDatetime(self):
        ''' Returns a dictionary of the data from Datetime to a collection of data for each
            datetime. Use is somewhat discouraged in favor of data.datetimes and data.forDatetime()
        ''' 
        if self._dictByDatetime is None:
            self._dictByDatetime = self._groupByDatetime(self.factlist)
        return self._dictByDatetime

    def _grouped(self, key):
        '''
        Returns a mapping of FactCollections, whose Facts are taken from this FactCollection.
        The keys of the mapping are specified by the given function, which can return any object.
        The key-function should take a single Fact as a parameter.
        '''
        groups = {}
        for fact in self.factlist:
            groups.setdefault(key(fact), []).append(fact)

        results = {}        
        for group, facts in groups.iteritems():
            results[group] = FactCollection(facts)
        
        return results

    def forStation(self,station):
        ''' returns a FactCollection of all those facts which belong to a particular Station.
            Pass in a Station or any description of a Station. Use data.stations to get a list 
            of all stations present in returned data. '''
        if self._dictByStation is None:
            self._dictByStation = self._groupByStation(self.factlist)
        try:
            dForStation = self._dictByStation[dsl.domainquery.findStation(station)]
        except KeyError:
            dForStation = FactCollection([])
        return dForStation
    
    def forDatetime(self,station):
        ''' returns a FactCollection of all those facts which belong to a particular Datetime.
            Pass in a Datetime or any description of a Datetime. Use data.datetimes to get a 
            list of all datetimes present in returned data. '''
        if self._dictByDatetime is None:
            self._dictByDatetime = self._groupByDatetime(self.factlist)
        try:
            dForDatetime = self._dictByDatetime[dsl.domainquery.findDate(station)]
        except KeyError:
            dForDatetime = FactCollection([])
        return dForDatetime
    
    def forElement(self,element):
        ''' returns a FactCollection of all those facts which belong to a particular Element.
            Pass in a Element or any description of a Element. Use data.elements to get a list 
            of all elements present in returned data.'''
        if self._dictByElement is None:
            self._dictByElement = self._groupByElement(self.factlist)
        try:
            dForElement = self._dictByElement[dsl.domainquery.findElement(element)]
        except KeyError:
            dForElement = FactCollection([])
        return dForElement
    
    def forObservation(self,*args):
        ''' returns a FactCollection of all those facts which belong to a particular Observation.
            Pass in an observation, or a station and a datetime. Use data.observations to get
            a list of all observations present in returned data. '''
        if len(args) == 2:
            (station,datetime) = args
        elif len(args) == 1:
            if isinstance(args[0],tuple):
                (station,datetime) = args[0]
            elif isinstance(args[0],Observation):
                (station,datetime) = (args[0].stationId,args[0].datetimeId)
            else:
                raise Exception("Argument(s) to forObservation must be an Observation or a station, datetime pair")
        else:
            raise Exception("Argument(s) to forObservation must be an Observation or a station, datetime pair")
        if self._dictByObservation is None:
            self._dictByObservation = self._groupByObservation(self.factlist)
        if type(datetime) != str: # Keep it a str if it is one to handle subhourly times
            datetime = _prettyDate(dsl.domainquery.findDate(datetime))
        try:
            return self._dictByObservation[(dsl.domainquery.findStation(station).name,datetime)]
        except KeyError:
            return FactCollection([])
        
    def forLocalDay(self,datestring):
        ''' returns a FactCollection of all those Facts which fall on a particular local day.
            Pass in an 8-digit string, eg '20080531' (strongly preferred to avoid ambiguity)
            or any description of a date. Use data.localDays to get a list of all observations 
            present in returned data.''' 
        if self._dictByLocalDay is None:
            self._dictByLocalDay = self._groupByLocalDay(self.factlist)
            
        try:
            localDayData = self._dictByLocalDay[datestring]
        except KeyError: # If they didn't pass in an appropriate 8-digit datestring
            datestring = (dsl.domainquery.findDate(datestring).datetime0_23)[0:8]
            try:
                localDayData = self._dictByLocalDay[datestring]
            except KeyError:
                localDayData = FactCollection([])
        return localDayData
    
    def _fillMissing(self):
        ''' Fills in any missing facts in a collection of data in the following way: any 
            elements which appear in *any* observation in the data will appear in
            *all* observations; if they are not already present, they will appear with a 
            missing value. This is primarily useful when you want to import the output of 
            crnscript into a tool like Excel, and wish to ensure that all the columns line
            up. '''
        self._dictByObservation = self._groupByObservation(self.factlist, fillMissing=True)
   
# TODO: Replaced the custom iterator with just returning the iterator for the underlying 
# factlist. Keeping these around (commented) for a minute in case anything breaks.
# Delete after 04/11.     
#    # Iterator functions:
#    def next(self):
#        if self.index >= len(self.factlist): 
#            self.index = 0
#            raise StopIteration
#        fact = self.factlist[self.index]
#        self.index += 1
#        return fact
#    
#    def __iter__(self):
#        return self
    
    def __iter__(self):
        return iter(self.factlist)
    
    def append(self,fact):
        if isinstance(fact,Fact):
            self.factlist.append(fact)
        else:
            raise Exception("Only a Fact can be appended to a FactCollection")
        
    def extend(self,factCollection):
        if isinstance(factCollection,FactCollection):
            self.factlist.extend(factCollection.factlist)
        else:
            raise Exception("Only a FactCollection can be used to extend another FactCollection")
    
    def __repr__(self):
        factstrings = [str(f) for f in sorted(self.factlist)]
        return ", ".join(factstrings)

    def __len__(self):
        return len(self.factlist)
    
    def __getitem__(self,item):
        return self.factlist[item]
    
    def __setitem__(self,key,value):
        self.factlist[key] = value
        
    def __contains__(self,item):
        return item in self.factlist

    ''' We define some custom math functions so that FactCollections can be added and subtracted '''
    
    def __add__(self,other):
        return FactCollection(self.factlist + other)
    def __radd__(self,other):
        return FactCollection(self.factlist + other)
    
    def __sub__(self,other):
        return FactCollection(self.factlist - other)
    def __rsub__(self,other):
        return FactCollection(other - self.factlist)
        
    def _groupByLocalDay(self,data):
        ''' Given a list of Facts, returns a dict from datestring to a FactCollection of Facts for the local day
            represented by that datestring.
        '''
        stationdays = {}
        for f in data:
            utcdate = f.datetime
            subhourlyOffset = 0 if f._isSubhourly() else -1 # Add a 1-hour offset for non-subhourly variables since they refer to the end of the observation hour 
            localdate = dsl.domainquery.findDate(utcdate.datetimeId + f.station.getOffset() + subhourlyOffset)
            localdatestring = str(localdate.getDatetime0_23())[0:8]
            stationdays.setdefault(localdatestring,[]).append(f)
        for (day,factlist) in stationdays.items(): # Sort each list of facts and convert to a FactCollection
            factlist.sort(key=lambda f: str(f.datetime)+" "+str(f.element.name))
            stationdays[day] = FactCollection(factlist)
        return stationdays
    
    def _groupByStation(self,data):
        ''' Given a list of Facts, returns a dict from Station to a list of Facts for that station. '''
        groupedById = {}
        for f in data:
            groupedById.setdefault(f.stationId,[]).append(f)
    
        # We created the map using station ids for efficiency (big gains because it means that each
        # Fact doesn't have to call findStation) but now we remap by Station (only hit findStation once
        # per key, ie once per station).
        groupedByStation = {}
        for curId in groupedById:
            groupedByStation[dsl.domainquery.findStation(curId)] = groupedById[curId]
        # Now sort and convert to FactCollection
        for station in groupedByStation:
            factlist = groupedByStation[station]
            factlist.sort()
            groupedByStation[station] = FactCollection(factlist)
        return groupedByStation
    
    def _groupByElement(self,data):
        ''' Given a list of Facts, returns a dict from Element to a FactCollection of Facts for that station. '''
        groupedById = {}
        for f in data:
            groupedById.setdefault(f.elementId,[]).append(f)
    
        # We created the map using element ids for efficiency (big gains because it means that each
        # Fact doesn't have to call findElement) but now we remap by Element (only hit findElement once
        # per key, ie once per element).
        groupedByElement = {}
        for curId in groupedById:
            groupedByElement[dsl.domainquery.findElement(curId)] = groupedById[curId]
        # Now sort and convert to FactCollection
        for station in groupedByElement:
            factlist = groupedByElement[station]
            factlist.sort()
            groupedByElement[station] = FactCollection(factlist)
        return groupedByElement
    
    def _groupByDatetime(self,data):
        ''' Given a list of Facts, returns a dict from Datetime to a FactCollection of Facts for that station. '''
        groupedById = {}
        for f in data:
            groupedById.setdefault(f.datetimeId,[]).append(f)
    
        # We created the map using datetime ids for efficiency (big gains because it means that each
        # Fact doesn't have to call findDatetime) but now we remap by Datetime (only hit findDatetime once
        # per key, ie once per datetime).
        groupedByDatetime = {}
        for curId in groupedById:
            groupedByDatetime[dsl.domainquery.findDate(curId)] = groupedById[curId]
        # Now sort and convert to FactCollection
        for station in groupedByDatetime:
            factlist = groupedByDatetime[station]
            factlist.sort()
            groupedByDatetime[station] = FactCollection(factlist)
        return groupedByDatetime
    
    def _groupByObservation(self,data,fillMissing=False):
        ''' Takes a dataset (a list of Facts) and groups it by station-datetime, ie
            consolidates into observations each of which contains (potentially)
            multiple element values. Returns a dict from a tuple (station name, date) to
            a FactCollection of Facts (modified to print tersely); this returned map can
            be passed to printlist, printfile, or csv. Pass an optional fillMissing=True to
            ensure that columns match for all observations.
        '''
        groupedData = {}
        elementSet = Set() # Represents the set of all elements found in this data
        
        for fact in data:
            stationDate = fact.station.name,_prettyDate(fact.datetime)
            groupedData.setdefault(stationDate,[]).append(fact)
            fact._factRepr = fact._terseRepr # We override the string representation of each Fact so that 
            #                                  printing the results of groupByObservation() will be less verbose.
            elementSet.add(fact.element)
            
        for key in groupedData:
            
            ob = groupedData[key]
            # Logic to fill in missing values if desired. Any element which is present in
            # *any* Fact seen here, if not present in the current ob, is added with a 
            # value of -9999.
            newFacts = []
            if fillMissing:
                elsInOb = set([f.element for f in ob])
                valsToAdd = []
                missingEls = elementSet.difference(set(elsInOb))
                for el in missingEls:
                    stationId  = ob[0].stationId  # pulls stationId and datetimeId from an 
                    datetimeId = ob[0].datetimeId # arbitrary representative Fact
                    newFact = _createMissingValueFact(stationId, datetimeId, el.elementId)
                    newFact._factRepr = newFact._terseRepr # To match the other facts in grouped obs
                    valsToAdd.append(newFact)
                ob.extend(valsToAdd)
            ob.sort()
            groupedData[key] = FactCollection(ob)
            
            if newFacts: # if we're adding new facts to fill in missing values, we have to
                self.factlist.extend(newFacts) # invalidate any dicts we've built.
                self._dictByStation = None
                self._dictByLocalDay = None
                self._dictByElement = None # Maybe?
                self._dictByDatetime = None
                
        return groupedData

    @staticmethod
    def _showFunctions():
        ''' Show all methods in FactCollection along with some minimal documentation. '''
        import inspect
        import re
        
        factCollection = FactCollection([])
        functions = inspect.getmembers(factCollection,predicate=inspect.ismethod)
        
        for f in functions:
            if re.match("_",f[0]): continue # skip private methods
            #if "getcontext" in f[0] or "setcontext" in f[0]: continue # getcontext and setcontext show up from elsewhere (java.lang.Object?)
            if f[0] in ["append","count","extend","next"]: continue # Skip certain ones
            print f[0]+":"
            print f[1].__doc__
            print

def _prettyDate(d):
    ''' Takes a datetime or datetime id or CRN datestring (yyyymmddhh) and reformats it as mm/dd/yy hh:mm UTC
    '''
    if isinstance(d,int): d = dsl.domainquery.findDate(d)
    if isinstance(d,Datetime): d = d.getDatetime0_23()
    minutes = d[10:12] if len(d) > 10 else "00"
    return str("%s/%s/%s %s:%s UTC" % (d[4:6],d[6:8],d[2:4],d[8:10],minutes))
 
def _createMissingValueFact(stationId,datetimeId,elementId):
    ''' creates a Fact with a missing value. Note that by convention the flag value for
        such facts is 0.
    '''
    return Fact(ElementValue(stationId,datetimeId,elementId,str(missingValue1),0,1,1))

# TODO: doctests?
        