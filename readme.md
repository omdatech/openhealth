# Open Health - ODOO 9 MODULE - PYTHON

## Description:
Service Oriented Module for Odoo. 
Odoo is an ERP system for a Clinic. 
Inherits OeHealth. 
Contains ALL the Data Model. 
Business logic is in classes and libraries.


## Created: 
11 Sep 2016

## Last updated: 
29 Oct 2019

## Database: 
Postgres

## Contains:
- All External Dependencies,
- All Models,
- All Users,
- All Views,
- All Security,
- All Data.


## External modules:
- Spanish translation,
- Oehealth,
- Base multi image,
- Web Export View, 
- Accounting and Finance. Adjust tax to zero.


## Python Libs:
- Numpy, Num2words, Pandas, QrCode, 
- Unidecode - dep
- pysftp - dep


## For PDF Reporting (tickets):
- Install wkhtmltopdf (0.12.2 v). Other versions will not work.


## For Tickets (right button printing):
- On Chrome, install extension: PDF Viewer. Link it to Adobe Reader. 


## Deprecated services: 
- Ooor, 
- Testcafe, 
- Auto-backup, 
- Inventory. 


## Remember Robert C. Martin:
- Respect the Law of Demeter: avoid Train Wreckages. When you see more than two dots, this needs fixing.
- Do not mix the Data Model and Business Rules. Encapsulate Business Rules in a separate module. 
- Use Three layered model: Odoo Active Data - Customized Class with BR - General purpose Library.
- Handle Exceptions.
- The Database should not contain Business rules. Remove computes.


## Always clean your System: 
- Remove Procurement Orders, 
- Remove Stock Moves,
- Remove Products Consumables,
- Remove Computes.





## Author': Javier Revilla

## Website: http://jrevilla.com

## Category: Object Oriented, Service Oriented, Medical Services

## Version: 7.0

## Depends': ['base', 'oehealth', 'base_multi_image'],




### Products ----------------------------------------------------------

	#'data/categs/base_data_categs_prods.xml',
	#'data/allergies/allergy.xml',
	#'data/prods/odoo_data_products.xml',
	#'data/prods/odoo_data_products_new.xml',
	#'data/prods/odoo_data_services_consult.xml',
	#'data/prods/odoo_data_services_co2.xml',
	#'data/prods/odoo_data_services_exc.xml',
	#'data/prods/odoo_data_services_m22.xml',
	#'data/prods/odoo_data_services_med.xml',
	#'data/prods/odoo_data_services_cos.xml',
	#'data/prods/odoo_data_services_med_dep.xml',



# Users -----------------------------------------------------------------------

	# Categs
	'data/categs/base_data_categs_partners.xml',

	# Users
	'data/users/base_data_users_generics.xml',                 
	'data/physicians/base_data_physicians.xml',                
	'data/physicians/base_data_physicians_inactive.xml',        
	'data/users/base_data_users_platform.xml',  
	'data/users/base_data_users_cash.xml',
	'data/users/base_data_users_account.xml',       
	'data/users/base_data_users_managers.xml',  
	'data/users/base_data_users_doctors.xml',
	'data/users/base_data_users_assistants.xml',    
	'data/users/base_data_users_directors.xml',  

	# Inactive
	'data/users/base_data_users_inactive.xml', 

	# Users Tacna
	'data/users/base_data_users_tacna.xml',



# Security --------------------------------------------------------------------
	
	'security/openhealth_security.xml',             
	'security/openhealth_security_readers.xml',   	
	'security/openhealth_security_managers.xml',
	'security/ir.model.access.csv',	
	'security/ir.rule.xml',              




# Configurator ------------------------------------------------------
	
	'views/configurators/configurator_emr.xml',         # Includes Menu



# Actions ------------------------------------------------------

	'views/patients/patient_actions.xml',




# ----------------------------------------------------------- Recent ------------------------------------------------------

# Produc ------------------------------------------------------

	# Product Selector  - RSP
	#'views/report_sale/report_sale_product.xml',
	#'views/report_sale/item_counter.xml',
	'views/rsp/report_sale_product.xml',
	'views/rsp/item_counter.xml',


# Accounting ------------------------------------------------------

	# Account - Payments
	#'views/payment_method/payment_method_line.xml',
	'views/orders/payment_method/payment_method_line.xml',


	# Account
	'views/account/account_line.xml',
	'views/account/account_line_actions.xml',
	'views/account/account_contasis_actions.xml',
	'views/account/account_contasis.xml',

	# Electronic
	'views/electronic/electronic_order.xml',
	'views/electronic/electronic_line.xml',


# Marketing ------------------------------------------------------

	# Marketing 
	'views/marketing/patient_line_search.xml',
	'views/marketing/patient_line.xml',
	'views/marketing/patient_line_actions.xml',
	'views/marketing/patient_line_pivot.xml',
	'views/marketing/marketing_order_line.xml',
	'views/marketing/marketing_reco_line.xml',
	'views/marketing/media_line.xml',
	'views/marketing/histogram.xml',
	'views/marketing/place_actions.xml',
	'views/marketing/place_pivot.xml',
	'views/marketing/place.xml',
	'views/marketing/marketing.xml',
	'views/marketing/marketing_pivot.xml',


# Management ------------------------------------------------------

	# Management 
	'views/management/management_day_line.xml',
	'views/management/management_day_doctor_line.xml',
	'views/management/management_family_line.xml',
	'views/management/management_subfamily_line.xml',
	'views/management/management_order_line.xml',
	'views/management/management_doctor_line.xml',
	'views/management/management_trees.xml',
	'views/management/management_actions.xml',
	'views/management/management.xml',
	



