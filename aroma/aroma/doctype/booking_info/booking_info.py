# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BookingInfo(Document):
	pass


@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Booking Info", filters)

	data = frappe.db.sql("""
select name,room,timestamp(party_date,from_time)as 'start',timestamp(party_date,to_time)as 'end',type_of_booking, IF(type_of_booking='Initial',"blue","green") as "color" 
from `tabBooking Info`
where docstatus < 2 and party_date  between %(start)s and %(end)s""",{"start": start, "end": end}, as_dict=True,debug=True, update={"allDay": 0})


	return data