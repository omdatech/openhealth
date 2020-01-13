
# 4 May 2019

# ----------------------------------------------------------- Dep --------------------------
	# Management - Used by Old method - Dep ?
	mgt = fields.Many2one(
			'openhealth.management',
			required=True,
		)



# ----------------------------------------------------------- Electronic - Dep --------------------------
	@api.multi
	def create_electronic(self):
		"""
		Create Electronic Orders - Step 1
		"""
		print()
		print('Create - Electronic')

		# Clean
		self.electronic_order_ids.unlink()

		# Init Dates
		date_format = "%Y-%m-%d"
		date_dt = datetime.datetime.strptime(self.export_date_begin, date_format) + \
																					datetime.timedelta(hours=+5, minutes=0)

		self.export_date = date_dt.strftime(date_format).replace('-', '_')


		# Init Mgt
		self.mgt.date_begin = self.export_date_begin
		self.mgt.date_end = self.export_date_begin
		self.mgt.container = self.id
		self.mgt.state_arr = 'sale,cancel,credit_note'

		#print('mark 1')

		# Update
		self.mgt.update_fast()

		#print('mark 2')

		# Create
		self.amount_total, self.receipt_count, self.invoice_count = self.mgt.update_electronic()

		#print('mark 3')

	# create_electronic



# ----------------------------------------------------------- Export - Dep ------------------------------
	@api.multi
	def export_txt(self):
		"""
		Export TXT - Step 2
		"""
		print()
		print('Export - Txt')

		# Clean
		self.txt_ids.unlink()



		# Export - Here !
		fname = export.export_txt(self, self.mgt.electronic_order, self.export_date)



		# Download file
		fname_txt = fname.split('/')[-1]
		# Read Binary
		f = io.open(fname, mode="rb")
		out = f.read()
		f.close()

		# Update
		self.write({
					'txt_pack': base64.b64encode(out),
					'txt_pack_name': fname_txt,
				})
	# export_txt
















# 2 May 2019

# ----------------------------------------------------------- Relational - Dep --------------------------

	# Patients
	#patient_ids = fields.One2many(
	#		'oeh.medical.patient',
	#		'container_id',
	#	)

	# Doctor
	#doctor = fields.Many2one(
	#		'oeh.medical.physician',
	#		string="Doctor",
	#	)

# ----------------------------------------------------------- Actions -----------------------------

	# Clear
	@api.multi
	def clear(self):
		"""
		high level support for doing this and that.
		"""
		# Loop
		for patient in self.patient_ids:
			patient_id = patient.id

			# Protected
			if patient.x_test:
				creates.remove_orders(self, patient_id)


		# Electronic
		self.mgt.electronic_order.unlink()

		# Txt
		self.txt_ids.unlink()

		# Stats
		self.amount_total = 0
		self.invoice_count = 0
		self.receipt_count = 0
	# clear



# ----------------------------------------------------------- Fields ------------------------------

	# Flags
	ticket_invoice_create = fields.Boolean(
			'Ticket Invoice',
		)

	ticket_receipt_create = fields.Boolean(
			'Ticket Receipt',
		)

	invoice_create = fields.Boolean(
			'Invoice',
		)

	receipt_create = fields.Boolean(
			'Receipt',
		)

	sale_note_create = fields.Boolean(
			'SN',
		)

	advertisement_create = fields.Boolean(
			'Adv',
		)


	# All Create
	@api.multi
	def all_create(self):
		"""
		high level support for doing this and that.
		"""
		self.ticket_invoice_create = True
		self.ticket_receipt_create = True
		self.invoice_create = True
		self.receipt_create = True
		self.sale_note_create = True
		self.advertisement_create = True



	# All Clear
	@api.multi
	def all_clear(self):
		"""
		high level support for doing this and that.
		"""
		self.ticket_invoice_create = False
		self.ticket_receipt_create = False
		self.invoice_create = False
		self.receipt_create = False
		self.sale_note_create = False
		self.advertisement_create = False




	#ticket_invoice_cancel = fields.Boolean(
	#		'Invoice Cancel',
	#	)

	#ticket_receipt_cancel = fields.Boolean(
	#		'Receipt Cancel',
	#	)






