'''
Determines the average departure for max and min temps for each season of each year for two
groups of stations (representing high-altitude and low-altitude stations).
Note that there are several additional functions here which support secondary analyses.

Created on Mar 9, 2011

@author: egg.davis

For each group: 
    For each season:
        For each station:
            Calculate the average departure for the season for tmax 
                as the simple average of three monthly average departures (all 3 must be present)
            Calculate the average departure for the season for tmin 
                as the simple average of three monthly average departures (all 3 must be present)
        Calculate the average departure for the group for tmax
        Calculate the average departure for the group for tmin
        Calculate the standard deviation of seasonal average tmax
            (and the number of stations from which the std dev was calculated)
        Calculate the standard deviation of seasonal average tmin
            (and the number of stations from which the std dev was calculated)
        
'''
from crn import *
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

seasons = {"spring":(2,3,4),
           "summer":(5,6,7),
           "fall"  :(8,9,10),
           "winter":(11,12,13)}
seasonnames = ["spring","summer","fall","winter"]

group1 = findStations("Boulder 14 W","Los Alamos 13 W","Montrose 11 ENE","Cortez 8 SE","Yosemite Village 12 W","Baker 5 W","Denio 52 WSW","Moose 1 NNE","Torrey 7 E","Dinosaur 2 E","Williams 35 NNW","Dillon 18 WSW","Arco 17 SW")
group2 = findStations("Spokane 17 SSW","John Day 35 WNW","Wolf Point 29 ENE","Redding 12 WNW","Fallbrook 5 NE","Yuma 27 ENE","Corvallis 10 SSW","Quinault 4 NE","Stovepipe Wells 1 SW","Merced 23 WSW","Bodega 6 WSW","Santa Barbara 11 W")

missingValue = Decimal("-999")

def asKey(station):
    ''' utility method -- keys for the departure files are the station names with spaces removed,
        so we return those for a station '''
    compressedName = station.nameString.replace(" ","")
    return compressedName
        
def parseDeparturesFromFile(filename):
    ''' From a file in a very specific format, create a nested dictionary:
        stationName -> year -> list of monthly departures. 
        Within the list, months are 0..11; element 12 is the yearly average.
    '''
    badlines = []
    departures = {}
    file = open(filename)
    for line in file:
        m = re.match(r"\d+\s+(?P<name>[\.\w]+)\s+\d+\s+(?P<year>\d+)\s+(?P<values>.*)",line)
        if m is None:
            badlines.append(line)
            continue
        (name,year,values) = m.groups()
        departuresForStation = departures.setdefault(name,{})
        departuresForStation[int(year)] = values.split()
    if badlines:
        print "BAD LINES:"
        printlist(badlines)
    file.close()
    return departures 
    
def getAverage(list,numMissingAllowed):
    
    missings = [v for v in list if Decimal(v) == missingValue]
    if len(missings) > numMissingAllowed: return missingValue
    
    values = [Decimal(item) for item in list if Decimal(item) != missingValue]
    if not values: return missingValue
    cursum = sum(values)
    ave = cursum / len(values)
    return ave

def getSeasonalDepartures(departures):
    ''' From 3 monthly departures, creates a seasonal departure. Builds a triply-nested dict
    that looks like this:

{   2001: {   'fall': {   'AKBarrow4ENE': Decimal("-999"),
                          'AKFairbanks11NE': Decimal("-999"),
                          'AKSitka1NE': Decimal("-999"),
                          'AKSt.Paul4NE': Decimal("-999"),
                          'ALFairhope3NE': Decimal("-999"),
                          ...
              'spring': {   'AKBarrow4ENE': Decimal("-999"),
                            'AKFairbanks11NE': Decimal("-999"),
                            'AKSitka1NE': Decimal("-999"),
                            'AKSt.Paul4NE': Decimal("-999"),
                            'ALFairhope3NE': Decimal("-999"),
                            ...
                            
    Note that winter of each year includes Jan and Feb of the following year.
    '''
    seasonaldepartures = {}
    for station in sorted(departures):
        #print station
        for year in sorted(departures[station]):
            for season in seasonnames:
                departuresForSeason = []
                for month in seasons[season]:
                    curYear = year
                    curMonth = month
                    # Increment into the next year for January and February
                    if month >= 12:
                        curYear += 1
                        curMonth = curMonth % 12
                    try:
                        departureForMonth = departures[station][curYear][curMonth]
                        departuresForSeason.append(departureForMonth)
                    except KeyError:
                        continue # We're out of data
                departuresForYearSeason = seasonaldepartures.setdefault(year,{}).setdefault(season,{})
                departuresForYearSeason[station] = getAverage(departuresForSeason,1)
                
    return seasonaldepartures

