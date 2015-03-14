# Just take the inputs and do conversions

# Variables we need:
# 	location
# 	height on arrivial
# 	height on departure
# 	price of oil
# 	route
# 	pickup 
# 		duration
# 		date 
# 		quality
# 		score
# 		fuel surcharge
# 			route / stops


# input should look like: 
	
# 		[ location ]

class Collection():
	"""docstring for Collection"""
	
	def __init__(self, inputs, route):
		# Bring in the input dictionary and store it to self for later reference
		
		self.route = route
		inputs

		# Given: 
		h = 36
		w = 28
		l = 48

		t_vol = 0.0043290 * l * w * h

		inputs['Gallons on Arrival'] = round(0.0043290 * l * w * inputs['Height on Arrival'] , 2)
		inputs['Gallons on Departure'] = round(0.0043290 * l * w * inputs['Height on Departure'] , 2)
		inputs['Gallons Collected'] = round(inputs['Gallons on Arrival'] - inputs['Gallons on Departure'] , 2)
		score = inputs['Gallons on Departure'] / inputs['Gallons on Arrival'] 
		inputs['Pickup Score'] = round(score * 100 , 2)

		# 7.75 lbs per gallon is set here
		lbs_collected = inputs['Gallons Collected'] * 7.75 * inputs['Quality']

		inputs['Expected Revenue'] = round(inputs['Oil Price'] * lbs_collected , 2)

		donation = inputs['Oil Price'] - inputs['Service Fee'] 

		inputs['Donation Rate'] = round(donation , 2) 
		inputs['Expected Income'] = inputs['Service Fee'] * lbs_collected
		inputs['Expected Donation'] = donation * lbs_collected

		# inputs['Diesel Price'] = 

		# income * weight

		# inputs['Expected Donation'] = 
		

		self.indict = inputs



		def route_analizer():

			# Takes the self.route which should be in the form:
			# 	{ 
			# 		"Total Distance" : 3,
			# 		"Number of Stops" : 3,
			# 	}
			# And returns the fuel charge for the collection being initiated.

			tdist = self.route['Total Distance']
			num_stops = self.route['Number of Stops']
			diesel_price = self.indict['Diesel Price']
			mpg_truck = 13.5

			fuel_surcharge = tdist / mpg_truck * diesel_price / num_stops

			return fuel_surcharge


		f_surcharge = route_analizer()

		print "\n\n\n\nRoute: " , f_surcharge 

		self.indict['Fuel Surcharge'] = f_surcharge

		self.indict['Miles in Route'] = route['Total Distance']
		self.indict['Stops on Route'] = route['Number of Stops']

		print "\n\n\n"
		for key in self.indict:
			print key , ":" , self.indict[key]






print "This is on the outside"


		





# Output:
print "End of collection\n"