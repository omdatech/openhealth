# -*- coding: utf-8 -*-


from openerp import models, fields, api
import datetime








# ----------------------------------------------------------- Create Procedure  ------------------------------------------------------

@api.multi

#def create_app_procedure(self, appointment_date, doctor_id, patient_id, treatment_id, x_create_procedure_automatic, flag_machine):
def create_app_procedure(self, adate_base, doctor_id, patient_id, treatment_id, x_create_procedure_automatic, flag_machine):


		print 
		print 'create app procedure'




		# Consultation 
		#date_format = "%Y-%m-%d %H:%M:%S"
		#adate_con = datetime.datetime.strptime(appointment_date, date_format)
		#delta_fix = datetime.timedelta(hours=1.5)
		#adate_base = adate_con + delta_fix





		# Doctor 
		doctor = self.env['oeh.medical.physician'].search([('id', '=', doctor_id)])
		doctor_name = doctor.name

		k = 0
		duration = 0.5 
		ret = 1



		# Log
		#print appointment_date
		#print doctor_id
		#print patient_id
		#print adate_con





		# Deltas
		delta_var = datetime.timedelta(hours=0.25)

		# Loop 
		while not ret == 0:


			# Procedure 
			#adate_pro = adate_con + delta_fix + k*delta_var
			adate_pro = adate_base + k * delta_var


			adate_pro_str = adate_pro.strftime("%Y-%m-%d %H:%M:%S")



			# Check for collisions 
			#ret, doctor_name, start, end = check_for_collisions(self, adate_pro_str, doctor_name, duration, False)
			ret, doctor_name, start, end = check_for_collisions(self, adate_pro_str, doctor_name, duration, False, 'doctor')



			if ret == 0: 	# Success - No Collisions
			
				print 'CRUD: Create !!!'



				# Create machine 
				x_machine = 'jx'

				if flag_machine:


					#start_machine = False 
					start_machine = self.x_machine


					#x_machine = search_machine(self, adate_pro_str, doctor_name, duration)
					x_machine = search_machine(self, adate_pro_str, doctor_name, duration, start_machine)



				if x_machine != False:


					if flag_machine:
						# Create Appointment - Machine 
						app = self.env['oeh.medical.appointment'].create(
																	{
																		'appointment_date': adate_pro_str,

																		'doctor': 		doctor_id,
																		'patient': 		patient_id,	
																		'treatment': 	treatment_id, 

																		'duration': 	duration,
																		'x_type': 		'procedure',
																		'x_create_procedure_automatic': False, 

																		'x_machine': 	x_machine,
							                    						'x_target': 	'machine',
																	}
																)

						

					else:
						# Create Appointment - Doctor  
						app = self.env['oeh.medical.appointment'].create(
																	{
																		'appointment_date': adate_pro_str,

																		'doctor': 		doctor_id,
																		'patient': 		patient_id,	
																		'treatment': 	treatment_id, 

																		'duration': 	duration,
																		'x_type':		'procedure',
																		'x_create_procedure_automatic': x_create_procedure_automatic,

																		'state':		'pre_scheduled',

							                    						'x_target': 	'doctor',

																		#'x_chief_complaint': x_chief_complaint, 

															}
													)


				else:
					k = k + 1 	# Collision
					ret = 1


			
			else:			# Collision 
				k = k + 1


		
			#if ret != 0:
			
			#			return {
			#						'warning': {
			#							'title': "Error: Colisión !",
			#							'message': 'Cita ya existente, con el ' + doctor_name + ": " + start + ' - ' + end + '.',
			#					}}


		print 
		print 'k'
		print k
		print 

		return app 

# create_app_procedure








# ----------------------------------------------------------- Machines  ------------------------------------------------------

@api.multi

