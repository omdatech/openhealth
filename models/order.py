# -*- coding: utf-8 -*-
"""
	Order

	Created: 			26 Aug 2016
	Last mod: 			 5 Nov 2018
"""
import math
import datetime
from num2words import num2words
from openerp import models, fields, api
from openerp import _
from openerp.exceptions import Warning
import ord_vars
import creates
import pat_vars
import user
import lib
import lib_qr
import chk_patient
import chk_order
import test_order
#import lib_con

class sale_order(models.Model):
	"""
	high level support for doing this and that.
	"""
	_inherit = 'sale.order'



# ----------------------------------------------------------- Checksum ----------------------------
	# Checksum 
	x_checksum = fields.Float(
			'Checksum', 
			readonly=True,

			default = 5,
		)


	# Checksum Func
	@api.multi 
	def checksum(self):
		#print
		#print 'Check Sum'

		self.check_payment_method()

		#self.x_checksum = self.amount_total - self.x_pm_total 

		#delta = self.amount_total - self.x_pm_total
		delta = int(self.amount_total) - int(self.x_pm_total)

		#print delta

		if delta != 0:
			self.x_checksum = 1
		else:
			self.x_checksum = 0




	# Pm Total 
	x_pm_total = fields.Float(
			'Total MP', 
			readonly=True, 
		)

	# Check payment method
	@api.multi 
	def check_payment_method(self):
		#print
		#print 'Check Payment Method'
		pm_total = 0 
		
		for pm in self.x_payment_method.pm_line_ids: 
			pm_total = pm_total + pm.subtotal
		
		self.x_pm_total = pm_total
		
		#if self.x_pm_total != self.amount_total:
		#	msg = 'Error: Verificar la Forma de Pago.'
		#	raise Warning(_(msg))





# ----------------------------------------------------------- Serial Nr ---------------------------

	# Serial Number 
	x_serial_nr = fields.Char(
			'Número de serie',
		)

	# Counter Value
	x_counter_value = fields.Integer(
			string="Contador",
		)


# ----------------------------------------------------------- Constraints - Sql -------------------
	# Uniqueness constraints for:
	# Serial Number
	_sql_constraints = [
				('x_serial_nr','unique(x_serial_nr)', 'SQL Warning: x_serial_nr must be unique !'),
			]





# ----------------------------------------------------------- Constraints - Python ----------------
	# Check Ruc
	@api.constrains('x_ruc')
	def _check_x_ruc(self):
		#print
		#print 'Check Ruc'
		if self.x_type in ['ticket_invoice', 'invoice']:
			chk_order.check_ruc(self)


	# Check Id doc - Documento Identidad 
	@api.constrains('x_id_doc')
	def _check_x_id_doc(self):
		#print
		#print 'Check Id Doc'
		#chk_patient.check_x_id_doc(self)
		if self.x_type in ['ticket_receipt', 'receipt']:
			#chk_order.check_id_doc(self)
			chk_patient.check_x_id_doc(self)


	# Check Serial Number
	#@api.constrains('x_serial_nr')
	#def _check_x_serial_nr(self):
	#	print
		#print 'Check Serial Nr'
		#chk_order._check_x_serial_nr(self)




# ---------------------------------------------- Electronic ------------------------------------

	x_title = fields.Char(
			'Titulo',
			default='Venta Electrónica',
		)

	x_electronic = fields.Boolean(
			'Electronic', 
			default=False,
		)

	x_qr_img = fields.Binary(
			'Código QR',
		)

	x_qr_data = fields.Char(
			'Data QR'
		)


	# Make QR
	@api.multi
	def make_qr(self):

		# Create Data
		self.x_qr_data = lib_qr.get_qr_data(self)

		# Create Img
		img_str, name = lib_qr.get_qr_img(self.x_qr_data)

		# Update
		self.write({
						'x_qr_img': img_str,
						'qr_product_name':name,
				})

	# make_qr




# ----------------------------------------------------------- Mode Admin --------------------------
	x_admin_mode = fields.Boolean(
			'Modo Admin',
		)






