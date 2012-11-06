''' Created on Apr 12, 2011
    @author: egg.davis
Current precip QC attempts to determine precip for each 5-minute period, and then sums them
to get hourly (and ultimately daily etc) precip. An approach which might be more accurate and
conceptually simpler would be to determine precip for a multi-hour period and then distribute
it among the 5-minute periods.
'''
from crn import *
import re

start = findDate("3/26/11 8:00")
end = findDate("3/29/11 8:00")

numHours = 3

def loadObsWithData():
    stations = ["Gadsden"]
    elements = findElements("P5_","D\d{3}","wet1\d{2}","precip")
    data = getData(stations,(start,end),elements)
    subdata = subhourly(data)
    print "Retrieved data."
    
    # Divide wetness value by 10 for easy graphing:
    for fact in subdata.forElement("WET1:"):
        fact.value /= 10
    
    graph(data,elements="precip")
    return (data,subdata)
    
def ave(vals):
    return sum(vals) / len(vals)

def getDepths(data,datetime,subhourly):
    onehourdata = data.forDatetime(datetime)
    depthsFor5min = [f.value for f in onehourdata if re.match("D\d"+subhourly,f.element.name)]
    return depthsFor5min
    

