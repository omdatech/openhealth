# -*- coding: utf-8 -*-
"""

 	Electronic Order - Sunat compatible

 	Created: 			13 Sep 2018
 	Last updated: 		15 Oct 2019

"""
from openerp import models, fields, api
from openerp.addons.openhealth.models.libs import lib
from openerp.addons.openhealth.models.order import ord_vars
from . import chk_electronic
from . import lib_coeffs

class electronic_order(models.Model):
	"""
	Electronic Order used by Accounting TXT generator
	"""
	_inherit = 'openhealth.line'

	_name = 'openhealth.electronic.order'

	_description = "Sunat Electronic Order"

	_order = 'serial_nr asc'




# ----------------------------------------------------------- Configurator ------------------------

	def _get_default_configurator(self):
		#print()
		#print('Default Configurator')

		# Search
		configurator = self.env['openhealth.configurator.emr'].search([
																		#('active', 'in', [True]),
											],
												#order='x_serial_nr asc',
												limit=1,
											)
		print(configurator)
		print(configurator.name)
		return configurator

	# Configurator
	configurator = fields.Many2one(
			'openhealth.configurator.emr',
			string="Configuracion",

			default=_get_default_configurator,
		)






# ----------------------------------------------------------- Emitter -----------------------------

	# Firm
	firm = fields.Char(
			'Firm',
			#default='SERVICIOS MÉDICOS ESTÉTICOS S.A.C',
			#required=True,
		)

	# Ruc
	ruc = fields.Char(
			'Ruc',
			#default='20523424221',
			#required=True,
		)


	# Ubigeo
	ubigeo = fields.Char(
			'Ubigeo',
			#default='150101',	# Verify
			#required=True,
		)

	# Address
	address = fields.Char(
			'Address',
			#default='Av. La Merced 161',
			#required=True,
		)


	# Country
	country = fields.Char(
			'Country',
			#default='PE',
			#required=True,
		)






# ----------------------------------------------------------- Required ----------------------------

	# Patient
	id_doc_type = fields.Char(
			string='Doc Id Tipo',
			default=".",
			required=True,
		)

	id_doc_type_code = fields.Char(
			string='Codigo',
			default=".",
			required=True,
		)



	# Order
	x_type = fields.Char(
			'Tipo',
			required=True,
		)

	type_code = fields.Char(
			'Codigo',
			required=True,
		)

	serial_nr = fields.Char(
			'Serial Nr',
			required=True,
		)

	receptor = fields.Char(
			string='Receptor',
			required=True,
		)



# ----------------------------------------------------------- Electronic -------------------------------

	def get_coeff(self):
		"""
		Used by Txt Generation
		From containers.lib_exp
		"""
		coeff = lib_coeffs.get_coeff(self.state)
		return coeff






# ----------------------------------------------------------- Credit Note -------------------------
	credit_note_type = fields.Selection(

			selection=ord_vars._credit_note_type_list,

			string='Motivo',
			default='cancel',
		)


	def get_credit_note_type(self):
		"""
		high level support for doing this and that.
		"""
		_dic_cn_type = {
							'cancel': 					'Anulacion de la operacion',
							'cancel_error_ruc': 		'Anulacion por error en el RUC',
							'correct_error_desc': 		'Correccion por error en la descripcion',
							'discount': 				'Descuento global',
							'discount_item': 			'Descuento por item',

							'return': 					'Devolucion total',
							'return_item': 				'Devolucion por item',
							'bonus': 					'Bonificacion',
							'value_drop': 				'Disminucion en el valor',
							'other': 					'Otros',

							False: 						'',
					}
		return _dic_cn_type[self.credit_note_type].upper()


# ----------------------------------------------------------- Handles -----------------------------

	# Treatment
	treatment_id = fields.Many2one(
			'openhealth.treatment',
			ondelete='cascade',
		)



	# Container
	container_id = fields.Many2one(
			'openhealth.container',
			ondelete='cascade',
		)

	# Management
	management_id = fields.Many2one(
			'openhealth.management',
			ondelete='cascade',
		)




# ----------------------------------------------------------- Dep ---------------------------------
	# Id
	#id_serial_nr = fields.Char(
	#		'Id Serial Nr',
	#	)







# ----------------------------------------------------------- Constraints - Python ----------------

	# Check
	@api.constrains('serial_nr')
	def check_serial_nr(self):
		"""
		high level support for doing this and that.
		"""
		#chk_electronic.check_serial_nr(self)
		chk_electronic.check_serial_nr(self, self.container_id.id)





# ----------------------------------------------------------- Receptor ----------------------------


	id_doc = fields.Char(
			'Doc Id',
			default=".",
		)

	patient = fields.Many2one(
			'oeh.medical.patient',
			string="Paciente",
		)







# ----------------------------------------------------------- Relational --------------------------

	# CN Owner
	credit_note_owner = fields.Many2one(
			'sale.order',
		)


	# Lines
	electronic_line_ids = fields.One2many(
			'openhealth.electronic.line',
			'electronic_order_id',
		)





# ----------------------------------------------------------- Sale --------------------------------

	currency_code = fields.Char(
			'Moneda',
			default="PEN",
		)


	state = fields.Selection(
			selection=ord_vars._state_list,
			string='Estado',
			readonly=False,
			default='draft',
		)


	export_date = fields.Char(
			'Export Date',

			compute='_compute_export_date',
		)

	@api.multi
	#@api.depends('x_msg')
	def _compute_export_date(self):
		for record in self:
			record.export_date = lib.correct_date(record.x_date_created).split()[0]



	# Counter Value
	counter_value = fields.Integer(
			string="Contador",
		)


	# Delta
	delta = fields.Integer(
			'Delta',
		)


	# Amount total
	amount_total = fields.Float(
			string="Total",
			digits=(16, 2),
		)


	# Amount total - Net
	amount_total_net = fields.Float(
			string="Net",
			digits=(16, 2),
		)

	# Amount total - Tax
	amount_total_tax = fields.Float(
			string="Tax",
			digits=(16, 2),
		)
