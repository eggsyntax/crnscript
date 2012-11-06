'''A helper script for graphing an element with its two corresponding
   layer elements. Takes stationId, start datetime, end datetime, and 
   element name as arguments.'''
from crn import *
import re

'''Based on the given element name, determine the other 2
   corresponding element names for that layer.'''
def getElementLayer(element):
    # The first digit is the probe number (1-3)
    elemDigit = re.search("\d", element)
    # The letters before the first digit are the type of sensor
    elemType = element[0:elemDigit.start()]
    # The numbers after the first digit are the layer depth
    elemDepth = element[elemDigit.end():]
    # The type and depth will be the same for all 3. Just insert 1, 2, and 3
    # into the first digit location in the string to get the element names.
    elements = elementDao.getElementsByName(["%s%s%s" % (elemType, x, elemDepth) for x in range(1,4)])
    return elements.values()

stationId = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]
element = sys.argv[4]
elements = getElementLayer(element)

data = getData(stationId, (start, end), elements)
graph(data)

raw_input("Press 'Enter' from this window to exit.\n")
