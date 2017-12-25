# -*- coding: utf-8 -*-
#
#
# 		*** OPEN HEALTH - Patient 
# 
# Created: 				26 Aug 2016
# Last updated: 	 	25 Aug 2017


from openerp import models, fields, api
from datetime import datetime

from . import pat_funcs
from . import pat_vars



class Patient(models.Model):

	#_name = 'openhealth.patient'		
	_inherit = 'oeh.medical.patient'

	#_order = 'x_date_created desc'
	_order = 'write_date desc'





	# Commons 
	vspace = fields.Char(
			' ', 
			readonly=True
			)















	x_dni = fields.Char(
			string = "DNI", 	

			#required=True, 
			#required=False, 
		)









	x_nothing = fields.Char(
		'Nothing', 
	)






	# QC - Flag  
	x_flag = fields.Char(

		"Flag",
		
		default = '', 
		store=True, 
	)





	# QC - Number of clones  
	x_nr_clones = fields.Integer(
			"QC - Nrc",

			compute="_compute_x_nr_clones",
	)

	@api.multi
	
	def _compute_x_nr_clones(self):
		for record in self:

			record.x_nr_clones = self.env['oeh.medical.patient'].search_count([
																				('name','=', record.name),
																			]) 

			if record.x_nr_clones > 1:
				record.x_flag = 'error'

			else:
				record.x_flag = ''





	# QC - Lowcase
	x_lowcase = fields.Boolean(

			"QC - Low",

			compute="_compute_x_lowcase",
	)


	@api.multi
	def _compute_x_lowcase(self):
		for record in self:
			#if name != name.upper.strip:
			if record.name != record.name.upper():
				record.x_lowcase = True
				record.x_flag = 'error'
			else:
				record.x_lowcase = False
	#			record.x_flag = ''


















	x_nationality = fields.Selection(
			[	
				('peruvian', 	'Peruano'),
				('other', 		'Otro'),
			], 
			'Nacionalidad', 
			default="peruvian",
			required=True,  
		)


	x_id_doc = fields.Char(
			'Doc. identidad', 
		)


	x_id_doc_type = fields.Selection(
			[	
				('passport', 		'Pasaporte'),
				('foreigner_card', 	'Carnet de Extranjería'),
				('dni', 			'DNI'),
				('other', 			'Otro'),
			], 
			'Tipo de documento', 
			#default="passport",
			#required=True,  
		)





	#@api.multi
	#def card_purchase(self):  
	#	print 'jx'










	# Spaced 		- ???
	x_spaced = fields.Boolean(
		string="Spaced",
		default=False, 

		compute='_compute_spaced', 
	)

	#@api.multi
	@api.depends('name')

	def _compute_spaced(self):
		for record in self:

			if record.name[0] == ' ':
				record.x_spaced = True








	# Vip 
	x_vip = fields.Boolean(
		string="VIP",
		default=False, 

		#store=True, 			

		compute='_compute_x_vip', 
	)


	#@api.multi
	@api.depends('x_card')

	def _compute_x_vip(self):
		for record in self:

			x_card = record.env['openhealth.card'].search([
															('patient_name','=', record.name),
														],
														#order='appointment_date desc',
														limit=1,)

			if x_card.name != False:
				record.x_vip = True 
	# 







	x_card = fields.Many2one(
			'openhealth.card',
			string = "Tarjeta VIP", 	
			#required=True, 
			compute='_compute_x_card', 

			#store=True, 			
		)


	#@api.multi
	@api.depends('name')

	def _compute_x_card(self):
		for record in self:

			x_card = record.env['openhealth.card'].search([
															('patient_name','=', record.name),
														],
														#order='appointment_date desc',
														limit=1,)

			record.x_card = x_card
	# 













	x_country_name = fields.Char(
			'Pais', 
			required=True, 			
			compute='_compute_x_country_name', 
		)

	#@api.multi
	@api.depends('country_id')

	def _compute_x_country_name(self):
		for record in self:
			record.x_country_name = 'Peru'




	x_year = fields.Char(
			string='Year', 
			required=False, 
		)

	x_month = fields.Char(
			string='Month',

			#required=True, 
			required=False, 
		)



	# Year created  
	x_year_created = fields.Char(
			string='Year created', 
			#default = '', 
			#required=False, 

			index=True, 
			#compute='_compute_x_year_created', 
		)

	#@api.multi
	#@api.depends('x_date_created')

	#def _compute_x_year_created(self):
	#	for record in self:
	#		#print 
	#		#print 'Compute x_year_created'
	#		record.x_year_created = record.x_date_created.split('-')[0]


	@api.onchange('x_date_created')
	
	def _onchange_x_date_created(self):

		self.x_year_created = self.x_date_created.split('-')[0]

		self.x_month_created = self.x_date_created.split('-')[1]






	# Month created
	x_month_created = fields.Char(
			string='Month created', 
			#default = '', 
			#required=True, 

			#compute='_compute_x_month_created', 
		)

	#@api.multi
	#@api.depends('x_date_created')

	#def _compute_x_month_created(self):
	#	for record in self:
	#		#print 
	#		#print 'Compute x_month_created'
	#		record.x_month_created = record.x_date_created.split('-')[1]





	# Date created
	x_date_created = fields.Date(
			string = "Fecha de apertura",
			default = fields.Date.today, 
			#readonly = True, 
			required=True, 
			)


	x_datetime_created = fields.Datetime(
			string = "Apertura",

			##default = fields.Datetime.now, 
			#default = '', 
			
			#readonly = True, 

			#required=True, 
			required=False, 

			#store=True, 
			#compute='_compute_x_datetime_created', 
			)


	#@api.onchange('x_date_created')
	#def _onchange_x_date_created(self):
		#self.x_datetime_created = self.x_date_created  
		#self.x_datetime_created = '10/03/2017 20:00:00'
	#	self.x_datetime_created = '2017-10-03 20:00:00'
	#'%Y-%m-%d %H:%M:%S'


	#@api.multi
	#@api.depends('state')
	#def _compute_x_datetime_created(self):
	#	for record in self:
	#		if record.comment == 'legacy':
				#record.x_datetime_created = record.x_date_created
	#			record.x_datetime_created = ''








	x_status = fields.Char(
			string='Status', 

			default = '00', 

			#required=False, 
			required=True, 
		)



	x_state = fields.Selection(

			selection = pat_vars._state_list, 

			string='Estado', 			

			#default = False, 
			default = 'active', 

			compute='_compute_x_state', 
		)



	@api.multi
	#@api.depends('state')

	def _compute_x_state(self):
		for record in self:
			#print 
			#print 'jx'
			#print 'Compute x_state'

			#record.x_state = treatment_vars._hash_x_state[record.state]

			flag = False


			for treatment in record.treatment_ids:
				if treatment.progress == False: 
					flag = True

			if flag:
				record.x_state = 'incomplete'
			else:
				record.x_state = 'active'

			#print 










	x_first_impression = fields.Char(
			string="Primera impresión", 
			required=False, 
		)





