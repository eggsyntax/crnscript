'''
@author: diana.kantor

Soil Sensor Report. Checks data for all stations measuring soil for all 
soil sensors for the previous month to detect potential problems.
Sends a report to the specified senders.
'''

from crn import *
import StandardReport
import SoilReport
import datetime
import smtplib
import base64

RANGE_MAX = 0
MISSING_MAX = 0
NOISE_RATIO_MAX = 0.6
SPIKE_MAX = 0
JUMP_MAX = 0
EMAIL_SERVER = "localhost"

stndReport = StandardReport.StandardReport()
soilReport = SoilReport.SoilReport()
reportTypes = []
columns = []
rowFormat = ""

class ReportWriter:

    def __init__(self, types=["standard"]):
        global reportTypes, columns, rowFormat
        reportTypes = types
        columns = self.getColumnInfo()
        # format is %s,%s,%s,%s,etc for the number of columns
        rowFormat = ",".join(["%s" for x in columns]) + "\n"
        return

    '''Sends an email with the provided recipients, sender, subject, and message
       text, and with the specified file as an attachment.'''
    def sendReport(self, recipients, sender, subject, text, attachFile):
        fo = open(attachFile, 'rb')
        fileContent = fo.read()
        encodedContent = base64.b64encode(fileContent)
        part1 = """From: %s
To: %s
Subject: %s
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (sender, recipients, subject, "AUNIQUEMARKER", "AUNIQUEMARKER")
        part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (text, "AUNIQUEMARKER")

        part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--""" % (attachFile, os.path.basename(attachFile), encodedContent, "AUNIQUEMARKER")
        message = part1 + part2 + part3

        s = smtplib.SMTP(EMAIL_SERVER)
        s.sendmail(sender, recipients, message)
        s.quit()
        return

    '''Writes the specified text content to the specified file location.'''
    def writeReport(self, filePath, text):
        file = open(filePath, 'w')
        file.write(text)
        file.close()
        return

    '''A mapping of report column names with their descriptions.'''
    def getColumnInfo(self):
        columns = []
        columns.append(('start', "The first datetime for which the sensor is being analyzed. Format is yyyymmddhh."))
        columns.append(('end',"The last datetime for which the sensor is being analyzed. Format is yyyymmddhh."))
        columns.append(('stationId', "The internal CRN id for this station."))
        columns.append(('station', "The human-readable station name."))
        columns.append(('sensor', "The name of the CRN element that corresponds with the sensor being analyzed."))
    
        if("standard" in reportTypes):
            columns += stndReport.getColumnInfo()
        if("soil" in reportTypes):
            columns += soilReport.getColumnInfo()

        return columns

    '''Prints the first row of the file, which is the comma-separated
       names of each column.'''
    def constructHeader(self):
        # For each column info list item, the column name is the
        # first item in a tuple.
        headerItems = [x[0] for x in columns]
        headerText = ",".join(headerItems) + "\n"
        return headerText

    '''Prints everything that goes under the sensor data rows.'''
    def constructFooter(self):
        footerText = "\nColumn definitions:\n"
        for col in columns:
            footerText += "\"%s: %s\"\n" % (col[0], col[1])
        return footerText

    '''For the given station, for each element, construct the output rows for
       any sensor that is considered bad.'''
    def constructRow(self, station, start, end, element):
        text = ""
        rowValues = []
        isSensorSuspect = False
        firstBadDates = []

        data = getData(station,(start,end),element)
        # Not all stations have soil sensors at all 5 layers,
        # so skip this element if there's no data.
        if not data: return text
        facts = data.factlist
        facts.sort(key=attrgetter("datetimeId"))

        # Standard checks for any sensor.
        if("standard" in reportTypes):
            rangeFlags = stndReport.countRangeFlags(facts)
            missing = stndReport.countMissing(facts)
            rangeFlagCount = rangeFlags[0]
            missingCount = missing[0]
            doorFlagCount = stndReport.countDoorFlags(facts)
            noiseRatio = stndReport.getNoiseRatio(facts)
            onList = stndReport.onBadSensorList(station, element)
            firstBadDates = [rangeFlags[1], missing[1]]
            rowValues = [onList, missingCount, rangeFlagCount, doorFlagCount, noiseRatio]
            if rangeFlagCount>RANGE_MAX or missingCount>MISSING_MAX or noiseRatio>NOISE_RATIO_MAX or onList=="Yes":
                isSensorSuspect = True
        
        # Soil-specific checks.
        if("soil" in reportTypes):
            spikes = soilReport.countSpikes(data)
            jumps = soilReport.countJumps(data)
            frozenFlagCount = soilReport.countFrozenFlags(facts)
            noVolCount = soilReport.countNoVolumetric(facts)
            spikeCount = spikes[0]
            jumpCount = jumps[0]
            firstBadDates = firstBadDates + [spikes[1], jumps[1]]
            rowValues += [spikeCount, jumpCount, frozenFlagCount, noVolCount]
            if spikeCount>SPIKE_MAX or jumpCount> JUMP_MAX:
                isSensorSuspect = True

        validFirstBads = [fb for fb in firstBadDates if fb is not 0]
        if validFirstBads: firstBad = min(validFirstBads)
        else: firstBad = "None"

        # Print if it meets the criteria for a suspected bad sensor.
        rowValues = [start, end, station.stationId, station.name, element.name, firstBad] + rowValues
        if isSensorSuspect:
            text += (",".join([str(x) for x in rowValues])) + "\n"
        return text

    '''Puts together the header, rows for each station for each
       element, and the footer.'''
    def constructReport(self, stations, start, end, elements):
        header = self.constructHeader()
        rows = ""
        for station in stations:
            for elem in elements:
                row = self.constructRow(station, start, end, elem)
                rows += row
                
        footer = self.constructFooter()
        return header + rows + footer

# END
