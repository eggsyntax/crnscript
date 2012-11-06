'''
Provides graphing functions for crnscript data using the JFreeChart API.

Created on Jan 19, 2011

@author: egg.davis
'''

from crn import *

from org.apache.commons.math.stat.regression import SimpleRegression

def graph(*data,**kwargs):
    ''' Creates a simple time series graph. Takes the output from getData (a list of Facts). 
        Alternately, you can pass the same set of parameters that are passed to getData().
        Takes an optional elements argument which expresses which elements to show. Also
        takes an optional showMissing argument which determines whether missing values (-9999.0)
        should be displayed. Also takes an optional lineWidth argument which lets you set lines
        heavier or lighter. Example: graph(data,elements=("temp","precip"),showMissing=False). 
        Returns the plot object in case you want to customize the graph in some way.
    '''
    from org.jfree.chart import ChartFactory,ChartFrame
    from org.jfree.data.time import TimeSeries,TimeSeriesCollection, Minute
    from java.awt import BasicStroke

    # Were we passed a dataset or parameters for obtaining a dataset?
    if len(data) == 3:
        station,date,element = data
        graph(getData(station,date,element))
        return
    else:
        data = data[0] # unwrap from tuple
    
    showMissing = kwargs.get('showMissing',True)
    lineWidth = kwargs.get('lineWidth',2.0)
    title = kwargs.get('title',"Time series graph")
    elementsToShow = [e.name for e in findElements(kwargs.get('elements',""))]
    datasets = {}
    for fact in sorted(data):
        
        if fact.value in missingValues and not showMissing: continue  
        station = str(fact.station.name)
        element = fact.element.name
        if elementsToShow and element not in elementsToShow: continue
        series = station+":"+element
        date = fact.datetime
        hour = date.getHour()
        if fact.subhourlyTime is not None:
            subhourlyTime = int(fact.subhourlyTime)
        else:
            subhourlyTime = 0
        if subhourlyTime == 60: # JFreeChart can't handle the 1-60 representation of minute in CRN
            subhourlyTime = 0
        minute = Minute(subhourlyTime,hour,date.getDay(),date.getMonth()+1,date.getYear()) # JFreeChart's representation of time
        if series not in datasets:
            datasets[series] = TimeSeries(series)
        datasets[series].add(minute,float(fact.value))
    
    timeSeriesCollection = TimeSeriesCollection()
    for dataset in datasets.values():
        timeSeriesCollection.addSeries(dataset)

    chart = ChartFactory.createTimeSeriesChart("", "UTC Date", "Value", timeSeriesCollection, True, True, False)
    plot = chart.getPlot()

    r = plot.getRenderer()
    r.setStroke(BasicStroke(lineWidth))
    
    frame = ChartFrame(title, chart)
    frame.pack()
    frame.setVisible(True)
    return plot

def histogram(*data,**kwargs):
    ''' Creates a histogram. Takes the output from getData (a list of Facts), or alternately the
        same parameters that getData() takes. Takes an optional 'numBins=k' argument, where k
        specifies the number of bins. Returns the plot object in case you want to customize the 
        graph in some way. Takes an optional 'title' argument.
    '''
    # TODO: offset labels.
    from org.jfree.data.category import DefaultCategoryDataset
    from org.jfree.chart import ChartFactory,ChartFrame
    from org.jfree.chart.plot import PlotOrientation
    from java.lang import Float
    
    # Were we passed a dataset or parameters for obtaining a dataset?
    if len(data) == 3:
        station,date,element = data
        histogram(getData(station,date,element),**kwargs)
        return
    else:
        data = data[0] # unwrap from tuple
    
    # Find min and max; decide on number of bins
    numBins=kwargs.get('numBins',16)
    datamin,datamax = _getminmax(data)
    binsize = abs((datamax - datamin) / (Decimal(numBins)*Decimal("0.999"))) # divide by .999; otherwise there's always a final bin with one member, the max
    if binsize == 0: 
        raise Exception("Cannot create histogram; all values are equal to "+str(datamin))
    
    title = kwargs.get('title',"Histogram")
    
    # Create bins based on value.
    stations = {}
    for d in data:
        if d.value in missingValues: continue
        binkey = round(float(datamin + binsize * int((d.value - datamin) / binsize)),2)
        name = d.station.getNameString()+", "+d.element.name
        bin = stations.setdefault(name,{}).setdefault(binkey,0)
        stations[name][binkey] = bin + 1
    # Create dataset from bins
    dataset = DefaultCategoryDataset()
    for station in stations:
        
        # Ensure that bins exist even if they're empty
        i = datamin
        while i < datamax:
            stations[station].setdefault(round(float(i),2),0)
            i += binsize
            
        #print "Number of bins:",len(stations[station])
        for bin in sorted(stations[station]):
            #print "bin:",bin,type(bin)
            dataset.addValue(stations[station][bin],station,Float(bin))
    
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
    frame = ChartFrame(title, chart);
    frame.pack();
    frame.setVisible(True);
    return plot

