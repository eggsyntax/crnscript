'''
Provides a couple of useful functions for crnscript users.

Created on Jan 19, 2011

@author: egg.davis
'''

from crn import *

import os, re, time
from ftplib import FTP

#from Fact import Fact

import gov.noaa.ncdc.crn.domain.POR as POR
import gov.noaa.ncdc.crn.domain.Datetime as Datetime

def uploadConsoleHistory():
    ''' If you encounter something you don't understand while using the interactive console, you may wish to speak 
        with a crnscript developer about it. Before doing so, please call this function, which will make your 
        interactive console history available to a developer. (*nix-only -- this functionality is not yet available
        under windows)
    '''
    # TODO: candidate for deletion.
    import getpass
    import random
    home = os.path.expanduser("~")
    #username = getpass.getuser()
    try: # unix boxen
        file = open(os.path.join(home,".jline-jython.history"))
    except:
        
        print "Console history does not yet work under windows (JLine not yet fully implemented under jython)."
        '''
        try: # windows boxen
            filename = os.path.join("C:\\Documents and Settings",username,".jline-jython.history")
            print filename
            file = open(filename)
            print type(file)
        except:
            print "Sorry, unable to open your console history. Please see a developer."
            return
        '''
        
    ftp = FTP("ftp0")
    ftp.login()
    ftp.cwd("/pub/download")
    uploadFilename = "jline-jython."+str(int(random.random()*1000))+".history"
    ftp.storlines("STOR "+uploadFilename,file)
    file.close()
    
    print "Console history uploaded as",uploadFilename,"-- Please alert a crnscript developer."
    
def history(*term):
    ''' Searches your console history for the string passed in as a parameter (or prints the last 100 lines of the
        history if there's no parameter). (*nix-only -- this functionality is not yet available
        under windows)
    '''
    from dsl.output import printlist
    try:
        import readline
    except:
        raise Exception("Sorry, unable to read console history (doesn't work on Windows).")

    history = []
    for i in range(readline.get_current_history_length()):
        history.append(readline.get_history_item(i))
    if len(term)==0: # no args
        printlist(history[-100:-1],sortData=False)
        return
    else:
        term = term[0] # unpack from tuple
    selectedHistory = [l for l in history if term in l]
    printlist(selectedHistory[-100:-1],sortData=False)
 
def log(target):
    ''' Convenience method for logging. If you annotate any function with @log, you'll get a print statement
        showing when the function is called and what its output is.
    '''
    def wrapper(*args,**kwargs):
        print "Executing",target.__name__,"with args",str(args),str(kwargs)
        retval = target(*args,**kwargs)
        print target.__name__,"returned",str(retval)
        return retval
    return wrapper

def _userDataDirectory():
    ''' Return the standard user data directory (as a string). '''
    rootpath = os.path.expanduser(os.path.join("~","crnscript-data"))
    if not os.path.exists(rootpath): os.mkdir(rootpath)
    return rootpath

def _createEmptyDirectory(path):
    ''' Creates an empty directory as given by path. If the directory already exists, ensure
    it's empty (by deleting everything in it! So use with caution. '''
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.makedirs(path)

''' Note -- no doctests; none of these functions is really testable. '''
