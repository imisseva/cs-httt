# Dữ liệu mẫu Ling IELTS ERP

Bộ dữ liệu này được tạo từ Data Dictionary trong [A2_ERD_DataDictionary_Ling_IELTS.docx](A2_ERD_DataDictionary_Ling_IELTS.docx), chỉ dùng để tham khảo và nhập thử trên site.

## Lưu ý trước khi nhập

- Các bảng dưới đây theo entity và field logic trong A2, không đảm bảo tên field khớp 1:1 với form ERPNext. A2 ghi mapping sang ERPNext là dự kiến; app `ling_ielts_erp` hiện chưa có khai báo DocType riêng.
- Hãy xem trước DocType và field đang có trong UI. Một số entity (như `LEVEL_TRANSFER`, `TEACHER_LEAVE_REQUEST`) cần custom DocType; các field `guardian_id`, `current_level_id`, `room_type`, `discount_amount`, `final_fee_amount` có thể cần bổ sung.
- Các ID `MGR-01`, `LVL-40`, `STU-01`... là mã tham chiếu để nối các bảng mẫu, không nhất thiết là ID ERPNext sẽ tự sinh. Khi tạo trên UI, thay bằng mã document thực tế rồi dùng mã đó ở các liên kết.
- Tên, số điện thoại, email và điểm số đều là dữ liệu giả lập. Học phí trong mẫu cũng là giá trị minh họa, cần thay bằng bảng giá được trung tâm xác nhận.
- Ngày dùng định dạng `YYYY-MM-DD`; tiền tệ tính bằng VND. Các giá trị enum giữ theo A2.

## Thứ tự nhập

Nhập theo thứ tự để các liên kết đã tồn tại trước khi dùng:

1. `MANAGER`, `COURSE`, `LEVEL`, `FEE_STRUCTURE`, `GUARDIAN`, `TEACHER`, `ROOM`
2. `STUDENT`, `CLASS`, `COURSE_SCHEDULE`
3. `ENROLLMENT`, `PAYMENT_ENTRY`
4. `ASSESSMENT_RESULT`, `STUDENT_ATTENDANCE`, `LEVEL_TRANSFER`, `TEACHER_LEAVE_REQUEST`

## 1. Danh mục gốc

### MANAGER

| manager_id | full_name | phone | email |
|---|---|---|---|
| MGR-01 | Nguyễn Minh Anh | 0900000101 | minh.anh@example.test |

### COURSE

| course_id | course_name | duration_months | sessions_per_week | hours_per_session |
|---|---|---:|---:|---:|
| CRS-IELTS | IELTS 4 kỹ năng | 3 | 2 | 2.0 |

### LEVEL

| level_id | course_id | level_name | order_index |
|---|---|---|---:|
| LVL-40 | CRS-IELTS | Band 4.0-4.5 | 1 |
| LVL-45 | CRS-IELTS | Band 4.5-5.0 | 2 |
| LVL-50 | CRS-IELTS | Band 5.0-5.5 | 3 |

### FEE_STRUCTURE

| fee_structure_id | level_id | base_fee_amount | effective_date |
|---|---|---:|---|
| FEE-40-2026 | LVL-40 | 3600000 | 2026-01-01 |
| FEE-45-2026 | LVL-45 | 4200000 | 2026-01-01 |
| FEE-50-2026 | LVL-50 | 4800000 | 2026-01-01 |

### GUARDIAN

| guardian_id | full_name | phone | email | relationship |
|---|---|---|---|---|
| GUA-01 | Trần Thị Hoa | 0900000201 | hoa@example.test | Mẹ |
| GUA-02 | Lê Văn Nam | 0900000202 | nam@example.test | Cha |

### TEACHER

| teacher_id | full_name | teacher_type | nationality | qualified_level_id | phone | email |
|---|---|---|---|---|---|---|
| TCH-01 | Phạm Thu Linh | Cơ hữu | Việt Nam | LVL-50 | 0900000301 | linh@example.test |
| TCH-02 | David Nguyen | Thỉnh giảng | Nước ngoài | LVL-45 | 0900000302 | david@example.test |
| TCH-03 | Võ Minh An | Cơ hữu | Việt Nam | LVL-40 | 0900000303 | an@example.test |

Theo quy tắc A2, giáo viên được dạy cấp có `order_index` nhỏ hơn hoặc bằng cấp được chứng nhận. Vì vậy TCH-01 có thể dạy cả ba cấp; TCH-03 chỉ dạy LVL-40.

### ROOM

| room_id | room_name | room_type | capacity |
|---|---|---|---:|
| ROOM-01 | Phòng 101 | Giảng dạy chung | 15 |
| ROOM-02 | Speaking 201 | Speaking | 6 |
| ROOM-03 | Listening 301 | Listening | 15 |

## 2. Học viên và lớp

### STUDENT

| student_id | full_name | date_of_birth | phone | guardian_id | current_level_id | status |
|---|---|---|---|---|---|---|
| STU-01 | Nguyễn Gia Hân | 2012-04-18 | 0900000401 | GUA-01 | LVL-40 | Đang học |
| STU-02 | Trần Minh Khoa | 2011-11-02 | 0900000402 | GUA-02 | LVL-40 | Đang học |
| STU-03 | Lê Bảo Ngọc | 2009-08-25 | 0900000403 |  | LVL-45 | Đang học |

`guardian_id` để trống là hợp lệ nếu học viên không liên kết người giám hộ.

### CLASS

| class_id | level_id | teacher_id | start_date | end_date | total_sessions | sessions_taught | status |
|---|---|---|---|---|---:|---:|---|
| CLS-40-A | LVL-40 | TCH-01 | 2026-07-06 | 2026-10-12 | 24 | 8 | Đang mở |
| CLS-45-A | LVL-45 | TCH-02 | 2026-09-14 | 2026-12-14 | 24 | 4 | Đang mở |

