#!/usr/bin/python

# This should make a class to run pickups at each location.... Should. 

# Cheating...

from tabulate import tabulate #makes the nice tables
import os.path #pathfinder
import time #this is for any delays I want
import sys
import os
from os import listdir
import csv
import urllib
import urllib2
from bs4 import BeautifulSoup		# pip install BeautifulSoup4




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


class Menu():
	def __init__(self, prefix , choices, suffix, default,  *args):

		print "\nMenu usage: Name(string, list, string, int)"
		# Here's all the attributes the menu is going to have upon initialization. Can add more later
		self.prefix = prefix
		self.choices = choices # May have to do some [choice.decode('utf-8') for choice in choices]
		self.suffix = suffix
		self.default = default

	def display(self):
		os.system('clear')
		print '\n' , '	', self.prefix , '\n'
		trunk_list = [ ( '		' + str(index ) , choice ) for index, choice in enumerate(self.choices) ]
		print tabulate( trunk_list , tablefmt ='plain')  
		print '\n' , '			', self.suffix ,'\n' , '						[BLANK] --> ' , self.default

		# Got the table to display ok but now I need to get the rawinput to return the same things as in v2.py
		# Should be in the format of:  
		#								response = [ int(selection), word] 
		# 	This should be ok now. 

		selection = raw_input()
		# while selection not in trunk... ? I don't think I need this bc it should loop outside this fcn
			
		if selection == '':
			selection = self.default

		else:
			selection = selection 
			# Not sure I neeeeeeed this, but something tells me it's a good idera to keep it here for the time being. 
			# Can figure it out later, eh?
			# Need to figure out how to get word and 

		try: 
			word = self.choices[ int(selection) ]
		except IndexError:
			print "You picked something not on the list"
			word = 'Try harder'
		# print 'Good work, you picked: ' , selection
		# print 'Hopefully your choice was: ' , word
		response = [ int (selection) , word ]

		print "\nResponse: " , response 
		return response

	def return_to_main(self):
		return 0


# -----------------------------------------------------------------

def make_locations(locfile):

	# Here is the list that controls the headers on the pickup_files
	pickup_heads = []

	# Open the master file and get the nicknames. The Nicknames will become the individual
	# filenames for the pickup files. 

	apple = open(locfile + '/master.csv')
	oranges = csv.DictReader(apple, dialect = 'excel', skipinitialspace = True)

	nicknames = [x['Name'] for x in oranges]
	print "Files exist for: " 
	for nick in nicknames:
		pickup_file = locfile + '/' + nick + '.csv'
		if os.path.exists(pickup_file):
			print  '		', nick 
			

		else:
			print "There is no '" ,  pickup_file   , "' we should make one!\n" 
			to_make = open( pickup_file, 'a' )
			writer = csv.DictWriter( to_make , fieldnames = pickup_heads)
			writer.writeheader()
			to_make.close() 
	return nicknames
	apple.close()

# -----------------------------------------------------------------


class Collection():
	def __init__(self):
		print "this can be use as a function?"
		self.link_diesel = 'http://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_r20_w.htm'
		self.link_ams = 'http://www.ams.usda.gov/mnreports/nw_ls442.txt'

		
		# Need to get work on this parser.  

		print ""
		print "Price_lookup():" # Input gallons or inches?
		print ""
		response = urllib2.urlopen(self.link_ams)
		# response = urllib2.urlopen('http://www.ams.usda.gov/mnreports/nw_ls442.txt')
		soup = BeautifulSoup(response)
		# page = response.readline()
		text = soup.get_text()
		print text[301:475]
		print ""
		# soup.prettify(formatter= 'html')
		# total = pounds * price
		# return total
		print "What is the AMS price you would like to use for this collection?"
		self.ams = float( raw_input('\n ') ) / 100.0
		response.close()




