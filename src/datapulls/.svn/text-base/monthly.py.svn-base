'''
Created on Jun 8, 2011

@author: scott.embler
'''

from crn import *
from period import *
from timezone import *
from summary import *
from datetime import datetime as pydt, timedelta, tzinfo
from string import ljust, rjust

def format(som):
    '''
    Formats the important fields of a SOM(Summary of Month) into fixed-width columns.
    '''
    text = ""
    text += ljust(str(som.station.getNameString()).replace(" ", "_"), 30) + " "
    text += rjust(str(som.station.wbanno), 5) + " "
    text += rjust(str(som.station.getLatitude()), 9) + " "
    text += rjust(str(som.station.getLongitude()), 9) + " "
    text += str(som.month).replace("-", " ") + " "
    text += rjust(pick(som.temp_max,"-9999"), 5) + " "
    text += rjust(pick(som.temp_min, "-9999"), 5) + " "
    text += rjust(pick(som.temp_mean, "-9999"), 5) + " "
    text += rjust(pick(som.temp_avg, "-9999"), 5) + " "
    text += rjust(pick(som.precip_sum, "-9999"), 5)
    return text

def pick(decimal, substitute):
    if decimal != None:
        return str(decimal)
    else:
        return str(substitute)
        

stations = sorted(getAllStations(), key=lambda station: station.getNameString())
elements = findElements("T_OFFICIAL", "T_MAX", "T_MIN", "P_OFFICIAL")
file = open('./som.txt','w')
for station in stations:
    por = getPor(station)
    for month in months(por):
        try:
            data = getDataForPeriod(station, month, elements)._grouped(byLocalMonth)
            som = SOM(month, station, data)
            print format(som)
            file.write(format(som) + "\n")
            file.flush() 
        except Exception, e:
            print e
file.close()
