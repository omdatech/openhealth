# -*- coding: utf-8 -*-
"""
 	Corrector

 	Created: 				 6 Nov 2018
 	Last mod: 				 6 Nov 2018
"""
from openerp import models, fields, api

class Corrector(models.Model):
	"""
	high level support for doing this and that.
	"""
	_name = 'openhealth.corrector'
	
	_description = 'Corrector'

	#_inherit = 'openhealth.container'

	#_order = 'date_begin asc'



	name = fields.Char(
			required=True,
		)

	delta = fields.Integer(
			default=1,
		)


	# Flags
	go_flag = fields.Boolean()

	product_flag = fields.Boolean()

	co2_flag = fields.Boolean()
	exc_flag = fields.Boolean()
	ipl_flag = fields.Boolean()
	ndy_flag = fields.Boolean()
	qui_flag = fields.Boolean()

	cos_flag = fields.Boolean()
	med_flag = fields.Boolean()

	con_flag = fields.Boolean()



# ----------------------------------------------------------- Creates ------------------------------

	# Create Codes
	@api.multi
	def create_codes(self):
		"""
		high level support for doing this and that.
		"""
		print
		print 'Create - Codes'


		# Product
		if self.product_flag:

			count = self.env['product.product'].search_count([
																('type', 'in', ['product']),
																('sale_ok', 'in', [True]),
												],
													#order='name asc',
													#limit=1,
												)

			products = self.env['product.product'].search([
																('type', 'in', ['product']),
																('sale_ok', 'in', [True]),
												],
													order='name asc',
													#limit=1,
												)


		# Laser

		if self.co2_flag:
			treatment = 'laser_co2'
		
		if self.exc_flag:
			treatment = 'laser_excilite'
		
		if self.ipl_flag:
			treatment = 'laser_ipl'
		
		if self.ndy_flag:
			treatment = 'laser_ndyag'
		
		if self.qui_flag:
			treatment = 'laser_quick'
		


		#if self.co2_flag:
		if self.co2_flag or self.exc_flag or self.ipl_flag or self.ndy_flag or self.qui_flag:

			count = self.env['product.product'].search_count([
																('type', 'in', ['service']),
																('sale_ok', 'in', [True]),
																#('x_treatment', 'in', ['laser_co2']),
																('x_treatment', 'in', [treatment]),
												],
													#order='name asc',
													#limit=1,
												)

			products = self.env['product.product'].search([
																('type', 'in', ['service']),
																('sale_ok', 'in', [True]),
																#('x_treatment', 'in', ['laser_co2']),
																('x_treatment', 'in', [treatment]),
												],
													order='x_name_short asc',
													#limit=1,
												)


		# Correct
		idx = self.delta

		#for product in products.sorted(key=lambda l: l.type in ['product']):
		for product in products:

			print product.name
			print product.x_name_short

			if self.go_flag:
				product.x_counter = idx
			
			idx = idx + 1


		print
		print count
		print

	# create_codes
