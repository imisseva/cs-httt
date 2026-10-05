app_name = "ling_ielts_erp"
app_title = "Ling IELTS ERP"
app_publisher = "Ling IELTS Team"
app_description = "Ling IELTS ERP Custom App"
app_email = "admin@lingielts.vn"
app_license = "mit"

app_include_js = "ling_ielts_erp.js"

doctype_calendar_js = {
	"Course Schedule": "public/js/ling_ielts_erp.js"
}

doc_events = {
	"Course Schedule": {
		"validate": "ling_ielts_erp.course_schedule_handler.validate_course_schedule"
	},
	"Level Transfer": {
		"on_update": "ling_ielts_erp.level_transfer_handler.on_level_transfer_update"
	}
}

fixtures = [
	"Custom DocPerm",
	"Client Script",
	"Workflow",
	"Workflow State",
	"Workflow Action Master",
	"Notification",
	"Property Setter"
]