# ----------------------------------------------------------- Autofill ------------------------------------------------------
	
	# Autofill

	x_autofill = fields.Boolean(
		string="Autofill",
		default=False, 
	)

	@api.onchange('x_autofill')
	
	def _onchange_x_autofill(self):

		if self.x_autofill == True:


			#self.x_last_name = 'Revilla Rondon'
			#self.x_first_name = 'Toby'


			self.sex = 'Male'

			self.dob = '1965-05-26'
			
			self.x_dni = '09817194'

			self.email = 'jrevilla55@gmail.com'
			
			self.phone = '4760118'

			self.x_allergies = 'Ninguna'

			self.x_first_contact = 'recommendation'

			self.street = 'Av. San Borja Norte 610'
			
			self.street2_sel = 41


			self.comment = 'test'
			
			
			#self.x_last_name = 'Fuchs Vibors'
			#self.x_first_name = 'Hans'
			#self.name = self.x_last_name + ' ' + self.x_first_name
			#self.street2 = 'San Borja'
			#self.zip = 41
			#self.city = 'Lima'
			#self.country_id = 175



# ----------------------------------------------------------- Relational ------------------------------------------------------


	treatment_ids = fields.One2many(
			'openhealth.treatment', 		
			'patient', 
			string="Tratamientos"
			)


	cosmetology_ids = fields.One2many(
			'openhealth.cosmetology', 		
			'patient', 
			string="Cosmiatrías"
			)







	appointment_ids = fields.One2many(
			'oeh.medical.appointment', 
			'patient', 
			
			#ondelete='cascade', 		# No - Very dangerous		

			string = "Citas", 
			)




