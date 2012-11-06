'''
A set of attempts to detect spikes in real time (ie from just one side of the spike), starting
with a histogram to find distribution of magnitude of spikes.

Created on Sep 13, 2011

@author: egg.davis
'''
from crn import *
from math import floor

#stations = findStations("Asheville 8", "Asheville 13", "Crossville", "NC Durham", "Los Alamos", "Bedford", "Necedah", "Limestone", "Blackville", "Joplin", "Salem")
stations = sorted(stationDao.getStationsCurrentlyWithSmSt().values())

start = findDate("2010060100")
end   = findDate("2010060800").previous()

smels = ['SM2020', 'SM3010', 'SM1005', 'SM1050', 'SM3005', 'SM2010', 'SM3020', 'SM1020', 
         'SM1010', 'SM2100', 'SM2050', 'SM3050', 'SM1100', 'SM2005', 'SM3100']
stels = ['ST2020', 'ST3010', 'ST1005', 'ST1050', 'ST3005', 'ST2010', 'ST3020', 'ST1020', 
         'ST1010', 'ST2100', 'ST2050', 'ST3050', 'ST1100', 'ST2005', 'ST3100']

def gatherSoilTriplets(d,smel,stel):
    ''' Takes a FactCollection and, for each consecutive triplet of hours therein, creates 
    a triplet containing data for each soil sensor as a pair of facts, one for SM and one for
    ST. Each such triplet looks like:
        ( (hour1-sm,hour1-st),(hour2-sm,hour2-st),(hour3-sm,hour3-st) )
    A list containing all such triplets is returned.
    '''
    returnlist = []
    depths = ['005','010','020','050','100']
    try:
        dts = sorted([dt.datetimeId for dt in d.datetimes])[1:-1] # Omit first and last
    except: # if not a valid station id (1147)
        return returnlist
    for dt in dts:
        try:
            facts = [(d.forElement(smel).forDatetime(subdt)[0],
                      d.forElement(stel).forDatetime(subdt)[0])
                      for subdt in range(dt-1,dt+2)
                      ]
        except KeyError: # Missing data
            continue
        returnlist.append(facts)
    return returnlist

def gatherSoilTripletsAllEls(d):
    ''' Takes a FactCollection and, for each consecutive triplet of hours therein, creates 
    a triplet containing data for each soil sensor as a pair of facts, one for SM and one for
    ST. Each such triplet looks like:
        ( (hour1-sm,hour1-st),(hour2-sm,hour2-st),(hour3-sm,hour3-st) )
    A list containing all such triplets is returned.
    '''
    returnlist = []
    depths = ['005','010','020','050','100']
    try:
        dts = sorted([dt.datetimeId for dt in d.datetimes])[1:-1] # Omit first and last
    except: # if not a valid station id (1147)
        return returnlist
    for dt in dts:
        for hole in range(1,4):
            for depth in range(5):
                elsuffix = '%d%s'%(hole,depths[depth])
                try:
                    facts = [(d.forElement('SM'+elsuffix).forDatetime(subdt)[0],
                              d.forElement('ST'+elsuffix).forDatetime(subdt)[0])
                              for subdt in range(dt-1,dt+2)
                              ]
                except KeyError: # Missing data
                    continue
                returnlist.append(facts)
    return returnlist

def areSameSign(v1,v2):
    ''' Returns true iff v1 and v2 are either both positive or both negative. '''
    return (v1 > 0 and v2 > 0 or
            v1 < 0 and v2 < 0)

def filterMissing(triplets):
    ''' Filters out triplets which have any missing SM values and returns the filtered list.
    This is a simplified criterion.
    Note that we are not checking for missing ST facts -- the following check for frozen soil will catch missing as well.
    '''
    cutoff = Decimal("-150")
    return [t for t in triplets if all(v[0].value > cutoff for v in t)] # v[0] is SM fact
    
def filterOutOfRange(triplets):
    ''' Filters out triplets whose SM values are out of range. (Catches missing SM values as well) 
    '''
    lowercutoff = Decimal("0")
    uppercutoff = Decimal("84.35")
    return [t for t in triplets if all(lowercutoff < v[0].value < uppercutoff for v in t)] # v[0] is SM fact
        
