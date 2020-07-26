# -*- coding: utf-8 -*-
"""
	Order Funcs
	Encapsulate Order Business Rules
	Created: 			 4 Dec 2019
	Last up: 	 		26 Jul 2020
"""
from __future__ import print_function
import datetime
from openerp.exceptions import Warning as UserError


def get_doctor_uid(doctor):
	"""
	Used by Order
	"""
	print('get_doctor_uid')
	if doctor.name != False:
		uid = doctor.x_user_name.id
		doctor_uid = uid
	else: 
		doctor_uid = False
	return doctor_uid

# ----------------------------------------------------------- Create procedure ----------------
def create_procedure(treatment, order_line):
	"""
	Used by Order
	"""
	print('Create Procedure')
	if treatment.name:
		for line in order_line:
			product = line.product_id
			if product.is_procedure():
				treatment.create_procedure_auto(product)
			line.update_recos()
		# Update Order - Dep ?
		#set_procedure_created(True)

# ----------------------------------------------------------- Check Id Doc ----------------
def check_docs(type, ruc, id_doc, id_doc_type):
	"""
	Used by Order
	"""
	# Invoice
	if type in ['ticket_invoice', 'invoice']:
		if ruc in [False, '']:
			msg = "Error: RUC Ausente."
			raise UserError(_(msg))

	# Receipt
	elif type in ['ticket_receipt', 'receipt']:
		if id_doc_type in [False, '']  or id_doc in [False, '']:
			msg = "Error: Documento de Identidad Ausente."
			raise UserError(_(msg))

# ----------------------------------------------------------- Get Treatment ----------------
def get_title(type):
	"""
	Used by Order
	"""
	if type in ['ticket_receipt', 'receipt']:
		title = 'Boleta de Venta Electrónica'
	elif type in ['ticket_invoice', 'invoice']:
		title = 'Factura de Venta Electrónica'
	else:
		title = 'Venta Electrónica'
	return title 


# ----------------------------------------------------------- Get Treatment ----------------
def get_treatment(env, patient_name, doctor_name):
	"""
	Used by Order
	"""
	if doctor_name:
		treatment = env.search([('patient', '=', patient_name),
								('physician', '=', doctor_name),
							],
								order='write_date desc',
								limit=1,
							)
	return treatment

# ----------------------------------------------------------- Get Patient ids ----------------
def get_patient_ids(patient):
	"""
	Used by Order
	"""
	
	if patient.name != False:
		dni = False 
		ruc = False
		partner_id = patient.partner_id.id
		# Id Doc
		if patient.x_id_doc != False:
			id_doc = patient.x_id_doc
			id_doc_type = patient.x_id_doc_type
		# Get x Dni
		elif patient.x_dni not in [False, '']:
			id_doc = patient.x_dni
			id_doc_type = 'dni'
			dni = patient.x_dni
		# Ruc
		if patient.x_ruc != False:
			ruc = patient.x_ruc

	return partner_id, dni, ruc, id_doc, id_doc_type


# ----------------------------------------------------------- Ticket - Get Amount Flow ----------------
def get_amount_flow(block_flow, state, credit_note_amount, amount_total):
	"""
	Used by Order
	"""
	if block_flow:
		value = 0
	elif state in ['credit_note']  and  credit_note_amount not in [0, False]:
		value = - credit_note_amount
	else:
		value = amount_total
	return value

# ----------------------------------------------------------- Ticket - Get Raw Line - Aux ----------------
def get_date_corrected(date_order):
	"""
	Used by:
		- Get Ticket Raw
	"""
	print()
	print('Get Date Corrected')
	DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
	date_field1 = datetime.datetime.strptime(date_order, DATETIME_FORMAT)
	date_field2 = date_field1 + datetime.timedelta(hours=-5, minutes=0)
	DATETIME_FORMAT_2 = "%d-%m-%Y %H:%M:%S"
	date_corrected = date_field2.strftime(DATETIME_FORMAT_2)
	return date_corrected

# ----------------------------------------------------------- Ticket - Get Raw Line - Aux ----------------
def get_credit_note_type(self):
	"""
	Used by:  
		- Get Ticket Raw
	"""
	_dic_cn = {
				'cancel': 					'Anulación de la operación.',
				'cancel_error_ruc': 		'Anulación por error en el RUC.',
				'correct_error_desc': 		'Corrección por error en la descripción.',
				'discount': 				'Descuento global.',
				'discount_item': 			'Descuento por item.',
				'return': 					'Devolución total.',
				'return_item': 				'Devolución por item.',
				'bonus': 					'Bonificación.',
				'value_drop': 				'Disminución en el valor.',
				'other': 					'Otros.',
				False: 						'',
	}

	return _dic_cn[credit_note_type]

