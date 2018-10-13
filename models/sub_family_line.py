# -*- coding: utf-8 -*-
#
# 		Family Line 
# 
# Last up: 			20 Aug 2018
# Last up: 			20 Aug 2018
#
from openerp import models, fields, api

import mgt_vars


class SubFamilyLine(models.Model):	

	_inherit = 'openhealth.management.line'
	
	_name = 'openhealth.management.sub_family.line'
	
	#_order = 'idx asc'



# ----------------------------------------------------------- Update ------------------------------------------------------

	# Update Fields
	@api.multi
	#def update_fields(self):  
	def update(self):  

		#print 
		#print 'Update fields - Mgt Line - Family'
		#print 


		# Name Sp 
		if self.name in mgt_vars._h_name: 
			self.name_sp = mgt_vars._h_name[self.name]
		else: 
			self.name_sp = self.name



		# Idx 
		_h_idx = {

					False: 0, 		

					'laser_co2': 			10,
					'laser_excilite': 		11,
					'laser_ipl': 			12,
					'laser_ndyag': 			13,
					'laser_quick': 			14,


					'criosurgery' : 	31, 		
					'botulinum_toxin' : 32, 		
					'hyaluronic_acid' : 33, 		


					'cosmetology': 		70,

					'product': 			80, 	
					
					'consultation': 	90, 		
		}


		# Medical 
		medical_arr = [
							'botulinum_toxin', 		# Bot
							'criosurgery', 			# Crio
							'hyaluronic_acid', 		# Hial
							
							'infiltration_scar', 	# Infil
							'infiltration_keloid', 	# Infil

							'intravenous_vitamin', 		# Intra
							'lepismatic', 				# Lep
							
							'plasma', 				# Pla
							'mesotherapy_nctf', 	# Meso
							'sclerotherapy', 		# Escl
		]



		# Idx
		if self.name in _h_idx: 
			self.idx = _h_idx[self.name]
		else: 
			self.idx = 100




		# Meta 
		if self.name in ['laser_co2', 'laser_excilite', 'laser_ipl', 'laser_ndyag', 'laser_quick']: 

			self.meta = 'laser'
			self.meta_sp = 'Laser'


		#elif self.name in ['criosurgery', 'botulinum_toxin', 'hyaluronic_acid', '']: 
		elif self.name in medical_arr: 

			self.meta = 'medical'
			self.meta_sp = 'TM'



		elif self.name in ['cosmetology']: 

			self.meta = 'cosmetology'
			self.meta_sp = 'Cosmiatria'



		elif self.name in ['consultation']: 

			self.meta = 'consultation'
			self.meta_sp = 'Consulta'


		elif self.name in ['product']: 

			self.meta = 'product'
			self.meta_sp = 'Producto'



		elif self.name in ['other']: 

			self.meta = 'other'
			self.meta_sp = 'Otros'

	# update_fields
