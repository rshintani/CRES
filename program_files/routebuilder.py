#!/Users/AsianCheddar/the_matrix/bin/python

# Here's what's currently in progress:
# 	Make the Tk() call happen in a function so it can return something
# 		or learn how to read class instances.


# This is the Menu script
from Tkinter import *
import ttk
import csv
from tabulate import tabulate
import urllib
import urllib2
from bs4 import BeautifulSoup 
from mapper import *
from collection import *
from mapper import *
import thread
import time
import subprocess
from cal_prompter import cal_prompt 
from cal_prompter import Calendar


class Route():
	"""docstring for FrontPage"""
	def __init__(self, options, locfile):
		self.locfile = locfile
		print "\n\nRoute() initialized...\n"
		self.options = options
		self.route = []
		# self.deets = Keeper(locfile)
		self.names = options[1]
		self.names.sort()
		self.master_list = options[1]
		self.client_fields = options[0].fields("Locations")

		self.link_diesel = 'http://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_r20_w.htm'
		self.link_ams = 'http://www.ams.usda.gov/mnreports/nw_ls442.txt'
		self.check = 1

	def build(self):
		# print self.names
		# print "\nOptions: This list is a placeholder for the locations list " ,  self.options
		# Need to make a menu, with a button and see how it returns from 
		# the loop when the window is closed... 



		def add_stop(*args):
			sel = lbox.curselection()
			# Make sure you're only adding one place to the list at once to establilsh clear order. 
			# print "Length of x" , len(sel)
			if len(sel) == 1:
				print "\n\nThis is SEL: ", sel
				# idx is the integer index of the selected location to add in the listbox loop. 
				idx = int(sel[0])

				# matchmaker searches for the first occurence of the STRING (in the listbox box) returned by idx above 
				# 	to be compared against the master_list in order to add the correct address, regardless of order in the listbox.
				# 	Hopefully that allows of self.names to be Sorted before it's displayed by alphabeticle order. 
				# matchmaker = [place for place in self.master_list].index(self.names[idx])
				print idx, self.master_list[idx]
				chop = self.master_list[idx]
				newthing = tuple( [int(len(self.route) ) , str(self.names[idx]) ]) + self.options[0].route_informer( str(chop) )
	        	self.route.append(  newthing    )

	        	# Add the selected restaurant to the routebox display. 
	        	routebox.insert(len(self.route) - 1, self.names[idx] )
	        	routebox.update()

	        	# Remove the selection from the choices listbox. 
	        	r = self.names.pop(idx)

	        	# Re.set() the StringVar()'s so the update() changes the display. 
	        	self.rnames.set(value = tuple(self.names))

	        	# lbox.delete(idx)
	        	lbox.update()

	        	# Make it so the rows' background alternates colors
	        	for i in range(0,len(self.route),2):
					routebox.itemconfigure(i, background='#f0f0ff')


		def remove_stop():
			# Essentially, this is the same as add route just in reverse. 
			y = routebox.curselection()
			if len(y) == 1: 
				rem = int(y[0])
				self.names.append( ( int( len(self.names) ), self.route[rem] ) )

				o = self.route.pop(rem)
				self.rnames.set(value = tuple(self.names))

				lbox.insert(len(self.names) , self.route[idx] )

	        	lbox.update()
			print "Going to remove " , 

		def exit():

			page.destroy()
			self.check = 0

		def	price_of_diesel():
			print "\nStart of price_of_diesel()\n"
			diesel= urllib2.urlopen(self.link_diesel)
			dsoup = BeautifulSoup(diesel)
			# links = soup.find_all( "Current2")
			# print "This is the price of Fuel today according to: ", self.link_diesel
			dsoup.prettify()
			data = dsoup.find_all('td' , 'Current2')
			length = len(data)
			# print data[13]
			temp = str(data[13])
			price = temp[32:36]
			diesel.close()
			print "End of price_of_diesel()\n"
			self.price_of_diesel = price
			return price

		def ams_lookup():
			response = urllib2.urlopen(self.link_ams)
			soup = BeautifulSoup(response)
			# Ruh-roh the ams gives us a .txt file to parse
			text = soup.get_text()
			# Start at the index where Choice white appears, go to EDIBLE LARD 
			self.yg_price = text[text.index('Choice white') :text.index('EDBLE LARD')]
			# Do the same thing for the report location
			ams_edit = text[text.index('Des') : text.index('2015') + 4 ].replace("     ", "\n Current as of ")
			self.ams_location = ams_edit
			print self.ams_location

		def add_row_gui(categories):
			page.destroy()
			print "This is the beginning of add_row_gui"

			adder = Tk()
			adder.title("Add Client")
			addframe = ttk.Frame(adder, padding = " 3 3 12 12 ")
			addframe.grid(column=0, row=0, sticky=(N, W, E, S))
			addframe.columnconfigure(0, weight=1)
			addframe.rowconfigure(0, weight=1)
			print categories
			sparks = StringVar(value = categories)
			gui_out = { x : StringVar() for y, x in enumerate(categories) }
		
			rw = 0
			for cat in categories:
				print rw, cat

				ttk.Label(addframe, text = cat).grid(row = rw, column = 0, sticky = W)
				ttk.Entry(addframe, textvariable = gui_out[cat]).grid(row = rw, column = 2)
				rw += 1
			ttk.Button(addframe, text = "CLOSE", command = adder.destroy).grid(row = rw, column = 2)
			adder.mainloop()
			
			for g in gui_out:
				print g, gui_out[g].get()

			self.new_row = { g : gui_out[g].get() for g in gui_out}
			
			chex = len(self.new_row['Name'])
			print "This is the end of add_row_gui()"
			print "The length of new client dict: ", chex
			if chex >= 1:
				self.add_check = 1

		def pickup_lister(*args):
			page.destroy()
			os.system('clear')
			# Use Numbers for now to open each pickup file. 
			for stpr in self.route:
				stringy = '/Users/AsianCheddar/GDrive/cres_sheets/' + stpr[1] + '.csv'
				# stringy = stringy.encode("utf-8")
				stringy = str(stringy)
				stringy = stringy.replace(" ", "\\ ")
				stringy = stringy.replace("'"  , "\\'" )
				# stringy = "open -a 'Numbers' " + stringy
				stringy = 'open -a "Numbers" ' + stringy
				# stringy = 'tabview ' + stringy
				os.system(stringy)	
				self.add_check = 2

		self.add_check = 0
		# Set up the initial window and grid
		page = Tk()
		page.title("Route Builder")
		mainframe = ttk.Frame(page, padding = " 3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)

		# Build selectable field populated by the names of restatants
		# restaurant_names = self.names

		self.rnames = StringVar()
		self.rnames.set(value = tuple(self.names))

		self.stops = StringVar()
		self.stops.set(value = tuple(self.route))


		# Create GUI elements here
		lbox = Listbox(
			mainframe, 
			listvariable = self.rnames, 
			height = 15
			)

		lbox.pack(side = LEFT, fill = BOTH )


		routebox = Listbox(mainframe, listvariable = self.stops, height = 10)
		routebox.pack()

		def new_client():
			# Need to parse the list of keys in the sql database
			to_show = [
				"Name" ,
				"Address",
				"City", 
				"Zip" ,
				"Phone Number",
				"Email", 
				"Contact", 
				"Charity" ,
				"Notes" ,
			]
			# fields = self.client_fields.intersection(to_show)
			add_row_gui( to_show )

		def add_charity():
			fields = [
				"Name" ,
				"Street",
				"City", 
				"Zip" ,
				"Phone Number",
				"Email", 
				"Contact", 
				"Notes" ,
				]
			add_row_gui(fields)
			self.add_check = 3


		add_but = ttk.Button(mainframe, text = "Add Stop", command = add_stop )
		quit = ttk.Button(mainframe, text = "Close Window" , command = exit)
		remove_but = ttk.Button(mainframe, text = 'Remove Stop', command = remove_stop)
		# details_but = ttk.Button(mainframe, text = 'Master List', command = self.options[0].show_master)
		new_place = ttk.Button(mainframe, text = "Add Client", command = new_client)
		pickups = ttk.Button(mainframe, text = "List Pickups", command = pickup_lister )
		add_charity_button = ttk.Button(mainframe, text = "Add Charity", command = add_charity)
		oil_on = ttk.Label(mainframe, text = self.options[2])


		# Set elements using .grid
		oil_on.grid(column = 8, row = 6)
		lbox.grid(column = 0, row = 0, rowspan = 6, sticky = (N,S,E,W) )
		add_but.grid(column = 2, row = 0)
		routebox.grid(column = 3, row = 0, rowspan = 6, sticky = (N,S,E,W) )
		quit.grid(column = 3, row = 8)
		# details_but.grid(column = 0, row = 8)
		new_place.grid(column = 2, row = 9)
		pickups.grid(column = 3, row = 9)
		add_charity_button.grid(column = 2, row = 8)

		# Set bindings
		lbox.bind('<Double-1>', add_stop)
		routebox.bind('<Double-1>', remove_stop)

		# Colorize alternating lines of the listbox
		for i in range(0,len(self.names),2):
			lbox.itemconfigure(i, background='#f0f0ff')
		
		# Start a thread for the window and another to get the fuel... 
	
		thread.start_new_thread( ams_lookup, () )
		thread.start_new_thread( price_of_diesel, () )
		
		print "Are we here yet?"
		page.mainloop()

		# self.route[0] =  cal_prompt() 

		print "************** ",self.route

		if self.add_check == 1:
			# Need to do some formatting on the dictionary values from string to float

			self.options[0].add_row( "Locations" , self.new_row)
			print "\n\nTHIS IS WHERER WE ARE\n"
			print "You added a new_row: ", self.new_row
			self.route = []
		# -------- FOR DEBUGGING --------

		# This is the end of the RouteBuilder mainframe loop. Whatever is placed here will be returned when the main window is closed
		elif self.add_check == 2:
			print "You looked at details, need to start over to rebuild the route. "
			self.route = []

		elif self.add_check == 0:
			if len(self.route) == 0:
				print "You have chosen to exit the program early, or at least without building a route."
			else:
				print "\nYour route.build() was a success!\n"
				print'\nThis is your route: ', self.route

		elif self.add_check == 3:
			print "You added a CHARITY"
			self.options[0].add_row( "Charities" , self.new_row)
			print "You added a new_row: ", self.new_row
			self.route = []

		# while self.check == 1:
		# 	print "hello work"

		# 	break

		return self.route


   
	def run_route(self):
		print "Start of run_route()"


		print "This is the beginning of .run_route()"
		print "Need to make this run in the background..."

		print "\nself.route:" , self.route
		self.link_diesel = 'http://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_r20_w.htm'
		self.link_ams = 'http://www.ams.usda.gov/mnreports/nw_ls442.txt'
		print "\nDiesel source:" , self.link_diesel
		print "AMS source:" , self.link_ams , '\n'

		pickup_date = cal_prompt()

		# Set up main Frame for the route display to be shown on. 
		disp = Tk()
		disp.title("Route Details")
		dframe = ttk.Frame(disp, padding = " 3 3 12 12")
		dframe.grid(column=0, row=0, sticky=(N, W, E, S))
		dframe.columnconfigure(0, weight=1)
		dframe.rowconfigure(0, weight=1)

		# Got the price in the new threads created with page.mainloop() in build(). 
		price = self.price_of_diesel
		print "Price of diesel: $" + str( price )

		# Make all the legs of the route from google maps
		route_starts = [ (q[2] + " " + q[3] + " " + str(q[4]) ) for q in self.route]
		route_starts.insert(0, ("2021 W. Fulton Chicago 60612") )
		route_stops = [ (p[2] + " " + p[3] + " " + str(p[4]) ) for p in self.route]
		route_stops.append( ("2021 W. Fulton Chicago 60612") ) 
		# legs = GoogleMap( [ list(addr[2:5]) for addr in self.route ])
		self.legs = zip(route_starts, route_stops)

		print '\nlegs: '
		for leg in self.legs:
			print leg

		# print legs.google_directions()

		# Set the second origin in dframe to use for collections inputs
		start_col = 0
		start_row = 10

		# Start building list of input dictionaries from GUI form. Add the results to collections.
		# First, the questions we need to ask at EVERY stop
		questions = [
					"Pickup Date",
					"Arrival",
					"Departure",
					"Quality",
					"Duration", 
					"Charity",
					"Notes", 
					"Diesel Price", 
					]
		
		# Now the list of dictionary tuples for the responses.
		#	THESE NAMES NEED TO MATCH WITH THE INPUTS DICTIONARY
		responses = []
		for leg in self.legs:
			print '\n\nleg: ', len(responses)
			print '\n************************\n', len(responses), leg, self.options[0].which_charity(leg[1][0:12])
			charity_name_only = self.options[0].which_charity(leg[1][0:8])
			responses.append({
					'Pickup Date' : StringVar(value = pickup_date),
					"Arrival" : StringVar(value = "1"),
					"Departure": StringVar(value = "1"),
					"Quality": IntVar(value = 90),
					"Duration": IntVar(value = 60),
					"Charity": StringVar(value = str(charity_name_only) ),
					"Notes": StringVar(),
					"Diesel Price": StringVar(value = price),
			})
		# responses = [ { questions[y] : IntVar() for y, x in enumerate(questions) } for leg in self.legs ]

		# Need to pop the last stop off the list because it's the ICNC.
		responses.pop()

		for stop , dest_pair in enumerate(self.route):
			# ttk.Label(dframe, text = "Some text").grid(column = start_col, row = start_row + stop)
			cols = start_col + 1 + stop
			ttk.Label(dframe, text =  dest_pair[1] + ":").grid( column =  cols , row = start_row )
			
			for question in questions:
				rws = start_row + 1 + questions.index(question)
				ttk.Label(dframe, text = question + ": ").grid(column = start_col , row = rws , sticky = 'e' )
				ttk.Entry(dframe, textvariable = responses[stop][question]).grid(column = start_col + stop + 1, row = rws)

		# Assign the entry variable for the AMS price we want to use for ALL of the stops on the route
		yellow_grease_ent = StringVar()
		yellow_grease_ent.set('21.5')

		# Assign names to the Labels and Buttons on the Frame
		ams_location_text = ttk.Label(dframe, text = self.ams_location)
		ams_price_text = ttk.Label(dframe, text = self.yg_price)
		dprice = ttk.Label(dframe, text = "The price of diesel today is $" + str(price))
		# route_list = ttk.Label(dframe, text = tabulate(self.route))
		directs = ttk.Button(dframe, text = "Get Directions", command = show_directions)
		yellow_grease_in = ttk.Label(dframe, text = "What is the AMS price today?")
		yellow_grease_set = ttk.Entry(dframe, textvariable = yellow_grease_ent)
		# map_label = ttk.Label(dframe, text = tabulate(legs.google_directions()) )

		# Set everything to the .grid()
		# route_list.grid 		(column = 1, row = 0)
		ams_location_text.grid	(column = 0, row = 1)
		ams_price_text.grid		(column = 1, row = 1)
		dprice.grid				(column = 1, row = 2)
		directs.grid			(column = 1, row = 3)
		yellow_grease_in.grid	(column = 1, row = 4)
		yellow_grease_set.grid	(column = 2, row = 4)
		
		# map_label.grid(column = 3, row = 3)
		# Start the mainloop() for the route you just made
		disp.mainloop()


		# print "THIS IS THE END! HERE's self.route, it should not have icnc at the ends. " 
		# print "\n\n"
		# for item in self.route:
		# 	print item
		# print "\n\n"

		
		# ------------------------------------------------------------------------
		# This is where I left off... Trying to mimic the inputs from the GUI thing I made. 
		# Need to make what this for loop makes into a dicitonary. 

		fart = 0
		for ind , dic in enumerate(responses):
			print "\n\nInputs for leg #" , fart
			fart += 1
			for d in questions:
				print d, responses[ind][d].get()
		
		print "\nCongragulations, you have run a route!\n\n"
		
		route_length = GoogleMap(self.legs).google_directions()


		# Need to build a dict like inputs from a GUI window.
		
		usr_inp = [{} for res in responses]
		count = 0

		for response in responses:
			print response.keys()
			for key in response.keys():
				print "***********\n\n", self.route[count], "\n\n*************"
				usr_inp[count][key] = response[key].get()
				# usr_inp[count]['Diesel Price'] = float( response[key].get() )
				usr_inp[count]["Total Distance"] = route_length
				usr_inp[count]['Number of Stops'] = len(self.route)
				usr_inp[count]["Service Fee"] = 0.15
				usr_inp[count]['Contact Person'] = self.route[count][7]
				usr_inp[count]['Contact Email'] = self.route[count][5]
				usr_inp[count]['Oil Price'] = float(yellow_grease_ent.get()) / float(100)
				usr_inp[count]['Location'] = self.route[count][1]

			count += 1
		
		print "\nEnd of run_route()"
		
		return usr_inp # This is legs in main_program
		# finp = {
		# 		"Location" : 'Robby',
		# 		"Height on Departure" : 35,
		# 		"Height on Arrival" : 51, 
		# 		"Oil Price" : 0.2434, 
		# 		"Service Fee" : 0.15,
		# 		"Quality" : 0.95, 
		# 		"Diesel Price" : price_of_diesel(),
		# 		"Total Distance" : route_length,
		# 		"Number of Stops" : len(self.route),
		# 		}

		# return finp

# -----------------------------------------------------------------


def the_end():
	pass

def show_directions():
	print "Make it so clicking this button pops a window up to display the route's directions. "

	

# -----------------------------------------------------------------

if __name__ == '__main__':
	# print "I'm running!"
	# locfile = os.path.expanduser( "~/GDrive/cres_sheets" )
	# keep = Keeper(locfile)
	# ops = [keep, keep.all_names(), keep.master_lister()]
	# route = Route(ops, locfile )
	# route.build()

	cal_prompt()


	





