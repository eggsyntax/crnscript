'''
Created on Jan 18, 2011

@author: egg.davis

Creates daily summaries for a year for a station of solar radiation as a % of max. Uses the same
algorithm which is in production for the geographic solar visualizations (see 
https://local.ncdc.noaa.gov/svn/repos/svn-repos/show/CRN/crnweb/trunk/src/flex/utils/Algorithms.as?revision=HEAD
and https://local.ncdc.noaa.gov/svn/repos/svn-repos/show/CRN/crnweb/trunk/src/flex/geosolardailyplustimeseriesvis.mxml?revision=HEAD )

Edit the main function at the end to your taste.

Presumes you've unzipped a daily01 snapshot 
(eg http://www1.ncdc.noaa.gov/pub/data/uscrn/products/daily01/snapshots/CRNDAILY01-201012281930.zip )
into a subdirectory called 'temp' of your home directory (your home directory being ~ on a unix
box or the network drive on a windows box.

'''

from math import pi,cos,sin,acos,tan
from dsl.graph import graphArbitraryData

# These are atmospheric transmission constants
atc1 = 0.23
atc2 = 0.49

# solar constant (MJ/m**2 hr)
g = 4.92

elevations = {}

# compute Julian Day (day-of-year) (This is MP's algorithm for conversion to doy)
def getDoy(datearray):
    month = float(datearray[0])
    day   = float(datearray[1])
    year  = float(datearray[2])
    doy = int((day - 32) + (275 * (month/9)) + (2*(3 / (month + 1))) + (month/100 - (year % 4) + 0.975))
    return doy


def toDegrees(rad):
    return rad * (180.0 / pi)

def toRadians(deg):
    return deg * (pi/180.0)

# Restricts a number to the domain in which acos applies, namely -1 <= x <= 1
def acosable(x):
    return min(1,max(-1,x))


# Given a representation of a daily solar total for a station (as created by geosolardailyplustimeseriesvis),
# returns the percentage of expected total solar radiation which that solar total represents.
def getPercentSolar(daily):
    
    datestring = daily["prettydate"]
    datearray = datestring.split("/")
    elevation = daily["elev"]
    lat = daily["lat"]
    lon = daily["lon"]
    rawSolar = daily["value"] 
    observedSolarMj = rawSolar * 3600.0 / 1000000.0
    # convert latitude to radians
    latRad = toRadians(lat)
    
    # convert elevation to meters
    elev_m = elevation / 3.281
    
    # get day of year
    doy = getDoy(datearray)
    # compute solar declination angle in radians
    declin = 0.409 * sin((((2*pi)/365) * doy) - 1.39)
    
    # compute sunset hour angle in radians
    sunsetAngle = acos(acosable(0-(tan(latRad))*(tan(declin))));
    
    # relative earth-sun distance (dimensionless)
    distanceRatio = (1 + (0.033*cos(((2*pi)/365) * doy)));
    
    # compute extraterrestrial radiation
    exRad = (24.0/pi) * g * distanceRatio * ((sunsetAngle*(sin(latRad)*sin(declin))) 
        + (cos(latRad)*cos(declin)*sin(sunsetAngle)));
    
    # compute clear-sky solar radiation as a function of elevation
    maxSolar = ((atc1 + atc2) + (0.00002 * elev_m)) * exRad;
    
    # calculate the percent of expected solar for the day and station
    if maxSolar <= 0: # Can happen in Alaska
        percent = 0
    else:
        percent = (observedSolarMj/maxSolar) * 100.0
    
    # for testing, I would like the output to include all % calculations
    # in production, we will limit to 100%
    #if (percent > 100.0) percent = 100.0;
    
    return (maxSolar,percent)

def readData(stationName,year):
    # reads data from a file and constructs some key info from it.
    import os,string
    dates = []
    solars = []
    filename = "CRNDAILY01-%s-%s.txt" % (year,stationName)
    f = open(os.path.expanduser(os.path.join("~","temp",str(year),filename)))
    lines = f.readlines()
    for line in lines:
        date = line[17:19]+"/"+line[19:21]+"/"+line[13:17]
        dates.append(date)
        solar = float(string.lstrip(line[85:93]))
        solars.append(solar)
        lat = float(string.lstrip(line[37:44]))
        lon = float(string.lstrip(line[29:36]))
    return (dates,solars,lat,lon)

def generatePercentSolar(stationName,year): # example stationName: SD_Sioux_Falls_14_NNE
    if not elevations: populateElevations()
    print("Station,Date,Observed Solar,Max Solar,Percent")

    graphdata = []

    day = {}
    day["elev"] = elevations[stationName]
    (dates,solars,lat,lon) = readData(stationName,year)
    day["lat"] = lat
    day["lon"] = lon
    
    for i in range(len(dates)):
        day["prettydate"] = dates[i]
        if solars[i] == -9999.0:
            print(stationName+","+day["prettydate"]+",-9999.0,-9999-0,-9999.0")
            continue
        
        day["value"] = solars[i] * 1000000 / 3600
        (maxSolar,percent) = getPercentSolar(day)
        print "%s,%s,%02.2f,%02.2f,%03.2f" % (stationName,day["prettydate"],day["value"] * 3600 / 1000000,maxSolar,percent)
        graphdata.append((day["prettydate"],solars[i],"OBSERVED"))
        graphdata.append((day["prettydate"],maxSolar,"MAX"))
        #graphdata.append((day["prettydate"],percent,"PERCENT"))
    graphArbitraryData(graphdata)
    