# ----------------------------------------------------------- Credit Note -------------------------

	x_credit_note_type = fields.Selection(
			[
				('cancel', 		'Anulación'),
				('discount', 	'Descuento'),
				('bonus', 		'Bonificación'),
				('return', 		'Devolución'),
				('other', 		'Otros'),
			],
			string='Motivo',
			default='cancel',
		)


	x_credit_note_owner = fields.Many2one(
			'sale.order',
			#'Propietario NC',
			'Documento que modifica',
		)

	x_credit_note = fields.Many2one(
			'sale.order',
			'Nota de Crédito',
		)


	def get_credit_note_type(self):
		#print
		#print 'Get Credit Note Type'

		_dic_cn = {
					'cancel':	'Anulación',
					'discount':	'Descuento',
					'bonus':	'Bonificación', 
					'return': 	'Devolución', 
					'other': 	'Otros',
		
		}

		return _dic_cn[self.x_credit_note_type]


# ----------------------------------------------------------- Electronic - Getters ----------------

	def get_patient_address(self):
		#print
		#print 'Get Patient Address'
		return self.partner_id.x_address



	def get_firm_address(self):
		#print
		#print 'Get Firm Address'
		#return self.partner_id.x_firm_address
		return self.partner_id.x_address




# ----------------------------------------------------------- Onchange - DNI ----------------------
	# Dni
	@api.onchange('x_partner_dni')
	def _onchange_x_partner_dni(self):
		#print
		#print 'On Change - DNI'

		if self.x_partner_dni != False:

			#print 'By Id Doc'

			# Search Patient - by ID IDOC
			patient = self.env['oeh.medical.patient'].search([
																('x_id_doc', '=', self.x_partner_dni),
												],
													order='write_date desc',
													limit=1,
												)
			#print patient.name



			if patient.name == False:

				#print 'By Dni'

				# Search Patient - by DNI
				patient = self.env['oeh.medical.patient'].search([
																	('x_dni', '=', self.x_partner_dni),
													],
														order='write_date desc',
														limit=1,
													)
				#print patient.name


			# Update
			self.patient = patient.id

	# _onchange_x_partner_dni




# ----------------------------------------------------------- Id Doc ------------------------------

	# Id Document
	x_id_doc = fields.Char(
			'Nr. Doc.',
			required=False,
		)


	# Id Document Type 
	x_id_doc_type = fields.Selection(
			selection = pat_vars._id_doc_type_list,
			string='Tipo de documento',
			required=False,
		)


	# Type Code 
	x_type_code = fields.Char(
			string='Tipo Codigo',

			compute='_compute_x_type_code',
		)

	@api.multi
	def _compute_x_type_code(self):
		for record in self:
			if record.x_type in ['ticket_receipt', 'ticket_invoice', 'receipt', 'invoice', 'advertisement', 'sale_note']:
				record.x_type_code = ord_vars._dic_type_code[record.x_type]



	# Type
	x_type = fields.Selection(
			[
				('receipt', 			'Boleta'),
				('invoice', 			'Factura'),
				('advertisement', 		'Canje Publicidad'),
				('sale_note', 			'Canje NV'),
				('ticket_receipt', 		'Ticket Boleta'),
				('ticket_invoice', 		'Ticket Factura'),
			],
			string='Tipo',
			required=False,
			states={
					'draft': [('readonly', True)],
					'sent': [('readonly', True)],
					'sale': [('readonly', True)],
				}, 
		)





# ----------------------------------------------------------- Correct -----------------------------
	# Correct payment method
	@api.multi
	def correct_pm(self):
		#print
		#print 'Correct Payment Method'

		#order_id = self.id


		if self.x_payment_method.name == False:
			#print 'Create'
			self.x_payment_method = self.env['openhealth.payment_method'].create({
																					'order': 	self.id,

																					'partner':	self.partner_id.id,
																					'total':	self.amount_total,
				})


		#print self.x_payment_method
		
		res_id = self.x_payment_method.id


		return {
			# Mandatory
			'type': 'ir.actions.act_window',
			'name': 'Open Payment Method Current',
			# Window action

			'res_id': res_id,

			'res_model': 'openhealth.payment_method',
			# Views
			"views": [[False, "form"]],
			'view_mode': 'form',
			'target': 'current',
			#'view_id': view_id,
			#"domain": [["patient", "=", self.patient.name]],
			#'auto_search': False, 
			'flags': {
						'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
						#'form': {'action_buttons': True, }
						#'form': {'action_buttons': False, }
					},
			'context': {
						#'default_order': order_id,
					}
		}
	# correct_pm




# ----------------------------------------------------------- Legacy ------------------------------
	# Legacy
	x_legacy = fields.Boolean(
			'Legacy',
		)



# ----------------------------------------------------------- Pay ---------------------------------
	# DNI
	x_dni = fields.Char(
			string='DNI',
			readonly=True,
		)

	# RUC
	x_ruc = fields.Char(
			string='RUC',
			#readonly=True,
		)



