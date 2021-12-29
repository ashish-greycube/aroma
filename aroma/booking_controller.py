import frappe
from frappe import _
from frappe.utils import get_link_to_form

def create_booking(self,method):
	room_item_group = frappe.db.get_single_value('Booking Settings', 'room_item_group')
	if room_item_group:
		for item in self.items:
			if item.item_group==room_item_group:
				doc = frappe.new_doc('Booking Info')
				doc.room = item.item_code
				doc.party_date=self.party_date_cf
				doc.from_time=self.from_time_cf
				doc.to_time=self.to_time_cf
				doc.booked_by=self.owner
				doc.type_of_booking= 'Initial' if self.doctype =='Quotation' else 'Confirm' 
				doc.booking_expiry_date=self.valid_till if self.doctype =='Quotation' else  self.booking_expiry_date_cf
				doc.booked_via=self.doctype
				doc.reference=self.name
				doc.save(ignore_permissions=True)
				msg = _('Booking {} is created for {}'.format(get_link_to_form('Booking Info',doc.name),item.item_code))
				frappe.msgprint(msg, alert=1)			

