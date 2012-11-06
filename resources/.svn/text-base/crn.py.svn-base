''' crn is the core module which starts up crnscript. It initializes the spring context, imports 
    the relevant parts of crnshared, and imports all the dsl functions. Any script in crnscript 
    should start with 'from crn import *'.
'''

import org.springframework.context.support.ClassPathXmlApplicationContext as ClassPathXmlApplicationContext
from gov.noaa.ncdc.crn.util import TimeUtils
from gov.noaa.ncdc.crn.util import ConversionUtils
from gov.noaa.ncdc.crn.util import MathUtils

# get the context
context = ClassPathXmlApplicationContext('application-context-jdbc.xml')
print "Spring loaded."
# set up the DAOs and services:
# Note -- it's somewhat unfortunate that we're relying directly on the name of each implementing
# class when really we just want some class implementing the DAO interface, but it's not a big
# problem because as of now crnshared only has one implementation for each of the interfaces.
# If this changes later, we'll have to think about some more sophisticated approach here.
elementDao = context.getBean("elementDaoImpl")
datetimeDao = context.getBean("datetimeDaoImpl")
observationDao = context.getBean("observationDaoImpl")
porDao = context.getBean("porDaoImpl")
stationDao = context.getBean("stationDaoImpl")
stationService = context.getBean("stationService")
streamDao = context.getBean("streamDaoImpl")
dataSource = context.getBean("dataSource")
print "Beans cooked."

timeUtils = TimeUtils()
conversionUtils = ConversionUtils()
mathUtils = MathUtils()

# Import the decimal module into the main namespace, as we want to deal with all our data in a decimal-float context.
# If you put in something from decimal in
# another module and it doesn't recognize it, add it to this list. 
from decimal import Decimal,setcontext,Context,ROUND_HALF_UP,Overflow,DivisionByZero,InvalidOperation,getcontext
setcontext(Context(prec=10, rounding=ROUND_HALF_UP, Emin=-999999999, Emax=999999999,
        capitals=1, flags=[], traps=[Overflow, DivisionByZero, InvalidOperation]))

missingValue1 = Decimal("-9999.0")
missingValue2 = Decimal("-999.0")
missingValues = [missingValue1,missingValue2]

from Fact import Fact

from operator import attrgetter

print "Importing utilities;", # Order is important on these to avoid circular import
# TODO -- continue thinking about refactoring in order to not have to worry about import order.
from dsl.utils import *
from dsl.domainquery import *
from FactCollection import FactCollection
from dsl.data import *
from dsl.graph import *
from dsl.observation import *
from dsl.output import *

print "utilities imported."
print

