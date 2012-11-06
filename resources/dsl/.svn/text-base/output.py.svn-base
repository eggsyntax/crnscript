'''
Provides functions which handle output of crnscript data to terminal or to file, in human-
readable, csv, or fixed-width format.
 
Created on Jan 19, 2011

@author: egg.davis
'''

from crn import *
from utils import _userDataDirectory

from java.util import Map

def printlist(*data,**kwargs):
    ''' Prints a list, nicely formatted, with one member on each line. Pass it nearly anything
        -- a list, a map, a dict, whatever -- and it'll do its best to print it nicely. Special
        case: it'll take the same parameters as getData(), so rather than calling 
        printlist(getData(stations,dates,elements)), feel free to directly call 
        printlist(station,dates,elements).
        Prints sorted by default, using the classes' internal compareTo() method (which sorts 
        by station/datetime/element for Facts). Use sortData=False to bypass 
        sorting.
    '''
    sortData = kwargs.get('sortData',True) # sort by default

    # Special case: were we passed parameters for obtaining a dataset?
    if len(data) == 3:
        station,date,element = data
        printlist(getData(station,date,element))
        return
    else:
        data = data[0] # unwrap from tuple
        
    if isinstance(data,Map): # Special case -- for maps, print key : value by zipping them into tuples
        data = zip(data.keySet(),data.values())
    if isinstance(data,dict): # Similar special case but for python dicts
        data = zip(data.keys(), data.values())
        
    try:
        if sortData: data = sorted(data) 
        for n in data:
            print str(n).rstrip('\r\n')
    except: # In case the user accidentally passes in something un-iterable
        print "Your argument to printlist is not any sort of list."
        print data

def printfile(filename,data,sortData=True,append=False):
    ''' Writes the output from getData (or an arbitrary list) to a file of your choice. Takes 
        a filename, data, and an optional "sortData" argument. File will be placed in a 
        directory called "crnscript-data" in your home directory (typically your network drive 
        on Windows boxen, or ~ on *nix) unless a directory is specified.
    '''
    openmode = "a" if append else "w"

    if not os.path.dirname(filename): # ie if a raw filename is given rather than a directory+filename 
        rootpath = _userDataDirectory()
        file = open(os.path.join(rootpath,filename),openmode)
    else:
        file = open(filename,openmode)
            
    if isinstance(data,Map): # Special case -- for maps, print key : value by zipping them into tuples
        data = zip(data.keySet(),data.values())
        
    if isinstance(data,dict): # Similar special case but for python dicts
        data = zip(data.keys(), data.values())
    
    try:
        if sortData: data = sorted(data)
        for n in data:
            file.write(str(n).rstrip('\r\n'))
            file.write("\n")
    except TypeError: # In case the user accidentally passes in something besides a list
        file.write(str(data))

    file.close()

def csv(*data):
    ''' Takes the output from getData and formats it in csv, suitable for 
        pasting into Excel, sorted by station, date, element. Alternately, it accepts the same 
        set of parameters that getData() does. Typically passed on to printlist or printfile, 
        eg "printlist(csv(data))".
    '''
    # Were we passed a dataset or parameters for obtaining a dataset?
    if len(data) == 3:
        station,date,element = data
        return csv(getData(station,date,element))
    else:
        data = data[0] # unwrap from tuple
    isListOfFacts = True
    
    if type(data) not in (list,FactCollection):
        isListOfFacts = False
    returnList = []
    for fact in sorted(data): # iterate over keys so we can sort
        if not isinstance(fact,Fact):
            isListOfFacts = False
            break
        returnList.append("%s,%s,%s,%s,%s" % (fact.station.name,fact.datetime.datetime0_23,fact.element.name,fact.value,fact.flag))
    
    # TODO: the following section, handling the dict which is output by
    # groupByObservation(), is a bit of a hack. Would it be better to have
    # groupByObservation() and similar methods output a custom class which
    # inherits from dict and which have a .csvrepr() function which provides
    # its own csv representation? And perhaps a .fixedrepr()? Needs more thought.
    
    if not isListOfFacts: # try treating it as the output of groupByObservation
        try:
            returnList = []
            for key in data:
                linevals = []
                for item in key:
                    linevals.append(str(item))
                factlist = data[key]
                for fact in factlist:
                    linevals.append(str(fact.element.name))
                    linevals.append(str(fact.value))
                line = ','.join(linevals)
                returnList.append(line)
        except:
            raise Exception("Input to csv must be a FactCollection or a list of Facts or a set of facts grouped by Observation.")

    return returnList

def fixed(*data):
    ''' Takes the output from getData (a FactCollection) and formats it in fixed-width, 
        suitable for import into Fortran. Alternately, it accepts the same set of parameters 
        that getData() does. Typically passed on to printlist or printfile, eg 
        "printfile('myfile.txt', fixed(data))".
    '''
    # Were we passed a dataset or parameters for obtaining a dataset?
    if len(data) == 3:
        station,date,element = data
        return fixed(getData(station,date,element))
    else:
        data = data[0] # unwrap from tuple
    
    if not isinstance(data,FactCollection): 
        raise Exception("Input to fixed must be a FactCollection.")
    outList = []
    for fact in sorted(data): # iterate over keys so we can sort
        if not isinstance(fact,Fact):
            raise Exception("Input to fixed must be a FactCollection.")
        if len(fact.datetime.datetime0_23) == 10: fact.datetime.datetime0_23 = fact.datetime.datetime0_23 + "00"
        outList.append("%04d %12d %10s %9.3f %2d" % (int(fact.station.getStationId()),
                                                        int(fact.datetime.datetime0_23),
                                                        fact.element.name,
                                                        Decimal(fact.value),int(fact.flag)))
    return outList

