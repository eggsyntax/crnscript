'''
Created on Oct 14, 2011

@author: egg.davis
'''
'''
Finds % of missing dielectric and volumetric for each station for one month. Caveat: any probe
that appears nowhere in the month is not counted. '''

from crn import *

diels = findElements('soil moisture dielectric for set')
vols =  findElements('soil moisture volumetric average')

start = findDate('2011050101')
end   = findDate('2011060100')
numhours = float((end.datetimeId - start.datetimeId) + 1)

soilstations = ["AL Fairhope 3 NE", "AL Gadsden 19 N", "AL Selma 13 WNW", "AR Batesville 8 WNW", "AZ Elgin 5 S", "AZ Tucson 11 W", "AZ Williams 35 NNW", "CA Fallbrook 5 NE", "CA Santa Barbara 11 W", "CA Stovepipe Wells 1 SW", "CO Cortez 8 SE", "CO La Junta 17 WSW", "CO Montrose 11 ENE", "FL Everglades City 5 NE", "FL Sebring 23 SSE", "FL Titusville 7 E", "GA Brunswick 23 S", "GA Newton 11 SW", "GA Newton 8 W", "GA Watkinsville 5 SSE", "IA Des Moines 17 E", "IL Champaign 9 SW", "IL Shabbona 5 NNE", "IN Bedford 5 WNW", "KS Manhattan 6 SSW", "KS Oakley 19 SSW", "KY Bowling Green 21 NNE", "KY Versailles 3 NNW", "LA Lafayette 13 SE", "LA Monroe 26 N", "ME Limestone 4 NNW", "ME Old Town 2 W", "MN Goodridge 12 NNW", "MO Chillicothe 22 ENE", "MO Joplin 24 N", "MO Salem 10 W", "MS Holly Springs 4 N", "MS Newton 5 ENE", "MT Wolf Point 29 ENE", "MT Wolf Point 34 NE", "NC Asheville 13 S", "NC Asheville 8 SSW", "NC Durham 11 W", "ND Jamestown 38 WSW", "ND Medora 7 E", "ND Northgate 5 ESE", "NE Harrison 20 SSE", "NE Lincoln 11 SW", "NE Lincoln 8 ENE", "NE Whitman 5 ENE", "NH Durham 2 N", "NH Durham 2 SSW", "NM Las Cruces 20 N", "NM Los Alamos 13 W", "NM Socorro 20 N", "NV Mercury 3 SSW", "OH Coshocton 8 NNE", "OK Goodwell 2 E", "OK Stillwater 2 W", "OK Stillwater 5 WNW", "OR Coos Bay 8 SW", "OR Corvallis 10 SSW", "OR Riley 10 WSW", "PA Avondale 2 N", "RI Kingston 1 NW", "RI Kingston 1 W", "SC Blackville 3 W", "SC McClellanville 7 NE", "SD Aberdeen 35 WNW", "SD Buffalo 13 ESE", "SD Pierre 24 S", "SD Sioux Falls 14 NNE", "TN Crossville 7 NW", "TX Austin 33 NW", "TX Bronte 11 NNE", "TX Edinburg 17 NNE", "TX Monahans 6 ENE", "TX Muleshoe 19 S", "TX Palestine 6 WNW", "TX Panther Junction 2 N", "WI Necedah 5 WNW"]

maxmissing = Decimal('-200')

def printNumNonMissing():

    fileoutput = []
    for s in soilstations:
        try:
            d1 = getData(s,(start,end),diels+vols)
            if not d1: continue
            for el in d1.elements:
                dForEl = d1.forElement(el)
                d1nm = FactCollection([f for f in dForEl if f.value > maxmissing])
                fileoutput.append("%s,%s,%d,%d"%(s,el.name,len(dForEl),len(d1nm)))
        except:
            continue
    printfile("num-nonmissing.txt",fileoutput,sortData=False)
        
def printMissingDieAndVol():
    
    fileoutput=[]
    for s in soilstations:
        
        d1 = getData(s,(start,end),diels)
        if not d1: continue
        d1nm = FactCollection([f for f in d1 if f.value > maxmissing])
        m1 = 100*(1 - (len(d1nm) / (len(d1.elements)*numhours)))
        d2 = getData(s,(start,end),vols)
        d2nm = FactCollection([f for f in d2 if f.value > maxmissing])
        m2 = 100*(1 - (len(d2nm) / (len(d1.elements)*numhours)))

        fileoutput.append("%s,%6.2f%%,%6.2f%%"%(s,m1,m2))
    printfile("missing-die-and-vol.txt",fileoutput,sortData=False)

printNumNonMissing()
printMissingDieAndVol()      