# ----------------------------------------------------------- Re-definitions ------------------------------------------------------

	age = fields.Char(
			string = "Edad", 		
			)

	
	sex = fields.Selection(

			selection = pat_vars._sex_type_list, 

			string="Sexo",

			#required=True, 
			required=False, 
		)



	# Dictionary - For Reports 
	_dic = {
				'Male':		'Masculino', 
				'Female':	'Femenino', 
				'none':		'Ninguno', 
				'':			'', 
			}





	#x_sex_name = fields.Char(
	#		'Sexo', 
	#		required=True, 
	#		compute='_compute_x_sex_name', 
	#	)
	#@api.multi
	#def _compute_x_sex_name(self):
	#	for record in self:
	#		record.x_sex_name = record._dic[record.sex] 






	# For Ccdata compatibility 

	dob = fields.Date(
			string="Fecha nacimiento",

			#required=True, 
			required=False, 
		)





	# Street 
	street = fields.Char(

			string = "Dirección", 	
			#string = "Dirección fiscal", 	
			
			#required=True, 
			required=False, 
		)

	@api.onchange('street')
	def _onchange_street(self):

		if self.street != False: 
			self.street = self.street.strip().title()





	street2 = fields.Char(
			string = "Distrito", 	
			
			#required=True, 
			required=False, 
		)



	zip = fields.Integer(
			string = 'Código',  
			#compute='_compute_zip', 

			#required=True, 			
			required=False, 			
			)

	#@api.multi
	@api.depends('street2','city')

	def _compute_zip(self):
		for record in self:
			if (record.street2 in pat_vars.zip_dic) and (record.city == 'lima')  :
				record.zip=pat_vars.zip_dic[record.street2]
			else:
				record.zip=0





	# Email 
	email = fields.Char(
			string = 'Email',  
			placeholder = '',

			required=True, 
			#required=False, 
			)


	@api.onchange('email')
	def _onchange_email(self):
		print 'jx'
		print 'Change email'

		if self.email != False: 
			self.email = self.email.strip().lower()
			print self.email
			print 







	country_id = fields.Many2one(
			'res.country', 
			string = 'País', 
			default = 175,	# Peru

			#required=False, 
			required=True, 
			)

	city = fields.Selection(
			selection = pat_vars._city_list, 
			string = 'Departamento',  
			default = 'lima', 

			required=True, 
			#required=False, 
		)





	phone_1 = fields.Char(
		string="Teléfono 1",
		
		#required=True, 
		required=False, 
		)

	# Phone 2
	phone_2 = fields.Char(
		string="Teléfono 2",

		required=False, 
		)





	phone_3 = fields.Char(
		string="Teléfono",
		required=False, 
		)


	street2_char = fields.Char(
			string = "Distrito", 	
			#required=True, 
		)


	street2_sel = fields.Selection(
			selection = pat_vars._street2_list, 
			string = "Distrito", 	
			
			#required=True, 
			required=False, 
		)


	function = fields.Char(
			string = 'Ocupación',  
			placeholder = '',
			#required=True, 
			)





