'''
There are some cases (eg AK Port Alsworth, 5/15/2011 20:05 UTC) where we falsely report precip
due to power issues which result in a 0 or near-0 transmitter voltage under load. Power fluctuations
cause all three wire depths to rise and fall rapidly in a correlated way.
 
We speculate that we could identify such cases by looking for all the following conditions to 
be met:
1. Wire depth (on all 3 wires?) drops by, say, > 20 in a 5-minute period.
2. Datalogger door flag is not set (ie rule out AMV/UMV events)
3. (Possibly) transmitter voltage under load is 0 or near 0.

Under such conditions, we would refuse to recognize precipitation for some period of time.


  
Created on Sep 6, 2011

@author: egg.davis
'''

from crn import *

def ave(l):
    return sum(l) / float(len(l))
    
''' First order of business: do some analysis of how frequently problems like this occur. For
each station in a representative group, for all of 2010, look for drops in all 3 wires of > 5 in a 5-minute period,
where wires do not have datalogger door flag. Note transmitter voltage. Separately output info
to reload the relevant facts in order to do further analysis. '''

results2010 = [["SD Buffalo 13 ESE","84657","06/01/10 17:15 UTC","-447.17","13.9"],
    ["SD Buffalo 13 ESE","85091","06/19/10 19:15 UTC","-82.35","0.0"],
    ["SD Buffalo 13 ESE","88094","10/22/10 22:15 UTC","-170.62","13.7"],
    ["FL Titusville 7 E","86889","09/02/10 17:15 UTC","-273.62","13.5"],
    ["CO Nunn 7 NNE","87155","09/13/10 19:15 UTC","-413.42","12.9"],
    ["SC McClellanville 7 NE","87051","09/09/10 11:15 UTC","-409.36","13.0"],
    ["WA Quinault 4 NE","81276","01/11/10 20:15 UTC","-231.34","12.7"],
    ["WA Quinault 4 NE","81276","01/11/10 20:15 UTC","-696.65","12.7"],
    ["WA Quinault 4 NE","81759","01/31/10 23:15 UTC","-375.22","12.7"],
    ["WA Quinault 4 NE","83192","04/01/10 16:15 UTC","-679.35","12.7"],
    ["WA Quinault 4 NE","85241","06/26/10 01:15 UTC","-431.52","12.7"],
    ["WA Quinault 4 NE","85241","06/26/10 01:15 UTC","-395.75","12.7"],
    ["WA Quinault 4 NE","88813","11/21/10 21:15 UTC","-432.34","12.8"],
    ["WA Quinault 4 NE","88813","11/21/10 21:15 UTC","-121.64","12.8"],
    ["WA Quinault 4 NE","89439","12/17/10 23:15 UTC","-802.31","12.8"],
    ["ID Arco 17 SW","84971","06/14/10 19:15 UTC","-518.81","13.1"]]

els = findElements('D\d{3}','P5_','BV_UFL')

def graphResults():
    for (stationname,dt,prettydate,avedrop,bvufl) in results2010:
        dt = int(dt)
        graph(subhourly(stationname,(dt-3,dt+3),els),title="%s - %s"%(stationname,prettydate))
        
def hasdataloggerflag(el):
    f = el.flag
    return (f & 4) > 0 # True iff the datalogger door bit is set in the flag integer

def findWireDrops():
    # 12 stations -- should be almost complete overlap with the ones we're testing the precip algorithm on
    stations = findStations("Quinault", "Monahans", "Titusville", "Sioux Falls", "Kingston", "Arco", "Nunn", "Newton 11", "Merced", "McClellanville", "Buffalo", "Yuma")
    depthels = [10010,10011,10012]
    
    for station in stations:
        allowQuerySizeOverride()
        hd = getData(station,('2010010100','2010123123'),els)
        for hourlyob in sorted(hd.observations):
            curDatetimeId = findDate(hourlyob[1]).datetimeId
            try:
                dForHour = hd.forObservation(hourlyob)
            except:
                continue
            bv_ufl_val = dForHour.forElement('BV_UFL')[0]
            d = subhourly(dForHour)
            try:
                dByOb = d.groupedByObservation()
            except:
                continue
    #        printlist(dByOb)
    #        print
            obs = sorted(dByOb.keys())
            numobs = len(dByOb)
            for i in range(1,numobs): # we skip first ob because we're always doing comparisons between consecutive obs
                curob  = dByOb[obs[i]]
                lastob = dByOb[obs[i-1]]
                try:
                    curobdepths  = [curob.forElement(e)[0] for e in depthels]
                except:
                    continue # We've hit an ob with hourly elements instead of subhourly (as expected)
                
                if any(hasdataloggerflag(depth) for depth in curobdepths):
                    continue # We want to ignore AMV/UMV events
                
                try:
                    lastobdepths = [lastob.forElement(e)[0] for e in depthels]
                except KeyError:
                    continue # In case of missing data
                depthchanges = [float(curobdepths[i] - lastobdepths[i]) for i in range(3)]
                if all(change < -5 for change in depthchanges):
                    averagedrop = ave(depthchanges)
                    print "%s,%d,%s,%8.2f,%s"%(obs[i][0],curDatetimeId,obs[i][1],averagedrop,float(bv_ufl_val.value))
                
#findWireDrops()
graphResults()