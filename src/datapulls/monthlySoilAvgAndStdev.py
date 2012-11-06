'''
Created on Dec 15, 2011

@author: scott.embler
'''

from crn import *
import csv

def statistics(elements, facts):
    '''
    Returns a tuple containing the count, average, and standard deviation of facts
    that have the specified elements.
    '''
    values = [fact for fact in facts if fact.element in elements]
    valid =  [fact for fact in values if 0 <= fact.value < 70]
    return (len(valid), avg(valid), stdev(valid))

def avg(sequence):
    '''
    Division-by-zero safe averaging of a sequence.
    '''
    if len(sequence) == 0:
        return None
    else:
        return sum(sequence)/len(sequence)

def stdev(sequence):
    '''
    Standard deviation of the sequence.
    '''
    if len(sequence) <= 1: 
        return None
    else:
        avg = sum(sequence) / len(sequence)
        sdsq = sum([(i - avg) ** 2 for i in sequence])
        stdev = (sdsq / (len(sequence) - 1)) ** Decimal(".5")
        return stdev

soilStations = sorted(stationDao.getStationsCurrentlyWithSmSt().values())

#The start and end of the time-span that will be examined.
#Change these dates if you want a different time period.
start = findDate("8/01/2011 0:00");
end = findDate("9/01/2011 0:00");

#Elements for soil probes at 5 and 10 cm depths.
soil5cm = findElements("SMV1005","SMV2005","SMV3005")
soil10cm = findElements("SMV1010","SMV2010","SMV3010")

#A summary file that will hold the averaged three-probe averages and standard deviations.
s = open('./august-2011-soil-moisture-avg-stdev/summary.csv','w')
summaries = csv.writer(s, lineterminator='\n')
summaries.writerow(['wban','monthly-5cm-average','monthly-5cm-stdev', 'monthly-10cm-average','monthly-10cm-stdev'])

#The main loop that will retrieve the soil data, compute summaries, and populate csv files.
for station in soilStations:
    f = open('./august-2011-soil-moisture-avg-stdev/' + str(station.getName()) + '.csv','w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['wban','hour','hourly-5cm-count','hourly-5cm-average','hourly-5cm-stdev','hourly-10cm-count', 'hourly-10cm-average','hourly-10cm-stdev'])
    try:
        allowQuerySizeOverride()
        stationValues = getData(station, (start, end), soil5cm + soil10cm)
    except Exception , e:
        #Requests for data from non-public stations might fail here.
        #just skip past any of those stations.
        f.close()
        continue
    monthly5cm = []
    monthly10cm = []
    for hour in stationValues.datetimes:
        hourlyValues = stationValues.forDatetime(hour)
        stats5cm = statistics(soil5cm, hourlyValues)
        stats10cm = statistics(soil10cm, hourlyValues)
        monthly5cm.append(stats5cm)
        monthly10cm.append(stats10cm)
        row = [station.getWbanno(), hour.getDatetime0_23(), stats5cm[0], stats5cm[1], stats5cm[2], stats10cm[0], stats10cm[1], stats10cm[2]]
        writer.writerow(row)
        
    f.flush()
    f.close()

    monthly5cmavg = avg(filter(None, [t[1] for t in monthly5cm]))
    monthly5cmstdev = avg(filter(None, [t[2] for t in monthly5cm]))
    monthly10cmavg = avg(filter(None, [t[1] for t in monthly10cm]))
    monthly10cmstdev = avg(filter(None, [t[2] for t in monthly10cm]))
    summaries.writerow([station.getWbanno(), monthly5cmavg, monthly5cmstdev, monthly10cmavg, monthly10cmstdev])
    s.flush()
    
s.close()