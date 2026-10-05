import frappe

def setup_guardian_permissions():
    # 1. Custom DocPerm for Phụ huynh role across required DocTypes
    doctypes = [
        "Student", "Student Attendance", "Assessment Result", 
        "Student Payment Entry", "Level Transfer", "Course Schedule", 
        "Guardian", "Level", "Class"
    ]
    
    for dt in doctypes:
        if not frappe.db.exists("Custom DocPerm", {"parent": dt, "role": "Phụ huynh"}):
            dp = frappe.get_doc({
                "doctype": "Custom DocPerm",
                "parent": dt,
                "parenttype": "DocType",
                "parentfield": "permissions",
                "role": "Phụ huynh",
                "read": 1,
                "write": 0,
                "create": 0,
                "delete": 0
            })
            dp.insert(ignore_permissions=True)
            print(f"Granted read perm on {dt} for Phụ huynh")

    # 2. Create Guardian record for Trần Thái Toàn (STU-2026-00329)
    student_id = "STU-2026-00329" # Trần Thái Toàn
    student_doc = frappe.db.get_value("Student", student_id, "full_name")
    
    guardian_email = "phuhuynh.toan@example.com"
    guardian_name = frappe.db.get_value("Guardian", {"email": guardian_email}, "name")
    
    if not guardian_name:
        g = frappe.get_doc({
            "doctype": "Guardian",
            "full_name": "Trần Văn Hùng (PH Trần Thái Toàn)",
            "email": guardian_email,
            "phone": "0912345678",
            "relationship": "Cha"
        })
        g.insert(ignore_permissions=True)
        guardian_name = g.name
        print(f"Created Guardian record: {guardian_name}")


    # Link Guardian to Student
    frappe.db.set_value("Student", student_id, "guardian_id", guardian_name)

    # 3. Create User account for Phụ huynh
    if not frappe.db.exists("User", guardian_email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": guardian_email,
            "first_name": "Trần Văn Hùng",
            "send_welcome_email": 0,
            "roles": [{"role": "Phụ huynh"}]
        })
        user.insert(ignore_permissions=True)
        # Set password to 123456
        from frappe.utils.password import update_password
        update_password(user.name, "123456")
        print(f"Created User account: {guardian_email} / 123456")

    # 4. Create User Permissions for Guardian to view their Student
    if not frappe.db.exists("User Permission", {"user": guardian_email, "allow": "Student", "for_value": student_id}):
        up_student = frappe.get_doc({
            "doctype": "User Permission",
            "user": guardian_email,
            "allow": "Student",
            "for_value": student_id,
            "apply_to_all_doctypes": 1
        })
        up_student.insert(ignore_permissions=True)
        print(f"Created User Permission for {guardian_email} -> Student {student_id}")

    if not frappe.db.exists("User Permission", {"user": guardian_email, "allow": "Guardian", "for_value": guardian_name}):
        up_g = frappe.get_doc({
            "doctype": "User Permission",
            "user": guardian_email,
            "allow": "Guardian",
            "for_value": guardian_name,
            "apply_to_all_doctypes": 1
        })
        up_g.insert(ignore_permissions=True)

    # 5. Create Client Script for Guardian DocType "Tạo tài khoản Phụ huynh"
    script_name = "Guardian User Account Script"
    js_code = """
frappe.ui.form.on('Guardian', {
	refresh: function(frm) {
		if (!frm.is_new() && frm.doc.email) {
			frm.add_custom_button(__('👤 Tạo tài khoản Phụ huynh'), function() {
				frappe.call({
					method: 'ling_ielts_erp.setup_guardian_access.create_guardian_user',
					args: { guardian_id: frm.doc.name },
					freeze: true,
					freeze_message: __('Đang tạo tài khoản Phụ huynh...'),
					callback: function(r) {
						if (r.message) {
							frappe.msgprint(__('Tạo tài khoản Phụ huynh thành công!<br><b>Email:</b> ') + frm.doc.email + '<br><b>Mật khẩu mặc định:</b> 123456');
						}
					}
				});
			}).addClass('btn-primary');
		}
	}
});
"""

    if frappe.db.exists("Client Script", script_name):
        cs = frappe.get_doc("Client Script", script_name)
        cs.script = js_code
        cs.enabled = 1
        cs.save()
    else:
        cs = frappe.get_doc({
            "doctype": "Client Script",
            "name": script_name,
            "dt": "Guardian",
            "script": js_code,
            "enabled": 1
        })
        cs.insert()

    # Export fixtures
    frappe.db.commit()
    print("Guardian permissions, user account, and script successfully configured!")

@frappe.whitelist()
def create_guardian_user(guardian_id):
    g = frappe.get_doc("Guardian", guardian_id)
    if not g.email:
        frappe.throw("Phụ huynh chưa có địa chỉ Email!")

    if not frappe.db.exists("User", g.email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": g.email,
            "first_name": g.full_name,
            "send_welcome_email": 0,
            "roles": [{"role": "Phụ huynh"}]
        })
        user.insert(ignore_permissions=True)
        from frappe.utils.password import update_password
        update_password(user.name, "123456")

    # Link User Permission for all students belonging to this Guardian
    students = frappe.get_all("Student", filters={"guardian_id": guardian_id}, fields=["name"])
    for s in students:
        if not frappe.db.exists("User Permission", {"user": g.email, "allow": "Student", "for_value": s.name}):
            up = frappe.get_doc({
                "doctype": "User Permission",
                "user": g.email,
                "allow": "Student",
                "for_value": s.name,
                "apply_to_all_doctypes": 1
            })
            up.insert(ignore_permissions=True)

    if not frappe.db.exists("User Permission", {"user": g.email, "allow": "Guardian", "for_value": guardian_id}):
        up_g = frappe.get_doc({
            "doctype": "User Permission",
            "user": g.email,
            "allow": "Guardian",
            "for_value": guardian_id,
            "apply_to_all_doctypes": 1
        })
        up_g.insert(ignore_permissions=True)

    frappe.db.commit()
    return True

if __name__ == "__main__":
    setup_guardian_permissions()