# Should add the ability to build the route just before making inputs Below
# that way you'll have the distance for the fuel calculation. Once you make the list 
# you should be able to iterate through the list to make inputs




	def main_prompt(self):
		a = "Where are you collecting oil from?"
		b = "Thank you!"
		# locations = [sheet.replace('.csv' , '') for sheet in sheets]
		location_menu = Menu(a, name_list, b, 0) #locations was here before name_list
		collect_from = location_menu.display()

		# collect_from returns [ 0, word ] from the main menu prompt.
		# Take that and make it into the runpickup from v2.py

		print "This is where you have choosen to collect oil: " , collect_from[1] , '\n'
		
		# Need to set up the inputs dict. 

		height_on_arrival = int()
		height_on_departure = int()
		pickup_duration = int()


		inputs = {}
		inputs['Location'] = collect_from[1]
		inputs['Arrival Height'] = height_on_arrival
		inputs['Departure Height'] = height_on_departure
		inputs['Duration'] = pickup_duration
		inputs['AMS Price'] = self.ams

		# Try to make this input section a little more robust so you can move 
		#forwards and back while entering information. First try a bunch of nestled while loops. 
		stage = 1 # stage 0 should be quit!  
		
		while stage != 0:
			if stage == 1:
				print 'What was the height of the oil when you got there?'
				height_on_arrival = raw_input('\n ')
				if height_on_arrival != 'b':
					stage += 1 # move to the next 
				else:
					stage = 0
					print "This should send you back to the main menu."
					

			if stage == 2:
				print "\nWhat was the height of the oil when you left?"
				height_on_departure = raw_input('\n ')
				if height_on_departure != 'b':
					stage += 1
				else:
					stage = 1 

			if stage == 3:
					# Got the menu to at least loop, need to make it go through all the way then interate back. 
				print "\nHow long did the pickup take?"
				pickup_duration = raw_input('\n ')
				if pickup_duration != 'b':
					stage += 1
				else: 
					stage = 2

			if stage == 4:
				print "\nWhat is the price of oil today?"
				break
			
				

			print "this is the end of the pickup, you should have been spit back to the main menu"
			



		print inputs


		return inputs

	def conversions(self):
		pass

		# This should be on top so it can be called later. 


	def arrival(self):
		print "This is the on arrival def"
		print self.link_diesel
		# Need to get Location, initial height, condition of bin(?), record/input time, 
		# Do math 


	def weather(self):
		print "This def should get the local weather conditions"
		# Would be a nice spot for some geocoding, CDMA hackathonage. 
















# ----------------------------------------------------------------------------

	# This is the beginning of the actual "program" I think the menu
	# function is working ok. Time to move on to adding the other options



pre = 'This is the Main Menu, by all means choose an option:'
post = 'Thanks, jackass... '
main_choices = ['EXIT PROGRAM', 'Run Pickup', 'choice 2', "yadda y'adda yadda"]

# Load the Menu to a variable, 
main_menu = Menu(pre, main_choices, post, 1)




# Start the main loop. 
to_loop = 1
while to_loop != 0:
	# This is the main list of locations, got it from master.csv
	name_list = make_locations(locfile)
	# First prompt of Main Menu
	menu_choice = main_menu.display()
	print menu_choice

	# Below are all the programs associated with the choices in main_menu

	# First, let's let ourselves out of the loop. 
	if menu_choice[0] == main_choices.index('EXIT PROGRAM'): 
		break










# Here is where I'm working on the plane. 

	elif menu_choice[0] == main_choices.index('Run Pickup'):
		print "Run a pickup"

		# Define a Collection variable to get the ball rolling
		collect = Collection()
		pickup = collect.main_prompt()
		print '\nYou chose to run a pickup, here are the results: ' , pickup
















	elif menu_choice[0] == main_choices.index('choice 2'):
		print "That worked I think"

	else:
		os.system('clear')
		print "\n" * 7
		print "Nigga, '" , menu_choice[0] , "' wasn't a choice! Go fish! \n(Or that choice is not functiong just yet)"
		time.sleep(2)







	# This will end the main while loop
	# to_loop = main_menu.exit()

