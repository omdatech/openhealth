# -*- coding: utf-8 -*-

from openerp import models, fields, api
import datetime

# account_contasis

_h_type = {
				'invoice':			'01', 
				'receipt': 			'03', 
				'ticket_receipt': 	'12', 
				'ticket_invoice': 	'12', 

				'advertisement': 	'14', 
				'sale_note': 		'15', 
				
				False: 			False, 
	}



_doc_type = {
				'other':			'0', 
				'foreign_card':		'4', 
				'passport':			'7', 

				'ptp':				'1', 		# Verify 
				'dni':				'2', 		# Verify 

				False: 			False, 
}



# account_line 
_cuentab = {
				'service':			'704110001', 
				'product': 			'701101001', 
				'consu': 			'701101001', 
		}


# ----------------------------------------------------------- Get Orders Filter ------------------------------------------------------

# Provides sales between begin date and end date. 
# Sales and Cancelled also. 
@api.multi
def get_orders_filter(self, date_bx, date_ex):

	#print
	#print 'Get Orders Two'

	# Dates	
	#DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
	DATETIME_FORMAT = "%Y-%m-%d"
	date_begin = date_bx + ' 05:00:00'
	date_end_dt  = datetime.datetime.strptime(date_ex, DATETIME_FORMAT) + datetime.timedelta(hours=24) + datetime.timedelta(hours=5,minutes=0)
	date_end = date_end_dt.strftime('%Y-%m-%d %H:%M')
	#print date_end_dt


	# Search Orders 
	orders = self.env['sale.order'].search([
													('state', 'in', ['sale','cancel']),
													('date_order', '>=', date_begin),													
													('date_order', '<', date_end),
											],
												order='x_serial_nr asc',
												#limit=1,
											)

	# Count 
	count = self.env['sale.order'].search_count([
													('state', 'in', ['sale','cancel']),
													('date_order', '>=', date_begin),
													('date_order', '<', date_end),
											],
												#order='x_serial_nr asc',
												#limit=1,
											)
	#count = 0 
	return orders, count
# get_orders_filter



# ----------------------------------------------------------- Get Net and Tax ------------------------------------------------------

# Get Net and Tax 
@api.multi
def get_net_tax(self, amount):
	# Net 
	x = amount / 1.18
	net = float("{0:.2f}".format(x))
	# Tax 
	x = amount * 0.18
	tax = float("{0:.2f}".format(x))
	return net, tax 
# get_net_tax



#------------------------------------------------ Correct Time ---------------------------------------------------

# Used by Account Line 

# Correct Time 
# Format: 	1876-10-10 00:00:00
def correct_time(self, date, delta):
	#print
	#print 'Correct'
	#print date 
	# Print delta 
	if date != False: 

		year = int(date.split('-')[0])

		if year >= 1900:

			DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
			DATETIME_FORMAT_sp = "%d/%m/%Y %H:%M"

			date_field1 = datetime.datetime.strptime(date, DATETIME_FORMAT)

			date_corr = date_field1 + datetime.timedelta(hours=delta,minutes=0)
			date_corr_sp = date_corr.strftime(DATETIME_FORMAT_sp)

			return date_corr, date_corr_sp
# correct_time

