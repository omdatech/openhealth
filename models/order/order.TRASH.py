# 28 Aug 2019
# App is Highly Deprecated !
# My Company also
# 


		# Manage Exception
		try:
			configurator.ensure_one()

		except:
			msg = "ERROR: Record Must be One."
			class_name = type(configurator).__name__
			#obj_name = counter.name
			#msg =  msg + '\n' + class_name + '\n' + obj_name
			#msg =  msg 
			msg =  msg + '\n' + class_name

			raise UserError(_(msg))




# ----------------------------------------------------------- Appointments - Dep !!! -----------------

	# Update Appointment in Treatment
	#@api.multi
	#def update_appointment(self):
	#	"""
	#	high level support for doing this and that.
	#	"""
	#	if self.x_family == 'consultation':
	#		for app in self.treatment.appointment_ids:
	#			if app.x_type == 'consultation':
	#				app.state = 'Scheduled'
	#	if self.x_family == 'procedure':
	#		for app in self.treatment.appointment_ids:
	#			if app.x_type == 'procedure':
	#				app.state = 'Scheduled'




# ----------------------------------------------------------- Dep ! -------------------------

	# My company
	#x_my_company = fields.Many2one(
	#		'res.partner',
	#		string="Mi compañía",
	#		domain=[
	#					('company_type', '=', 'company'),
	#				],

	#		compute="_compute_x_my_company",
	#	)

	#@api.multi
	#def _compute_x_my_company(self):
	#	for record in self:
	#			com = self.env['res.partner'].search([
	#														('x_my_company', '=', True),
	#												],
	#												order='date desc',
	#												limit=1,
	#				)
	#			record.x_my_company = com







	def action_confirm_nex(self):


		#if self.x_serial_nr != '' and self.x_admin_mode == False:
			# Prefix
			#prefix = ord_vars._dic_prefix[self.x_type]

			# Padding
			#padding = ord_vars._dic_padding[self.x_type]

			# Serial Nr
			#self.x_serial_nr = prefix + self.x_separator + str(self.x_counter_value).zfill(padding)

			#self.x_counter_value = user.get_counter_value(self)

			#self.x_serial_nr = user.get_serial_nr(self.x_type, self.x_counter_value)


		#res = super(sale_order, self).action_confirm()




# ----------------------------------------------------- Product Selector - Dep --------------------------

	@api.multi
	def open_product_selector_product(self):
		"""
		high level support for doing this and that.
		"""
		return self.open_product_selector('product')


	@api.multi
	def open_product_selector_service(self):
		"""
		high level support for doing this and that.
		"""
		return self.open_product_selector('service')


	# Buttons  - Agregar Producto Servicio
	@api.multi
	def open_product_selector(self, x_type):
		"""
		high level support for doing this and that.
		"""

		# Init Vars
		order_id = self.id
		res_id = False

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
								'form':{'action_buttons': False, 'options': {'mode': 'edit'}}
							},
				'context': {
								'default_order_id': order_id,
								'default_x_type': x_type,
					}}
	# open_product_selector
