# -*- coding: utf-8 -*-
"""
    lib.py

    Used by: 
        management_order_line

    Abstract, general purpose. Can be Unit-tested.
    Is completely standard. Gives service to all Users.

    Created: 			13 aug 2018
    Last up: 	 		18 oct 2020
"""
from __future__ import print_function
import datetime

_date_format = "%Y-%m-%d %H:%M:%S"
_date_format_day = "%Y-%m-%d"

#------------------------------------------------ Date - Correct for Utc --------------------------
def get_date_with_format(date_format, date):
	"""
	Get Date with Format
	"""
	date_format_1 = _date_format
	date_dt = datetime.datetime.strptime(date, date_format_1) + datetime.timedelta(hours=-5, minutes=0)
	#print(date_dt)
	date_s = date_dt.strftime(date_format)
	#print(date_s)
	return date_s


#------------------------------------------------ Date - Todays Name ------------------------------
def get_todays_name(date_format):
	"""
	Get Todays Name
	"""
	today = datetime.datetime.today() + datetime.timedelta(hours=-5, minutes=0)
	name = today.strftime(date_format)
	return name

#------------------------------------------------ Date - Is Today ---------------------------------
def is_today_date(date):
	"""
	Is Today Date
	"""
	date_format = _date_format_day
	date_dt = datetime.datetime.strptime(date, date_format) + datetime.timedelta(hours=0, minutes=0)
	if date_dt.date() == datetime.datetime.today().date():
		is_today = True
		print(date)
		print(date_dt)
	else:
		is_today = False
	return is_today

#------------------------------------------------ Date - Is Today ---------------------------------
def is_today(date):
	"""
	Is Today
	"""
	date_format = _date_format
	date_dt = datetime.datetime.strptime(date, date_format) + datetime.timedelta(hours=-5, minutes=0)
	if date_dt.date() == datetime.datetime.today().date():
		is_today = True
	else:
		is_today = False
	return is_today

#------------------------------------------------ Get Next Date -----------------------------------
def get_next_date(self, evaluation_start_date, nr_days):
	"""
	Get Next Date
	"""
	date_format = _date_format
	delta = datetime.timedelta(days=nr_days)
	start = datetime.datetime.strptime(evaluation_start_date, date_format)
	next_date = delta + start
	return next_date
# get_next_date

# ----------------------------------------------------------- Delta from Now ----------------------
def get_delta_now(self, date_1):
	"""
	Get Delta Now
	"""
	date_format = _date_format
	now = datetime.datetime.now()
	dt_1 = datetime.datetime.strptime(date_1, date_format)
	delta = dt_1 - now
	delta_sec = delta.total_seconds()
	return delta, delta_sec
# get_delta_now

# ----------------------------------------------------------- Get Next Slot------------------------
def get_next_slot(self):
	"""
	Get Next Slot
	"""
	# Init
	date_format = _date_format
	date_2_format = _date_format_day
	now = datetime.datetime.now() + datetime.timedelta(hours=-5, minutes=0)
	now_date_str = now.strftime(date_2_format)
	# Loop
	for idx in range(0, 48):
		slot = get_slot(idx)
		slot_x = now_date_str + ' ' + slot
		slot_dt = datetime.datetime.strptime(slot_x, date_format)
		delta = slot_dt - now
		delta_sec = delta.total_seconds()
		if delta_sec > 0:
			return (slot_dt + datetime.timedelta(hours=5, minutes=0)).strftime(date_format)

	return now_date_str + ' 14:00:00'		# If no slot available
# get_next_slot