# ----------------------------------------------------------- Locked - By State -------------------
	
	# States
	READONLY_STATES = {
		'draft': 		[('readonly', False)],
		'sent': 		[('readonly', False)],
		'sale': 		[('readonly', True)],
		'cancel': 		[('readonly', True)],
	}


	# Patient 
	patient = fields.Many2one(
			'oeh.medical.patient',
			string='Paciente', 
			#default=lambda self: user._get_default_id(self, 'patient'),
			
			#states=READONLY_STATES, 
		)


	# Doctor 
	x_doctor = fields.Many2one(
			'oeh.medical.physician',
			string = "Médico",
			#default=lambda self: user._get_default_id(self, 'doctor'),
			states=READONLY_STATES, 
		)


	# Treatment 
	treatment = fields.Many2one(
			'openhealth.treatment',
			ondelete='cascade', 
			string="Tratamiento",
			states=READONLY_STATES, 
		)


	# Family 
	x_family = fields.Selection(
			string = "Familia", 	
			selection = [
							('product','Producto'), 
							('consultation','Consulta'), 
							('procedure','Procedimiento'), 
							('cosmetology','Cosmiatría'), 
			], 

			#required=False, 
			#states=READONLY_STATES, 
			#readonly=True, 
		)


	# Product
	x_product = fields.Char(		
			string="Producto",	

			#required=False, 			
			#states=READONLY_STATES, 
			#readonly=True, 
		)






	# Order Line 
	order_line = fields.One2many(
			'sale.order.line', 
			'order_id', 
			string='Order Lines', 
			#states=READONLY_STATES, 			# By XML 
		)



# ----------------------------------------------------------- On Changes --------------------------


	# Patient  
	@api.onchange('patient')
	def _onchange_patient(self):	
		#print
		#print 'On Change Patient'

		if self.patient.name != False: 

			# Init 
			self.x_ruc = False
			self.partner_id = self.patient.partner_id.id 


			#print self.patient.x_id_doc
			#print self.patient.x_id_doc_type


			# Id Doc 
			if self.patient.x_id_doc != False:
				self.x_id_doc = self.patient.x_id_doc
				self.x_id_doc_type = self.patient.x_id_doc_type


			# Get x Dni 
			elif self.patient.x_dni not in [False, '']:				
				self.x_id_doc = self.patient.x_dni
				self.x_id_doc_type = 'dni'
				self.x_dni = self.patient.x_dni

				# Update Patient - Dep 
				#self.x_msg = '1'
				#self.patient.x_id_doc = self.patient.x_dni
				#self.patient.x_id_doc_type = 'dni'


			# Ruc 				
			if self.patient.x_ruc != False:
				self.x_ruc = self.patient.x_ruc





	# Doctor 
	@api.onchange('x_doctor')
	def _onchange_x_doctor(self):
		if self.x_doctor.name != False: 
			treatment = self.env['openhealth.treatment'].search([															
																	('patient', '=', self.patient.name), 
																	('physician', '=', self.x_doctor.name), 
													],
														order='write_date desc',
														limit=1,
													)
			self.treatment = treatment




	# Partner  
	@api.onchange('partner_id')	
	def _onchange_partner_id(self):		
		if self.partner_id.name != False: 			
			self.x_partner_dni = self.partner_id.x_dni









# ----------------------------------------------------------- Check - Content ---------------------

	# Personal identifiers: Dni, Ruc 
	# Check for length and digits 

	# Check Content 
	@api.multi 
	def check_content(self):
		#print
		#print 'Check Content'

		#self.x_dni = self.partner_id.x_dni
		#self.x_ruc = self.partner_id.x_ruc

		#print self.patient.name 				# Generates an Error ! With Ñ
		#print 'Dni: ', self.x_dni
		#print 'Ruc: ', self.x_ruc 


		_length = {
					'dni': 8,
					'passport': 12,
					'foreign_card': 12,
					'ptp': 12,					# Verify !
		}


		# Dni - Generalize, to accept other docs (passport, foreign card, ptp)
		if self.x_type in ['ticket_receipt', 'receipt']: 

			#print 'Receipt'

			# Test 


			# Nr of characters
			if self.x_id_doc_type not in ['other']: 
				length = _length[self.x_id_doc_type]
				ret = lib.test_for_length(self, self.x_id_doc, length)
				if ret != 0:
					msg = "Error: Documento debe tener " + str(length) + " caracteres."
					raise Warning(_(msg))



			# Must be Number - Only for DNIs 
			if self.x_id_doc_type in ['dni']: 
				ret = lib.test_for_digits(self, self.x_id_doc)
				if ret != 0:
					#msg = "Error: DNI debe ser un Número."
					msg = "Error: Documento debe ser un Número."
					raise Warning(_(msg))
	


			# Update 
			self.partner_id.x_dni = self.x_dni



		# Ruc
		elif self.x_type in ['ticket_invoice', 'invoice']: 

			#print 'Invoice'
			#print self.x_ruc
			

			# Test 
			length = 11
			ret = lib.test_for_length(self, self.x_ruc, length)
			if ret != 0:
				msg = "Error: RUC debe tener " + str(length) + " caracteres."
				raise Warning(_(msg))

			ret = lib.test_for_digits(self, self.x_ruc)
			if ret != 0:
				msg = "Error: RUC debe ser un Número."
				raise Warning(_(msg))

			# Update 
			self.partner_id.x_ruc = self.x_ruc