# ----------------------------------------------------------- New fields ------------------------------------------------------



	# Full name
	x_full_name = fields.Char(
		string = "Nombre completo",

		compute='_compute_full_name',
	)
	

	@api.depends('x_first_name', 'x_last_name')
	#@api.multi

	def _compute_full_name(self):
		for record in self:
			if record.x_first_name and record.x_last_name:				
				full = record.x_last_name.lower() + '_' + record.x_first_name.lower()
				full = full.replace (" ", "_")
				full = pat_funcs.strip_accents(full)
				record.x_full_name = full





	x_first_name = fields.Char(
		string = "Nombres", 	
		required=True, 
		default='',		
	)



	x_last_name = fields.Char(
		string = "Apellidos", 	
		required=True, 
		default='',	
	)







	x_date_consent = fields.Date(
			string = "Fecha de consentimiento informado", 	
			default = fields.Date.today, 
			#readonly = True, 
			#required=True, 
			)



	x_active = fields.Boolean(
			string = "Activa", 	
			default = True, 
			#readonly = True, 
			required=True, 
			)






	# Allergies 
	x_allergies = fields.Char(
			string = "Alergias", 

			#required=True, 
			#required=False, 
			)

	@api.onchange('x_allergies')
	def _onchange_x_allergies(self):

		if self.x_allergies != False: 
			self.x_allergies = self.x_allergies.strip().title()




	x_first_contact = fields.Selection(
			selection = pat_vars._first_contact_list, 
			string = '¿ Cómo se enteró ?',
			#default = 'none', 

			#required=True, 
			#required=False, 
			)


	# Caregiver
	x_caregiver_last_name = fields.Char(
			string = 'Apellidos',
			#default = '', 
			#required=True, 
			)

	x_caregiver_first_name = fields.Char(
			string = 'Nombres',
			#default = '', 
			#required=True, 
			)

	x_caregiver_dni = fields.Char(
			string = "DNI", 	
			#required=True, 
			)

	x_caregiver_relation = fields.Selection(
			selection = pat_vars._FAMILY_RELATION, 		
			string = 'Parentesco',
			default = 'none', 
			#required=True, 
			)



	x_country_residence= fields.Many2one(
			'res.country', 
			string = 'País de residencia', 
			default = '', 
			#required=True, 
			)

	x_education_level= fields.Selection(
			selection = pat_vars._education_level_type,
			string = 'Grado de instrucción',
			#default = 'university', 
			#required=True, 
			)



	# Control docs 

	x_control_dni_copy = fields.Boolean(
			string = 'Copia de DNI', 
			default = False 
			)

	x_control_informed_consent = fields.Boolean(
			string = 'Consentimiento informado', 
			default = False 
			)

	x_control_visia_record = fields.Boolean(
			string = 'Registro VISIA pre-procedimiento', 
			default = False 
			)

	x_control_photo_record = fields.Boolean(
			string = 'Registro fotográfico pre-procedimiento', 
			default = False 
			)

	x_control_treatment_signed_patient = fields.Boolean(
			string = 'Copia de información de tratamiento Láser firmada por el paciente', 
			default = False 
			)

	x_control_postlaser_instructions_signed = fields.Boolean(
			string = 'Copia de indicaciones post-Láser firmado por el paciente', 
			default = False 
			)

	x_control_treatment_signed_doctor = fields.Boolean(
			string = 'Informe de tratamiento Láser firmado por el doctor', 
			default = False 
			)

	x_control_clinical_analsis = fields.Boolean(
			string = 'Análisis clínicos', 
			default = False 
			)

	x_control_control_pictures = fields.Boolean(
			string = 'Fotos de controles', 
			default = False 
			)

	x_control_control_pictures_visia = fields.Boolean(
			string = 'Fotos de controles con VISIA', 
			default = False 
			)

	x_control_physician = fields.Many2one(
			'oeh.medical.physician',
			string="Médico responsable del control", 
			#required=True, 
			#index=True
			)







# ----------------------------------------------------------- On Changes ------------------------------------------------------



	# Last Name 
	@api.onchange('x_last_name', 'x_first_name')
	def _onchange_x_last_name(self):
		if self.x_last_name and self.x_first_name:
			self.name = pat_funcs.strip_accents(self.x_last_name.upper() + ' ' + self.x_first_name)




	@api.onchange('x_last_name')
	def _onchange_x_last_name_test(self):
		
		#print 'Test name'

		if self.x_last_name:
			ret = pat_funcs.test_name(self, self.x_last_name)
			
			#print ret 
			#print 
			
			return ret











	# Phone 1
	@api.onchange('phone_1')
	def _onchange_phone_1(self):
		ret = pat_funcs.test_for_digits(self, self.phone_1)
		if ret != 0: 
			return ret



	# Phone 2
	@api.onchange('phone_2')
	def _onchange_phone_2(self):
		ret = pat_funcs.test_for_digits(self, self.phone_2)
		if ret != 0: 
			return ret





	# Phone 3 - Caregiver 
	@api.onchange('phone_3')
	def _onchange_phone_3(self):
		ret = pat_funcs.test_for_digits(self, self.phone_3)
		if ret != 0: 
			return ret



	@api.onchange('street2_sel')
	def _onchange_street2_sel(self):
		self.street2 = pat_vars.zip_dic_inv[self.street2_sel]
		self.zip = self.street2_sel



	@api.onchange('street2_char')
	def _onchange_street2_char(self):
		self.street2 = self.street2_char







# ----------------------------------------------------------- Computes ------------------------------------------------------

	# Treatment count  
	x_treatment_count = fields.Integer(
			string = "Número de tratammientos",
			default = 0, 

			compute='_compute_x_treatment_count',
		)

	
	@api.multi
	#@api.depends('x_allergies')

	def _compute_x_treatment_count(self):

		for record in self:
			count = 0 

			for tr in record.treatment_ids:   
				count = count + 1  

			record.x_treatment_count = count  





	x_nr_cosmetologies = fields.Integer(

			'Nr Cosmiatrías', 

			default=0, 

			compute='_compute_x_nr_cosmetologies',
		)

	
	@api.multi
	#@api.depends('x_allergies')

	def _compute_x_nr_cosmetologies(self):

		for record in self:
			
			count = 0 

			for tr in record.cosmetology_ids:   
				count = count + 1  

			record.x_nr_cosmetologies = count  















