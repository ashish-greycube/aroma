// Copyright (c) 2022, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Function Sheet', {
	refresh: function (frm) {}
})

frappe.ui.form.on('Function Sheet Extra Item', {
	before_function_sheet_extra_item_remove: function (frm, cdt, cdn) {
		let row=locals[cdt][cdn]
		if (row.ref_sales_invoice != undefined) {
			frappe.throw(__("Cannot delete item #{0} : {1} with linked sales invoice {2}. Please cancel linked sales invoice first.", [row.idx,row.item_name, 
				frappe.utils.get_form_link("Sales Invoice", row.ref_sales_invoice, true)
				]));
		}
	},
	qty: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		if (row.qty && row.price) {
			row.total = flt(row.qty * row.price)
			frm.refresh_fields('function_sheet_extra_item')
		}
	},
	price: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		if (row.qty && row.price) {
			row.total = flt(row.qty * row.price)
			frm.refresh_fields('function_sheet_extra_item')
		}
	},
	create_si: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		if (row.ref_sales_invoice == undefined && frm.doc.docstatus == 0 && frm.doc.function_sheet_extra_item.length > 0) {
			frappe.call({
				method: "create_sales_invoice",
				doc: frm.doc,
				args: {
					row_name: row.name,
				},
				callback: function (r) {
					if (!r.exc) {
						frm.refresh_fields('function_sheet_extra_item')
					}
				}
			});
		}
	}
})