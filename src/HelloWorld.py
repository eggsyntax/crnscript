'''
Demonstration of python scripting. Prints a list of CRN station locations.  
'''

from crn import *

stations = getAllStations()
printlist(stations)    