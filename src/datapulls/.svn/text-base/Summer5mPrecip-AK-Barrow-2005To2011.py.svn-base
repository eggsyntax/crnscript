'''
Created on Jan 13, 2012

From: Martin Bulla <mbulla@orn.mpg.de>
Date: Mon, Jan 9, 2012 at 1:53 AM
Subject: Re: Fwd: Re: Fwd: Barrrow precipitation
To: CRN Helpdesk <ncdc.crn@noaa.gov>


Dear Andrea,

Thank you very much for your reply. 

Ideally, the historical record of precipitation (if available then per minute) from 2005 till 
2011 for May-July would be of a great help to us.

Best wishes,
Martin


On 1/6/2012 17:11, CRN Helpdesk wrote:
Dear Herr Bulla,

I'm not familiar with the ftp site you sent, and it is not currently available. Are you looking
for a daily source of current 5-minute calculated precipitation data for AK Barrow 4 ENE, or are
you looking for the historical record? The CRN Element Listing report (the sample link you sent)
is the best source for retrieving this data on a daily basis. We have several ftp products, but
none of them have that level of granularity. If you'd like the historical record, we can provide
that to you; just let us know which variables you'd like us to provide.

Regards,
Andrea

On 1/5/2012 1:55 AM, Martin Bulla wrote:
Dear Mrs. Braun, 

We are looking for per minute precipitation data for Barrow. 

We were getting Barrow environmental data for (June-July) fromftp://ftp.cmdl.noaa.gov/met/BRW/. 
We wish to use also precipitation, but although variable precipitation can be downloaded from 
this site, it has no values. Yet when we look at the hourly summaries at 

http://www.ncdc.noaa.gov/crn/newelementlisting?station_id=1007&element_group_id=1&element_group_id=2&element_group_id=5&element_group_id=6&element_group_id=7&yyyymmddhh0=2011060101&yyyymmddhh1=2011071601&tref=LST&flags=1&format=web 

the precipitation is present. 

It would help us greatly, if you can suggest a Barrow per minute precipitation source to us. 

Best wishes, 
Martin

@author: Scott.Embler
'''

from crn import *
from dsl.observation import getObservations
from period import Month
import csv

def precipFor15MinuteStream(observation):
    ''' Returns a list representing the record for the 15-minute precipitation of the given observation.'''
    elements = (314,315,316,317)
    hour = findDate(ob.getDatetimeId()).getDatetime0_23()
    facts = getData(observation.getStationId(), observation.getDatetimeId(),elements)
    record = [str(hour), "15"]
    record.extend(values(elements, facts))
    return record
    
def precipFor5MinuteStream(observation):
    ''' Returns a list representing the record for the 5-minute precipitation of the given observation.'''
    elements = (319,320,321,322,323,324,325,326,327,328,329,330)
    hour = findDate(ob.getDatetimeId()).getDatetime0_23()
    facts = getData(observation.getStationId(), observation.getDatetimeId(),elements)
    record = [str(hour), "5"]
    record.extend(values(elements, facts))
    return record

def values(elements, facts):
    '''Returns a list containing facts of the requested elements in the order specified by the first argument.'''
    firsts = [first(facts.forElement(element)) for element in elements]
    return [fact.value if fact is not None else None for fact in firsts]

def first(facts):
    '''Returns the first fact, if available, in the given fact collection.'''
    if len(facts.factlist) > 0:
        return facts.factlist[0]
    else:
        return None

AK_Barrow = findStation("AK Barrow 4 ENE")
f = open('./AK_Barrow_Precip_Record.txt','w')
writer = csv.writer(f, lineterminator='\n')
 
for year in range(2005,2012):
    may, june, july = Month(year,5), Month(year, 6), Month(year, 7)
    for month in (may,june,july):
        for ob in sorted(getObservations(AK_Barrow, (month.start(), month.end()))):
            if ob.getStreamId() == 3:\
                #Stream 3 is a 15-minute precipitation stream used in the early part.
                writer.writerow(precipFor15MinuteStream(ob))
            else:
                writer.writerow(precipFor5MinuteStream(ob))
    