frappe.provide("frappe.views.calendar");

frappe.views.calendar["Course Schedule"] = {
	field_map: {
		start: "session_date",
		end: "session_date",
		id: "name",
		title: "class_id",
		allDay: "all_day"
	},
	get_events_method: "frappe.desk.calendar.get_events"
};
