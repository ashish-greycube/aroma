
frappe.views.calendar["Booking Info"] = {
	field_map: {
		"start": "start",
		"end": "end",
		"id": "name",
		"title": "room",
		"status": "type_of_booking",
		"allDay": "allDay",
		"color": "color"
	},
	style_map: {
		"Initial": "success",
		"Confirm": "info"
	},	
	gantt: true,
	get_events_method: "aroma.aroma.doctype.booking_info.booking_info.get_events"
};
