# -*- coding: utf-8 -*-
"""
 		clos_funcs.py

 		Created: 			       2016
		Last up: 	 		 4 Sep 2018
"""
from __future__ import print_function
import datetime



# ----------------------------------------------------------- Set Proof ---------------------------
def get_gen_totals(self):
	"""
	Abstract, General purpose.
	Gives service to other methods.
	Provider of services.
	"""
	print()
	print('Get Generic Totals')


	# Get Orders
	orders, count = get_orders(self, self.date, self.x_type)


	# Init
	total = 0
	for order in orders:
		total = total + order.amount_untaxed
	gen_tot = total

	if count != 0:
		serial_nr_first = orders[0].x_serial_nr
		serial_nr_last = orders[-1].x_serial_nr
	else:
		serial_nr_first = ''
		serial_nr_last = ''

	return gen_tot, serial_nr_first, serial_nr_last



# ----------------------------------------------------------- Set Proof ---------------------------

def set_proof_totals(self):
	"""
	Object oriented. 
	User of services.
	"""
	print()
	print('Set By Proof')


	# Receipt
	self.x_type = 'receipt'
	self.rec_tot, self.serial_nr_first_rec, self.serial_nr_last_rec = get_gen_totals(self)

	# Invoice
	self.x_type = 'invoice'
	self.inv_tot, self.serial_nr_first_inv, self.serial_nr_last_inv = get_gen_totals(self)

	# Ticket Receipt
	self.x_type = 'ticket_receipt'
	self.tkr_tot, self.serial_nr_first_tkr, self.serial_nr_last_tkr = get_gen_totals(self)

	# Ticket Invoices
	self.x_type = 'ticket_invoice'
	self.tki_tot, self.serial_nr_first_tki, self.serial_nr_last_tki = get_gen_totals(self)

	# Advertisement
	self.x_type = 'advertisement'
	self.adv_tot, self.serial_nr_first_adv, self.serial_nr_last_adv = get_gen_totals(self)

	# Sale Notes
	self.x_type = 'sale_note'
	self.san_tot, self.serial_nr_first_san, self.serial_nr_last_san = get_gen_totals(self)




	# Credit Notes

	# Get Orders
	state = 'credit_note'
	orders, count = get_orders_state(self, self.date, state)

	# Init
	total = 0
	for order in orders:
		total = total + order.amount_untaxed

	self.crn_tot = total

	if count != 0:
		self.serial_nr_first_crn = orders[0].x_serial_nr
		self.serial_nr_last_crn = orders[-1].x_serial_nr




	# Totals Proof
	#self.total_proof = self.rec_tot + self.inv_tot + self.tkr_tot + self.tki_tot + self.adv_tot + self.san_tot
	self.total_proof = self.rec_tot + self.inv_tot + self.tkr_tot + self.tki_tot + self.adv_tot + self.san_tot - self.crn_tot

	self.total_proof_wblack = self.rec_tot + self.inv_tot + self.tkr_tot + self.tki_tot 	#+ self.adv_tot + self.san_tot

# set_proof_totals




# ----------------------------------------------------------- Get Orders --------------------------

def get_orders_state(self, date, state):
	"""
	Abstract, General purpose.
	Provider of services.
	"""
	print()
	print('Get Orders State')


	# Init
	count = 0
	DATETIME_FORMAT = "%Y-%m-%d"
	date_begin = date + ' 05:00:00'
	date_end_dt = datetime.datetime.strptime(date, DATETIME_FORMAT) + datetime.timedelta(hours=24) + datetime.timedelta(hours=5, minutes=0)
	date_end = date_end_dt.strftime('%Y-%m-%d %H:%M')


	# Search
	orders = self.env['sale.order'].search([
												('state', '=', state),
												('date_order', '>=', date_begin),
												('date_order', '<', date_end),
										])
	count = self.env['sale.order'].search_count([
												('state', '=', state),
												('date_order', '>=', date_begin),
												('date_order', '<', date_end),
										])
	return orders, count