# ----------------------------------------------------------- Validate ----------------------------

	# Action confirm 
	@api.multi 
	def validate(self):
		#print
		#print 'Validate'


		# Payment method validation
		self.check_payment_method()


		# Doctor User Name
		if self.x_doctor.name != False: 
			uid = self.x_doctor.x_user_name.id
			self.x_doctor_uid = uid


		# Date - Must be that of the Sale, not the Budget. 
		self.date_order = datetime.datetime.now()


		# Update Descriptors (family and product) 
		self.update_descriptors()


		# Change Appointment State - To Invoiced 
		self.update_appointment()


		# Vip Card - Detect and Create 
		self.detect_create_card()


		# Type 
		#print 'Type'
		if self.x_payment_method.saledoc != False: 
			self.x_type = self.x_payment_method.saledoc
		#print self.x_type



		# Create Procedure with Appointment 
		if self.treatment.name != False: 
			for line in self.order_line: 
				if line.product_id.x_family in ['laser', 'medical', 'cosmetology']:
					# Create 
					creates.create_procedure_wapp(self, line.product_id.x_treatment, line.product_id.id)
				line.update_recos()
			# Update 
			self.x_procedure_created = True
			self.treatment.update_appointments()





		# Check Content - DEP 
		#self.check_content()

		# Id Doc and Ruc
		#print self.x_type
		#print self.x_id_doc
		#print self.x_ruc

		# Invoice
		if self.x_type in ['ticket_invoice', 'invoice']:
			if self.x_ruc in [False, '']:
				msg = "Error: RUC Ausente."
				raise Warning(_(msg))

		# Receipt
		elif self.x_type in ['ticket_receipt', 'receipt']:
			if self.x_id_doc_type in [False, '']  or self.x_id_doc in [False, '']:
				msg = "Error: Documento de Identidad Ausente."
				raise Warning(_(msg))






		# Update Patient 
		if self.patient.x_id_doc in [False, '']: 
			self.patient.x_id_doc_type = self.x_id_doc_type
			self.patient.x_id_doc = self.x_id_doc



		# Change Electronic 
		self.x_electronic = True

		# Title
		if self.x_type in ['ticket_receipt', 'receipt']:
			self.x_title = 'Boleta de Venta Electrónica'
		elif self.x_type in ['ticket_invoice', 'invoice']:
			self.x_title = 'Factura de Venta Electrónica'
		else:
			self.x_title = 'Venta Electrónica'



		# Change State 
		self.state = 'validated'
	# validate



# ----------------------------------------------------------- Action Confirm ----------------------

	# Action confirm 
	@api.multi 
	def action_confirm_nex(self):
		#print
		#print 'Action confirm - Nex'

		
		#Write your logic here - Begin

		# Generate Serial Number		
		if self.x_serial_nr != '' and self.x_admin_mode == False: 


			# Prefix 
			#prefix = ord_vars._dic_prefix[self.x_type]

			# Padding 
			#padding = ord_vars._dic_padding[self.x_type]

			# Serial Nr
			#self.x_serial_nr = prefix + self.x_separator + str(self.x_counter_value).zfill(padding)



			# Counter 
			#self.x_counter_value = user.get_counter_value(self)
			self.x_counter_value = user.get_counter_value(self, self.x_type, self.state)

			# Serial Nr
			#self.x_serial_nr = user.get_serial_nr(self.x_type, self.x_counter_value)
			self.x_serial_nr = user.get_serial_nr(self.x_type, self.x_counter_value, self.state)




		#Write your logic here - End 


		# The actual procedure 
		res = super(sale_order, self).action_confirm()


		#Write your logic here



		# QR
		#if self.x_type in ['ticket_receipt']:
		if self.x_type in ['ticket_receipt', 'ticket_invoice']:
			self.make_qr()



	# action_confirm_nex




