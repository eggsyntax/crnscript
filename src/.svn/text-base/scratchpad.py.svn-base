from crn import *

s = findStation('asheville 13')
#d = getData(s,('2011010800','+24'),'soil moisture volumetric.*for 5 minutes')
d = FactCollection()
d += getData(s,('2011010800'),'SOLARAD')
d += getData(s,('2011010800'),'SOLRAD_MN')
printlist(d)
