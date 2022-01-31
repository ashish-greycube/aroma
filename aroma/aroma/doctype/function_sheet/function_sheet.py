# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form,flt
from frappe.utils.data import getdate, nowdate

class FunctionSheet(Document):
	def on_submit(self):
		for item in self.function_sheet_extra_item:
			if not item.ref_sales_invoice:
				msg = _('Item #{0} : {1} in "Function Sheet Extra Item" has no sales invoice. Please create sales invoice.'.format(item.idx,item.item_name))
				frappe.throw(msg)				
			elif item.is_billed==0:
				msg = _('Item #{0} : {1} in "Function Sheet Extra Item" is not billed. Please submit {1} to bill it.'.format(item.idx,item.item_name,frappe.bold(get_link_to_form('Sales Invoice',item.ref_sales_invoice))))
				frappe.throw(msg)				

	@frappe.whitelist()
	def create_sales_invoice(self,row_name):
		si = frappe.new_doc('Sales Invoice')
		si.customer=self.guest_name
		si.due_date=getdate(nowdate())
		for item in self.function_sheet_extra_item:
			if item.name==row_name:
				row = si.append('items', {})		
				row.item_code=item.item_code
				row.item_name=item.item_name
				row.qty=item.qty
				row.rate=item.price

		si.flags.ignore_permissions = True
		si.function_sheet_cf=self.name
		si.run_method("set_missing_values")
		si.run_method("calculate_taxes_and_totals")		
		si.save()		
		for item in self.function_sheet_extra_item:
			if item.name==row_name:
				item.ref_sales_invoice=si.name
		frappe.db.set_value('Function Sheet Extra Item', row_name, 'ref_sales_invoice', si.name)
		msg = _('Sales Invoice {} is created'.format(frappe.bold(get_link_to_form('Sales Invoice',si.name))))
		frappe.msgprint(msg)