### COURSE_SCHEDULE

| schedule_id | class_id | teacher_id | room_id | session_date | start_time | end_time | session_type | status |
|---|---|---|---|---|---|---|---|---|
| SCH-40-01 | CLS-40-A | TCH-01 | ROOM-01 | 2026-08-05 | 18:00:00 | 20:00:00 | Chính khóa | Đã dạy |
| SCH-40-02 | CLS-40-A | TCH-01 | ROOM-01 | 2026-09-30 | 18:00:00 | 20:00:00 | Chính khóa | Đã lên lịch |
| SCH-45-01 | CLS-45-A | TCH-02 | ROOM-03 | 2026-10-01 | 18:00:00 | 20:00:00 | Chính khóa | Đã lên lịch |

Buổi `Học online` có thể để trống `room_id`. Không gán hai schedule trùng giờ cho cùng giáo viên hoặc cùng phòng.

### ENROLLMENT

| enrollment_id | student_id | class_id | enrollment_status | enrollment_date | discount_amount | final_fee_amount |
|---|---|---|---|---|---:|---:|
| ENR-01 | STU-01 | CLS-40-A | Đang học | 2026-07-01 | 200000 | 3400000 |
| ENR-02 | STU-02 | CLS-40-A | Đang học | 2026-07-02 | 0 | 3600000 |
| ENR-03 | STU-03 | CLS-45-A | Đang học | 2026-09-10 | 0 | 4200000 |

`final_fee_amount = học phí theo cấp độ - discount_amount`. Không cho học viên bắt đầu học nếu chưa thanh toán đủ 100%.

### PAYMENT_ENTRY

| payment_id | enrollment_id | level_transfer_id | payment_type | amount | payment_date | payment_status |
|---|---|---|---|---:|---|---|
| PAY-01 | ENR-01 |  | Học phí đầu khóa | 3400000 | 2026-07-01 | Đã thanh toán đủ |
| PAY-02 | ENR-02 |  | Học phí đầu khóa | 3600000 | 2026-07-02 | Đã thanh toán đủ |
| PAY-03 | ENR-03 |  | Học phí đầu khóa | 4200000 | 2026-09-10 | Đã thanh toán đủ |

Chỉ điền một trong hai liên kết `enrollment_id` hoặc `level_transfer_id` theo `payment_type`.

## 3. Theo dõi học tập và chuyển cấp

### ASSESSMENT_RESULT

| assessment_id | student_id | assessment_type | assessment_date | listening_score | reading_score | writing_score | speaking_score | overall_band_score | recorded_by |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| ASM-01 | STU-01 | Kiểm tra tháng | 2026-08-28 | 5.5 | 5.0 | 4.5 | 5.0 | 5.0 | TCH-01 |
| ASM-02 | STU-02 | Kiểm tra tuần | 2026-08-28 | 4.0 | 4.0 | 3.5 | 4.0 | 4.0 | TCH-01 |

### STUDENT_ATTENDANCE

| attendance_id | student_id | schedule_id | attendance_status | recorded_by |
|---|---|---|---|---|
| ATT-01 | STU-01 | SCH-40-01 | Có mặt | TCH-01 |
| ATT-02 | STU-02 | SCH-40-01 | Vắng có phép | TCH-01 |

### LEVEL_TRANSFER

| transfer_id | student_id | current_level_id | proposed_level_id | current_class_id | proposed_by | proposal_date | proposal_type | surcharge_amount | student_decision | decision_date | approved_by |
|---|---|---|---|---|---|---|---|---:|---|---|---|
| TRF-01 | STU-01 | LVL-40 | LVL-45 | CLS-40-A | TCH-01 | 2026-09-28 | Đề xuất giữa kỳ bởi GV | 400000 | Chưa phản hồi |  | MGR-01 |

Ví dụ tính phụ thu theo A2: `(4.200.000 - 3.600.000) x (24 - 8) / 24 = 400.000 VND`. Đây là đề xuất chưa phản hồi, nên chưa tạo giao dịch `PAYMENT_ENTRY` phụ thu và chưa cập nhật cấp/lớp học viên.

## 4. Xin nghỉ dạy

### TEACHER_LEAVE_REQUEST

| leave_request_id | teacher_id | schedule_id | reason | request_date | resolution_type | new_schedule_id | substitute_teacher_id | approval_status | approved_by | approved_date |
|---|---|---|---|---|---|---|---|---|---|---|
| LVE-01 | TCH-01 | SCH-40-02 | Việc cá nhân | 2026-09-28 | Đổi giáo viên |  | TCH-03 | Đã duyệt | MGR-01 | 2026-09-28 |

Nếu dùng mẫu này, cập nhật `teacher_id` của `SCH-40-02` sang giáo viên thay sau khi duyệt. Chỉ chọn giáo viên thay đủ điều kiện cấp độ và không bị trùng lịch.

## Kiểm tra trước khi lưu

- Mỗi mã liên kết phải trỏ đến document đã tạo trước; dùng ID ERPNext thực tế nếu ID mẫu không được giữ.
- `end_date` phải sau `start_date`; `sessions_taught` không vượt `total_sessions`.
- Tổng tiền enrollment phải khớp học phí cấp độ sau giảm giá; payment học phí đầu khóa phải bằng số tiền cần thu.
- `surcharge_amount` chỉ tính khi có đề xuất chuyển cấp; chỉ thu phụ thu sau khi học viên đồng ý và đề xuất được duyệt.
- Kiểm tra các field bắt buộc riêng của DocType ERPNext trên UI. A2 không bao gồm hết các field mặc định của Student, Instructor, Course, Student Group và các DocType tài chính.