def stdev(sequence):
    if len(sequence) <= 1: 
        return None
    else:
        avg = sum(sequence) / len(sequence)
        sdsq = sum([(i - avg) ** 2 for i in sequence])
        stdev = (sdsq / (len(sequence) - 1)) ** Decimal(".5")
        return stdev

def getMonthlyAves(departures,group):
    ''' Temporary method -- creates monthly averages to check against the results of the old
        perl script. Results look like this:
        2008: {   0: Decimal("-1.157142857"),
                  1: Decimal("0.1625"),
                  2: Decimal("-0.375"),
                  3: Decimal("-0.6222222222"),
                  4: Decimal("0.06"),
                  5: Decimal("0.29"),
                  6: Decimal("0.6636363636"),
                  7: Decimal("0.6636363636"),
                  8: Decimal("1.30"),
                  9: Decimal("0.80"),
                  10: Decimal("2.466666667"),
                  11: Decimal("-1.609090909")},
    '''
    monthlyValues = {}
    for station in group:
        if asKey(station) in departures:
            for year in departures[asKey(station)]:
                for month in range(0,12):
                    spotToAdd = monthlyValues.setdefault(year,{}).setdefault(month,[])
                    valueToAdd = Decimal(departures[asKey(station)][year][month])
                    if valueToAdd != missingValue: spotToAdd.append(valueToAdd)

        else:
            print "Couldn't find",station.name
    monthlyAves = {}
    for year in monthlyValues:
        for month in monthlyValues[year]:
            values = monthlyValues[year][month]
            spotToAdd = monthlyAves.setdefault(year,{})
            if len(values) > 0:
                spotToAdd[month] = sum(values) / len(values)
            else:
                spotToAdd[month] = missingValue
    return monthlyAves

def getAvesAndStdDevs(seasonalDepartures,group):
    ''' expects the output from getSeasonalDepartures and a group of stations. For each year/season, determines the average,
        std dev, and num of stations used. Creates a nested dict that looks like this:
        
        2008: {   'fall': {   'ave': Decimal("0.6749999999"),
                              'len': 12,
                              'stdev': Decimal("0.4127084719")},
                  'spring': {   'ave': Decimal("-0.8833333333"),
                                'len': 8,
                                'stdev': Decimal("0.4693798678")},
        
    '''
    avesAndStdDevs = {}
    for year in sorted(seasonalDepartures):
        for season in seasonnames:
            stationDepartures = seasonalDepartures[year][season]
            departuresForGroup = []
            for station in group:
                if asKey(station) in stationDepartures:
                    value = stationDepartures[asKey(station)] 
                    if value != missingValue:
                        departuresForGroup.append(value)
                else:
                    print "Couldn't find",asKey(station) # Note -- no such cases exist
            #print year, season, departuresForGroup
            groupsum = sum(departuresForGroup)
            grouplen = len(departuresForGroup)
            if grouplen == 0: continue
            groupave = groupsum / grouplen
            groupstdev = stdev(departuresForGroup)
            
            entryForSeason = avesAndStdDevs.setdefault(year,{}).setdefault(season,{})
            entryForSeason["ave"] = groupave
            entryForSeason["stdev"] = groupstdev
            entryForSeason["len"] = grouplen
    return avesAndStdDevs

def addToMasterDict(masterDict,dictToAdd,groupname,maxminname):
    ''' Adds a subdict (the output of getAvesAndStdDevs) to a massively nested dict.
        Output looks like this:
        2005: {   'fall': {   1: {   'max': {   'ave': Decimal("1.009523810"),
                                                'len': 7,
                                                'stdev': Decimal("0.5187999992")},
                                     'min': {   'ave': Decimal("1.066666667"),
                                                'len': 7,
                                                'stdev': Decimal("0.4895197950")}},
                              2: {   'max': {   'ave': Decimal("0.450000000"),
                                                'len': 4,
                                                'stdev': Decimal("1.223988622")},
                                     'min': {   'ave': Decimal("0.1833333332"),
                                                'len': 4,
                                                'stdev': Decimal("0.9746794345")}}},        
    '''
    for (year,subdict) in dictToAdd.items():
        for (season,subsubdict) in subdict.items():
            spotToAdd = masterDict.setdefault(year,{}).setdefault(season,{}).setdefault(groupname,{})
            spotToAdd[maxminname] = subsubdict