def filterFrozen(triplets):
    ''' Filters out any triplets which have *any* frozen soil elements and returns the filtered list.
    This is a simplified criterion. '''
    cutoff = Decimal("2")
    return [t for t in triplets if all(v[1].value > cutoff for v in t)] # v[1] is ST fact

def filterNonBumps(triplets):
    bumptriplets = []
    for t in triplets:
        v1 = t[1][0].value - t[0][0].value
        v2 = t[1][0].value - t[2][0].value
        if areSameSign(v1, v2):
            bumptriplets.append(t)
    return bumptriplets

def getMagnitude(t):
    ''' Returns the *smaller* of the two jumps -- both sides of a spike must be > 5.0. '''
    v1 = abs(t[1][0].value - t[0][0].value)
    v2 = abs(t[1][0].value - t[2][0].value)
    return min(v1,v2)

def getBumps(triplets):
    tripletsInRange = filterOutOfRange(triplets)
    tripletsUnfrozen = filterFrozen(tripletsInRange)
    bumps = filterNonBumps(tripletsUnfrozen)
    return bumps

def bumpMagnitudes(bumps):
    return [getMagnitude(bump) for bump in bumps]

def gatherBumpMagnitudes():
    ''' Create a histogram showing the distribution of "bump" magnitudes (where a "bump" is
    a dielectric jump in one direction and then immediately back to baseline, which may be
    ordinary variation or may be a spike).
    '''
    magnitudes = []
    for station in stations:
        d = getData(station,(start,end),(smels,stels))
        if not d: continue
        print station.name,
        triplets = gatherSoilTriplets(d) # Slightly complex data structure containing all consecutive 3-hour triplets
        bumps = getBumps(triplets)
        bumpmagnitudes = bumpMagnitudes(bumps)
        magnitudes.extend(bumpmagnitudes)
        #printlist(bumps,sortData=False)
    printlist(magnitudes,sortData=False)
    printfile("magnitudes.txt",magnitudes,sortData=False)
    
def findRealBumpsAllEls():
    for station in stations:
        
        d = getData(station,(start,end),(smels,stels))
        if not d: continue
        print str(station.name)+",",
        triplets = gatherSoilTriplets(d) # Slightly complex data structure containing all consecutive 3-hour triplets
        bumps = getBumps(triplets)
        
        bumpmagnitudes = bumpMagnitudes(bumps)
        actualspikes = [b for b in bumpmagnitudes if float(b) > 5.0]
        numspikes = len(actualspikes)
        print  "%d,%f"%(numspikes, (float(numspikes) / len(d)))
    
def findRealBumps():
    for station in stations:
        for i in range(len(smels)):
            d = getData(station,(start,end),(smels[i],stels[i]))
            if not d: continue
            print str(station.name)+","+smels[i]+",",
            triplets = gatherSoilTriplets(d,smels[i],stels[i]) # Slightly complex data structure containing all consecutive 3-hour triplets
            bumps = getBumps(triplets)
            
            bumpmagnitudes = bumpMagnitudes(bumps)
            actualspikes = [b for b in bumpmagnitudes if float(b) > 5.0]
            numspikes = len(actualspikes)
            print  "%d,%f"%(numspikes, (float(numspikes) / len(d)))
    
def binMagnitudes(rawbumps,simpleprint=False):
    ''' Takes a list of magnitudes and bins them up, outputting a list of bins and the frequency
    associated with them. '''
    binsize = .05
    counts = {}
    for bump in rawbumps:
        bin = "%.2f"%(floor(bump*(1.0/binsize)) / (1.0/binsize))
        #print bump, bin, counts.get(bin,0),
        counts[bin] = counts.get(bin,0) + 1
        #print counts[bin]
    if simpleprint:
        maxbin = float(max(counts.keys()))
        bin = 0.00
        while bin <= maxbin:
            binstring = "%.2f"%(bin)
            count = counts.get(binstring,0)
            print "%s,%d,%d"%(binstring,min(count,20),count)
            bin += binsize
    return counts

def binFromFile():
    f = open("h:/crnscript-data/magnitudes.txt")
    rawbumps = [float(v) for v in f.readlines()]
    binMagnitudes(rawbumps, simpleprint=True)

#gatherBumpMagnitudes()
#binFromFile()
findRealBumps()