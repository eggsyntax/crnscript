from crn import *
from java.lang import Object
import re

def showDaos():
    ''' Prints a list of each of the data access objects made available by crnshared. Useful when the main crnscript
        functions are not sufficient. Call dir() on any of these to get more information.
    '''
    for beanName in context.getBeansOfType(Object): # aka all beans
        if "Dao" in beanName: 
            print beanName

def showUtils():
    ''' Prints a list of utils objects available from crnshared (timeUtils, mathUtils, and conversionUtils) '''
    print "timeUtils, mathUtils, conversionUtils"
    
def showFunctions():
    ''' Show all crnscript functions along with some minimal documentation. '''
    import inspect
    import sys
    
    mod = sys.modules[__name__]
    functions = inspect.getmembers(mod,predicate=inspect.isfunction)
    
    for f in functions:
        if re.match("_",f[0]): continue # skip private methods
        if "getcontext" in f[0] or "setcontext" in f[0]: continue # getcontext and setcontext show up from elsewhere (java.lang.Object?)
        print f[0]+":"
        print f[1].__doc__
        print

    print "*******************************************************************************"
    print "The following are methods of FactCollection and can be called on returned data,"
    print "eg 'datasubset = data.forStation(\"barrow\").forLocalDay(\"20081031\")'"
    print "*******************************************************************************"
    print
    FactCollection._showFunctions()
    
# Import tab completion in the interactive console (*nix only):
try:
    import readline
except ImportError:
    print "Unable to load readline module."
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

freshenGlobals() # ensure that we have an up-to-date list of elements and stations

