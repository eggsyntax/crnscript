'''
Created on Oct 15, 2010

@author: egg.davis

Sample python script. Suppose we want to know the current calculated precip at 
each of the soil moisture/soil temp stations in Arizona. How can we most easily 
do this? This example is a bit more pythonic than some of the others, with 
its use of list comprehensions.
'''
from crn import *

# We need the element for official precip, so we use crnscript's built-in findElement() method to grab it.
precipId = findElement("precip").elementId

# Now we grab current values for all stations for precip. Inefficient -- there are much more sophisticated methods
# to use if we need to do this a bunch of times -- but we're only doing it once.
allPrecipValues = elementDao.getCurrentElementValues(precipId)

# We grab the list of stations in AZ and the list of stations with soil moisture/soil temp
azStations = findStations("AZ")
soilStations = stationDao.getStationsCurrentlyWithSmSt().values()

# Find the stations that appear in both lists:
azSoilStations = [s for s in azStations if s in soilStations]

# Now that we know what stations we want, we pull their values out of the precipValues we obtained. The results are 
# ElementValue objects, so we have to ask them for the actual value. We print the station's name and the value for each.
printlist([s.getNameString()+": "+allPrecipValues.get(s.stationId).getValue()+" mm" for s in azSoilStations])

# Here's an alternate way we could have printed the values we wanted:
#def showPrecip(stationId): 
#    print soilStations.get(stationId).getNameString(),":",allPrecipValues.get(stationId).getValue(),"mm"
#map(showPrecip,azSoilStations)


