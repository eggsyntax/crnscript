'''
@author: diana.kantor

Standard Report functionality. Checks data for general
indicators that may apply to most types of sensors, such
as range flags, missing values, door flags, presence
on the "bad sensor" list, and noise.
'''

from crn import *
import datetime
import csv
import os

MISSING_VALUE = -999
NOISE_THRESHOLD = 0.5
BAD_SENSOR_LIST_LOC = "/home/crn/dev/crninputs/BadSensorList.csv"

# Global vars populated in constructor, which do not change 
# throughout program run.
badSensors = []
columns = []

class StandardReport:
    '''Constructor. Sets global vars to be used throughout program.'''
    def __init__(self):
        global badSensors, columns 
        badSensors = self.getBadSensorList()
        columns = self.getColumnInfo()

        return

    '''A mapping of report column names with their descriptions.'''
    def getColumnInfo(self):
        columns = []
        columns.append(('first bad', "The first date for which this sensor experienced a range flag, missing value, spike, or jump."))
        columns.append(('on list', "Whether or not this sensor is already on the 'bad sensor list'."))
        columns.append(('missing', "Number of values equal to the missing value (-999)."))
        columns.append(('range', "Number of values with a range flag."))
        columns.append(('door', "Number of values with a datalogger door open flag."))
        columns.append(('noise', "The noise ration for this sensor."))

        return columns

    '''A generic method that counts the number of 
       a specified type of flags on a list of facts.'''
    def countFlagsForType(self, facts, bitVal):
        firstBad = 0
        count = 0
        for fa in facts:
            fl = fa.flag
            if (fl & bitVal) > 0:
                if firstBad==0: firstBad = fa.datetime.datetime0_23
                count += 1
        return (count, firstBad)

    '''Counts facts with datalogger door bit set in the flag integer.'''
    def countDoorFlags(self, facts):
        return self.countFlagsForType(facts, 4)[0]

    '''Counts facts with range bit set in the flag integer.'''
    def countRangeFlags(self, facts):
        return self.countFlagsForType(facts, 1) 

    '''Counts facts with bad sensor bit set in the flag integer.'''
    def countSensorFlags(self, facts):
        return self.countFlagsForType(facts, 32)[0]

    '''Counts the number of facts with the missing value.'''
    def countMissing(self, facts):
        count = 0
        firstBad = 0
        for fa in facts:
            if fa.value == MISSING_VALUE:
                if firstBad == 0: firstBad = fa.datetime.datetime0_23
                count+=1
        return (count, firstBad)

    '''Gets a list of bad sensor rows from the specified 
       "bad sensor list".'''
    def getBadSensorList(self):
        badSensors = []
        fileRows = csv.reader(open(BAD_SENSOR_LIST_LOC,'rb'))
        for row in fileRows:
            badSensors.append(row)
        return badSensors

    '''If this sensor for this station is on the bad sensor
       list as a currently bad sensor (no end date), return True.
       Otherwise, return false.'''
    def onBadSensorList(self, station, sensor):
        # Make a fresh copy so that we start looping through from the beginning
        badSensorsCopy = []
        badSensorsCopy.extend(badSensors)

        for row in badSensorsCopy:
            if not len(row) >= 3:
                continue
            rowStationId = row[0].strip()
            rowSensorName = row[1].strip()
            rowEndDate = row[3].strip()
            if (str(station.stationId)==rowStationId) and (sensor.name==rowSensorName) and (rowEndDate==''):
                return "Yes"
        return "No"

    '''Gets the "noise ratio" for the facts for a station's sensor.
       This algorithm created by Egg Davis. 
       See also crnscript/trunk/src/evaluateSoilNoise.py'''
    def getNoiseRatio(self, facts):
        largeSteps = 0
        totalSteps = 0
        for i,f in enumerate(facts):
            prevVal = facts[i-1].value if i > 0 else 0 # No step change on first step 
            step = float(abs(f.value - prevVal))
            if step > NOISE_THRESHOLD and step < 150: # ignore changes to/from missing values
                largeSteps += 1
            totalSteps += 1
        noiseRatio = float(largeSteps) / totalSteps
        return round(noiseRatio, 3)

# END