# ----------------------------------------------------------- Buttons Update ------------------------------------------------------


	# Button - Update 
	# -------------------
	@api.multi
	def x_update(self):  

		#print 
		#print 'Update'

		self.x_date_created = self.x_date_created








# ----------------------------------------------------------- Buttons Treatment ------------------------------------------------------


	# Button - Treatment 
	# -------------------
	@api.multi
	def open_treatment_current(self):  


		treatment_id = self.env['openhealth.treatment'].search([
																		
																		('patient','=', self.id),
																
																],
																#order='start_date desc',
																order='write_date desc',
																limit=1,).id


		#print 
		#print 'Open Treatment'
		patient_id = self.id 
		#print patient_id

		return {

			# Mandatory 
			'type': 'ir.actions.act_window',
			'name': 'Open Treatment Current',



			# Window action 
			'res_model': 'openhealth.treatment',
			'res_id': treatment_id,


			# Views 
			"views": [[False, "form"]],
			'view_mode': 'form',
			'target': 'current',

			

			'flags': {
					'form': {'action_buttons': True, }
					#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
			},	

			'context':   {
				'search_default_patient': patient_id,
				'default_patient': patient_id,
			}
		}

	# open_treatment_current 








# ----------------------------------------------------------- Buttons Cosmetology ------------------------------------------------------


	# Button - Cosmetology 
	# -------------------
	@api.multi
	def open_cosmetology_current(self):  


		cosmetology_id = self.env['openhealth.cosmetology'].search([
																		('patient','=', self.id),
																],
																order='start_date desc',
																limit=1,).id




		#print 
		#print 'Open Cosmetology'
		patient_id = self.id 
		#print patient_id

		return {

			# Mandatory 
			'type': 'ir.actions.act_window',
			'name': 'Open cosmetology Current',


			# Window action 
			'res_model': 'openhealth.cosmetology',
			'res_id': cosmetology_id,


			# Views 
			"views": [[False, "form"]],
			'view_mode': 'form',
			'target': 'current',



			'flags': {
					'form': {'action_buttons': True, }
					#'form': {'action_buttons': True, 'options': {'mode': 'edit'}}
			},	



			'context':   {
				'search_default_patient': patient_id,
				'default_patient': patient_id,
			}
		}

	# open_cosmetology_current 






# ----------------------------------------------------------- Actions ------------------------------------------------------

	# Removem
	#@api.multi
	#def remove_myself(self):  	
	#	self.unlink()






# ----------------------------------------------------------- CRUD ------------------------------------------------------

# Create 
	@api.model
	def create(self,vals):

		#print 'jx'
		#print 'Patient - Create - Override'
		#print vals
	


		# Put your logic here 
		res = super(Patient, self).create(vals)
		# Put your logic here 



		# My logic 
		# Create a Treatment - When Patient is created - DEPRECATED !
		#name = vals['name']
		#patient_id = self.env['oeh.medical.patient'].search([('name', '=', name),]).id 
		#treatment = self.env['openhealth.treatment'].create({'patient': patient_id,})

		return res
	# CRUD - Create 




# Write 
	@api.multi
	def write(self,vals):

		print 
		print 'CRUD - Patient - Write'
		print 
		print vals
		print 
		#print 

		#if vals['x_doctor'] != False: 
		#	print vals['x_doctor']
		#if vals['user_id'] != False: 
		#	print vals['user_id']



		#Write your logic here
		res = super(Patient, self).write(vals)
		#Write your logic here




		# Validations
		#self.email = self.email.lower()
		#self.street = self.street.title()



		# Update Partner 
		if self.street != False:

			self.partner_id.street = self.street

			self.partner_id.street2 = self.street2

			self.partner_id.street2_sel = self.street2_sel




			self.partner_id.zip = self.zip

			self.partner_id.city = self.city.title()

			self.partner_id.state_id = self.state_id

			self.partner_id.country_id = self.country_id

			self.partner_id.x_dni = self.x_dni

			self.partner_id.email = self.email



			self.partner_id.phone = self.phone

			self.partner_id.mobile = self.mobile



			self.partner_id.lang = 'es_ES'



		if self.x_ruc != False:

			self.partner_id.x_ruc = self.x_ruc

			self.partner_id.x_firm = self.x_firm



		#print 
		#print 

		return res

	# CRUD - Write 

