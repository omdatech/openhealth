# -*- coding: utf-8 -*-
"""
 	Test - Order
	Explore treatment
	Renamed - To avoid conflict with nose2. 

	Created: 			20 Nov 2018
	Last up: 	 		23 oct 2020
"""
from __future__ import print_function


# ----------------------------------------------------------- Test ---------------------------------
def test(self):
	"""
	high level support for doing this and that.
	"""
	print('')
	print('Test')
	self.test_actions()
	self.test_computes()



# ----------------------------------------------------------- Pay ---------------------------------
def pay_myself(self):
	"""
	high level support for doing this and that.
	"""
	#print
	#print 'Pay myself'

	if self.state == 'draft':
		self.create_payment_method()
		self.x_payment_method.saledoc = 'ticket_receipt'
		self.x_payment_method.state = 'done'
		self.state = 'sent'

		#self.validate()
		#self.action_confirm_nex()
		self.validate_and_confirm()

