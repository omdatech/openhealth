def create_procedure_wapp(self, subtype, product_id):
...
		# Create Sessions - Dep !
		#self.treatment.create_sessions()


def create_order(self, target):


	# Pricelist 
	# Vip 
	if self.x_vip_inprog: 
		print 'Vip'
		pl = self.env['product.pricelist'].search([
															('name', 'like', 'VIP'), 
													],
														#order='write_date desc',
														limit=1,
													)
		pl_id = pl.id 
	
	# Public 
	else: 
		print 'Public'
		pl = self.env['product.pricelist'].search([
															('name', 'like', 'Public Pricelist'), 
															#('name', '=', 'Public Pricelist'), 
													],
														#order='write_date desc',
														limit=1,
													)
		# jx - Hack !
		#pl_id = pl.id 
		pl_id = 1

	#pl_id = pl.id 



# 1 Oct 2018

	# Unlink Patient
	#patients = self.env['oeh.medical.patient'].search([
	#														('name', '=', name), 
	#												],).unlink()

	# Unlink Partner 
	#partners = self.env['res.partner'].search([
	#														('name', '=', name), 
	#												],).unlink()
	

	# Unlink - Card
 	#cards = self.env['openhealth.card'].search([
	#														('patient_name', '=', name), 	
	#													],)
 	#for card in cards: 
 	#	card.unlink()



 	