'''
@author: diana.kantor

Soil-specific Report functionality. Checks data for soil-specific
indicators such as spikes, jumps, frozen soil flags, and missing
volumetric calculations.
'''

from crn import *
import StandardReport

SPIKE_THRESHOLD = 5.0
stndReport = StandardReport.StandardReport()

class SoilReport:
    '''Constructor. Sets global vars to be used throughout program.'''
    def __init__(self):
        return

    '''A mapping of report column names with their descriptions.'''
    def getColumnInfo(self):
        columns = []
        columns.append(('spike', "The number of spikes for this sensor. Values with range, frozen, or door flags are not included as spikes."))
        columns.append(('jump', "The number of jumps for this sensor. Values with range, frozen, or door flags are not included as jumps."))
        columns.append(('frozen', "The number of values with a frozen flag. Or 'N/A' for non-soil moisture sensors."))
        columns.append(('no volumetric', "The number of values for which volumetric was not calculated. Or 'N/A' for non-soil moisture sensors."))

        return columns

    '''Counts facts with frozen soil bit set in the flag integer.'''
    def countFrozenFlags(self, facts):
        count = stndReport.countFlagsForType(facts, 16)[0] 
        if count==0 and len(facts)>0 and not self.isSoilMoistureElement(facts[0].element):
            return "N/A"
        return count

    '''Counts the number of facts with no corresponding calculated
       volumetric values. Ignores facts that are not for soil moisture
       dielectric elements.'''
    def countNoVolumetric(self, facts):
        count = 0
        for fa in facts:
            elem = findElement(fa.elementId)
            elemName = elem.name
            if not self.isSoilMoistureElement(elem):
                return "N/A"

            stationId = fa.stationId
            datetimeId = fa.datetimeId
            volElemName = elemName.replace('M','MV')
            volElem = list(elementDao.getElementsByName([volElemName]).values())
            volFact = getData(stationId, datetimeId, volElem)
            if len(volFact) is 0:
                count += 1; 
        return count;    

    '''Counts the number of spikes in this collection of facts. A spike
       occurs when a value goes far up/down from normal for 1 hour'''
    def countSpikes(self, facts):
        firstBad = 0
        triplets = self.gatherFactGroups(facts, 3)
        spikeCount = 0
        for trip in triplets:
            diff1 = trip[1].value - trip[0].value
            diff2 = trip[1].value - trip[2].value
            # Check that both changes are greater than the allowed "spike threshold"
            if (float(abs(diff1))>SPIKE_THRESHOLD) and (float(abs(diff2))>SPIKE_THRESHOLD):
                # If so, it is only a spike if one change is positive and the other is negative.
                if(diff1 > 0 and diff2 > 0) or (diff1 < 0 and diff2 < 0):
                    spikeCount+=1
                    if firstBad==0: firstBad = trip[1].datetime.datetime0_23

        return (spikeCount, firstBad)

    '''Counts the number of "jumps" in a set of facts for a station and sensor.
       A jump is similar to a spike except that it goes up/down for 2 hours
       before returning to normal, rather than for just one hour.'''
    def countJumps(self, facts):
        firstBad = 0
        quadruples = self.gatherFactGroups(facts, 4)
        jumpCount = 0
        for quad in quadruples:
            diff1 = (quad[1].value - quad[0].value)
            diff2 = (quad[1].value - quad[2].value)
            diff3 = (quad[2].value - quad[3].value)
            # Check that the first and last change are greater than the allowed "spike threshold"
            # and that the middle change is LESS than the allowed threshold.
            if (float(abs(diff1))>SPIKE_THRESHOLD) and (float(abs(diff2))<SPIKE_THRESHOLD) and (float(abs(diff3))>SPIKE_THRESHOLD):
                # If so, it is only a jump if the first and last changes are in the opposite direction.
                if (diff1 > 0 and diff3 > 0) or (diff1 < 0 and diff3 < 0):
                    jumpCount+=1
                    if firstBad==0: firstBad = quad[1].datetime.datetime0_23

        return (jumpCount, firstBad)


    '''Group facts for a sensor together in each consecutive group of X datetimes.
       Used for soil spike test.'''
    def gatherFactGroups(self, facts, numInGroup):
        factGroupList = []

        # Could work without sorting it first, but sort anyway
        sorted(facts, key=attrgetter("datetimeId"))

        for fa in facts:
            # Get each group of size numInGroup, which will be returned as lists of 1-item lists
            factGroup = [facts.forDatetime(fa.datetimeId-idx) for idx in range(numInGroup)]
            if any(not fact for fact in factGroup):
                continue

            # Now that we only have lists with all elNum facts, turn each 1-item fact 
            # list into a fact
            factGroup = [fact[0] for fact in factGroup]

            # Remove any groups of elNum facts that have any flagged facts.
            if any(self.isFlaggedOtherThanSensor(fact) for fact in factGroup):
                continue

            #print "range: %s-%s elems: %s %s" % (dt-1,dt+2,smel,stel)
            factGroupList.append(factGroup)

        return factGroupList

    '''For a fact, determines if it has any range, door, frozen flags or any
       other flag that is not a bad sensor flag. Since this application is intended
       to determine independently whether the sensor is "bad" we do not want to 
       take into account any previous determination that it is bad.'''
    def isFlaggedOtherThanSensor(self, fact):
        return (fact.flag > 0) and (fact.flag != 32)

    '''Determines if an element represents a soil moisture dielectric sensor.'''
    def isSoilMoistureElement(self, elem):
        elemName = elem.name
        regexMatch = re.match("SM[123][(005)|(010)|(020)|(050)|(100)]",elemName)
        if regexMatch is not None:
            return True
        return False

# END