# ---------------------------------------------- Credit Note --------------------------------------
	# Duplicate
	@api.multi
	def create_credit_note(self):
		#print
		#print 'Create CN'


		# State
		state = 'credit_note'

		# Counter 
		counter_value = user.get_counter_value(self, self.x_type, state)

		# Serial Nr
		serial_nr = user.get_serial_nr(self.x_type, counter_value, state)




		# Duplicate with different fields
		credit_note = self.copy(default={
											'x_serial_nr': serial_nr,
											'x_counter_value': counter_value,
											'x_credit_note_owner': self.id,
											'amount_total': self.amount_total,
											'amount_untaxed': self.amount_untaxed,
											'x_title': 'Nota de Crédito Electrónica',
											'state': state,

											'x_payment_method': False, 
								})
		#print credit_note


		# Counter
		#credit_note.x_counter_value = user.get_counter_value(credit_note)
		#x_counter_value = user.get_counter_value(credit_note)
		#print x_counter_value


		# Update Self
		ret = self.write({
							'x_credit_note': credit_note.id,
						})







# ----------------------------------------------------------- Create Card -------------------------

	# Create Card Vip 
	@api.multi 
	def detect_create_card(self):


		# Detect if Card in Sale 
		sale_card = False 

		for line in self.order_line:
			if line.product_id.x_name_short == 'vip_card':
				sale_card = True




		# If Card in Sale  
		if sale_card:


			# Search Card in the Db
			card = self.env['openhealth.card'].search([ ('patient_name', '=', self.partner_id.name), ], order='date_created desc', limit=1)
			


			# If it does not exist - Create 
			if card.name == False: 
				card = self.env['openhealth.card'].create({
																'patient_name': self.partner_id.name,
															})




			# Update Partner - Vip Price List 
			pl = self.env['product.pricelist'].search([
																('name','=', 'VIP'),
															],
															#order='appointment_date desc',
															limit=1,)
			self.partner_id.property_product_pricelist = pl



	# detect_create_card









# ----------------------------------------------------------- Vars --------------------------------

	# Delta 
	x_delta = fields.Integer(
			'Delta',
		)



	# Date 
	#date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
	date_order = fields.Datetime(
		states={	
					'draft': [('readonly', False)], 
					'sent': [('readonly', False)], 
					'sale': [('readonly', True)], 

					#'editable': [('readonly', False)], 
				}, 
		
		index=True, 
	)


	# State 
	#state = fields.Selection([
	#	('draft', 'Quotation'),
	#	('sent', 'Quotation Sent'),
	#	('sale', 'Sale Order'),
	#	('done', 'Done'),
	#	('cancel', 'Cancelled'),
	#	], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
	state = fields.Selection(
			selection = ord_vars._state_list, 
			string='Estado',	
			readonly=False,
			default='draft',

			index=True,
		)






	# Pricelist 
	pricelist_id = fields.Many2one(
			'product.pricelist', 
			string='Pricelist', 
			readonly=True, 
			states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, 
			help="Pricelist for current sales order.", 

			required=True, 
		)


	
	# Payment Method 
	x_payment_method = fields.Many2one(
			'openhealth.payment_method',
			string="Pago", 

			states={	
					'draft': [('readonly', False)],
					'sent': [('readonly', False)],
					#'sale': [('readonly', True)],
					'sale': [('readonly', False)],
				}, 
		)





	x_doctor_uid = fields.Many2one(
			'res.users',
			string = "Médico Uid", 	
			readonly = True,
		)




	# Nr lines 
	nr_lines = fields.Integer(
			default=0,
			string='Nr líneas',
			required=False, 

			compute='_compute_nr_lines', 
			)

	@api.multi
	#@api.depends('order_line')
	def _compute_nr_lines(self):
		for record in self:			
			ctr = 0
			for l in record.order_line:
				ctr = ctr + 1
			record.nr_lines = ctr 
			
	

	# Partner Vip 
	x_partner_vip = fields.Boolean(
			'Vip', 
			default=False, 

			compute="_compute_partner_vip",
			)

	@api.multi
	def _compute_partner_vip(self):
		for record in self:
			count = self.env['openhealth.card'].search_count([
																('patient_name','=', record.partner_id.name),
														]) 
			if count == 0:
				record.x_partner_vip = False 
			else:	
				record.x_partner_vip = True 




