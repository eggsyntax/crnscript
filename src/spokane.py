''' Example script: get all transmitted values from the Spokane station for a 
    certain date range, and print them as a line for each date, in the order we 
    receive them (ie stream order) so that the resulting output exactly mimics the 
    PDA file we would receive for the same data.
'''
from crn import *

station  = findStation("Spokane")
start    = findDate('2009091601')
end      = findDate('2009092117')
elements = getAllElements()

allowQuerySizeOverride()
data = getData(station, (start,end), elements)

streamElementList = [el.elementId for el in streamDao.getStreamElementList(2)]  # returns the element ids for this
                                                                                # stream as an ordered list
for datetime in data.datetimes:
    hourdata = data.forDatetime(datetime)
    if not hourdata: continue                                           # Skip over missing observations

    dataMap = dict([ (e.element.elementId,e.value)                      # From the ElementValues list, extract the element id
                        for e in hourdata                               # and value, but don't include values not in 
                        if e.element.elementId in streamElementList])   # streamElementList (ie calculated values)

    orderedKeys = sorted(dataMap.keys(), key=streamElementList.index)   # Sort based on where elements appear in stream
    
    orderedValues = [str(dataMap[id]) for id in orderedKeys]            # Use the ordered list of keys to create an 
                                                                        # ordered list of values
    print ",".join(orderedValues)

    