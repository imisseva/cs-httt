import json
import frappe
import frappe.desk.calendar

__version__ = "0.0.1"

if not getattr(frappe.desk.calendar, "_ling_ielts_patched", False):
	_orig_get_events = frappe.desk.calendar.get_events

	def _patched_get_events(doctype, start, end, field_map, filters=None, fields=None):
		if doctype == "Course Schedule" and field_map:
			try:
				fm = json.loads(field_map) if isinstance(field_map, str) else field_map
				if fm.get("start") in ("start", None):
					fm["start"] = "session_date"
				if fm.get("end") in ("end", None):
					fm["end"] = "session_date"
				if fm.get("title") in ("title", None):
					fm["title"] = "class_id"
				field_map = json.dumps(fm)
			except Exception:
				pass
		return _orig_get_events(doctype, start, end, field_map, filters=filters, fields=fields)

	frappe.desk.calendar.get_events = _patched_get_events
	frappe.desk.calendar._ling_ielts_patched = True
