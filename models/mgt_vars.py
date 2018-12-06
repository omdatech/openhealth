# -*- coding: utf-8 -*-



# States
_state_arr_list = [
					('sale,cancel,credit_note', 'sale,cancel,credit_note'),
					('sale,cancel', 'sale,cancel'),
					('sale', 		'sale'),
					('cancel', 		'cancel'),
]



# types
_type_arr_list = [
				('all', 'all'),

				('ticket_receipt,ticket_invoice,receipt,invoice,sale_note,advertisement', 'ticket_receipt,ticket_invoice,receipt,invoice,sale_note,advertisement'),

				('ticket_receipt,ticket_invoice,receipt,invoice', 	'ticket_receipt,ticket_invoice,receipt,invoice'),
				('ticket_receipt,ticket_invoice', 	'ticket_receipt,ticket_invoice'),
				('ticket_receipt', 					'ticket_receipt'),
				('ticket_invoice', 					'ticket_invoice'),
]




_h_name = {
				# 13 Jul 2018 
				'other': 		'Otro',



				'product': 		'Producto',

				'consultation': 'Consulta', 		
				'consultation_gyn': 'Consulta Ginecológica', 		
				'consultation_100': 'Consulta 100', 		
				'consultation_0': 'Consulta Gratuita', 		

				#'procedure': 	'Procedimiento', 		
				'procedure': 	'Procedimiento Laser', 		
				'laser': 		'Laser', 		

				'medical': 		'Tratamiento Médico', 		
				'cosmetology': 	'Cosmeatria', 	

				'card': 		'Tarjeta Vip', 	
				'kit': 			'Kits', 	
				'topical': 		'Cremas', 	




					'laser_co2' : 		'Laser Co2', 		
					'laser_excilite' : 	'Laser Exc', 		
					'laser_ipl' : 		'Laser Ipl', 		
					'laser_ndyag' : 	'Laser Ndyag', 		
					'laser_quick' : 	'Quick Laser', 		


					'criosurgery' : 			'Criocirugía', 		
					'intravenous_vitamin' : 	'Vitamina Intravenosa', 		
					'botulinum_toxin' : 		'Toxina Botulínica', 		
					'hyaluronic_acid' : 		'Acido Hialurónico', 		

					'mesotherapy_nctf': 		'Mesoterapia NCTF', 
					'infiltration_scar': 		'Infiltración Cicatriz', 
					'infiltration_keloid': 		'Infiltración Queloide', 


				#False: False, 	
}










_h_family_sp = {
				'product': 		'Producto',
				'consultation': 'Consulta',
				'procedure': 	'Procedimiento',
				'medical': 		'Tratamiento Médico',
				'cosmetology': 'Cosmeatria',
				#False: False, 	
}
