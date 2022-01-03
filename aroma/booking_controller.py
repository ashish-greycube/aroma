import frappe
from frappe import _
from frappe.utils import get_link_to_form

def create_booking(self,method):
	room_item_group = frappe.db.get_single_value('Booking Settings', 'room_item_group')
	if room_item_group:
		for item in self.items:
			if item.item_group==room_item_group:
				existing_found=False
				if self.doctype=='Sales Order':
					existing_booking_name=frappe.db.sql("""select tbi.name from `tabSales Order` so inner join `tabSales Order Item` sot on so.name=sot.parent 
inner join `tabBooking Info` tbi  on tbi.reference = sot.prevdoc_docname
where tbi.room = sot.item_code 
and tbi.party_date = so.party_date_cf 
and tbi.from_time = so.from_time_cf 
and tbi.to_time  = so.to_time_cf 
and tbi.booked_via = 'Quotation'
and sot.item_code =%s
and sot.prevdoc_docname =%s """,(item.item_code,item.prevdoc_docname),as_dict=True)
					if len(existing_booking_name)>0:
						doc = frappe.get_doc('Booking Info',existing_booking_name[0].name)
						doc.update({
							'type_of_booking':'Confirm',
							'booking_expiry_date':self.delivery_date,
							'booked_via':self.doctype,
							'reference':self.name
						})
						doc.save(ignore_permissions=True)
						existing_found=True
						msg = _('Existing Booking {} is updated for Sales Order {}'.format(get_link_to_form('Booking Info',doc.name),self.name))
						frappe.msgprint(msg, alert=1)			
				if existing_found==False:					
					doc = frappe.new_doc('Booking Info')
					doc.room = item.item_code
					doc.party_date=self.party_date_cf
					doc.from_time=self.from_time_cf
					doc.to_time=self.to_time_cf
					doc.booked_by=self.owner
					doc.type_of_booking= 'Initial' if self.doctype =='Quotation' else 'Confirm' 
					doc.booking_expiry_date=self.valid_till if self.doctype =='Quotation' else  self.delivery_date
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