def scatter(data,x=None,y=None,**kwargs):
    ''' Creates a scatter plot comparing two elements. At minimum, takes a collection of data.
        The second and third arguments, if they exist, are treated as the two elements to 
        compare. If these arguments do not exist, the first two elements in the list are 
        compared. If an optional regress=True argument is present, superimposes a linear 
        regression for each series and prints some related info (R-value etc). 
        Note that scatter plots can be zoomed with the mouse. Returns the plot object in
        case you want to customize the graph in some way. Takes an optional showMissing argument 
        which determines whether missing values (-9999.0) should be displayed. 
        Examples: scatter(data), scatter(data,"tmin","tmax",regress=True)
    '''
    from org.jfree.data.xy import XYSeriesCollection,XYSeries
    from org.jfree.data import UnknownKeyException
    from org.jfree.chart import ChartFactory,ChartFrame
    from org.jfree.chart.plot import PlotOrientation,DatasetRenderingOrder
    from org.jfree.chart.renderer.xy import XYLineAndShapeRenderer
    from java.awt import Color
    
    regress=kwargs.get('regress',False)
    showMissing=kwargs.get('showMissing',False)
    
    # Try to be flexible about element parameters
    if x is not None: x = findElement(x).name
    if y is not None: y = findElement(y).name

    # Create a dataset from the data
    collection = XYSeriesCollection()
    for ob in data.groupedByObservation().items():
        key,values = ob
        name = str(key[0])
        if x==None:
            x = values[0].element.name
        try:
            xFact = (i for i in values if i.element.name == x).next()
        except StopIteration: # missing value
            continue
        xval  = xFact.value
        if xval in missingValues and not showMissing: continue  
        if y==None:
            try:
                y = values[1].element.name
            except IndexError:
                raise Exception("Error! Your data request returned only 1 value per observation. " 
                                "Must have 2 values to generate a scatter plot.")
        try:
            yFact = (i for i in values if i.element.name == y).next()
        except StopIteration: # missing value
            continue
        yval  = yFact.value
        if yval in missingValues and not showMissing: continue  
        
        try: 
            series = collection.getSeries(name)
        except UnknownKeyException:
            collection.addSeries(XYSeries(name))
            series = collection.getSeries(name)
        
        series.add(float(xval),float(yval))

    # Create chart from dataset        
    chart = ChartFactory.createScatterPlot( "", x, y, collection, PlotOrientation.VERTICAL,
                                            True, True, False );
    plot = chart.getPlot()
    frame = ChartFrame("Scatter Plot", chart);
    frame.pack();
    frame.setVisible(True);

    # Superimpose regression if desired
    if regress:
        regressioncollection = XYSeriesCollection()
        for series in collection.getSeries():
            regression = _getregression(series)
            x1 = series.getMinX()
            y1 = regression.predict(x1)
            x2 = series.getMaxX()
            y2 = regression.predict(x2)
            regressionseries = XYSeries(series.getKey())
            regressionseries.add(float(x1),float(y1))
            regressionseries.add(float(x2),float(y2))
            regressioncollection.addSeries(regressionseries)

            print series.getKey(),":"
            print "  R:            %8.4f" % regression.getR()
            print "  R-squared:    %8.4f" % regression.getRSquare()
            print "  Significance: %8.4f" % regression.getSignificance()
            print
            
        plot.setDataset(1,regressioncollection)
        regressionRenderer = XYLineAndShapeRenderer(True,False)
        plot.setRenderer(1,regressionRenderer)
        plot.setDatasetRenderingOrder(DatasetRenderingOrder.FORWARD);
        
        colors = [0xec0000,0x58b911,0x6886ea,0xedd612,0xa93bb9,0xffb71b,0xe200df,0x1de2b6,0xdc91db,0x383838,0xb09344,0x4ea958,0xd78c9e,0x64008d,0xb0c95b]
        mainRenderer = plot.getRenderer(0)
        for i in range(collection.getSeriesCount()):
            try:
                mainRenderer.setSeriesPaint(i,Color(colors[i]))
                regressionRenderer.setSeriesPaint(i,Color(colors[i]))
            except IndexError: # Finite # of colors in the color array; beyond that let jfreechart pick
                break
        '''
        # Jump through some hoops to ensure regressions are same color as scatters for each series.
        # Initially: doesn't work because series are not indexed the same. And I don't see a way
        # to get the actual series from the renderer in order to compare names or something.
        mainRenderer = plot.getRenderer(0)
        print "Renderer is",type(mainRenderer)
        index = 0
        paint = mainRenderer.lookupSeriesPaint(index)
        print "Paint is",type(paint)
        while (paint is not None):
            print "Setting paint."
            regressionRenderer.setSeriesPaint(index,paint)
            index += 1
            paint = mainRenderer.getSeriesPaint(index)
        '''
        return plot

