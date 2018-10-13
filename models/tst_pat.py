# -*- coding: utf-8 -*-
#
# 	tst_pat.py
#  	
# 	Test Case for - Patients
#
#	Created: 			28 Sep 2018
#	Last up: 	 		28 Sep 2018
# 
import creates as cre


# ----------------------------------------------------------- Test Cases - Treatment ------------------------------------------------------
# Test Cases - Patients
def test_cases(self, container_id, patient_id=False, partner_id=False, doctor_id=False, treatment_id=False, pl_id=False):
	print 
	print 'Tst - Patient - Test Init'
	print self 


	_pars = [
				# Patient 1 - Passport
				{
						#'test_case': 	'passport, ticket_receipt', 
						'test_case': 	'passport, receipt', 

						'name': 		'NUÑEZ NUÑEZ FATIMA', 
						'name_last': 	'nuñez nuñez', 
						'name_first':  	'fatima', 
						'ruc': 			False, 
						'firm': 		False, 

						'id_doc_type': 	'passport', 
						'id_doc':  		'PA-123456789', 
						'dni':			False, 

						'sex': 			'Female', 
						'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

						'id_code':  	False,
				}, 


				# Patient 2 - CE
				{
						#'test_case': 	'foreign_card, ticket_receipt', 
						'test_case': 	'foreign_card, invoice', 

						'name': 		'RABELAIS RABELAIS FRANCOIS', 
						'name_last': 	'rabelais rabelais', 
						'name_first':  	'francois', 
						'ruc': 			False, 
						'firm': 		False, 

						'id_doc_type': 	'foreign_card', 
						'id_doc':  		'CE-123456789', 
						'dni':			False, 

						'sex': 			'Male', 
						'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

						'id_code':  	False,
				}, 



				# Patient 3 - PTP
				{
						'test_case': 	'ptp, ticket_receipt', 

						'name': 		'TOTTI TOTTI FRANCESCO', 
						'name_last': 	'totti totti', 
						'name_first':  	'francesco', 
						'ruc': 			False, 
						'firm': 		False, 

						'id_doc_type': 	'ptp', 
						'id_doc':  		'PTP-12345678', 
						'dni':			False, 

						'sex': 			'Male', 
						'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

						'id_code':  	False,
				}, 



				# Patient 4 - OTHER
				{
						'test_case': 	'other, ticket_receipt', 

						'name': 		'MICHELOT MICHELOT IVANNA', 
						'name_last': 	'michelot michelot', 
						'name_first':  	'ivanna', 
						'ruc': 			False, 
						'firm': 		False, 

						'id_doc_type': 	'other', 
						'id_doc':  		'1234567', 
						'dni':			False, 

						'sex': 			'Female', 
						'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

						'id_code':  	False,
				}, 





				# Patient 5 - DNI
				{
						'test_case': 	'dni, ticket_receipt', 

						'name': 		'REVILLA REVILLA JOSEX', 
						'name_last': 	'revilla revilla', 
						'name_first':  	'josex', 
						'ruc': 			False, 
						'firm': 		False, 

						'id_doc_type': 	'dni', 
						'id_doc':  		'12345678', 
						'dni':			False, 

						'sex': 			'Male', 
						'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

						'id_code':  	False,
				}, 



				# Patient 6 - RUC
				{
						'test_case': 	'other, ticket_invoice', 

						'name': 		'RONDON RONDON SEBASTIAN', 
						'name_last': 	'rondon rondon', 
						'name_first':  	'sebastian', 
						'ruc': 			'12345678902', 
						'firm': 		'Rondon y Asociados', 

						'id_doc_type': 	'other', 
						'id_doc':  		'12345', 
						'dni':			False, 

						'sex': 			'Male', 
						'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

						'id_code':  	False,
				}, 



				#  Patient 7 - DNI, Legacy 
				{
						'test_case': 	'dni, ticket_receipt, legacy', 

						'name': 		'NEO NEO NEODIUMX', 
						'name_last': 	'neo neo', 
						'name_first':  	'neodiumx', 
						'ruc': 			False, 
						'firm': 		False, 

						'id_doc_type': 	False, 
						'id_doc':  		False, 
						'dni':			'49171890', 

						'sex': 			'Male', 
						'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

						'id_code':  	'000003',
				}, 



				# Patient 8 - Ticket Receipt Canceled 
				{
						'test_case': 	'dni, ticket_receipt_cancel', 

						'name': 		'DIBALA DIBALA PAOLO', 
						'name_last': 	'dibala dibala', 
						'name_first':  	'paolo', 
						'ruc': 			False, 
						'firm': 		False, 

						'id_doc_type': 	'dni', 
						'id_doc':  		'49171891', 
						'dni':			False, 

						'sex': 			'Male', 
						'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

						'id_code':  	False,
				}, 


				# Patient 9 - Ticket Invoice Canceled
				{
						'test_case': 	'dni, ticket_invoice_cancel', 

						'name': 		'COMANECI COMANECI NADIA', 
						'name_last': 	'comaneci comaneci', 
						'name_first':  	'nadia', 
						'ruc': 			'12345678903', 
						'firm': 		'Comaneci y Asociados', 

						'id_doc_type': 	'dni', 
						'id_doc':  		'12345679', 
						'dni':			False, 

						'sex': 			'Female', 
						'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

						'id_code':  	False,
				}, 





				# x
				#{
				#		'test_case': 	'', 

				#		'name': 		'', 
				#		'name_last': 	'', 
				#		'name_first':  	'', 
				#		'ruc': 			False, 
				#		'firm': 		False, 

				#		'id_doc_type': 	'', 
				#		'id_doc':  		'', 
				#		'dni':			False, 

				#		'sex': 			'Female', 
				#		'address': 		'Av. San Borja Norte 610,San Borja,Lima',						

				#		'id_code':  	False,
				#}, 
		]


	
	pat_array = []

	for par in _pars: 
		print par 
		print par['test_case']
		print par['name']
		print 


		# Init
		test_case = 	par['test_case']

		id_doc_type = 	par['id_doc_type']
		id_doc = 		par['id_doc']
		dni = 			par['dni']

		name = 			par['name']
		name_last =		par['name_last']
		name_first = 	par['name_first']

		sex = 			par['sex']
		address = 		par['address']
		
		# Nils 
		name_last = 	par['name_last']
		name_first = 	par['name_first']
		ruc = 			par['ruc']
		firm = 			par['firm']

		id_code = 		par['id_code']


		# Create 
		#patient = cre.create_patient(self, container_id, test_case, name, sex, address, id_doc_type, id_doc, ruc, firm, doctor_id, name_last, name_first)
		patient = cre.create_patient(self, container_id, test_case, name, sex, address, id_doc_type, id_doc, ruc, firm, doctor_id, name_last, name_first, id_code, dni)


		pat_array.append(patient)

	return pat_array

	# test_cases

