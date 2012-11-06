'''
Created on Jul 29, 2011

@author: egg.davis
'''

from crn import *
from math import exp
import datetime

stations = ["Stillwater 5"]
years = range(2002,2012)
els = sorted(findElements("temp","ST005","RH\d\d","precip","solarad")) # TODO: confirm soil
onehour = datetime.timedelta(hours=1)

def c_to_k(temp_c):
    return float(temp_c) + 273.15
#def fToK(temp_f):
#    return ((temp_f - 32.0) / 1.8) + 273.15

def vapor_pressure_deficit(temp,rh):
    temp_k = c_to_k(temp)
    vp_sat = 6.1078 * exp(17.27 * (temp_k-273)/(temp_k-35.83)) 
    vapor_pressure = vp_sat * rh / 100.0
    vpd = 1000 * (vp_sat - vapor_pressure)
    return vpd

def retrieve_data(station,year):
    ''' Returns a dict from observation to FactCollection '''
    allowQuerySizeOverride()
    d = getData(station,("%s010100"%(year),"%s010100"%(year+1)),els)
    return d

def getHeader():
    return "year\tdoy\thour\ttair\tTsoil\tVDEF\tRH\tprecp\trad_h"
    
def formattedDate(dt):
    ''' Returns the datetime as a string formatted for crnscript conventions '''
    return dt.strftime("%Y%m%d%H")

def dateLine(dt):
    return "%d\t%6.2f\t%5.2f\t" % (dt.year,dt.timetuple().tm_yday,dt.hour)

def extractRh(d):
    ''' Given a FactCollection, finds the average of the 12 5-minute RH values '''
    rhtotal = Decimal("0")
    rhcount = 0
    for elid in range(426,438):
        try:
            val = d.forElement(elid)[0].value
            rhtotal += val
            rhcount += 1
        except KeyError:
            pass
    if rhcount == 0: return -999
    return float(rhtotal / rhcount)    

def dataLine(d,s,dt):
    ''' Returns the data component of the output line. Has some irreducible complexity since
    different elements have different requirements. '''
    output = []
    try:
        dataForHour = d.forObservation(s,dt)
    except : # No data for this hour
        return "-999.00\t-999.00\t-999.00\t-999.00\t-999.00\t-999.00"
    
    for el in ["temp","ST005"]:
        try:    
            output.append(dataForHour.forElement(el)[0].value)
        except KeyError: # No fact for this element
            output.append(-999)
    
    rh = extractRh(dataForHour)
    try:
        output.append(vapor_pressure_deficit((dataForHour.forElement("temp")[0]).value, rh))
    except KeyError: # in case temp is missing
        output.append(-999)
    output.append(rh)
    
    for el in ["precip","solarad"]:
        try:    
            output.append(dataForHour.forElement(el)[0].value)
        except KeyError: # No fact for this element
            output.append(-999)
    return "\t".join(["%8.2f"%(float(v)) for v in output])
    
for station in stations:
    for year in years:
        output = []
        output.append(getHeader())
        d = retrieve_data(station,year)
        if not d: continue 
        dt = datetime.datetime(year,1,1,1) - onehour
        while dt.year == year:
            dt += onehour
            line = dateLine(dt) + dataLine(d,station,dt)
            output.append(line)
        #printlist(output,sortData=False)
        printfile("h:/crnscript-data/ecosystem/%s_%d.txt"%(station.replace(' ','_'),year),output,sortData=False)