def printMasterDict(md):
    ''' Prints the masterDict as a series of lines, filling in missing values as necessary.
        Dependent on knowledge of the format produced by addToMasterDict()
    '''
    print "YEAR   SEASON  1-M-LEN  1-M-AVE  1-M-STD  1-N-LEN  1-N-AVE  1-N-STD  2-M-LEN  2-M-AVE  2-M-STD  2-N-LEN  2-N-AVE  2-N-STD"
    for year in sorted(md):
        for season in seasonnames:
            outvals = [year,season]
            for group in range(1,3):
                for type in ('max','min'):
                    for cat in ['len','ave','stdev']:
                        try:
                            val = md[year][season][group][type][cat]
                            if val is None: val = missingValue
                        except KeyError:
                            val = missingValue
                            #print "Missing:",year,season,group,type,cat
                        outvals.append(val)
            print "%s %8s %8d %8.2f %8.2f %8d %8.2f %8.2f %8d %8.2f %8.2f %8d %8.2f %8.2f" % tuple(outvals)

def printCount(departures,group):
    ''' test method -- pass maxSeasonalDepartures or minSeasonalDepartures to this method
        to get a count of how many stations in a group have valid seasonal departures for
        each season.'''
    for (year,seasonal) in sorted(departures.items()):
        for season in seasonnames:
            bystation = seasonal[season]
            goodvalues = []
            for station in group:
                if asKey(station) in bystation:
                    if bystation[asKey(station)] != missingValue: goodvalues.append(bystation[asKey(station)])
            print year,season,len(goodvalues)
            
def getGroup1summer2004(departures,group):
    ''' Specific small analysis '''
    somedep = {}
    for station in group:
        yearlyvalues = departures[asKey(station)][2004]
        summervalues = [yearlyvalues[5],yearlyvalues[6],yearlyvalues[7]]
        somedep[asKey(station)] = summervalues
    return somedep

def chartDiscrepancyBetweenSeasonalAndMonthly(departures,group):
    print "The following are the values for summer 2004 for group 1 stations (high-alt):"
    summerdeps = getGroup1summer2004(departures,group)
    
    monthlySums = [[],[],[]]
    seasonAves = []
    for station in summerdeps:
        values = [Decimal(val) for val in summerdeps[station]]
        for i in range(0,3):
            if values[i] != missingValue:
                monthlySums[i].append(values[i])
        
        #version omitting missing months
        if any([value == missingValue for value in values]):
            avestring = " "
        else:
            ave = sum(values) / len(values)
            avestring = "%8.2f" % (ave)
            seasonAves.append(Decimal(ave))
        print "%20s %8.2f %8.2f %8.2f : %8s" %(station,values[0],values[1],values[2],avestring)
    
    #    #version allowing missing months
    #    v2 = [v for v in values if v != missingValue]
    #    if len(v2) == 0:
    #        avestring = " "
    #    else:
    #        ave = sum(v2) / len(v2)
    #        avestring = "%8.2f" % (ave)
    #        seasonAves.append(Decimal(ave))
    #    print "%20s %8.2f %8.2f %8.2f : %8s" %(station,values[0],values[1],values[2],avestring)
    
    aves = [0,0,0]
    for i in range(0,3):
        aves[i] = sum(monthlySums[i]) / len(monthlySums[i])
    
    avesAcrossSeason = sum(seasonAves) / len(seasonAves)
    avesAcrossMonths = sum(aves) / len(aves)
    
    print "                                                  %8.2f aveAcrossSeasons"%(avesAcrossSeason)
    print
    print "%20s %8.2f %8.2f %8.2f : %8.2f aveAcrossMonths" %(" ",aves[0],aves[1],aves[2],avesAcrossMonths)

def calculateDeparturesPerGroup():
    ''' This is the main method which accomplishes the task described at the beginning. '''
    maxdepartures = parseDeparturesFromFile("US_annual_tx_deps.dat")
    mindepartures = parseDeparturesFromFile("US_annual_tn_deps.dat")
    
    #pp.pprint(maxdepartures)
    #pp.pprint(getMonthlyAves(maxdepartures, group1))
    
    maxSeasonalDepartures = getSeasonalDepartures(maxdepartures)
    minSeasonalDepartures = getSeasonalDepartures(mindepartures)
    
    maxAves1 = getAvesAndStdDevs(maxSeasonalDepartures,group1)
    maxAves2 = getAvesAndStdDevs(maxSeasonalDepartures,group2)
    minAves1 = getAvesAndStdDevs(minSeasonalDepartures,group1)
    minAves2 = getAvesAndStdDevs(minSeasonalDepartures,group2)
    
    masterDict = {}
    addToMasterDict(masterDict,maxAves1,1,"max")
    addToMasterDict(masterDict,minAves1,1,"min")
    addToMasterDict(masterDict,maxAves2,2,"max")
    addToMasterDict(masterDict,minAves2,2,"min")
    
    printMasterDict(masterDict)

