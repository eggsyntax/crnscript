'''
Created on Nov 5, 2010

@author: egg.davis

Fact is a domain object encapsulating the contents of the a row from the
CRN_FACT_FLAG table; in other words it maps a station-datetime-element to a
value and flag value. It is based on the Java domain object ElementValue, but
it has lazy-evaluated station, datetime, and element properties, which return
domain objects (as opposed to stationId, datetimeId, elementId). It also
implements comparison (the __cmp__ method), which allows for the sorting most
useful to crnscript users, and arithmetic operators which act on value.
Further, it implements subhourly name/description/time, which allow crnscript
to treat 5-minute and 15-minute data in a more sophisticated way (see
dsl.data.subhourly()) for details.

It is generally best to treat Facts as immutable; they should be created by
getData() and other methods of crnscript. This is not, however, enforced.

One design consideration: since we sometimes have lots and lots of Facts, we
could decrease memory overhead by implementing __slots__ in Fact. A bit of
initial research suggests that savings is approximately 150 bytes per object
(http://www.redmountainsw.com/wordpress/archives/python-memory-usage-using-__slots__).
Since getData() is by default capped to 120,000 facts, that'd be a savings of
about 18MB. Big, but not enough to warrant the change at this point. If we find
that a) users are wanting many more Facts pretty often, or b) users are hitting
memory limits, we can reevaluate.
'''

from crn import *
from decimal import Decimal
from ElementSubhourlyGroupManager import ElementSubhourlyGroupManager
from dsl.domainquery import *