# ----------------------------------------------------------- Doctor Available---------------------
def doctor_available(self, app_date_str):
	"""
	Doctor Available
	Check if not too late (before 21:00)
	"""
	# Init
	date_2_format = _date_format_day
	now = datetime.datetime.now() + datetime.timedelta(hours=-5, minutes=0)
	now_date_str = now.strftime(date_2_format)
	app_limit_str = now_date_str + ' 21:00:00'
	date_format = _date_format

	# Delta
	app_date_dt = datetime.datetime.strptime(app_date_str, date_format) + \
																		datetime.timedelta(hours=-5, minutes=0)

	app_limit_dt = datetime.datetime.strptime(app_limit_str, date_format)
	delta = app_limit_dt - app_date_dt
	delta_sec = delta.total_seconds()

	if delta_sec < 0:
		available = False
	else:
		available = True

	return available

# doctor_available

# ----------------------------------------------------------- Get Nr Days--------------------------
def get_nr_days(self, date_ref_str, date_str):
	"""
	Get Nr Days
	"""
	# Init
	delta_days = 0
	if date_ref_str != False and date_str != False:
		date_format = _date_format_day
		date_ref_str = date_ref_str.split()[0]
		date_ref_dt = datetime.datetime.strptime(date_ref_str, date_format)
		date_str = date_str.split()[0]
		date_dt = datetime.datetime.strptime(date_str, date_format)
		delta = date_dt - date_ref_dt
		delta_days = delta.days
	return delta_days

#------------------------------------------------ Get Slot ----------------------------------------
def get_slot(idx):
	"""
	Get empty slot
	"""
	date_format = "%H:%M:%S"
	date_str = "09:00:00"
	date_dt = datetime.datetime.strptime(date_str, date_format) + datetime.timedelta(minutes=idx*15)
	slot = date_dt.strftime(date_format)
	return slot

#------------------------------------------------ Change State ------------------------------------
def change_state(obj, state):
	"""
	Change the state of the Object
	"""
	if obj.state != False:
		obj.state = state
# change_state

#------------------------------------------------ Checksum ----------------------------------------
def get_checksum_tic(generated):
	"""
	Get Checksum Ticket
	"""
	if generated == 'x':
		checksum = '0'
	else:
		checksum = '1'
	return checksum

#------------------------------------------------ Get Tax -----------------------------------------
def get_net_tax(amount):
	"""
	Get Tax
	"""
	# Net
	net = amount/1.18
	net = round(net, 2)
	# Tax
	tax = net * 0.18
	tax = round(tax, 2)
	return net, tax

#------------------------------------------------ Date - Correct for Utc - With Delta--------------
def correct_date_delta(date, delta_hou=0, delta_min=0, delta_sec=0):
	"""
	Correct Date Delta
	"""
	date_format = _date_format
	date_dt = datetime.datetime.strptime(date, date_format) + \
															datetime.timedelta(hours=delta_hou, minutes=delta_min, seconds=delta_sec)
	date_s = date_dt.strftime(date_format)
	return date_s

#------------------------------------------------ Date - Correct for Utc --------------------------
def correct_date(date):
	"""
	Correct Date
	"""
	date_format = _date_format
	date_dt = datetime.datetime.strptime(date, date_format) + datetime.timedelta(hours=-5, minutes=0)
	date_s = date_dt.strftime(date_format)
	return date_s

#------------------------------------------------ Partner On change - Test ------------------------
# Length
def test_for_length(self, token, length):
	"""
	Test for Length
	"""
	if token and (len(str(token)) != length):
		return {
				'warning': {
					'title': "Error: Debe tener " + str(length) + " caracteres.",
					'message': token,
				}}
	else:
		return 0
# test_for_length

# Digits
def test_for_digits(self, token):
	"""
	Test for Digits
	"""

	if token and (not token.isdigit()):
		return {
				'warning': {
					'title': "Error: Debe ser número.",
					'message': token,
				}}
	else:
		return 0
# test_for_digits

#------------------------------------------------ Checksum ----------------------------------------
def get_checksum_gen(generated, name):
	"""
	Get Checksum Generated
	"""
	if generated == name:
		checksum = '1'
	else:
		checksum = '0'
	return checksum
