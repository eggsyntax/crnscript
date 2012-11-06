'''
Created on Jun 23, 2011

@author: scott.embler
'''
from crn import *
from period import *
from timezone import *
from summary import *
from datetime import datetime, timedelta, tzinfo
from string import rjust

def format(sod):
    '''
    Formats the important fields of a SOD(Summary of Day) into fixed-width columns.
    '''
    text = ""
    text += str(sod.station.wbanno) + " "
    text += str(sod.day) + " "
    text += rjust(str(sod.temp_max), 5) + " "
    text += rjust(str(sod.temp_min), 5) + " "
    text += rjust(str(sod.temp_mean), 5) + " "
    text += rjust(str(sod.temp_avg), 5) + " "
    text += rjust(str(sod.precip_sum), 5)
    return text

stations = getAllStations()
elements = findElements("T_OFFICIAL", "T_MAX", "T_MIN", "P_OFFICIAL")
file = open('./sod.txt','w')
for station in stations:
    por = getPor(station)
    print por
    for day in days(por):
        data = getDataForPeriod(station, day, elements)._grouped(byLocalDay)
        summary = SOD(day, station, data)
        print format(summary)
        file.write(format(summary) + "\n")
        file.flush()    
file.close()