frappe.ui.form.on("Sales Order", {
	refresh: function (frm) {
		debugger
		if (frm.doc.docstatus != 2) {
			frm.add_custom_button(__('Function Sheet'), () => create_function_sheet(), __('Create'));
		}
	}
})

function create_function_sheet() {
	frappe.model.open_mapped_doc({
		method: "aroma.booking_controller.create_function_sheet",
		frm: cur_frm
	})
}