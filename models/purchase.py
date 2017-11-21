# -*- coding: utf-8 -*-
#
#
# 		*** OPEN HEALTH - Purchase   
# 
# Created: 				30 Oct 2017
# Last updated: 	 	14 Nov 2017

from openerp import models, fields, api




class PurchaseOrder(models.Model):
	
	_inherit = 'purchase.order'
	_description = "Purchase Order"




# New




# ----------------------------------------------------------- Fields ------------------------------------------------------
	state = fields.Selection([


		('pre_draft', 'Por Validar'),



		
		#('draft', 'Draft PO'),
		('draft', 'Por Enviar'),
		


		#('validated', 'Validado'),		# Tmp



		('sent', 'RFQ Sent'),			# Tmp 
		#('sent', 'Enviado'),
		
		

		('to approve', 'To Approve'),
		


		#('purchase', 'Purchase Order'),
		('purchase', 'Orden de C/S'),
		

		#('done', 'Done'),
		('done', 'Completo'),
		

		#('cancel', 'Cancelled')
		('cancel', 'Cancelado')


		], string='Status', readonly=True, index=True, copy=False, 
		
		#default='draft', 
		default='pre_draft', 
		
		track_visibility='onchange')





	x_token= fields.Char(
			'Token', 

			#compute='_compute_x_token', 
		)

	@api.multi
	#@api.depends('')
	def _compute_x_token(self):
		for record in self:
			print 'jx'
			print 'Compute Token'
			print
			#record.x_token = 'jx'





# ----------------------------------------------------------- Actions ------------------------------------------------------


	# Clean
	@api.multi
	def clean_myself(self):  

		print 'jx'
		print 'Clean Myself'

		po_menu = self.env['ir.ui.menu'].search([('name', '=', 'Purchase Orders')])
		
		print po_menu
		po_menu.unlink()
		print po_menu
		print 		

		return {}







	# Validate 
	@api.multi
	def button_validate(self):

		#self.write({'state': 'validated'})
		self.write({'state': 'draft'})
		
		return {}



	# Removem
	@api.multi
	def remove_myself(self):  

		self.state = 'cancel'
		self.unlink()






# ----------------------------------------------------------- Classes ------------------------------------------------------

class MailComposeMessage(models.Model):
	_inherit = 'mail.compose.message'

	@api.multi
	def send_mail(self, auto_commit=False):
		if self._context.get('default_model') == 'purchase.order' and self._context.get('default_res_id'):
			order = self.env['purchase.order'].browse([self._context['default_res_id']])
			if order.state == 'draft':
				
				#order.state = 'sent'
				order.state = 'purchase'
		
		return super(MailComposeMessage, self.with_context(mail_post_autofollow=True)).send_mail(auto_commit=auto_commit)



