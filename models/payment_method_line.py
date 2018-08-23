# -*- coding: utf-8 -*-
#
# 	payment method line
# 
# 	Created: 				2016
# 	Last mod: 				21 Aug 2018
#
from openerp import models, fields, api

from . import pm_vars

class payment_method_line(models.Model):
	
	_name = 'openhealth.payment_method_line'

	_order = 'date_time asc'



# ----------------------------------------------------------- Relational ------------------------------------------------------

	# Payment Method
	payment_method = fields.Many2one(
			'openhealth.payment_method',
			ondelete='cascade', 
			required=False, 			
		)


	# Account - Contabilidad  
	account_id = fields.Many2one(
			'openhealth.account.contasis',
			ondelete='cascade', 
		)




# ----------------------------------------------------------- Meta ------------------------------------------------------

	# Document 
	document = fields.Char(
			string="Documento", 
		)

	document_type = fields.Char(
			string="Tipo Doc", 
		)


	# Other 
	patient = fields.Many2one(
			'oeh.medical.patient', 
			string="Nombre", 
		)

	serial_nr = fields.Char(
			string="Nr. de serie", 
		)

	x_type = fields.Selection(
			[	('receipt', 			'Boleta'),
				('invoice', 			'Factura'),
				('advertisement', 		'Canje Publicidad'),
				('sale_note', 			'Canje NV'),
				('ticket_receipt', 		'Ticket Boleta'),
				('ticket_invoice', 		'Ticket Factura'),	], 
			string='Tipo', 
		)

	date_time = fields.Datetime(
			string="Fecha", 
		)


# ----------------------------------------------------------- Primitives ------------------------------------------------------

	# Name 
	name = fields.Char( 
			string="#", 
			required=True, 
		)

	# Method
	method = fields.Selection(
			selection = pm_vars._payment_method_list,
			string="Forma de Pago", 
			default="cash", 
			required=True, 
		)

	# Subtotal 
	subtotal = fields.Float(
			string = 'Subtotal', 
			#default=self.balance, 
			required=True, 
		)

	# Currency 
	currency = fields.Char(
			string="Moneda", 
			default="S/.", 
		)

	# Vspace 
	vspace = fields.Char(
			' ', 
			readonly=True
			)