# ----------------------------------------------------------- Primitives --------------------------
	# Cosmetology 
	cosmetology = fields.Many2one(
			'openhealth.cosmetology',
			ondelete='cascade', 			
			string="Cosmiatría", 
		)

	# Blank line
	vspace = fields.Char(
			' ', 
			readonly=True
		)


# ----------------------------------------------------- Product Selector --------------------------

	@api.multi
	def open_product_selector_product(self):  
		return self.open_product_selector('product')


	@api.multi
	def open_product_selector_service(self):
		return self.open_product_selector('service')


	# Buttons  - Agregar Producto Servicio
	@api.multi
	def open_product_selector(self, x_type):  

		# Init Vars 
		#context = self._context.copy()		
		order_id = self.id
		res_id = False

		# Search Model 
		res = self.env['openhealth.product.selector'].search([],
																#order='write_date desc',
																limit=1,
															)
		return {
				'type': 'ir.actions.act_window',
				'name': ' New Orderline Selector Current', 
				'view_type': 'form',
				'view_mode': 'form',	
				#'target': 'current',
				'target': 'new',
				'res_id': res_id,
				#'res_model': 'sale.order.line',	
				'res_model': 'openhealth.product.selector',	
				'flags': 	{
								#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
								#'form': {'action_buttons': False, }
								'form': {'action_buttons': False, 'options': {'mode': 'edit'}  }
							},
				'context': {
								'default_order_id': order_id ,
								'default_x_type': x_type ,
					}}
	# open_product_selector






# ----------------------------------------------------------- Print Tickets -----------------------

	# Total in Words
	x_total_in_words = fields.Char(
			"",
			compute='_compute_x_total_in_words', 
		)

	@api.multi
	#@api.depends('')
	def _compute_x_total_in_words(self):
		for record in self:
			words = num2words(record.amount_total, lang='es')
			if 'punto' in words:
				words = words.split('punto')[0]			
			record.x_total_in_words = words.title()



	# Total in cents 
	x_total_cents = fields.Integer(
			"Céntimos",
			compute='_compute_x_total_cents', 
		)

	@api.multi
	#@api.depends('')
	def _compute_x_total_cents(self):
		for record in self:
			frac, whole = math.modf(record.amount_total)			
			record.x_total_cents = frac * 100



	# Net
	x_total_net = fields.Float(
			"Neto",
			compute='_compute_x_total_net', 
		)

	@api.multi
	#@api.depends('')
	def _compute_x_total_net(self):
		for record in self:
			x = record.amount_total / 1.18
			g = float("{0:.2f}".format(x))
			record.x_total_net = g



	# Tax
	x_total_tax = fields.Float(
			"Impuesto",
			compute='_compute_x_total_tax', 
		)
	@api.multi
	#@api.depends('')
	def _compute_x_total_tax(self):
		for record in self:
			x = record.x_total_net * 0.18
			g = float("{0:.2f}".format(x))
			record.x_total_tax = g





	# My company 
	x_my_company = fields.Many2one(
			'res.partner',
			string = "Mi compañía", 	
			domain = [
						('company_type', '=', 'company'),
					],
			compute="_compute_x_my_company",
		)


	@api.multi
	#@api.depends('partner_id')

	def _compute_x_my_company(self):

		for record in self:
				com = self.env['res.partner'].search([
															#('name', '=', 'Clinica Chavarri'),
															('x_my_company', '=', True),
													],
													order='date desc',
													limit=1,
					)
				record.x_my_company = com 													



	# Date corrected 
	x_date_order_corr = fields.Char(
			string='Order Date Corr', 

			compute="_compute_date_order_corr",
		)

	@api.multi
	#@api.depends('partner_id')

	def _compute_date_order_corr(self):
		for record in self:

			DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
			date_field1 = datetime.datetime.strptime(record.date_order, DATETIME_FORMAT)
			
			date_field2 = date_field1 + datetime.timedelta(hours=-5,minutes=0)
			DATETIME_FORMAT_2 = "%d-%m-%Y %H:%M:%S"
			date_field2 = date_field2.strftime(DATETIME_FORMAT_2)
			record.x_date_order_corr = date_field2