#def search_machine(self, appointment_date, doctor_name, duration):
def search_machine(self, appointment_date, doctor_name, duration, start_machine):

	m_list = ['laser_co2_1', 'laser_co2_2', 'laser_co2_3']


	_hash_machine_idx = {

							False:			0, 

							'laser_co2_1':	1, 
							'laser_co2_2':	2, 
							'laser_co2_3':	0, 
					}

	
	#idx = 0 
	idx = _hash_machine_idx[start_machine]

	
	x_machine = m_list[idx]


	target = 'machine'


	ret = 1 



	while not ret == 0:

		#ret, doctor_name, start, end = appfuncs.check_for_collisions(self, appointment_date, doctor, duration, x_machine)
		#ret, doctor_name, start, end = check_for_collisions(self, appointment_date, doctor_name, duration, x_machine)
		ret, doctor_name, start, end = check_for_collisions(self, appointment_date, doctor_name, duration, x_machine, target)



		if ret != 0:	# Error 

			idx = idx + 1

			if idx == 3:
				#idx = 0
				return False

			x_machine = m_list[idx]




			#return {'warning': {'title': "Error: Colisión !",'message': 'La sala ya está reservada: ' + start + ' - ' + end + '.',}}


		else: 			# Success 

			print 'Success !'

			return x_machine





# ----------------------------------------------------------- Collisions  ------------------------------------------------------

@api.multi

#def check_for_collisions(self, appointment_date, doctor_name, duration):
#def check_for_collisions(self, appointment_date, doctor_name, duration, x_machine):
def check_for_collisions(self, appointment_date, doctor_name, duration, x_machine, target):


		print 
		print 'jx'
		print 'Check for collision'

		print appointment_date, doctor_name, duration, x_machine
		print 

		dt = appointment_date[2:10]
		#print dt
		#print 



		# Search for the rec set
		#if x_machine == False:
		#	app_ids = self.env['oeh.medical.appointment'].search([
		#															('doctor', '=', doctor_name), 
		#															('appointment_date', 'like', dt), 
		#															('x_machine', '=', x_machine),
		#														])
		#else:
		#	app_ids = self.env['oeh.medical.appointment'].search([
		#															('appointment_date', 'like', dt), 
		#															('x_machine', '=', x_machine)  
		#														])


		# Always a total check
		if target == 'doctor':
			app_ids = self.env['oeh.medical.appointment'].search([
																	('appointment_date', 'like', dt), 

																	('doctor', '=', doctor_name), 
																	#('x_machine', '=', x_machine),
																])
		if target == 'machine':
			app_ids = self.env['oeh.medical.appointment'].search([
																	('appointment_date', 'like', dt), 

																	#('doctor', '=', doctor_name), 
																	('x_machine', '=', x_machine),
																])


		print app_ids 





		# Appointment end 
		date_format = "%Y-%m-%d %H:%M:%S"

		delta = datetime.timedelta(hours=duration)

		sd = datetime.datetime.strptime(appointment_date, date_format)
		
		ae_dt = delta + sd

		ae = ae_dt.strftime("%Y-%m-%d %H:%M:%S")


		#print delta
		#print sd 
		#print ae_dt
		#print 



		# Check if Collision 
		ad = appointment_date

		for app in app_ids:

			print app

			start = app.appointment_date

			end = app.appointment_end


			if 	app.state != 'pre_scheduled_control' and  	(	
															(ad >= start and ae <= end)  or  (ad <= start and ae >= end)  	or    (ad < start and ae > start)  or  (ad < end and ae > end)
															): 


				#print 'Collision !!!'



				# Local
				delta = datetime.timedelta(hours=5)


				# Start 
				sd = datetime.datetime.strptime(start, date_format)
				sl =  sd - delta 
				#sl = start_local.strftime("%Y-%m-%d %H:%M:%S")
				start_local = sl.strftime("%H:%M")


				# End 
				sd = datetime.datetime.strptime(end, date_format)
				el =  sd - delta 
				end_local = el.strftime("%H:%M")



				#print delta
				#print end_local
				#print el



				# Did not pass 
				return -1, doctor_name, start_local, end_local




		# Passed test - All is Ok 
		return 0, '', '', '' 




