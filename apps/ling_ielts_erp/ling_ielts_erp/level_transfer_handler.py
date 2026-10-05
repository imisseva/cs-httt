import frappe

def on_level_transfer_update(doc, method=None):
	if doc.workflow_state == "Transferred":
		# 1. Update Student current_level_id
		if doc.student_id and doc.proposed_level_id:
			frappe.db.set_value("Student", doc.student_id, "current_level_id", doc.proposed_level_id)

		# 2. Update existing active Enrollments to 'Đã chuyển lớp'
		active_enrollments = frappe.get_all("Enrollment", filters={
			"student_id": doc.student_id,
			"enrollment_status": ["in", ["Đang học", "Chưa đủ điều kiện"]]
		})
		for en in active_enrollments:
			frappe.db.set_value("Enrollment", en.name, "enrollment_status", "Đã chuyển lớp")

		# 3. Determine target new class
		target_class = doc.proposed_class_id
		if not target_class and doc.proposed_level_id:
			classes = frappe.get_all("Class", filters={"level_id": doc.proposed_level_id}, fields=["name"])
			if classes:
				target_class = classes[0].name

		if target_class:
			# Create or update Enrollment record for target_class
			existing_en = frappe.db.exists("Enrollment", {"student_id": doc.student_id, "class_id": target_class})
			if not existing_en:
				new_en = frappe.get_doc({
					"doctype": "Enrollment",
					"student_id": doc.student_id,
					"class_id": target_class,
					"enrollment_status": "Đang học",
					"enrollment_date": frappe.utils.today()
				})
				new_en.insert(ignore_permissions=True)
			else:
				frappe.db.set_value("Enrollment", existing_en, "enrollment_status", "Đang học")

			# Update User Permission for Class for linked User account
			student_users = frappe.get_all("User Permission", filters={"allow": "Student", "for_value": doc.student_id}, fields=["user"])
			for su in student_users:
				user_email = su.user
				frappe.db.delete("User Permission", {"user": user_email, "allow": "Class"})
				new_up = frappe.get_doc({
					"doctype": "User Permission",
					"user": user_email,
					"allow": "Class",
					"for_value": target_class
				})
				new_up.insert(ignore_permissions=True)

		frappe.db.commit()