# ----------------------------------------------------------- Primitives --------------------------
	
	# Proc Created - For Doctor budget creation 
	x_procedure_created = fields.Boolean(

			'Procedimiento Creado', 

			default=False, 
		)



	# Partner 
	partner_id = fields.Many2one(
			'res.partner',
			string = "Cliente", 	
			ondelete='cascade', 			
			#required=True, 
			required=False, 

			states={	
					'draft': [('readonly', False)], 
					'sent': [('readonly', True)], 
					'sale': [('readonly', True)], 
					
					#'editable': [('readonly', False)], 
				}, 
		)



	# DNI 
	x_partner_dni = fields.Char(
			string='DNI', 

			states={
						'draft': 	[('readonly', False)], 
						'sent': 	[('readonly', True)], 
						'sale': 	[('readonly', True)], 
						'cancel': 	[('readonly', True)], 
						'done': 	[('readonly', True)], 
					}, 
		)










# ---------------------------------------------- Create Payment Method - Amount Total -------------

	# Amount total 
	x_amount_total = fields.Float(
			string = "x Total",

			compute="_compute_x_amount_total",
		)

	@api.multi
	def _compute_x_amount_total(self):
		for record in self:
			sub = 0.0
			for line in record.order_line:
				sub = sub + line.price_subtotal 
			#if sub == 0.0:
			#	sub = float(record.x_ruc)
			record.x_amount_total = sub



# ---------------------------------------------- Create Payment Method --------------------------------------------------------
	@api.multi 
	def create_payment_method(self):
		"""
		high level support for doing this and that.
		"""

		# Update Descriptors
		self.update_descriptors()

		# Init vars
		name = 'Pago'
		method = 'cash'
		balance = self.x_amount_total
		firm = self.patient.x_firm
		ruc = self.patient.x_ruc



		# Create 
		self.x_payment_method = self.env['openhealth.payment_method'].create({
																				'order': self.id,
																				'method': method,
																				'subtotal': balance,
																				'total': self.x_amount_total,
																				'partner': self.partner_id.id, 
																				'date_created': self.date_order,

																				'firm': firm,
																				'ruc': ruc,

																				# Deprecated 
																				#'name': name,
																				#'dni': dni,
																				#'id_doc_type': 	id_doc_type,
																				#'id_doc': 			id_doc,
																			})
		payment_method_id = self.x_payment_method.id 


		# Create Lines 
		name = '1'
		method = 'cash'
		subtotal = self.x_amount_total
		payment_method = self.x_payment_method.id

		ret = self.x_payment_method.pm_line_ids.create({
																	'name': name,
																	'method': method,
																	'subtotal': subtotal,
																	'payment_method': payment_method, 
										})


		return {
				'type': 'ir.actions.act_window',
				'name': ' New PM Current', 
				'view_type': 'form',
				'view_mode': 'form',	
				'target': 'current',
				'res_model': 'openhealth.payment_method',				
				'res_id': payment_method_id,
				'flags': 	{
							#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
							#'form': {'action_buttons': False, }
							'form': {'action_buttons': False, 'options': {'mode': 'edit'}  }
							},
				'context': {
				
							'default_order': self.id,
							'default_name': name,
							'default_method': method,
							'default_subtotal': balance,
							'default_total': self.x_amount_total,
							'default_partner': self.partner_id.id,
							'default_date_created': self.date_order,
							'default_firm': firm,
							'default_ruc': ruc,

							#'default_dni': dni,
							#'default_saledoc': 'receipt', 
							#'default_pm_total': self.pm_total,
							}
				}
	# create_payment_method






# ----------------------------------------------------------- Update Descriptors ------------------------------------------------------

	# For batch 
	@api.multi 
	def update_descriptors_all(self):
		"""
		high level support for doing this and that.
		"""

		orders = self.env['sale.order'].search([
													('state', '=', 'sale'),
											],
												order='date_order desc',
												#limit=2000,
												limit=300,
											)
		#print orders 

		for order in orders: 
			order.update_descriptors()



	# Update Family and Product 
	@api.multi 
	def update_descriptors(self):
		"""
		high level support for doing this and that.
		"""

		out = False

		for line in self.order_line:

			if not out: 

				# Consultations
				if line.product_id.categ_id.name in ['Consulta','Consultas']:
					self.x_family = 'consultation'
					self.x_product = line.product_id.x_name_ticket
					out = True

				# Procedures
				elif line.product_id.categ_id.name in ['Procedimiento', 'Quick Laser', 'Laser Co2', 'Laser Excilite', 'Laser M22', 'Medical']:
					self.x_family = 'procedure'
					self.x_product = line.product_id.x_name_ticket
					out = True

				# Cosmetology
				elif line.product_id.categ_id.name == 'Cosmeatria':
					self.x_family = 'cosmetology'
					self.x_product = line.product_id.x_name_ticket
					out = True


				# Products
				else:
					self.x_product = line.product_id.x_name_ticket
					if self.x_family != 'procedure':
						self.x_family = 'product'


		#print
		#print 'Update descriptors'
		#print self.x_family
		#print self.x_product

	#update_descriptors





