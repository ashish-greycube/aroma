import frappe
from frappe import _
from frappe.utils import get_link_to_form
from frappe.model.mapper import get_mapped_doc
from frappe.utils import getdate, nowdate

def remove_function_sheet_si_reference(self,method):
	if self.function_sheet_cf:
		function_sheet = frappe.get_doc('Function Sheet', self.function_sheet_cf)
		if function_sheet.docstatus==1:
				msg = _('Cannot cancel sales invoice as linked function sheet {0} is not in draft stage.'.format(frappe.bold(get_link_to_form('Function Sheet',self.function_sheet_cf))))
				frappe.msgprint(msg)		
		else:
			for item in function_sheet.function_sheet_extra_item:	
				if item.ref_sales_invoice==self.name:
					item.ref_sales_invoice=None
					item.is_billed=0
					function_sheet.save(ignore_permissions=True)
					msg = _('Function Sheet {0}, row #{1} : {2} sales invoice reference is removed.'.format(frappe.bold(get_link_to_form('Function Sheet',self.function_sheet_cf)),item.idx,item.item_name))
					frappe.msgprint(msg)				

def mark_function_sheet_as_billed(self,method):
	if self.function_sheet_cf:
		function_sheet = frappe.get_doc('Function Sheet', self.function_sheet_cf)
		for item in function_sheet.function_sheet_extra_item:
			if item.ref_sales_invoice==self.name:
				is_billed=frappe.db.set_value('Function Sheet Extra Item', item.name, 'is_billed', 1)
				msg = _('Function Sheet {0}, row #{1} : {2} is marked as billed.'.format(frappe.bold(get_link_to_form('Function Sheet',self.function_sheet_cf)),item.idx,item.item_name))
				frappe.msgprint(msg)

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
					if not self.party_date_cf:
						msg = _('Party Date is required for Booking. Please enter it.')
						frappe.throw(msg)								
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
					if self.doctype=='Quotation' and self.quotation_to=='Customer':
						doc.customer=self.party_name 
					if self.doctype =='Sales Order':
						doc.customer=self.customer
						doc.main_hall=self.main_hall_cf
						doc.dinner_hall=self.dinner_hall_cf
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

@frappe.whitelist()
def create_function_sheet(source_name, target_doc=None):
	doc = get_mapped_doc('Sales Order', source_name, {
		'Sales Order': {
			'doctype': 'Function Sheet',
			'field_map': {
				'customer':'guest_name',
				'name':'sales_order',
			'contact_mobile':	"mobile_no",
			"party_date_cf":	"party_date",
			"from_time_cf":	"start_time",
			"to_time_cf":	"end_time",
			},			
			'validation': {
				'docstatus': ['!=', 2]
			}
		}
	}, target_doc)
	so=frappe.get_doc('Sales Order',source_name)
	for item in so.items:
		doc.seating_hall=item.item_code
		break

	return doc

def delete_expired_booking_in_initial_state():
	frappe.db.delete("Booking Info", {
			"type_of_booking":['=', 'Initial'],
			"booking_expiry_date": ["<=", getdate(nowdate())]
	})	
	frappe.db.commit()			

	