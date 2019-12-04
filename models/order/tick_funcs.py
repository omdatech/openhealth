# -*- coding: utf-8 -*-
"""
	Ticket Funcs
	Encapsulate Ticket Business Rules

	Created: 			29 Aug 2019
	Last up: 	 		 4 Dec 2019
"""
import datetime
import math
try:
	from num2words import num2words
except (ImportError, IOError) as err:
	_logger.debug(err)





# ----------------------------------------------------------- Getters -------------------------
def get_date_corrected(self):
	#print()
	#print('Tic Funcs - Get date corrected')

	date_corrected = compute_date_corrected(self)
	
	print(date_corrected)
	return date_corrected 


def compute_date_corrected(self):
	#print()
	#print('Tic funds - Compute date corrected')

	DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

	date_field1 = datetime.datetime.strptime(self.date_order, DATETIME_FORMAT)

	date_field2 = date_field1 + datetime.timedelta(hours=-5, minutes=0)
	
	DATETIME_FORMAT_2 = "%d-%m-%Y %H:%M:%S"

	date_corrected = date_field2.strftime(DATETIME_FORMAT_2)

	return date_corrected



# ----------------------------------------------------------- Getters -------------------------
def get_total(self):
	#print()
	#print('Get Total')
	return self.amount_total


def get_net(self):
	#print()
	#print('Get Net')
	net = compute_net(self)
	print(net)
	return net 


def get_tax(self):
	#print()
	#print('Get Tax')
	tax = compute_tax(self)
	print(tax)
	return tax 


def get_words(self):
	#print()
	#print('Get Words')
	words = compute_words(self)
	print(words)
	return words 


def get_cents(self):
	#print()
	#print('Get Words')
	cents = compute_cents(self)
	print(cents)
	return cents 


# ----------------------------------------------------------- Funcs -------------------------

def compute_net(self):
	#print()
	#print('Compute Net')
	x = self.amount_total / 1.18
	net = float("{0:.2f}".format(x))
	return net


def compute_tax(self):
	#print()
	#print('Compute Tax')
	x = self.x_total_net * 0.18
	tax = float("{0:.2f}".format(x))
	return tax


def compute_words(self):
	#print()
	#print('Compute Words')
	words = num2words(self.amount_total, lang='es')
	if 'punto' in words:
		words = words.split('punto')[0]
	total_words = words.title()
	return total_words


def compute_cents(self):
	#print()
	#print('Compute Cents')
	frac, whole = math.modf(self.amount_total)
	total_cents = frac * 100
	return total_cents


