'''
Created on Nov 19, 2010

@author: egg.davis

Tests a method for evaluating soil sensor noisiness by creating time series graphs (for 
visual analysis) which give a figure for noise ratio:
noise ratio = ((|stepChanges| >  k) / totalStepChanges)
Note the two variables at the beginning which should be set to the desired values
'''

from crn import *
import org.jfree.chart.LegendItem as LegendItem
import org.jfree.chart.LegendItemCollection as LegendItemCollection


''' Set these two variables according to your needs '''
noiseThreshold = 0.5 # Anywhere from 0..1
rangeOfInterest = (.6,1.01) # Sensors whose noiseRatio falls in this range will be printed 
                            # to the console and also plotted.
                            
stations = list(stationDao.getStationsCurrentlyWithSmSt().values())[0:20] # Pick 20 stations.
# Alternately, set stations to a list of specific stations of interest, e.g. 
#stations = findStations("oakley 19","pierre 24","des moines 17")

def addRatioToLegend(plot,noiseRatio):
    legendString = "Noise Ratio: %2.2f" % (noiseRatio)
    legendItem = LegendItem(legendString)
    collection = plot.getLegendItems()
    collection.add(legendItem)
    plot.setFixedLegendItems(collection)

def createHistogram(data):
    ''' Creates a histogram from a list of arbitrary numerical data in range from 0..1'''
    from org.jfree.data.category import DefaultCategoryDataset
    from org.jfree.chart import ChartFactory,ChartFrame
    from org.jfree.chart.plot import PlotOrientation
    from java.lang import Float
    
    numBins=20
    datamin = min(data)
    datamax = max(data)
    #binsize = 1.01 / numBins

    bins = {}
    for d in data:
        binkey = round(d,1)
        bin = bins.setdefault(binkey,0)
        bins[binkey] = bin + 1
        
    # Create dataset from bins
    dataset = DefaultCategoryDataset()

    # Ensure that bins exist even if they're empty
    i = datamin
    while i <= 1.0:
        bins.setdefault(round(float(i),1),0)
        i += .1
        
    #print "Number of bins:",len(bins)
    for bin in sorted(bins):
        #print "bin:",bin,type(bin)
        dataset.addValue(bins[bin],"","%05.2f"%(bin))
    
    # Create chart from dataset
    chart = ChartFactory.createBarChart(
                "", # chart title
                "Bin", # domain axis label
                "Number of occurrences", # range axis label
                dataset, # data
                PlotOrientation.VERTICAL, # orientation
                True, # include legend
                True, # tooltips?
                False # URLs?
                )
    plot = chart.getPlot()
    plot.getRenderer().setShadowVisible(False)
    frame = ChartFrame("Histogram", chart);
    frame.pack();
    frame.setVisible(True);
    return plot


def normalizeRange(plot):
    axis = plot.getRangeAxis()
    axis.setRange(0,60)
    
def getNoiseRatio(dataset):    
    largeSteps = 0
    totalSteps = 0
    for i,f in enumerate(dataset):
#        if i==0: # No step change on first step
#            prevVal = 0
#        else:
#            prevVal = d[i-1].value 
        prevVal = dataset[i-1].value if i > 0 else 0 # No step change on first step 
        step = float(abs(f.value - prevVal))
        if step > noiseThreshold and step < 150: # ignore changes to/from missing values
            #print "At time %s comparing %5.2f and %5.2f" % (f.datetime.datetime0_23,f.value,prevVal)
            largeSteps += 1
        totalSteps += 1
    #print "large steps: %d, total steps: %d" % (largeSteps,totalSteps)
    noiseRatio = float(largeSteps) / totalSteps
    return noiseRatio

def createGraph(d,noiseRatio):
    plot = graph(d,showMissing=False)
    normalizeRange(plot)
    addRatioToLegend(plot,noiseRatio)


#def evaluate(station,(start,end),element):
#    d = getData(station,(start,end),element)
#    d.sort()
#    noiseRatio = getNoiseRatio(d)
#    #createGraph(d,noiseRatio)
#    return noiseRatio

smels = ['SM2020', 'SM3010', 'SM1005', 'SM1050', 'SM3005', 'SM2010', 'SM3020', 'SM1020', 
         'SM1010', 'SM2100', 'SM2050', 'SM3050', 'SM1100', 'SM2005', 'SM3100']

ratios = []
print ("Evaluating noise ratios with a noise threshold of %4.2f, graphing ratios between %4.2f and %4.2f" % (noiseThreshold,rangeOfInterest[0],rangeOfInterest[1]))
for station in stations:
    params = (station,('1/1/11','1/31/11'),smels)
    #print "Evaluating %s" %(station)
    stationData = getData(*params)
    for el in smels:
        d = [f for f in stationData if f.element.name == el]
        d.sort()
        #print "pulled %d facts from a total of %d for the station" % (len(d),len(stationData))
        
        if len(d) == 0: # May be 0 for stations that don't have sensors below 10 cm
            continue
        ratio = getNoiseRatio(d)
        if ratio > rangeOfInterest[0] and ratio < rangeOfInterest[1]:
            print station,el,ratio
            createGraph(d,ratio)
        ratios.append(ratio)
createHistogram(ratios)

#evaluate('lincoln 8',('12/1/10','12/31/10'),'SM2100')
#evaluate('riley 10',('12/1/10','12/31/10'),'SM3005')
#evaluate('joplin',('12/1/10','12/31/10'),'SM2100')
#evaluate('edinburg',('12/1/10','12/31/10'),'SM3050')
#evaluate('monroe 26',('1/1/11','1/31/11'),'SM1020')
#evaluate('monroe 26',('1/1/11','1/31/11'),'SM3010')
#evaluate('stillwater 5',('1/1/11','1/31/11'),'SM1100')
#evaluate('austin 33',('1/1/11','1/31/11'),'SM3010')
#evaluate('mercury 3',('1/1/11','1/31/11'),'ST1050')


