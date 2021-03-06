# -*- coding: utf-8 -*-
"""
 		*** RES PARTNER
 
 		Created: 			26 Aug 2016
		Last updated: 	 	20 Sep 2019
"""
from openerp import models, fields, api
from . import partner_vars

class Partner(models.Model):
	"""
	"""
	_inherit = 'res.partner'
	_order = 'write_date desc'




# ----------------------------------------------------------- Primitives ---------------------

	# Name 
	name = fields.Char(
			'Name', 
			#'(Generado automaticamente, no tocar)',
			select=True,
			index=True, 
		)




# ----------------------------------------------------------- Address -----------------------------	
	# Address
	x_address = fields.Char(
			"Dirección",

			compute='_compute_x_address', 
		)

	@api.multi
	#@api.depends('')
	def _compute_x_address(self):
		for record in self:
			if record.street != False and record.street2 != False and record.city != False:
				record.x_address = record.street.title() + ' ' + record.street2.title() + ' - ' + record.city.title()



# ----------------------------------------------------------- Hard wired - With Patient -----------

	# Company
	x_ruc = fields.Char(
			"RUC",
		)

	x_firm = fields.Char(
			"Razón social",
		)



	# Phones
	phone = fields.Char(
			'Fijo',
			required=False,
		)
	
	mobile = fields.Char(
			'Celular',
		)

	email = fields.Char(
			string = 'Email',
			placeholder = '',
			required=False,
		)

	# Address
	country_id = fields.Many2one(
			'res.country',
			string = 'País',
			default = 175,	# Peru
			#ondelete='restrict',
			required=True, 
		)

	city = fields.Selection(
			selection = partner_vars._city_list,
			string = 'Departamento',
			default = 'lima',
			required=False,
		)

	# For patient short card
	city_char = fields.Char(
			compute='_compute_city_char',
		)
	#@api.multi
	@api.depends('city')
	def _compute_city_char(self):
		for record in self:
			record.city_char = record.city

	street2 = fields.Char(
			string = "Distrito 2", 	
			
			#required=True, 
			required=False, 
		)

	street2_sel = fields.Selection(
			selection = partner_vars._street2_list,
			string = "Distrito",
			required=False, 
		)

	street = fields.Char(
			string = "Dirección",
			required=False,
		)

	zip = fields.Char(
			#'Zip',
			string = 'Código',
			size=24,
			#change_default=True,
			required=False,
		)


	# Only for foreign addresses
	x_foreign = fields.Boolean(
			string="Dirección en el extranjero",
		)


	x_address_foreign = fields.Text(
			'Dirección',
			#string=".",
		)


	# Vspace
	vspace = fields.Char(
			' ',
			readonly=True
		)




# ----------------------------------------------------------- Indexed ------------------------------------------------------

	# Dni 
	x_dni = fields.Char(
			"DNI", 	
			index=True,
			required=False,
		)

# ----------------------------------------------------------- My Company ------------------------------------------------------

	# My company 
	x_my_company = fields.Boolean(
			'Mi compañía ?', 
		)

	# Series 
	x_series = fields.Char(
			string='Serie', 
		)

	# Autorization 
	x_authorization = fields.Char(
			string='Autorización', 
		)

	# Warning Sales
	x_warning = fields.Text(
			'Condiciones de Venta', 
		)

	# Warning Purchase 
	x_warning_purchase = fields.Text(
			'Condiciones de Compra', 
		)


# ----------------------------------------------------------- Vip ------------------------------------------------------
	# Vip 
	x_vip = fields.Boolean(
		string="VIP",
		default=False, 

		compute='_compute_x_vip', 
	)

	@api.multi
	#@api.depends('x_card')
	def _compute_x_vip(self):

		# Does he have a Vip card ?
		for record in self:
			x_card = record.env['openhealth.card'].search([
															('patient_name','=', record.name),
														],
														#order='appointment_date desc',
														limit=1,)
			if x_card.name != False:
				record.x_vip = True 
				#pricelist_name = 'VIP'
				record.action_ppl_vip()
			else:
				record.x_vip = False 
				#pricelist_name = 'Public Pricelist'
				record.action_ppl_public()




# ----------------------------------------------------------- Pricelist ------------------------------------------------------

	# PPL - Public 
	@api.multi
	def action_ppl_public(self):  

		pricelist_name = 'Public Pricelist'

		# Pricelist 
		pricelist = self.env['product.pricelist'].search([
																	('name','=', pricelist_name),
															],
														#order='appointment_date desc',
														limit=1,)
		self.property_product_pricelist = pricelist
	# action_ppl_public


	# PPL - Vip 
	@api.multi
	def action_ppl_vip(self):  

		pricelist_name = 'VIP'

		# Pricelist 
		pricelist = self.env['product.pricelist'].search([
																	('name','=', pricelist_name),
															],
														#order='appointment_date desc',
														limit=1,)
		self.property_product_pricelist = pricelist
	# action_ppl_vip


# ----------------------------------------------------------- On Changes ------------------------------------------------------
# ----------------------------------------------------------- Validate - DNI RUC ------------------------------------------------------

	# Ternary If 
	#isApple = True if fruit == 'Apple' else False

	# Name 
	@api.onchange('name')
	def _onchange_name(self):
		if self.name != False: 
			name = self.name.strip().upper()
			self.name = " ".join(name.split())			

	# Foreign 
	@api.onchange('x_foreign')
	def _onchange_x_foreign(self):
		self.city = "" if self.x_foreign == True else 'don'



# ----------------------------------------------------------- CRUD ------------------------------------------------------

	# Create 
	@api.model
	def create(self,vals):
		#print 
		#print 'CRUD - Partner - Create'
		#print vals
		#print 
	
		# Compact and Uppercase Name
		if 'name' in vals:
			#  Name to upper. And strips beg and end spaces. 
			#print 'Compact'
			name = vals['name']
			name = name.strip().upper()			# Uppercase 
			name = " ".join(name.split())		# Compact - Strip beginning, inside and ending extra spaces
			vals['name'] = name 

		# Put your logic here 
		res = super(Partner, self).create(vals)
		# Put your logic here 

		return res
	# CRUD - Create 

