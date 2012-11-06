'''
Custom product for use in satellite validation. For each of twenty pre-chosen stations, creates
two daily files, one with several five-minute values for each five-minute period in the day
(local midnight to local midnight), and one with a number of hourly values for each hour in the
day. These are uploaded to directories on the FTP server for the product and date within 
/pub/data/uscrn/download/satval. 
  
Created on Jun 27, 2011
@author: egg.davis
'''
from crn import *
from datetime import datetime,timedelta

stations = ["AK Fairbanks 11 NE", "CA Fallbrook 5 NE", "CA Merced 23 WSW", "CA Yosemite Village 12 W", "IL Champaign 9 SW", 
                "IN Bedford 5 WNW", "KS Manhattan 6 SSW", "MT Wolf Point 29 ENE", "NC Durham 11 W", "NV Denio 52 WSW", 
                "NV Mercury 3 SSW", "OK Goodwell 2 E", "OR Coos Bay 8 SW", "PA Avondale 2 N", "SD Sioux Falls 14 NNE", 
                "TN Crossville 7 NW", "TX Austin 33 NW", "WA Darrington 21 NNE", "WA Quinault 4 NE", "WY Sundance 8 NNW"]
    
five_min_els = sorted(findElements('P5_\d','T5_',':RH\d\d:'),key=lambda e:e.name) # Temp,RH,windspeed,precip
hourly_els   = sorted(findElements('temp','precip','wind','solar','SUR_TEMP','ST\d{4}','SMV\d{4}'),key=lambda e:e.name)

def padded_day(day):
    ''' Returns the start and end datetimeIds for the day, with a chunk of padding at the beginning
    to account for timezone differences. Use d.forLocalDay() to pull out the precise local-day
    facts for each station. '''
    datetime = findDate(day).datetimeId
    start = datetime - 24
    end = datetime + 14
    return (start,end)

def flatten(listOfLists):
    "Flatten one level of nesting. All members of top-level list must be lists or other iterables."
    return [i for l in listOfLists for i in l]

def create_header(els):
    ''' Creates a header line for a product from a list of elements '''
    fields = ["Date             "]
    for e in els:
        fields.extend([e,"Flag"])
    return "\t".join(fields)
    
def format_obs(d):
    ''' Takes a FactCollection, groups it into observations, and formats them into a readable tab-separated line. '''
    output = []
    dbo = d.groupedByObservation()
    for o in sorted(dbo):
        line = [o[1]] # date
        for f in dbo[o]:
            line.extend(["%7.1f"%(f.value),"%2d"%(f.flag)])
        output.append("\t".join(line))
    return output

def build_product(day,els,productname,is_subhourly):
    ''' Building the 5-minute and hourly products is almost the same process, so we use a
    generic function. Gets the data, formats it, and uploads it. '''

    (start,end) = padded_day(day)
    data1 = getData(stations,(start,end),els)
    grouped_data = data1.groupedByObservation(fillMissing=True)
    data2 = FactCollection(flatten(grouped_data.values()))
    if is_subhourly: data2 = subhourly(data2)
    els_present = sorted(list(set([f.element.name for f in data2])))
    for station in stations:
        output = []
        output.append(create_header(els_present))
        output.extend(format_obs(data2.forStation(station).forLocalDay(day)))
        filename = productname+"_"+station.replace(" ","_") + "_" + day[0:8] + ".txt"
        uploadDataToFtp(output, "download/satval/%s/%s/%s" % (productname,day[0:8],filename))

def build_5min_product(day):
    build_product(day,five_min_els,"SatValIp5min01",is_subhourly=True)

def build_hourly_product(day):
    build_product(day,hourly_els,"SatValIpHourly01",is_subhourly=False)


dt = datetime.now() - timedelta(hours=24)
day = dt.strftime("%Y%m%d12")

build_5min_product(day)
build_hourly_product(day)


