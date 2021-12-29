// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Booking Info', {
	onload: function(frm) {
		frappe.db.get_single_value('Booking Settings', 'room_item_group')
    .then(room_item_group => {
			if (room_item_group) {
				frm.set_query('room', function(doc) {
					return {
						filters: {
							"item_group": ['=',room_item_group],
						}
					};
				});				
			}
    })
		frm.set_query('booked_via', function(doc) {
			return {
				filters: {
					"name": ['in',['Quotation','Sales Order']],
				}
			};
		});	

	},
});
