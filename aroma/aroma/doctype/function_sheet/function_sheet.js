// Copyright (c) 2022, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Function Sheet', {
	refresh: function (frm) {
		if (frm.doc.docstatus == 1 && frm.doc.function_sheet_extra_item.length>0) {

				frappe.db.get_list('Sales Invoice', {
					fields: ['name'],
					filters: {
						function_sheet_cf: frm.doc.name,
					}
				}).then(records => {
					if (records.length == 0) {
						frm.add_custom_button(__('Create Invoice'), function () {
							frappe.call({
								method: "create_sales_invoice",
								doc: frm.doc,
								callback: function (r) {
									if (!r.exc) {
										frm.refresh();
									}
								}
							});
						});
					}
				})
		}
}
})

frappe.ui.form.on('Function Sheet Extra Item', {
	qty: function (frm,cdt,cdn) {
		debugger
		let row=locals[cdt][cdn]
		if (row.qty && row.price) {
			row.total=flt(row.qty * row.price)
			frm.refresh_fields('function_sheet_extra_item')
		}
	},
	price: function (frm,cdt,cdn) {
		let row=locals[cdt][cdn]
		if (row.qty && row.price) {
			row.total=flt(row.qty * row.price)
			frm.refresh_fields('function_sheet_extra_item')
		}
	}	
})