# get_orders_state




# ----------------------------------------------------------- Set Form ----------------------------

def set_form_totals(self):
	"""
	Object oriented. 
	User of services.
	"""
	print()
	print('Set By Form')

	# Get Orders
	x_type = 'all'
	orders, count = get_orders(self, self.date, x_type)

	# Init
	cash_tot = 0
	ame_tot = 0
	din_tot = 0
	mac_tot = 0
	mad_tot = 0
	vic_tot = 0
	vid_tot = 0

	# Loop
	for order in orders:

		for pm_line in order.x_payment_method.pm_line_ids:

			if pm_line.method == 'cash':
				cash_tot = cash_tot + pm_line.subtotal

			elif pm_line.method == 'american_express':
				ame_tot = ame_tot + pm_line.subtotal

			elif pm_line.method == 'diners':
				din_tot = din_tot + pm_line.subtotal

			elif pm_line.method == 'credit_master':
				mac_tot = mac_tot + pm_line.subtotal

			elif pm_line.method == 'debit_master':
				mad_tot = mad_tot + pm_line.subtotal

			elif pm_line.method == 'credit_visa':
				vic_tot = vic_tot + pm_line.subtotal

			elif pm_line.method == 'debit_visa':
				vid_tot = vid_tot + pm_line.subtotal


	# Form
	#self.cash_tot = cash_tot
	self.cash_tot = cash_tot - self.crn_tot
	self.ame_tot = ame_tot
	self.din_tot = din_tot
	self.mac_tot = mac_tot
	self.mad_tot = mad_tot
	self.vic_tot = vic_tot
	self.vid_tot = vid_tot

# set_form_totals



# ----------------------------------------------------------- Set Totals ---------------------------

def set_totals(self):
	"""
	Object oriented. 
	User of services.
	"""
	print()
	print('Set All')


	# Get Orders
	x_type = 'all'
	orders, count = get_orders(self, self.date, x_type)

	# Init
	amount_untaxed = 0
	count = 0

	# Loop
	for order in orders:
		amount_untaxed = amount_untaxed + order.amount_untaxed
		count = count + 1


	# Total
	#self.total = amount_untaxed
	self.total = amount_untaxed - self.crn_tot

# set_totals




# ----------------------------------------------------------- Get Orders --------------------------

def get_orders(self, date, x_type):
	"""
	Abstract, General purpose.
	Gives service to other methods.
	"""
	#print()
	#print('Get Orders')
	#print(date)
	#print(x_type)

	# Init
	count = 0
	DATETIME_FORMAT = "%Y-%m-%d"
	date_begin = date + ' 05:00:00'
	date_end_dt = datetime.datetime.strptime(date, DATETIME_FORMAT) + datetime.timedelta(hours=24) + datetime.timedelta(hours=5, minutes=0)
	date_end = date_end_dt.strftime('%Y-%m-%d %H:%M')


	# Search
	if x_type == 'all':
		orders = self.env['sale.order'].search([
													('state', '=', 'sale'),
													('date_order', '>=', date_begin),
													('date_order', '<', date_end),
											])
		count = self.env['sale.order'].search_count([
													('state', '=', 'sale'),
													('date_order', '>=', date_begin),
													('date_order', '<', date_end),
											])

	else:
		orders = self.env['sale.order'].search([
													('state', '=', 'sale'),
													('date_order', '>=', date_begin),
													('date_order', '<', date_end),
													('x_type', '=', x_type),
											],
												order='x_serial_nr asc',
												#limit=1,
											)
		count = self.env['sale.order'].search_count([
													('state', '=', 'sale'),
													('date_order', '>=', date_begin),
													('date_order', '<', date_end),
													('x_type', '=', x_type),
											],
												#order='x_serial_nr asc',
												#limit=1,
											)

	return orders, count

# get_orders
