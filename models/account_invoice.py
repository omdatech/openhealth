# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AccountInvoice(models.Model):
	
	_inherit = 'account.invoice'

	_description = "Account Invoice"



# ----------------------------------------------------------- Constants ------------------------------------------------------

	vspace = fields.Char(
			' ', 
			readonly=True
		)





# ----------------------------------------------------------- Primitives ------------------------------------------------------


	# Vendor 
	#partner_id = fields.Many2one(
	#		'res.partner', 

			#string='Partner', 
	#		string='Proveedor', 
			
	#		change_default=True,
	#		required=True, 
	#		readonly=True, 
	#		states={'draft': [('readonly', False)]},
	#		track_visibility='always'
	#	)




	#x_delivery_order = fields.Char(
	#		string="Número de guia de remisión", 
	#	)


	#x_invoice_number = fields.Char(
	#		string="Número de factura", 
	#	)







# ----------------------------------------------------------- Actions ------------------------------------------------------

	# Removem
	#@api.multi
	#def remove_myself(self):  
	#	self.state = 'cancel'
	#	self.unlink()



