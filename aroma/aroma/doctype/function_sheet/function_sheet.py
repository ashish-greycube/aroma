# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form,flt
from frappe.utils.data import getdate, nowdate

class FunctionSheet(Document):
	@frappe.whitelist()
	def create_sales_invoice(self):
		# default_sales_invoice_naming_series = frappe.db.get_value('Company', self.company, 'default_sales_invoice_naming_series')
		# cost_center = frappe.db.get_value('Company', self.company, 'cost_center')

		si = frappe.new_doc('Sales Invoice')
		# si.naming_series=default_sales_invoice_naming_series
		si.customer=self.guest_name
		si.due_date=getdate(nowdate())
		# si.cost_center=cost_center
		for item in self.function_sheet_extra_item:
			row = si.append('items', {})		
			row.item_code=item.item_code
			row.item_name=item.item_name
			row.qty=item.qty
			row.rate=item.price

		si.flags.ignore_permissions = True
		# si.ignore_pricing_rule = 1
		# si.update_stock=0
		si.function_sheet_cf=self.name
		si.run_method("set_missing_values")
		si.run_method("calculate_taxes_and_totals")		
		si.save()		
		msg = _('Sales Invoice {} is created'.format(frappe.bold(get_link_to_form('Sales Invoice',si.name))))
		frappe.msgprint(msg)