def populateElevations():
        global elevations
        elevations = {"AK_Barrow_4_ENE":15,"AK_Fairbanks_11_NE":1140,"AK_Kenai_29_ENE":282,"AK_Port_Alsworth_1_SW":321,"AK_Red_Dog_Mine_3_SSW":942,"AK_Sand_Point_1_ENE":240,"AK_Sitka_1_NE":78,"AK_St._Paul_4_NE":20,"AL_Brewton_3_NNE":170,"AL_Clanton_2_NE":584,"AL_Courtland_2_WSW":575,"AL_Cullman_3_ENE":800,"AL_Fairhope_3_NE":95,"AL_Gadsden_19_N":1152,"AL_Gainesville_2_NE":107,"AL_Greensboro_2_WNW":280,"AL_Guntersville_2_SW":620,"AL_Highland_Home_2_S":614,"AL_Muscle_Shoals_2_N":530,"AL_Northport_2_S":150,"AL_Russellville_4_SSE":720,"AL_Scottsboro_2_NE":636,"AL_Selma_13_WNW":193,"AL_Selma_6_SSE":157,"AL_Talladega_10_NNE":525,"AL_Thomasville_2_S":350,"AL_Troy_2_W":472,"AL_Valley_Head_1_SSW":1020,"AR_Batesville_8_WNW":455,"AZ_Ajo_29_S":1661,"AZ_Amado_23_W":3300,"AZ_Bowie_23_SSE":5133,"AZ_Cameron_25_SSE":4807,"AZ_Camp_Verde_3_N":3434,"AZ_Coolidge_5_W":1425,"AZ_Elgin_5_S":4811,"AZ_Gila_Bend_3_ENE":780,"AZ_Heber_3_SE":6625,"AZ_Holbrook_17_ESE":5613,"AZ_Kayenta_16_WSW":7274,"AZ_Lake_Havasu_City_19_SE":416,"AZ_Page_9_WSW":3254,"AZ_Phoenix_7_S":1404,"AZ_Roosevelt_4_S":2435,"AZ_Tsaile_1_SSW":7071,"AZ_Tucson_11_W":2733,"AZ_Whiteriver_A_1_SW":5198,"AZ_Williams_35_NNW":5990,"AZ_Yuma_27_ENE":620,"CA_Bodega_6_WSW":63,"CA_Fallbrook_5_NE":1140,"CA_Merced_23_WSW":78,"CA_Redding_12_WNW":1418,"CA_Santa_Barbara_11_W":18,"CA_Stovepipe_Wells_1_SW":84,"CA_Yosemite_Village_12_W":6620,"CO_Akron_A_4_E":4542,"CO_Boulder_14_W":9828,"CO_Buena_Vista_2_SSE":7933,"CO_Center_A_4_SSW":7678,"CO_Colorado_Springs_23_NW":7872,"CO_Cortez_8_SE":8034,"CO_Craig_30_N":6518,"CO_Dinosaur_2_E":6062,"CO_Eads_16_ENE":3967,"CO_Eagle_13_SSE":8605,"CO_Genoa_35_N":4764,"CO_Grand_Junction_9_W":5806,"CO_Kim_9_WSW":5870,"CO_La_Junta_17_WSW":4386,"CO_Meeker_15_W":5761,"CO_Montrose_11_ENE":8402,"CO_Nunn_7_NNE":5390,"CO_Rifle_23_NW":7550,"CO_Rocky_Ford_1_ESE":4170,"CO_Saguache_2_WNW":7823,"CO_Springfield_6_WSW":4557,"CO_Stratton_24_N":4212,"CO_Woodland_Park_14_WSW":8535,"FL_Everglades_City_5_NE":4,"FL_Sebring_23_SSE":150,"FL_Titusville_7_E":3,"GA_Brunswick_23_S":25,"GA_Newton_11_SW":156,"GA_Newton_8_W":176,"GA_Watkinsville_5_SSE":741,"HI_Hilo_5_S":622,"HI_Mauna_Loa_5_NNE":11179,"IA_Des_Moines_17_E":921,"ID_Arco_17_SW":5920,"ID_Murphy_10_W":3950,"IL_Champaign_9_SW":700,"IL_Shabbona_5_NNE":861,"IN_Bedford_5_WNW":760,"KS_Manhattan_6_SSW":1137,"KS_Oakley_19_SSW":2870,"KY_Bowling_Green_21_NNE":790,"KY_Versailles_3_NNW":891,"LA_Lafayette_13_SE":35,"LA_Monroe_26_N":88,"ME_Limestone_4_NNW":737,"ME_Old_Town_2_W":127,"MI_Chatham_1_SE":875,"MI_Gaylord_9_SSW":1461,"MN_Goodridge_12_NNW":1150,"MN_Sandstone_6_W":1130,"MO_Chillicothe_22_ENE":833,"MO_Joplin_24_N":952,"MO_Salem_10_W":1198,"MS_Holly_Springs_4_N":484,"MS_Newton_5_ENE":374,"MT_Dillon_18_WSW":5971,"MT_Lewistown_42_WSW":5070,"MT_St._Mary_1_SSW":4555,"MT_Wolf_Point_29_ENE":2085,"MT_Wolf_Point_34_NE":2643,"NC_Asheville_13_S":2103,"NC_Asheville_8_SSW":2151,"NC_Durham_11_W":562,"ND_Jamestown_38_WSW":1920,"ND_Medora_7_E":2771,"ND_Northgate_5_ESE":1842,"NE_Harrison_20_SSE":4406,"NE_Lincoln_11_SW":1372,"NE_Lincoln_8_ENE":1189,"NE_Whitman_5_ENE":3740,"NH_Durham_2_N":119,"NH_Durham_2_SSW":63,"NM_Artesia_2_WNW":3501,"NM_Aztec_43_E":7024,"NM_Carrizozo_1_W":5366,"NM_Clayton_3_ENE":4885,"NM_Clovis_7_N":4316,"NM_Dulce_1_NW":6806,"NM_Grants_2_S":6443,"NM_Hagerman_10_ESE":3552,"NM_Las_Cruces_20_N":4327,"NM_Los_Alamos_13_W":8716,"NM_Mills_6_WSW":5866,"NM_Mountainair_2_WSW":6489,"NM_Nageezi_18_SSW":6449,"NM_Ramah_9_SE":7164,"NM_Raton_26_ESE":7232,"NM_Reserve_1_W":5842,"NM_San_Rafael_13_SW":7482,"NM_Santa_Fe_20_WNW":7258,"NM_Socorro_17_WSW":10486,"NM_Socorro_20_N":4847,"NM_Taos_27_NW":8151,"NM_Vaughn_36_SSE":5034,"NV_Baker_5_W":6617,"NV_Denio_52_WSW":6500,"NV_Mercury_3_SSW":3284,"NY_Ithaca_13_E":1228,"NY_Millbrook_3_W":413,"OH_Coshocton_8_NNE":1120,"OK_Goodwell_2_E":3266,"OK_Stillwater_2_W":890,"OK_Stillwater_5_WNW":888,"ON_Egbert_1_W":807,"OR_Coos_Bay_8_SW":12,"OR_Corvallis_10_SSW":312,"OR_John_Day_35_WNW":2245,"OR_Riley_10_WSW":4583,"PA_Avondale_2_N":400,"RI_Kingston_1_NW":115,"RI_Kingston_1_W":106,"SC_Blackville_3_W":317,"SC_McClellanville_7_NE":9,"SD_Aberdeen_35_WNW":1957,"SD_Buffalo_13_ESE":2883,"SD_Pierre_24_S":2124,"SD_Sioux_Falls_14_NNE":1594,"TN_Crossville_7_NW":1913,"TN_Oakridge_0_N":0,"TX_Austin_33_NW":1361,"TX_Bronte_11_NNE":1997,"TX_Edinburg_17_NNE":64,"TX_Monahans_6_ENE":2724,"TX_Muleshoe_19_S":3742,"TX_Palestine_6_WNW":383,"TX_Panther_Junction_2_N":3494,"TX_Port_Aransas_32_NNE":15,"UT_Blanding_26_SSW":4390,"UT_Bluff_32_NW":6428,"UT_Brigham_City_28_WNW":4951,"UT_Cedar_City_18_SSE":5096,"UT_Delta_4_NE":4761,"UT_Logan_5_SW":4497,"UT_Mexican_Hat_10_NW":6364,"UT_Midway_3_NE":5748,"UT_Milford_42_WNW":5255,"UT_Moab_9_N":5037,"UT_Monticello_24_NW":5025,"UT_Price_3_E":5808,"UT_Provo_22_E":7808,"UT_St._George_15_NE":3417,"UT_Torrey_7_E":6204,"UT_Tropic_9_SE":5895,"VA_Cape_Charles_5_ENE":29,"VA_Charlottesville_2_SSE":1177,"VA_Sterling_0_N":287,"WA_Darrington_21_NNE":407,"WA_Quinault_4_NE":286,"WA_Spokane_17_SSW":2267,"WI_Necedah_5_WNW":933,"WV_Elkins_21_ENE":3390,"WY_Lander_11_SSE":5773,"WY_Moose_1_NNE":6466,"WY_Sundance_8_NNW":5792}

if __name__ == '__main__':
    generatePercentSolar("FL_Titusville_7_E",2010)