def incrementSeason(season,year):
    curseason = seasonnames.index(season)
    curyear = year
    curseason += 1
    if curseason > 3:
        curseason = 0
        curyear += 1
    return (seasonnames[curseason],curyear)

def flattenDeparturesForGroupAndPeriod(departures,group,startseason,startyear,endseason,endyear):
    
    curseason = startseason
    curyear = startyear

    seasonalDepartures = getSeasonalDepartures(departures)

    departuresflat = []
    while curseason != endseason or curyear != endyear:
        #print curseason,curyear

        curDepartures = seasonalDepartures[curyear][curseason]
        for station in group:
            if asKey(station) in curDepartures:
                value = curDepartures[asKey(station)]
                if value != missingValue: departuresflat.append(value)
        (curseason,curyear) = incrementSeason(curseason,curyear)
    return departuresflat

def calculateAvesForAllInGroup(departures,group,startseason,startyear,endseason,endyear):
    ''' Note: start season/year is inclusive; end season/year is exclusive. '''
    departures = flattenDeparturesForGroupAndPeriod(departures,group, startseason, startyear, endseason, endyear)
    cursum = sum(departures)
    length = len(departures)
    ave = cursum / length
    dev = stdev(departures)
    return (length,ave,dev)
    

def getAvesForGroupsFor2004to2008():
    ''' Method to fulfill a request from MP:
        take all the individual station seasonal departures from fall 2004 to fall 2008, and 
        output the mean and standard deviation for all cases for group 1 and all cases for 
        group 2 (excluding missing, of course)
    '''
    maxdepartures = parseDeparturesFromFile("US_annual_tx_deps.dat")
    mindepartures = parseDeparturesFromFile("US_annual_tn_deps.dat")
    
    fmt = "%s  %d  %3d %8.2f %8.2f"
    
    print "type gp len      ave      dev"
    (length,ave,dev) = calculateAvesForAllInGroup(maxdepartures,group1,"fall", 2004, "winter", 2008)
    print fmt %("max",1,length,ave,dev)
    (length,ave,dev) = calculateAvesForAllInGroup(mindepartures,group1,"fall", 2004, "winter", 2008)
    print fmt %("min",1,length,ave,dev)
    (length,ave,dev) = calculateAvesForAllInGroup(maxdepartures,group2,"fall", 2004, "winter", 2008)
    print fmt %("max",2,length,ave,dev)
    (length,ave,dev) = calculateAvesForAllInGroup(mindepartures,group2,"fall", 2004, "winter", 2008)
    print fmt %("min",2,length,ave,dev)

def retrieveValue(dictionary,station):
    ''' Minor utility method to return the value from a station, or missingValue if not found.
        Relies on the knowledge that a station's asKey() value is used as the key. '''
    try:
        v = dictionary[asKey(station)]
    except KeyError:
        v = missingValue
    return v

def printSeasonalDeparturesPerStation():
    ''' MP requests: print seasonal departures for each station (x-axis) for each season (y-axis) '''
    maxdepartures = parseDeparturesFromFile("US_annual_tx_deps.dat")
    mindepartures = parseDeparturesFromFile("US_annual_tn_deps.dat")
    maxSeasonalDepartures = getSeasonalDepartures(maxdepartures)
    minSeasonalDepartures = getSeasonalDepartures(mindepartures)
    
    startseason = "fall"
    startyear = 2004
    endseason = "winter"
    endyear = 2008
    
    curseason = startseason
    curyear = startyear
    
    header = ["Year","Season"]
    for s in group1:
        header.append("max"+asKey(s))
        header.append("min"+asKey(s))
    for s in group2:
        header.append("max"+asKey(s))
        header.append("min"+asKey(s))
        
    outlines = [",".join(header)]
    while curseason != endseason or curyear != endyear:
        out = [str(curyear),curseason]
        curMaxDepartures = maxSeasonalDepartures[curyear][curseason]
        curMinDepartures = minSeasonalDepartures[curyear][curseason]
        for s in group1:
            out.append("%8.2f"%(retrieveValue(curMaxDepartures,s)))
            out.append("%8.2f"%(retrieveValue(curMinDepartures,s)))
        for s in group2:
            out.append("%8.2f"%(retrieveValue(curMaxDepartures,s)))
            out.append("%8.2f"%(retrieveValue(curMinDepartures,s)))
        outlines.append(",".join(out))
        (curseason,curyear) = incrementSeason(curseason, curyear)
    printlist(outlines,sortData=False)
    

calculateDeparturesPerGroup() # main method
#printSeasonalDeparturesPerStation()