#def graphArbitraryData(data):
#    ''' Creates a line graph of arbitrary data (as opposed to the rather specific format used by graph()). Pass in a 
#        list of datapoints, each consisting of a 3-part tuple: (x,y,category). If you're only graphing one sort of
#        data (ie you want a graph with one line), you can pass in any constant for category.
#        
#        Example (one category):
#            data = []
#            for i in range(10):
#                data.append((i,i*i,0))
#            graphArbitraryData(data)
#        
#        Example (multiple categories):
#            data = []
#            for i in range(30):
#                data.append((i,i*i,"squared"))
#                data.append((i,i*i*i,"cubed"))
#            graphArbitraryData(data)
#
#    '''
#    from org.jfree.data.category import DefaultCategoryDataset
#    from org.jfree.chart import ChartFactory, ChartFrame
#    from org.jfree.chart.plot import PlotOrientation
#
#    dataset = DefaultCategoryDataset()
#    for item in data:
#        #print item
#        dataset.addValue(float(item[1]), str(item[2]), str(item[0])); # Note weird ordering
#    chart = ChartFactory.createLineChart("", "", "", dataset, PlotOrientation.VERTICAL, True, True, False)
#    frame = ChartFrame("", chart);
#    frame.pack();
#    frame.setVisible(True);
    
def graphArbitraryData(data,title=""):
    ''' Creates a line graph of arbitrary data (as opposed to the rather specific format used by graph()). Pass in a 
        list of datapoints, each consisting of a 3-part tuple: (x,y,category). If you're only graphing one sort of
        data (ie you want a graph with one line), you can pass in any constant for category.
        
        Example (one category):
            data = []
            for i in range(10):
                data.append((i,i*i,0))
            graphArbitraryData(data)
        
        Example (multiple categories):
            data = []
            for i in range(30):
                data.append((i,i*i,"squared"))
                data.append((i,i*i*i,"cubed"))
            graphArbitraryData(data)

    '''
    from org.jfree.data.category import DefaultCategoryDataset
    from org.jfree.chart import ChartFactory, ChartFrame, ChartPanel
    from org.jfree.chart.plot import PlotOrientation
    from org.jfree.data.xy import XYSeriesCollection, XYSeries

    datasets = {} # dict of all series

    # First, create the individual series from the data
    for item in data:
        seriesname = str(item[2])
        if seriesname not in datasets:
            datasets[seriesname] = XYSeries(seriesname)
        datasets[seriesname].add(float(item[0]), float(item[1]));

    # Second, add those series to a collection
    datasetcollection = XYSeriesCollection()    
    for key in datasets:
        datasetcollection.addSeries(datasets[key])
        
    chart = ChartFactory.createXYLineChart("","","",datasetcollection,PlotOrientation.VERTICAL,True,True,False) 
    frame = ChartFrame(title, chart);
    frame.pack();
    frame.setVisible(True);
    panel = ChartPanel(chart)
    return chart.getPlot()

def _getregression(series):
    ''' given an XYSeries (a jfreechart object), returns a SimpleRegression (Apache commons) fitting
        the series.
    '''
    regression = SimpleRegression()
    for datapoint in series.getItems():
        regression.addData(datapoint.getX(),datapoint.getY())
    return regression

def _getminmax(data):
    ''' Returns the minimum and maximum value from a dataset (a list of Facts). Missing values
        are excluded.
    '''
    sortedkeys = sorted(data,key=lambda d: d.value)
    datamin = sortedkeys[0].value
    while sortedkeys[0].value in missingValues: # eliminate missing keys from DB
        del sortedkeys[0]
        datamin = sortedkeys[0].value
    datamax = sortedkeys[-1].value
    return (datamin,datamax)
    
    