****Working with crnscript:****

The crnscript project provides a turnkey environment for running python scripts or using an interactive
python console with use of the CRN data access capabilities, domain objects, and utilities available from the 
crnshared project. 

***Working with crnscript on a unix server:***

- Log into one of the unix boxes (front is an excellent choice). If you don't already have access
to a unix server, you'll want to put in a request at http://www3.ncdc.noaa.gov/itas/ . Check out 
the project from source control ('svn co https://conman/svn-repos/CRN/crnscript/tags/crnscript-1.14 crnscript') 
and change into the newly created crnscript directory ('cd crnscript').  

- Start X-Win on your desktop (if it's not already running). You may want to put it in your 
startup directory. If you can't find it in your start menu, you may need to put in a helpdesk 
request (https://servicedesk) to have it installed.

- Run the interactive python console: './crnscript'. Personally, I recommend leaving a crnscript
window running at all times -- it makes it easy to reach for crnscript for quick questions.

- You immediately have access to CRN resources. Let's try a few commands:

	station = findStation("Barrow")
	print(station)
		
findStation will search a station based on the station string (the station string is what you see
when you print the station, in this case "Station[1007] AK Barrow 4 ENE (00F0B0,27516)Comm:E, OpStat: Y"). 
You can use the station id or the state/city/vector, for example. findStations, plural, will return a list of 
stations matching the input. So findStations("AZ") would return a list of all Arizona stations.

	print(station.latitude,station.longitude)

Importantly, the returned station is not just an info string but a domain object with its own properties and methods
such as latitude and longitude (try dir(station) to get a full list).

	start = findDate("10/31/09 8:00")
	end = findDate("10/31/09 10:00")

findDate will accept a date string in most formats, a datetime id, "now", or variants like "last Tuesday."

	elements = findElements("precip")
	
findElements() functions much like findStations(). findElements(), by default, first checks a number of predefined
keywords like "temp" and "precip" (you can see them all with showElements()). If a parameter is not one of these 
keywords, findElements() searches the name, description, and element id of the elements (you can get a list of all
elements, by the way, just by doing getAllElements(), and similarly you can get a list of stations with 
getAllStations()). findElements() and findStations() both use smartcase -- if the search term is all lowercase, it 
does a case-insensitive search; otherwise it's case-sensitive. The element names are in all caps, so using an argument 
in all caps is an easy way of restricting the search to name. Also, if findElements() receives an integer input, 
it treats it as an element id. If you're familiar with regular expression syntax, findElements() and findStations() 
accept full regex (see http://docs.python.org/dev/howto/regex.html for details on regex in python).

	data = getData(station,(start,end),element)

Here we put together the parameters we've just obtained and use the getData() method to find the values and flags for 
calculated precip for a few hours at the Barrow station. Any time you want to get values/flags
for some combination of stations, elements, and dates, it should be as simple as that. getData() is limited to
retrieving 120,000 facts by default in order to avoid heavy impact on the database; if you need more, loop through
several requests or speak with a crnscript developer about overriding this limit.

Actually, we can bypass the findStation, findDate, and findElement process if we'd rather, and just pass the 
equivalent parameters directly to getData(). So for example, we could simply say 

	data = getData("Barrow",("2010110100","now"),"temp")
	
and we would get equivalent results. Note that these parameters, and the findStations() and findElements() methods, are
extremely forgiving about what they accept: you can hand them any sort of station/element ids, strings, domain objects,
or mixed collections of any of the above.

	printlist(data)
	
printlist() handles any of the return types from crnscript methods and prints them as a reasonably-formatted list. You
can format them differently using csv() or fixed(). csv() produces comma-separated output, suitable for copying and 
pasting into Excel or other applications. fixed() prints the results in fixed-column format suitable for fortran. 
In addition to printlist(), there are printfile(), graph(), histogram(), and scatter() functions. graph() produces 
a basic time-series graph, histogram() produces a histogram, and scatter() produces a scatterplot with optional
linear regression. printfile("filename.txt",data) prints to a file. 

	showFunctions() 
	
Call showFunctions() to get a list of all the functions you've seen so far, as well as other useful functions, along with
brief explanatory texts. You can also use help() for any of the crnscript functions (eg 'help(printlist)') 
to get information on it.

Reading the src/Examples.py file should give you all the info you need to handle common use cases. You may 
also want to take a look at the rest of the example scripts in the src directory. See also QuickReference.png,
which you may want to print out or otherwise keep handy.

- Use Ctrl-D to exit the console

- To run a python script instead of using the interactive console, just call, for example, 
'./crnscript src/HelloWorld.py'. You'll want to start your scripts with 'from crn import *' to 
provide access to crnscript's capabilities. You can edit scripts by doing, for example,
'gedit src/HelloWorld.py' (nice graphical editor that does syntax highlighting and runs over xwin) or
'nano src/HelloWorld.py' (non-graphical editor). If you happen to be a member of the vi cult, see
http://www.reddit.com/r/programming/comments/e9uvc/ultimate_vim_python_setup/ . You may wish to keep
your personal source files outside the crnscript directory to prevent them from being overwritten when
you update crnscript.

More information about the Python programming language can be found at http://www.python.org/. If you need further
guidance, type "import this" in the interactive console.

- Pro tip 1: one thing that's important to understand about crnscript is that some of its functions, notably
most of the dao methods, return a *Map*, aka a list whose members are key/value pairs. When working with a map, 
you need to think about whether you want to work with the keys or the values (or both). Consider the following example:

	 stations = stationDao.getStationsCurrentlyWithSmSt()
	 
stations now contains a map from integer (station id) to Station objects. To
get a list of just the keys, use stations.keySet(). To get a list of just the Stations, use 
stations.values(). Python's default is to work with the keys, so if you were to say: for s in stations: print s, you
would get a list of integers. If for some reason you wanted to work with both simultaneously, you would use 
stations.entrySet().

It's a bit complicated, to be sure, but if you're ever unsure what you're working with, just do type(myVariable) to
find out. When in doubt, you'll probably want to work with values().
	 
- Pro tip 2: Rounding is something we try to be very careful with in CRN (see 
https://local.ncdc.noaa.gov/wiki/index.php/CRN:Rounding). crnscript is already set up to round properly (half-up), but
there are issues with binary floating point representation of precise decimal numbers. Python has a class which 
avoids these issues (Decimal), and in general, if you need to be careful about precision and rounding, just cast
your numbers to Decimal (the value field of a Fact is already a Decimal) and use the quantize() method to round. 
However, there are a few pain points; in particular, if you use the comparison operators(>,<,=) to compare Decimals 
to non-Decimal numbers, you'll get some unexpected results. See 
http://docs.python.org/release/2.5.2/lib/decimal-faq.html and http://docs.python.org/library/decimal.html for details. 

In general, just be cautious: if you're going to work with Decimals, work with *all* Decimals. If you're considering 
using python for production situations where rounding is a factor, please unit test thoroughly. On the other hand, you can 
use ordinary arithmetic operators with Decimal (+,-,*, etc), which makes it rather less painful than using java's BigDecimal.
On a related note, many values are returned from the database as strings, which give unexpected results when compared
to numbers. If you're getting an odd result from a comparison, try casting the returned value to Decimal and see if
that fixes the problem.


***Accessing underlying Data Access objects***

- The commands you've seen so far are a layer of specialized crnscript methods. They overlay a shared layer of 
data access objects and domain objects. The data access objects serve as a centralized way of asking questions of the 
CRN database, and they return domain objects which themselves have rich functionality. When you need information that 
can't be obtained through the specialized methods shown above, you may want to begin using the daos directly 
(although it's valuable to try showFunctions() first, and check the examples shown in Examples.py -- there are 
rather more methods than have been shown so far!).

	showDaos()

This is a method built into crnscript, and shows us the data access objects underlying crnscript. We observe that one 
of them is stationDao.

	dir(stationDao)

This uses Python's built-in dir() method to show what methods the stationDao object offers. More detail about each method 
can be found in the javadocs (in crnscript/doc/crnshared/index.html). We observe that stationDao has a getStation method.

	station = stationDao.getStation(1124)

This retrieves a station from the database using its station ID.

	print(station)

This calls the station's print method, showing you the station's state, location, and vector and some other pertinent 
info.

	dir(station)

As you can see, the dir() method is extremely powerful and useful, and can be called on any object to show its available 
variables and methods.

	station.getLongName()

This calls one of the methods just shown in order to get the extended name of the station. Note that in the interactive 
console, the result of a method call is automatically printed, whereas in a script you'd need 'print station.getLongName()'.

- You can call the showDaos(), showDomainObjects(), or showUtils() methods to get an idea of what you have at 
your disposal.


***Working with crnscript in Eclipse***

The rest of this document will probably only be of use to developers. Non-developers may wish to leave now and read
Examples.py, which provides many more examples of using crnscript methods.

Working with crnscript on a *nix box is simplest and provides an interactive 
console, but working with crnscript in the Eclipse IDE is perhaps better for developers 
creating substantial projects and includes syntax highlighting/code completion. Personally, I use
both simultaneously -- I develop scripts in Eclipse while simultaneously working with an 
interactive console on front.

Running python scripts in eclipse (once pydev is installed) should be as easy as choosing Run/Run 
from the menu and selecting "Jython Run." 

To open an interactive console in Eclipse, choose the dropdown arrow farthest to the right on the console tab and choose
"Pydev Console." Click "OK" on any dialog boxes that come up. Type "from crn import *" as your first command to provide
access to crnscript functionality.

crnscript checkout in eclipse (this will vary by eclipse version):

1. Ensure pydev is installed as an Eclipse plugin:
	Help/Install New Software
	In "Work with" put http://pydev.org/updates
	Check "PyDev"
	Click "Finish"
	Allow Eclipse to restart.

2. Check out the project (https://conman/svn-repos/CRN/crnscript/tags/crnscript-1.02) as a Java project.

3. Right-click project, click Pydev/Set as pydev project (It needs both the Java and PyDev natures, 
	which is why we didn't just check it out as a PyDev project).

4. Under project/properties:

	A. Under Java Build Path:
		Under "Libraries", click "Add JARs." Add all the top-level
			jars in lib.
		Under "Source", click "Add Folder" and make sure both resources and src are checked

	B. Under PyDev - Interpreter/Grammar:
		Change project type from python to jython.
		Click link to configure an interpreter. Click "new". Set 
			interpreter name to "crn-jython". Browse for
			executable and select lib/jython.jar. Click OK
			in the "selection needed" dialog box, and OK in the
			preferences window.
		Change Interpreter from default to crn-jython.
	
	C. Under PyDev - PYTHONPATH:
		Under "source folders," click "add source folder." Add src and resources.
		Under "External libraries":
			Click "add zip/jar/egg." Add each of the top-level files
				in lib.
			Click "add source folder." Add bin.

5. To verify that the project is running, run src/HelloWorld.py; it should produce a list of CRN stations.

Note that all your python scripts should start with 'from crn import *'.

