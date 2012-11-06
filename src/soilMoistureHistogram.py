'''
Created on Aug 9, 2011

@author: egg.davis
'''
from crn import *

s = "Crossville"
por = getPor(s)
els = findElements('SMV\d{4}')
allowQuerySizeOverride()
d = getData(s,por,els)

for el in els:
    dForEl = sorted(d.forElement(el),key=lambda f:f.value)

    # Remove outliers -- aka remove 10% of the members of dForEl, namely 
    # the 5% with the lowest value and the 5% with the highest value
    deletelength = len(dForEl) / 20
    del(dForEl[-1*deletelength:])
    del(dForEl[:deletelength])

    graphTitle = "Soil moisture, middle 90%%: %s %s" % (s,el.name)
    histogram(dForEl,numBins=6,title=graphTitle)
    