import json
import frappe

def validate_course_schedule(doc, method=None):
	if not (doc.session_date and doc.start_time and doc.end_time):
		return

	doc_name = doc.name or ""

	# 1. Check Teacher time conflict (BR-SCH-01)
	if doc.teacher_id:
		overlapping_teacher = frappe.db.sql("""
			SELECT name, class_id, room_id, start_time, end_time 
			FROM `tabCourse Schedule`
			WHERE teacher_id = %s 
			  AND session_date = %s
			  AND name != %s
			  AND ifnull(status, '') != 'Đã huỷ'
			  AND (start_time < %s AND end_time > %s)
		""", (doc.teacher_id, doc.session_date, doc_name, doc.end_time, doc.start_time), as_dict=True)

		if overlapping_teacher:
			t = overlapping_teacher[0]
			frappe.throw(
				f"⚠️ <b>CẢNH BÁO TRÙNG GIỜ DẠY GIÁO VIÊN:</b><br><br>"
				f"Giáo viên <b>{doc.teacher_id}</b> đã có lịch dạy lớp <b>{t.class_id}</b> "
				f"tại <b>{t.room_id or 'Phòng học'}</b> từ <b>{t.start_time}</b> đến <b>{t.end_time}</b> vào ngày <b>{doc.session_date}</b>!"
			)

	# 2. Check Room time conflict (BR-ROOM-01)
	if doc.room_id:
		overlapping_room = frappe.db.sql("""
			SELECT name, class_id, teacher_id, start_time, end_time 
			FROM `tabCourse Schedule`
			WHERE room_id = %s 
			  AND session_date = %s
			  AND name != %s
			  AND ifnull(status, '') != 'Đã huỷ'
			  AND (start_time < %s AND end_time > %s)
		""", (doc.room_id, doc.session_date, doc_name, doc.end_time, doc.start_time), as_dict=True)

		if overlapping_room:
			r = overlapping_room[0]
			frappe.throw(
				f"⚠️ <b>CẢNH BÁO TRÙNG PHÒNG HỌC:</b><br><br>"
				f"Phòng <b>{doc.room_id}</b> đã được xếp cho lớp <b>{r.class_id}</b> "
				f"(Giáo viên <b>{r.teacher_id or 'N/A'}</b>) từ <b>{r.start_time}</b> đến <b>{r.end_time}</b> vào ngày <b>{doc.session_date}</b>!"
			)

@frappe.whitelist()
def get_class_students_for_attendance(schedule_id):
	schedule = frappe.get_doc("Course Schedule", schedule_id)
	if not schedule.class_id:
		return []

	enrollments = frappe.get_all("Enrollment", 
		filters={"class_id": schedule.class_id, "enrollment_status": "Đang học"},
		fields=["student_id"]
	)

	students = []
	for e in enrollments:
		student_name = frappe.db.get_value("Student", e.student_id, "full_name") or e.student_id
		existing_att = frappe.db.get_value("Student Attendance", 
			{"schedule_id": schedule_id, "student_id": e.student_id}, 
			"attendance_status"
		)
		students.append({
			"student_id": e.student_id,
			"full_name": student_name,
			"attendance_status": existing_att or "Có mặt"
		})
	return students

@frappe.whitelist()
def mark_batch_attendance(attendance_data):
	if isinstance(attendance_data, str):
		attendance_data = json.loads(attendance_data)

	# Link field `recorded_by` expects Teacher record name (e.g. TCH-00023)
	teacher_id = frappe.db.get_value("Teacher", {"email": frappe.session.user}, "name")
	if not teacher_id:
		# Fallback to teacher assigned on schedule or first available teacher
		teacher_id = frappe.db.get_value("Teacher", {}, "name")

	for item in attendance_data:
		student_id = item.get("student_id")
		schedule_id = item.get("schedule_id")
		status = item.get("attendance_status", "Có mặt")

		existing = frappe.db.exists("Student Attendance", {"student_id": student_id, "schedule_id": schedule_id})
		if existing:
			frappe.db.set_value("Student Attendance", existing, "attendance_status", status)
			if teacher_id:
				frappe.db.set_value("Student Attendance", existing, "recorded_by", teacher_id)
		else:
			att = frappe.get_doc({
				"doctype": "Student Attendance",
				"student_id": student_id,
				"schedule_id": schedule_id,
				"attendance_status": status,
				"recorded_by": teacher_id
			})
			att.insert(ignore_permissions=True)

	frappe.db.commit()
	return True