def __doctests():
    ''' These doctests are not (as is often the case) run when you run the module; running the module builds & uploads the product.
    >>> day = "10/10/10 10:00"
    >>> print padded_day(day)
    (87769, 87817)
    
    >>> l1 = [[1,2],[3,4],[5,6]]
    >>> print flatten(l1)
    [1, 2, 3, 4, 5, 6]
    
    >>> data2 = getData('asheville','10/10/10 10:00','temp+')
    >>> els_present = sorted(list(set([f.element.name for f in data2])))
    >>> print create_header(els_present) #doctest: +NORMALIZE_WHITESPACE
    Date                 FSPD_S1    Flag    FSPD_S2    Flag    FSPD_S3    Flag    ST1005    Flag    ST1010    Flag    ST1020    Flag    ST1050    Flag    ST1100    Flag    ST2005    Flag    ST2010    Flag    ST2020    Flag    ST2050    Flag    ST2100    Flag    ST3005    Flag    ST3010    Flag    ST3020    Flag    ST3050    Flag    ST3100    Flag    ST005    Flag    ST010    Flag    ST020    Flag    ST050    Flag    ST100    Flag    ST_MN    Flag    ST_MX    Flag    ST_STD    Flag    SUR_TEMP    Flag    T105    Flag    T110    Flag    T115    Flag    T120    Flag    T125    Flag    T130    Flag    T135    Flag    T140    Flag    T145    Flag    T150    Flag    T155    Flag    T160    Flag    T1_MAX    Flag    T1_MIN    Flag    T1_STD    Flag    T205    Flag    T210    Flag    T215    Flag    T220    Flag    T225    Flag    T230    Flag    T235    Flag    T240    Flag    T245    Flag    T250    Flag    T255    Flag    T260    Flag    T2_MAX    Flag    T2_MIN    Flag    T2_STD    Flag    T305    Flag    T310    Flag    T315    Flag    T320    Flag    T325    Flag    T330    Flag    T335    Flag    T340    Flag    T345    Flag    T350    Flag    T355    Flag    T360    Flag    T3_MAX    Flag    T3_MIN    Flag    T3_STD    Flag    T5_1    Flag    T5_10    Flag    T5_11    Flag    T5_12    Flag    T5_2    Flag    T5_3    Flag    T5_4    Flag    T5_5    Flag    T5_6    Flag    T5_7    Flag    T5_8    Flag    T5_9    Flag    TINLET_MX    Flag    TPANEL    Flag    TRH05    Flag    TRH10    Flag    TRH15    Flag    TRH20    Flag    TRH25    Flag    TRH30    Flag    TRH35    Flag    TRH40    Flag    TRH45    Flag    TRH50    Flag    TRH55    Flag    TRH60    Flag    TRH_MAX    Flag    TRH_MIN    Flag    TRH_STD    Flag    TSURFSB    Flag    TSURFSB_STD    Flag    T_MAX    Flag    T_MIN    Flag    T_OFFICIAL    Flag
    
    >>> printlist(format_obs(data2),sortData=False) #doctest: +NORMALIZE_WHITESPACE
    10/10/10 10:00 UTC      114.4     0      114.3     0      115.4     0       14.7     0       15.5     0       16.6     0       17.7     0       19.1     0       15.2     0       15.3     0       16.8     0       17.5     0       19.2     0     -999.0     1       16.2     0       16.8     0       17.6     0       18.8     0       15.0     0       15.7     0       16.7     0       17.6     0       19.1     0        4.0     0        5.5     0        0.1     0        4.2     0        5.0     0        4.7     0        4.8     0        4.8     0        4.8     0        4.8     0        4.7     0        4.8     0        4.6     0        4.7     0        4.6     0        4.6     0        5.0     0        4.6     0        0.1     0        5.0     0        4.7     0        4.8     0        4.8     0        4.8     0        4.8     0        4.7     0        4.8     0        4.6     0        4.7     0        4.6     0        4.6     0        5.0     0        4.6     0        0.1     0        4.9     0        4.7     0        4.8     0        4.8     0        4.8     0        4.8     0        4.7     0        4.8     0        4.6     0        4.7     0        4.6     0        4.6     0        5.0     0        4.6     0        0.1     0        5.0     0        4.7     0        4.6     0        4.6     0        4.7     0        4.9     0        4.8     0        4.8     0        4.8     0        4.7     0        4.8     0        4.6     0        4.5     0        4.9     0        4.9     0        4.7     0        4.8     0        4.8     0        4.8     0        4.7     0        4.7     0        4.8     0        4.6     0        4.6     0        4.6     0        4.6     0        4.9     0        4.6     0        0.1     0        4.1     0        0.1     0        5.0     0        4.6     0        4.7     0
    10/10/10 10:00 UTC      114.0     0      114.7     0      107.8     0       15.4     0       15.7     0       16.5     0       17.5     0       19.1     0       14.4     0       15.5     0       17.0     0       17.3     0       18.8     0       13.4     0       15.7     0       17.2     0       18.0     0       19.1     0       14.4     0       15.6     0       16.9     0       17.6     0       19.0     0        3.8     0        4.8     0        0.2     0        4.0     0        5.9     0        5.9     0        6.1     0        5.8     0        5.9     0        6.2     0        6.5     0        6.3     0        6.0     0        5.9     0        5.7     0        5.7     0        6.5     0        5.6     0        0.3     0        5.9     0        5.9     0        6.1     0        5.8     0        5.9     0        6.1     0        6.4     0        6.2     0        6.0     0        5.8     0        5.7     0        5.7     0        6.5     0        5.6     0        0.2     0        5.9     0        5.9     0        6.0     0        5.8     0        5.9     0        6.1     0        6.4     0        6.2     0        6.0     0        5.8     0        5.6     0        5.6     0        6.5     0        5.6     0        0.2     0        5.9     0        5.8     0        5.7     0        5.7     0        5.9     0        6.1     0        5.8     0        5.9     0        6.1     0        6.4     0        6.2     0        6.0     0        5.3     0        6.0     0        5.9     0        5.8     0        6.0     0        5.8     0        5.8     0        6.1     0        6.4     0        6.2     0        5.9     0        5.8     0        5.6     0        5.6     0        6.4     0        5.6     0        0.2     0        5.1     0        0.1     0        6.5     0        5.7     0        6.0     0

'''
