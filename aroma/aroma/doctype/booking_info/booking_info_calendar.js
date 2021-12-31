
frappe.views.calendar["Booking Info"] = {
	field_map: {
		"start": "start",
		"end": "end",
		"id": "name",
		"title": "room",
		"progress": "type_of_booking",
		"allDay": "allDay",
		"color": "calendar_color"
	},
	get_events_method: "aroma.aroma.doctype.booking_info.booking_info.get_events"
};