# ----------------------------------------------------------- Views - Base Actions ------------------------------------------------------

	# Base - Form and List Actions - Must be the first
	'views/base_actions.xml',                                       # Very important - All Actions should go here - Dependencies
	



# ----------------------------------------------------------- Reports ------------------------------------------------------

	# Patient
	'reports/patient/report_patient.xml',

	# Formats
	'reports/paper_format.xml',

	# Ticket - Electronic 
	'reports/report_layouts.xml',
	'reports/print_ticket_receipt_electronic.xml',



# ----------------------------------------------------------- Views - Actions ------------------------------------------------------

	# Service
	#'views/services/service_search.xml',  	# Dep


# ----------------------------------------------------------- Views - First Level ------------------------------------------------------

	# Users
	'views/users/user.xml',
	'views/users/user_actions.xml',

	# Groups
	'views/users/group.xml',


	# Orders
	'views/orders/order.xml',
	'views/orders/order_tree.xml',
	'views/orders/order_actions.xml',
	'views/orders/order_search.xml',

	'views/orders/order_admin.xml',
	'views/orders/order_account.xml',

	'views/orders/order_report_nex.xml',                # Estado de Cuenta New


	# Payment methods 
	#'views/payment_method/payment_methods.xml',
	'views/orders/payment_method/payment_methods.xml',


	# Counters 
	'views/counters/counter_actions.xml',
	'views/counters/counter.xml',


	# Companies 
	'views/companies/company.xml',


	# Controls
	'views/controls/control.xml',
	'views/controls/control_admin.xml',


	# Images 
	'views/images/image_view.xml',


	# Services - Dep ? 
	#'views/services/service.xml',



	# Procedures
	'views/procedures/procedure_search.xml',
	'views/procedures/procedure_actions.xml',
	'views/procedures/procedure.xml',


	# Consultation
	'views/consultations/consultation_search.xml',
	'views/consultations/consultation_actions.xml',
	'views/consultations/consultation.xml',



	# Treatments 
	#'views/services/service_actions.xml',  	# Just a dummy
	'views/treatments/service_actions.xml',  	# Just a dummy

	'views/treatments/treatment.xml',
	'views/treatments/treatment_actions.xml',




	# Physicians 
	'views/physicians/physician.xml',



	# Patients 
	'views/patients/patient.xml',
	'views/patients/patient_search.xml',

	# Containers 
	'views/containers/texto.xml',
	'views/containers/container.xml',
	'views/containers/corrector.xml',


	# Partners
	#'views/partners/partner.xml',
	#'views/partners/partner_actions.xml',
	'views/patients/partners/partner_actions.xml',
	'views/patients/partners/partner.xml',


	# Products
	'views/products/product_actions.xml',
	'views/products/product_product.xml',
	'views/products/product_template.xml',

	# Cards 
	'views/cards/card.xml',



# ----------------------------------------------------------- Views - Second ------------------------------------------------------

	# Sessions
	#'views/sessions/session_actions.xml',
	#'views/sessions/session_search.xml',
	'views/sessions/session.xml',

	'views/sessions/session_config_simple_1.xml',
	'views/sessions/session_config_simple_2.xml',

	'views/sessions/session_admin.xml',


	# Services - 2 - Dep !
	#'views/services/service_product.xml',
	#'views/services/service_co2.xml',
	#'views/services/service_excilite.xml',
	#'views/services/service_ipl.xml',
	#'views/services/service_ndyag.xml',
	#'views/services/service_quick.xml',     
	#'views/services/service_medical.xml',
	#'views/services/service_cosmetology.xml',


	# Consultation - 2
	'views/consultations/consultation_diagnosis.xml',
	

	# Treatments - 2 
	'views/treatments/treatment_orders.xml',
	'views/treatments/treatment_consultations.xml',
	'views/treatments/treatment_procedures.xml',
	#'views/treatments/treatment_sessions.xml',  	# Sab
	#'views/treatments/treatment_controls.xml', 	# Sab
	

	# Patients - 2 
	'views/patients/patient_personal.xml',
	'views/patients/patient_control_docs.xml',
	'views/patients/patient_admin.xml',
	#'views/patients/patient_treatments.xml',



# ----------------------------------------------------------- Closings ------------------------------------------------------

	# Closing 
	'views/closings/closings.xml',
	'views/closings/closings_search.xml',
	'reports/closing/closing.xml',


# ----------------------------------------------------------- Sale Reports ------------------------------------------------------
	'views/reports/report_sale_pivots.xml',
	'views/reports/report_sale_graphs.xml',
	'views/reports/report_sale_favorites.xml',
	'views/reports/report_sale_search.xml',
	'views/reports/report_sale.xml',

	#'views/reports/report_sale_actions.xml',            # Dep
	#'views/rsp/report_sale_actions.xml',            	# Dep


# ----------------------------------------------------------- Menus ------------------------------------------------------
	'views/menus/menus.xml',
	'views/menus/menus_dev.xml',

	'views/menus/menus_caja.xml',
	#'views/menus/menus_rsp.xml',		# Dep ?

	'views/menus/menus_marketing.xml',
	'views/menus/menus_management.xml',
	'views/menus/menus_account.xml',
	'views/menus/menus_products.xml',

	'views/menus/menus_oeh.xml',



# Static - Style Css 
'static/src/css/jx.css'

