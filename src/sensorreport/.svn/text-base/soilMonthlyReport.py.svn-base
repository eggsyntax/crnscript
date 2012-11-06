'''
@author: diana.kantor

Monthly Soil Sensor Report. Checks data for all stations measuring soil for all 
soil sensors for the previous month to detect potential problems.
Sends a report to the specified recipients.
'''

from crn import *
import ReportWriter
import datetime

ELEMENTS_REGEX = "soil moisture dielectric .* for the hour|soil temperature \(Celsius\) .* for the hour"
REPORT_OUTPUT_FILE_LOC = "/home/dkantor/sensorreports"
EMAIL_RECIPIENTS = ["diana.kantor@noaa.gov","jesse.bell@noaa.gov","michael.palecki@noaa.gov"]
EMAIL_SENDER = "diana.kantor@noaa.gov"
EMAIL_SUBJECT = "Soil sensor report"
REPORT_TYPES = ["standard","soil"]
reportWriter = ReportWriter.ReportWriter(REPORT_TYPES)

# Get the hourly soil elements for dielectric and temp
soilElems = findElements(ELEMENTS_REGEX)
soilElems.sort(key=attrgetter('name'))

# Get the stations that measure soil and order alphabetically
soilStations = list(stationDao.getStationsCurrentlyWithSmSt().values())
soilStations.sort(key=attrgetter('nameString'))

# Get start and end of previous month from current date.
now = datetime.datetime.now()
if now.month is 1:
    prevMonth = 12
    prevYear = (now.year) - 1
else:
    prevMonth = (now.month)-1
    prevYear = now.year

start = ("%4d%02d0100" % (prevYear, prevMonth))
end =   ("%4d%02d0100" % (now.year, now.month))

# Construct and write the report.
reportOutput = reportWriter.constructReport(soilStations, start, end, soilElems)
outputFilepath = "%s/SoilSensorReport%4d%02d%02d.csv" % (REPORT_OUTPUT_FILE_LOC, now.year, now.month, now.day)

# Send the report as an email attachment.
reportWriter.writeReport(outputFilepath, reportOutput)
messageText = "This soil sensor report was generated on %4d-%02d-%02d for the time period from %s to %s" % (now.year, now.month, now.day, start, end)
reportWriter.sendReport(EMAIL_RECIPIENTS, EMAIL_SENDER, EMAIL_SUBJECT, messageText, outputFilepath)

# END
