# -*- coding: utf-8 -*-





_dic_prefix = {
					#'ticket_receipt': 	'001',
					#'ticket_invoice': 	'001',
					#'ticket_receipt': 	'B01', 
					#'ticket_invoice': 	'F01', 
					'ticket_receipt': 	'B001',
					'ticket_invoice': 	'F001',


					#'receipt': 			'BB1', 
					#'invoice': 			'FF1', 
					'receipt': 			'001', 
					'invoice': 			'001', 


					#'sale_note': 		'S01', 
					#'advertisement': 	'A01', 
					'sale_note': 		'001', 
					'advertisement': 	'001', 
}



_dic_padding = {
					#'ticket_receipt': 	10,
					#'ticket_invoice': 	10,
					#'ticket_invoice': 	6,
					'ticket_receipt': 	8,
					'ticket_invoice': 	8,

					'receipt': 			6,
					'invoice': 			6,
					'sale_note': 		10, 
					'advertisement': 	10, 
}









_dic_tc_type = {
					'ticket_invoice': 	'ticket_invoice',	
					'ticket_receipt': 	'ticket_receipt',
					'invoice': 			'invoice',	
					'receipt': 			'receipt',

					'ticket_invoice_cancel': 	'ticket_invoice',	
					'ticket_receipt_cancel': 	'ticket_receipt',
					'invoice_cancel': 			'invoice_cancel',	
					'receipt_cancel': 			'receipt_cancel',
}






_dic_type_code = {
					'ticket_invoice': 	'01',	
					'ticket_receipt': 	'03',

					#'invoice': 		'01',
					#'receipt': 		'03',
					'invoice': 			'11',		# Not Sunat Compliant !
					'receipt': 			'13',		# Not Sunat Compliant !

					'advertisement': 	'14',
					'sale_note': 		'15',
}




# State - Current !!
_state_list = [

				#('draft', 		'Quotation'),
				#('sent', 		'Quotation Sent'),
				#('sale', 		'Sale Order'),
				#('done', 		'Done'),
				#('cancel', 	'Cancelled'),

				#('draft', 		'Presupuesto'),
				#('sent', 		'Pagado'),
				#('sale', 		'Facturado'),				
				#('done', 		'Completo'),
				#('cancel', 		'Anulado'),



				('draft', 		'Presupuesto'),
				('sent', 		'Generado'),			
				('validated', 	'Validado'),			
				('sale', 		'Pagado'),				
				('done', 		'Completo'),
				('cancel', 		'Anulado'),

				('credit_note', 'Nota de Credito'),


				#('printed', 	'Impreso'),
				#('editable', 	'e'),
			]




# Legacy 
_dic_type_leg = {

						'BOL' : 'receipt', 		
						'FAC' : 'invoice', 		
						'TKB' : 	'ticket_receipt', 		
						'TKF' : 	'ticket_invoice', 
						'advertisement' : 	'advertisement', 		
						'CE' : 		'sale_note', 		
						False: False, 
			}







# Deprecated ?

#_owner_type_list = [
#						('product', 			'Product'),
#						('service', 			'Servicio'),
#		]



#_sale_docs_list = [
		#('none','Ninguno'), 
#		('receipt','Boleta'), 
#		('invoice','Factura'), 
#		('advertisement','Canje publicidad'), 
#		('sale_note','Canje (nv)'), 
#		('ticket_receipt','Ticket boleta'), 
#		('ticket_invoice','Ticket factura'), 
		#('',''), 
#	]


#_dic_model = {
#
#						'receipt' : 'openhealth.receipt', 		
#						'invoice' : 'openhealth.invoice', 		
#						'advertisement' : 	'openhealth.advertisement', 		
#						'sale_note' : 		'openhealth.sale_note', 		
#						'ticket_receipt' : 	'openhealth.ticket_receipt', 		
#						'ticket_invoice' : 	'openhealth.ticket_invoice', 		
#						False :	False, 
#			}


# Deprecated !!!

#_x_state_list = [
#				('draft', 			'Presupuesto'),
#				('payment', 		'Pagado'),
				#('proof', 		    'Comprobante'),
				#('machine', 		'Reservación de Sala'),
				#('sale', 			'Venta'),
#				('sale', 			'Confirmado'),
				#('confirmed', 		'Confirmado'),
				#('invoice', 		'Facturado'),
#				('done', 			'Completo'),
#				('printed', 		'Impreso'),
#				('cancel', 			'Cancelado'),
#]

