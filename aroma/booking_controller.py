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

def after_migrations():
	update_dashboard_link_for_core_doctype(doctype='Quotation',link_doctype='Booking Info',link_fieldname='reference',group='Reference')
	update_dashboard_link_for_core_doctype(doctype='Sales Order',link_doctype='Booking Info',link_fieldname='reference',group='Reference')

def update_dashboard_link_for_core_doctype(doctype,link_doctype,link_fieldname,group=None):
	try:
		d = frappe.get_doc("Customize Form")
		if doctype:
			d.doc_type = doctype
		d.run_method("fetch_to_customize")
		for link in d.get('links'):
			if link.link_doctype==link_doctype and link.link_fieldname==link_fieldname:
				# found so just return
				return
		d.append('links', dict(link_doctype=link_doctype, link_fieldname=link_fieldname,table_fieldname=None,group=group))
		d.run_method("save_customization")
		frappe.clear_cache()
	except Exception:
		frappe.log_error(frappe.get_traceback())				