# ----------------------------------------------------------- Print -------------------------------
	# Print Ticket - Electronic
	@api.multi
	def print_ticket_electronic(self):
		"""
		high level support for doing this and that.
		"""
		#print
		#print 'Print Electronic'
		name = 'openhealth.report_ticket_receipt_electronic'
		action = self.env['report'].get_action(self, name)
		return action



	# Print Ticket - Deprecated !
	@api.multi
	def print_ticket(self):
		"""
		high level support for doing this and that.
		"""
		if self.x_type == 'ticket_receipt': 
			name = 'openhealth.report_ticket_receipt_nex_view'
			return self.env['report'].get_action(self, name)
		elif self.x_type == 'ticket_invoice': 
			name = 'openhealth.report_ticket_invoice_nex_view'
			return self.env['report'].get_action(self, name)






# ----------------------------------------------------------- Update Appointments -----------------

	# Update Appointment in Treatment 
	@api.multi 
	def update_appointment(self):
		"""
		high level support for doing this and that.
		"""
		if self.x_family == 'consultation':
			for app in self.treatment.appointment_ids:
				if app.x_type == 'consultation':
					app.state = 'Scheduled'
		if self.x_family == 'procedure':
			for app in self.treatment.appointment_ids:
				if app.x_type == 'procedure':
					app.state = 'Scheduled'



#----------------------------------------------------------- Quick Button - For Treatment ---------

	# For Treatments Quick access
	@api.multi
	def open_line_current(self):  
		"""
		high level support for doing this and that.
		"""
		consultation_id = self.id
		return {
				'type': 'ir.actions.act_window',
				'name': ' Edit Order Current', 
				'view_type': 'form',
				'view_mode': 'form',
				'res_model': self._name,
				'res_id': consultation_id,
				'target': 'current',
				'flags': {
						#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
						'form': {'action_buttons': True, }
						},
				'context': {}
		}






	#----------------------------------------------------------- Qpen myself ------------------------------------------------------------

	# For Payment Method comeback 
	@api.multi 
	def open_myself(self):
		"""
		high level support for doing this and that.
		"""
		order_id = self.id
		return {
			# Mandatory 
			'type': 'ir.actions.act_window',
			'name': 'Open Order Current',
			# Window action 
			'res_model': 'sale.order',
			'res_id': order_id,
			# Views 
			"views": [[False, "form"]],
			'view_mode': 'form',
			'target': 'current',
			#'view_id': view_id,
			#"domain": [["patient", "=", self.patient.name]],
			#'auto_search': False, 
			'flags': {
					'form': {'action_buttons': True, }
					#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
			},			
			'context':   {

			}
		}
	# open_myself



# ----------------------------------------------------------- Remove and Reset ------------
	# Reset 
	@api.multi 
	def reset(self):
		"""
		high level support for doing this and that.
		"""
		#print 
		#print 'Order - Reset'
		self.x_payment_method.unlink()
		self.state = 'draft'


	@api.multi
	def remove_myself(self):  
		"""
		high level support for doing this and that.
		"""
		#self.test_reset()
		self.reset()
		self.unlink()





# ---------------------------------------------- Cancel -------------------------------------------

	# Cancel 
	x_cancel = fields.Boolean(
			string='',
			default = False
		)



	# Cancel Order
	@api.multi
	def cancel_order(self):
		#print
		#print 'Cancel Order'
		self.x_cancel = True
		self.state = 'cancel'

		# Create CN
		#self.create_credit_note()



	# Activate
	@api.multi
	def activate_order(self):
		self.x_cancel = False
		self.state = 'sale'




# ----------------------------------------------------------- Test --------------------------------
	
	# Test Case	
	x_test_case = fields.Char()


	# Test
	def test(self):
		"""
		high level support for doing this and that.
		"""
		#print
		#print 'Order - Test - Interface'
		test_order.test(self)



	# Pay myself
	def pay_myself(self):
		"""
		high level support for doing this and that.
		"""
		#print
		#print 'Order - Pay myself - Interface'
		test_order.pay_myself(self)