class Fact(object): # subclassing object makes Fact a new-style class
    
    def __init__(self,elementValue):
        if elementValue.getValue() is None:
            raise Exception("Cannot create a Fact from an empty ElementValue.")
        self.stationId      = int(elementValue.stationId)
        self.datetimeId     = int(elementValue.datetimeId)
        self.elementId      = int(elementValue.elementId)
        self.value          = Decimal(elementValue.getValue())
        self.flag           = int(elementValue.getFlags().intValue())
        self.decimalPlaces  = int(elementValue.getDecimalPlaces() or 0)
        self.publishedDecimalPlaces = int(elementValue.getPublishedDecimalPlaces() or 0)
        self._esgManager     = ElementSubhourlyGroupManager.getManager()
        
    def getStation(self):
        try:
            return self._station
        except:
            self._station = findStation(self.stationId)
            return self._station
    def setStation(self,sta):
        self._station = sta
    station = property(getStation,setStation)
    
    def getElement(self):
        try:
            return self._element
        except:
            self._element = findElement(self.elementId)
            return self._element
    def setElement(self,el):
        self._element = el
    element = property(getElement,setElement)
    
    def getDatetime(self):
        try:
            return self._datetime
        except:
            self._datetime = findDate(self.datetimeId)
            return self._datetime
    def setDatetime(self,dt):
        self._datetime = dt
    datetime = property(getDatetime,setDatetime)
    
    @property
    def subhourlyName(self):
        try:
            return self._subhourlyName
        except:
            self._subhourlyName = self._esgManager.getNameFromId(self.elementId)
            return self._subhourlyName
        
    @property
    def subhourlyId(self):
        try:
            return self._subhourlyId
        except:
            self._subhourlyTime = self._esgManager.getTime(self.elementId) # Populate this 1st, because once the id's changed it can't be done.
            self._subhourlyId = self._esgManager.getId(self.elementId)
            return self._subhourlyId
        
    @property
    def subhourlyDescription(self):
        try:
            return self._subhourlyDescription
        except:
            self._subhourlyDescription = self._esgManager.getDescriptionFromId(self.elementId)
            return self._subhourlyDescription
        
    @property
    def subhourlyTime(self):
        try:
            return self._subhourlyTime
        except:
            self._subhourlyTime = self._esgManager.getTime(self.elementId)
            return self._subhourlyTime

    def _isSubhourly(self):
        return (self.elementId >= 10000) # This range of element IDs is used for the artificial subhourly elements
            
    def __cmp__(self,other):
        ''' Comparison operator for sorting. '''
        # Note: the cmp keyword disappears in python 3. If/when crnscript ever moves to python 3,
        # this __cmp__ method must be replaced by the rich comparison operators. See commented out
        # code at the end of this class for how to implement. Also see http://docs.python.org/reference/datamodel.html#specialnames
        
        if type(other) is not Fact: return -1 # Ensures a Fact is not equal to a non-Fact
        
        if self.station.nameString != other.station.nameString:
            return cmp(self.station.nameString,other.station.nameString)

        if self._isSubhourly(): # If this is a subhourly Fact, compare by datestring (because datetimeId is too low-granularity)
            if self.datetime.datetime0_23 != other.datetime.datetime0_23:
                return cmp(self.datetime.datetime0_23,other.datetime.datetime0_23)
        else: # Not subhourly; therefore datetimeId is sufficient (and often much cheaper)
            if self.datetimeId != other.datetimeId:
                return cmp(self.datetimeId,other.datetimeId)
        
        # We can now have some simpler logic for the remaining comparison fields (we couldn't earlier because of the subhourly logic)
        return cmp((self.element.name,self.value,self.flag),
                   (other.element.name,other.value,other.flag))

    def __key__(self): # Explanation of this key/hash functionality: http://stackoverflow.com/questions/2909106/python-whats-a-correct-and-good-way-to-implement-hash
        return (self.stationId,self.datetimeId,self.elementId,self.value,self.flag)
    
    def __hash__(self): 
        return hash(self.__key())
        
    def __repr__(self):
        ''' Supplies a string representation for Fact. If decimalPlaces is
            non-zero, decimalPlaces determines the number of dp displayed;
            otherwise a string representation is used.  Note that printing a Fact
            for the first time is slightly more expensive than one might expect,
            since it will probably be executing findStation, findElement, and
            findDate.
                    
            __repr__ can't be dynamically overridden in any easy way (see
            http://programming.itags.org/python/78/ ), which we sometimes want
            to do with facts, so we defer to an arbitrary _factRepr, which *can* be
            dynamically overridden.  
        '''
        return self._factRepr()
    
    def _factRepr(self):
        ''' Fact's __repr__ defers to this method. By default it references _standardRepr()
            but it can be reset to point to either _standardRepr() or _terseRepr() (see
            dsl.data.groupedByObservation() for example).
        ''' 
        return self._standardRepr()
    
    def _standardRepr(self):
        ''' Standard string representation for Facts '''
        if self.decimalPlaces == 0:
            return "%s, %s, %s: %s (%d)" % (self.station.name, self.datetime.getDatetime0_23(), self.element.name, self.value, self.flag)
        else:
            formatString = "%s, %s, %s: %."+str(self.decimalPlaces)+"f (%d)"
            return formatString % (self.station.name, self.datetime.getDatetime0_23(), self.element.name, self.value, self.flag)
    
    def _terseRepr(self):
        ''' Alternate representation for Facts, used by groupByObservation(). 
        '''
        if self.decimalPlaces == 0:
            return "%s: %s (%d)" % (self.element.name, self.value, self.flag)
        else:
            formatString = "%s: %."+str(self.decimalPlaces)+"f (%d)"
            return formatString % (self.element.name, self.value, self.flag)

    ''' We define some custom math functions so that math operators on Facts are applied to the value '''
    
    def __add__(self,other):
        return self.value + other
    def __radd__(self,other):
        return self.value + other
    
    def __sub__(self,other):
        return self.value - other
    def __rsub__(self,other):
        return other - self.value
    
    def __mul__(self,other):
        return self.value * other
    def __rmul__(self,other):
        return self.value * other
    
    def __div__(self,other):
        return self.value / other
    def __rdiv__(self,other):
        return other / self.value
    
    
#    def __lt__(self,other):
#        ''' Comparison operator for sorting. '''
#        if type(other) is not Fact: return False
#        name = self.station.nameString
#        othername = other.station.nameString
#        if name != othername:
#            return name < othername
#
#        if self.datetime or self._isSubhourly(): # If datetime exists or if this is a subhourly Fact, compare by datestring (covers the subhourly case)
#            if self.datetime.datetime0_23 != other.datetime.datetime0_23:
#                print "Comparing by datestring:",self.datetime.datetime0_23,other.datetime.datetime0_23,self.datetime.datetime0_23 < other.datetime.datetime0_23
#                return self.datetime.datetime0_23 < other.datetime.datetime0_23
#            #else: Fall through to element comparison
#        else:
#            if self.datetimeId != other.datetimeId:
#                return self.datetimeId < other.datetimeId
#
#        return self.element.name < other.element.name

#    def __eq__(self,other):
#        ''' Defines equality for facts. Compares station/date/element/value/flag. '''
#        if type(other) is not Fact: return False
#        return (self.stationId  == other.stationId and
#                self.datetimeId == other.datetimeId and
#                self.elementId  == other.elementId and
#                self.value      == other.value and
#                self.flag       == other.flag) 
#       
    