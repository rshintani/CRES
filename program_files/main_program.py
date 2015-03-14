#!/usr/bin/python

# This is the MAIN PAGE for the CRES Program.

# Functionality should include:
# 	Building a pickup route
# 		Run the route
# 		Add Data to CSV files
# 		Send pickup notices/reciepts 
# 			prior to pickup?
# 			post collection results
# 	Browsing client/location details/statistics
# 		Provide to website?


# Cheating...
mods = 1
while mods == 1:
	try:
		from tabulate import tabulate #makes the nice tables
		import os.path #pathfinder
		import time #this is for any delays I want
		import sys
		import os
		from os import listdir
		import csv
		import urllib
		import urllib2
		from bs4 import BeautifulSoup           # pip install BeautifulS
		from datetime import date


	except ImportError as err:
		print "Something didn't work right.\n"
		print "You don't have all the required modules on this computer."
		print  err.args

	mods = 0


# These Classes are imported from CRES folder, whereever it may be. 
from aaa import *
from collection import *

# First let's check which system is running.
	# Need to find a way to get the GDrive file on the the Linux side of things. That's going to be hard

# -----------------------------------------------------------------

if sys.platform.startswith('darwin'):
	print ""
	print "This is not a Linux, it's a Mac so you're going to get lost on the keyboard."
	print "It would be cool if you could actually specify if it's Robby or Mike too\n"

	locfile = os.path.expanduser( "~/GDrive/cres_sheets" )  #mac
	print "Locfile: ", locfile, '\n'
	sheets = [ f for f in listdir(locfile)   ]
	sheets.remove('.DS_Store') # Not sure what this is but we don't want it.

elif sys.platform.startswith('linux'):
	print ""
	print 'This is a Linux\n' 
	locfile = os.path.expanduser( '~/cres_sheets2')
	print "Locfile: ", locfile, '\n'
	sheets = [ f for f in listdir(locfile)   ]


# -----------------------------------------------------------------


options = ["this", 'That', 'Other thing']

route_map = RouteBuilder(options)

# locs_list = Locations()

# locs_list.list_locations()
# print men


# Essentially I need to make it so that instead of just inputs and route being entered, it's going to be
# 	multiple input dictionaries and the same route being interpreted at one go. 


# inputs needs to be built by the GUI menu. 

inputs = {
	"Location" : 'Robby',
	"Height on Departure" : 35,
	"Height on Arrival" : 51, 
	"Oil Price" : 0.2434, 
	"Service Fee" : 0.15,
	"Quality" : 0.95, 
	"Diesel Price" : 2.75,
}

route = { 
			"Total Distance" : 30,
			"Number of Stops" : 3,
		}


collect = Collection(inputs, route)








print "\n\n\n\nThis is the end of Main Program"