def uploadFileToFtp(source,target,server="ftp0"):
    ''' Uploads a file to the ftp server as a file of your choice. Target can be a path 
    (relative paths are treated as starting with /pub/data/uscrn) or path+filename. If you 
    give a path only, it is presumed that you wish to preserve the source filename. 
    Remember that, as with all NCDC data, data are placed on the ftp0 server and then 
    automatically moved over to the ftp server a little while later. '''
    from ftplib import FTP
    target = _createAbsoluteFilenameForFtp(target)
    
    (targethead,targettail) = os.path.split(target)
    (sourcehead,sourcetail) = os.path.split(source)
    
    # If a filename was not given, use the source filename
    if targettail == "":
        targettail = sourcetail
        target = "%s/%s"%(targethead,targettail)

    # Figure out location of source file
    if not os.path.dirname(source) or not os.path.isabs(source): # if target is a relative path: # ie if a raw filename is given rather than a directory+filename 
        rootpath = _userDataDirectory()
        source = os.path.join(rootpath,source)

    try:
        sourcefile = open(source)
    except IOError:
        print "Could not open %s -- are you sure the file exists?"
        return
    ftp = FTP()
    ftp.connect(server)
    ftp.login()
    try:
        ftp.cwd(targethead)
    except:
        ftp.mkd(targethead) # Will only create the leafmost directory.
        ftp.cwd(targethead)
    try:
        ftp.delete(target) # Permissions on NCDC FTP servers mean you have to delete instead of overwriting
    except:
        pass # Can't delete it if it's not there.
    ftp.storlines("STOR "+target,sourcefile)
    sourcefile.close()
    try:
        ftp.quit()
    except: # quit() can fail if the server behaves impolitely
        ftp.close()

def uploadDataToFtp(source,target,server="ftp0"):
    ''' Uploads data (typically a FactCollection) to the ftp server as a target filename of your
    choice. You can specify a directory (relative paths are presumed to begin with /pub/data/uscrn);
    if you do not, data are placed in /pub/data/uscrn/temp/. Remember that, as with all
    NCDC data, data are placed on the ftp0 server and then automatically moved over to the ftp
    server a little while later. If you upload data to the FTP server, you are encouraged to
    delete it when it is no longer needed. '''
    from ftplib import FTP
    from random import randint
    from java.io import File
    
    tempfilename = "crnscript_tempfile_" + str(randint(100000,999999)) + ".txt"
    printfile(tempfilename,source,sortData=False)
    uploadFileToFtp(tempfilename,target,server)
    os.remove(os.path.join(_userDataDirectory(),tempfilename))
    
def _createAbsoluteFilenameForFtp(target):
    rootDirectory = '/pub/data/uscrn/'
    defaultDirectory = rootDirectory + 'temp/'
    
    if not os.path.dirname(target): # ie if a raw target is given rather than a directory+target 
        absolutetarget = defaultDirectory + target
    elif not os.path.isabs(target): # if target is a relative path
        absolutetarget = rootDirectory + target
    else:
        absolutetarget = target
    return absolutetarget

def __doctests():
    ''' These doctests are automatically run if you run the module. You should get no output 
    unless there's a problem.
    
    >>> printlist(csv("Barrow",("10/10/2009 9:00","+1"),("temp","precip")))
    AK Barrow 4 ENE,2009101009,P_OFFICIAL,0,0
    AK Barrow 4 ENE,2009101009,T_OFFICIAL,-2,0
    AK Barrow 4 ENE,2009101010,P_OFFICIAL,0,0
    AK Barrow 4 ENE,2009101010,T_OFFICIAL,-1.5,0
    
    >>> printlist(fixed("Barrow",("10/10/2009 9:00","+1"),("temp","precip")))
    1007 200910100900 P_OFFICIAL     0.000  0
    1007 200910100900 T_OFFICIAL    -2.000  0
    1007 200910101000 P_OFFICIAL     0.000  0
    1007 200910101000 T_OFFICIAL    -1.500  0

    csv() also handles the output from groupByObservation():
    >>> data = getData("Barrow",("10/10/2009 9:00","+3"),("temp","precip"))
    >>> printlist(csv(data.groupedByObservation()))
    AK Barrow 4 ENE,10/10/09 09:00 UTC,P_OFFICIAL,0,T_OFFICIAL,-2
    AK Barrow 4 ENE,10/10/09 10:00 UTC,P_OFFICIAL,0,T_OFFICIAL,-1.5
    AK Barrow 4 ENE,10/10/09 11:00 UTC,P_OFFICIAL,0,T_OFFICIAL,-1.2
    AK Barrow 4 ENE,10/10/09 12:00 UTC,P_OFFICIAL,0,T_OFFICIAL,-1
 
'''

if __name__ == "__main__":
    import doctest #@UnresolvedImport
    doctest.testmod()

