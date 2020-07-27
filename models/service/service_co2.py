# -*- coding: utf-8 -*-
"""
 	Service Co2 - Legacy 2018
 
 	Created: 			2016
 	Last up: 	 		24 April 2019

	24 Apr 2019:		Cleanup after 2019 PL. Must disappear:
						- Onchanges. 
"""

from openerp import models, fields, api
from datetime import datetime
from openerp.addons.openhealth.models.product import prodvars

class ServiceCo2(models.Model):
	"""
	Service Co2
	"""
	_name = 'openhealth.service.co2'

	_inherit = 'openhealth.service'
	

# ----------------------------------------------------------- Natives ------------------------------
	service = fields.Many2one(
			'product.template',
			domain = [
						('type', '=', 'service'),
						('x_treatment', '=', 'laser_co2'),
					],
		)

# ---------------------------------------------- Fields --------------------------------------------------------
	# Laser 
	laser = fields.Selection(
			selection = prodvars._laser_type_list, 
			string="Láser", 			
			default='laser_co2',
			index=True,
		)

	# Pathology
	#pathology = fields.Selection(
	#		selection = prodvars._pathology_list, 
	#		string="Patología", 
	#	)

	# Zone 
	#zone = fields.Selection(
	#		selection = prodvars._zone_list,
	#		string="Zona", 
	#	)