# ----------------------------------------------------------- QC -----------------------------
	@api.multi
	def test_qc(self):
		"""
		high level support for doing this and that.
		"""
		# Gap and Checksum
		self.mgt.update_qc('ticket_receipt')
		self.mgt.update_qc('ticket_invoice')
	# test_qc


# ----------------------------------------------------------- Update -----------------------------
	@api.multi
	def update(self):
		"""
		high level support for doing this and that.
		"""
		self.test_qc()
		self.create_electronic()
		self.export_txt()



# ----------------------------------------------------------- Patients Remove ---------------------
	@api.multi
	def remove_patients(self):
		"""
		high level support for doing this and that.
		"""
		print()
		print('Remove Patients')

		# Search
		patients = self.env['oeh.medical.patient'].search([
															('name', 'not in', ['REVILLA RONDON JOSE JAVIER']),
															('x_test', 'in', [True]),
													],
														#order='write_date desc',
														#limit=1,
													)
		for patient in patients:
			name = patient.name
			creates.remove_patient(self, name)




# ----------------------------------------------------------- Create Sales ------------------------

	# Create Sales
	@api.multi
	def create_sales(self):
		"""
		high level support for doing this and that.
		"""
		#print
		#print 'Create Sales'

		# Search
		patients = self.env['oeh.medical.patient'].search([
																('x_test', '=', True),
															],
															#order='appointment_date desc',
															#limit=1,
														)
		# Loop
		for patient in patients:

			# Init
			patient_id = patient.id
			partner_id = patient.partner_id.id
			doctor_id = self.doctor.id
			treatment_id = False
			short_name = 'product_1'
			qty = 1
			pricelist_id = patient.property_product_pricelist.id


			# Ticket Invoice
			if self.ticket_invoice_create:
				x_type = 'ticket_invoice'
				creates.create_order_fast(self, patient_id, partner_id, doctor_id, treatment_id,\
																							 short_name, qty, x_type, pricelist_id)

			# Ticket Receipt
			if self.ticket_receipt_create:
				x_type = 'ticket_receipt'
				creates.create_order_fast(self, patient_id, partner_id, doctor_id, treatment_id,\
																							 short_name, qty, x_type, pricelist_id)


			# Invoice
			if self.invoice_create:
				x_type = 'invoice'
				creates.create_order_fast(self, patient_id, partner_id, doctor_id, treatment_id,\
																							 short_name, qty, x_type, pricelist_id)

			# Receipt
			if self.receipt_create:
				x_type = 'receipt'
				creates.create_order_fast(self, patient_id, partner_id, doctor_id, treatment_id,\
																							 short_name, qty, x_type, pricelist_id)

			# Sale Note
			if self.sale_note_create:
				x_type = 'sale_note'
				creates.create_order_fast(self, patient_id, partner_id, doctor_id, treatment_id,\
																							 short_name, qty, x_type, pricelist_id)

			# Receipt
			if self.advertisement_create:
				x_type = 'advertisement'
				creates.create_order_fast(self, patient_id, partner_id, doctor_id, treatment_id,\
																							 short_name, qty, x_type, pricelist_id)


			# Invoice Cancel
			#if self.ticket_invoice_cancel:
			#	invoice.cancel_order()

			# Receipt Cancel
			#if self.ticket_receipt_cancel:
			#	receipt.cancel_order()

	# create_sales










# ----------------------------------------------------------- Patients Create ---------------------
	# Create Patients
	@api.multi
	def create_patients(self):
		"""
		high level support for doing this and that.
		"""
		print()
		print('Create Patients')

		# Init
		container_id = self.id
		doctor_id = self.doctor.id


		# Create Patients
		test_cases_pat.test_cases(self, container_id, doctor_id)


		# Init
		name = 'Export'


		# Update Mgt
		if self.mgt.name != False:
			self.mgt.date_begin = self.export_date_begin
			self.mgt.date_end = self.export_date_begin

		# Create Mgt
		else:
			self.mgt = self.env['openhealth.management'].create({
																'name': 		name,
																'date_begin': 	self.export_date_begin,
																'date_end': 	self.export_date_begin,
													})
	# create_patients