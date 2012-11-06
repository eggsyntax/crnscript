'''
Created on Nov 5, 2010

Request for all 5-min/15-min temp and precip for the Champaign, IL station. Complicated a bit by the fact that
the 15-minute streams have no subhourly temp, but reuse the T5_12 element for instantaneous hourly temp.

@author: egg.davis
'''

from crn import *

station = findStation("Champaign")
por = getPor(station)
elements = findElements("T5_","P5_","P15_")

allowQuerySizeOverride()
data = getData(station,por,elements)
print "Data retrieved."

output15 = []
output05 = []

print len(data.observations)

for ob in data.observations:
    values = data.forObservation(ob)
    line = ob[1]
    is5minData = False
    for fact in sorted(values):
        elname = fact.element.name
        if elname == "T5_12" and not is5minData: continue
        if elname.startswith(("P5_","T5_")):
            is5minData = True
        line = line +  ","+str(elname)+","+str(fact.value)
    output05.append(line) if is5minData else output15.append(line)
printfile("temp15.txt",output15)
printfile("temp05.txt",output05)
