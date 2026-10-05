# Danh sách service — Hệ thống quản lý trung tâm Ling IELTS

> Tài liệu tổng hợp các quyết định thiết kế đã thảo luận, làm đầu vào cho bước chọn giải pháp / tech stack.
> Nền móng: dữ liệu khảo sát nghiệp vụ (100+ học viên, 6 giáo viên, 10+ phòng, khóa 3 tháng, 2 buổi/tuần).

---

## 1. Cấu trúc kiến trúc: 3 phần

| Phần | Vai trò | Nội dung |
| --- | --- | --- |
| **1. Client** | Quyết định cách người dùng giao tiếp với hệ thống | Giao diện quản trị, web chat nhúng, Zalo |
| **Biên** | Xác thực và phân quyền | Nằm giữa phần 1 và phần 2, một điểm vào chung cho cả 3 kênh |
| **2. Services** | Toàn bộ service, dữ liệu và dịch vụ ngoài | Chia thành các block: nghiệp vụ, giao tiếp, AI, data, external |
| **3. Infrastructure** | Nơi hệ thống chạy và được vận hành | Server, container, giám sát, sao lưu, CI/CD |

Người dùng: **quản lý, giáo viên, học viên, phụ huynh**. Quyền của chatbot bị giới hạn theo role của người đang hỏi.

---

## 2. Service nghiệp vụ (10)

| # | Service | Chức năng chính | Dữ liệu làm chủ |
| --- | --- | --- | --- |
| 1 | **Học viên** | Hồ sơ học viên và phụ huynh, test đầu vào, xếp lớp theo cấp độ, lịch sử cấp độ | Học viên, phụ huynh, kết quả test đầu vào, cấp độ |
| 2 | **Giáo viên** | Hồ sơ, hợp đồng và đơn giá, lịch rảnh, yêu cầu nghỉ dạy và phê duyệt, tính lương tháng | Giáo viên, hợp đồng, yêu cầu nghỉ, bảng lương |
| 3 | **Phòng học** | Danh mục và loại phòng, phân bổ, cảnh báo trùng, thống kê sử dụng | Phòng, lịch sử dụng phòng |
| 4 | **Học liệu** | Chương trình đào tạo, tài liệu theo cấp độ và kỹ năng, đề mẫu, ngân hàng đề kèm đáp án, phân quyền xem theo lớp | Chương trình, tài liệu, đề |
| 5 | **Lịch học và buổi học** | Xếp lịch, mở/đóng lớp, điểm danh (offline và online), xử lý giáo viên nghỉ (lùi lịch, đổi giáo viên, dạy bù, chuyển online), ghi nhận buổi dạy thực tế | Lịch, buổi học, điểm danh, buổi dạy thực tế |
| 6 | **Tài chính** | Học phí, giảm giá, ghi nhận thu, hoàn tiền (chờ xác nhận), hóa đơn và biên lai, chi trả lương giáo viên | Khoản thu, khoản chi, hóa đơn, hoàn tiền |
| 7 | **Kết quả học tập** | Kiểm tra tuần và tháng, điểm số, tổng kết cuối khóa, đề xuất và xử lý chuyển cấp | Điểm, tổng kết, đề xuất chuyển cấp |
| 8 | **Phụ thu** | Tính phụ thu khi chuyển cấp, ghi nhận thanh toán phụ thu | Khoản phụ thu |
| 9 | **Bài tập và kiểm tra online** | Giao bài, làm bài, nộp bài. Listening và Reading chấm tự động; Writing và Speaking giáo viên chấm tay | Bài giao, bài nộp, điểm chấm (trước khi chuyển sang service 8) |

## 3. Service dùng chung (3)

| Service | Chức năng chính | Trạng thái |
| --- | --- | --- |
| **Báo cáo** | Tổng hợp từ các service nghiệp vụ, gồm thống kê sử dụng phòng | Chưa thiết kế |
| **Chatbot** | Hỏi đáp theo role | Chỉ chừa chỗ; chi tiết RAG làm sau (học liệu là nguồn tri thức) |

## 4. Thành phần nền tảng (3)

| Thành phần | Nội dung |
| --- | --- |
| **Xác thực và phân quyền** | Điểm vào chung cho 3 kênh; phân quyền theo role và phạm vi dữ liệu (phụ huynh chỉ thấy con mình) |
| **Lưu trữ** | CSDL nghiệp vụ, kho file (tài liệu, video, bản ghi họp), cache, vector DB (khi làm RAG) |
| **Tích hợp** | Zalo, nền tảng họp, email, LLM |

---

## 5. Quy tắc nghiệp vụ đã chốt

### Học phí
- Học phí tính theo cấp độ; có thể giảm giá trong một số trường hợp.
- Đóng đủ 100% trước khi vào lớp, không cho nợ.

### Chuyển cấp và phụ thu
- Đủ điều kiện khi 1 tháng liên tục kiểm tra tuần + tháng đều vượt cấp hiện tại, hoặc giáo viên đề xuất giữa kỳ; quản lý phê duyệt.
- **Phụ thu = (Học phí cấp mới − Học phí cấp cũ) × (Số buổi còn lại / Tổng số buổi khóa)**
- Học viên đồng ý thì chuyển lớp; từ chối thì giữ lớp và lưu lịch sử đề xuất.

### Lịch, phòng, giáo viên nghỉ
- Không trùng giờ giáo viên; không trùng giờ trong cùng một phòng.
- Giáo viên nghỉ: thứ tự xử lý **lùi lịch → đổi giáo viên → dạy bù → học online**. Quản lý phê duyệt.

### Lương giáo viên
- **Lương tháng = Số buổi dạy thực tế trong tháng × đơn giá cố định.**
- Nghỉ rồi dạy bù không làm đổi số buổi; buổi bù và buổi online tính như buổi thường.
- Buổi tính cho giáo viên đã dạy thực tế (kể cả giáo viên thay thế).
- Chi trả theo tháng (tạm ghi nhận).

### Bài kiểm tra online
| Kỹ năng | Cách chấm |
| --- | --- |
| Listening, Reading | Tự động theo đáp án, quy đổi band |
| Writing | Giáo viên chấm tay theo tiêu chí IELTS |
| Speaking | Giáo viên chấm trực tiếp hoặc chấm bản ghi âm |

### Phạm vi đã loại
- Tuyển sinh và tư vấn.
- Bảo lưu, danh sách chờ và các quy trình phức tạp của lớp.

---

## 6. Phân tầng và luồng dữ liệu giữa các service

| Tầng | Service |
| --- | --- |
| Dữ liệu gốc | 1 Học viên, 2 Giáo viên, 3 Phòng học, 4 Học liệu |
| Vận hành | 6 Lịch và buổi học, 5 Phòng học online, 10 Bài tập và kiểm tra online |
| Kết quả và tiền | 8 Kết quả học tập, 9 Phụ thu, 7 Tài chính |

**Luồng chính**
- `6 → 2 → 7`: buổi dạy thực tế → tổng hợp lương → chi trả.
- `4 → 10 → 8`: đề lấy từ học liệu → làm bài → điểm vào kết quả học tập.
- `8 → 9 → 7`: đề xuất chuyển cấp → phụ thu → ghi nhận thu.
- `2 → 6`: yêu cầu nghỉ được duyệt thì lịch xử lý lại.
- `6 → 5 → 6`: buổi chuyển online tạo phòng họp; người tham dự trở thành điểm danh.

**Nguyên tắc**
1. Mỗi dữ liệu chỉ có một service làm chủ; service khác chỉ đọc hoặc nhận sự kiện.
2. Luồng đi một chiều theo tầng; chiều ngược lại dùng sự kiện (nghỉ đã duyệt, buổi học hoàn thành, người tham dự).
3. Tránh vòng phụ thuộc: service 6 làm chủ "buổi dạy thực tế", service 2 chỉ đọc để tính lương.

---

## 7. Cách thể hiện trên sơ đồ

- **Khung ngoài** ghi tên nền tảng (nếu dùng nền tảng có sẵn); **block bên trong** ghi tên vai trò từng service.
- Phân biệt bằng màu: tự xây / nền tảng có sẵn / dịch vụ bên ngoài / hạ tầng.
- Điểm chưa chọn giải pháp thì ghi tên vai trò (ví dụ "Dịch vụ họp online"), chọn xong thì thêm tên sản phẩm trong ngoặc.
- Zalo vẽ ở hai nơi: kênh vào (phần 1) và kênh gửi thông báo ra (external).

## 8. Hướng nền tảng đang nghiêng về

**Mở rộng nền tảng có sẵn (lai):** dùng nền tảng cho phần chuẩn (học viên, lịch, phòng, điểm danh, thu học phí), viết app tùy biến cho phần đặc thù (chuyển cấp, phụ thu, nghỉ dạy, lương theo buổi), và để dịch vụ rời cho phần khác bản chất (kiểm tra online, họp online, thông báo Zalo, chatbot).

| Mức phủ của nền tảng | Service |
| --- | --- |
| Phủ phần lớn | 1, 3, 6, 7 (phần thu học phí) |
| Phủ một phần | 4, 8 |
| Gần như tự làm | 2 (lương theo buổi), 5, 9, 10, nghỉ dạy và dạy bù |
| Ngoài nền tảng | Thông báo Zalo, chatbot, web chat nhúng |

> Mức phủ dựa trên tài liệu, chưa kiểm chứng trên bản cài thật.

---

## 9. Các điểm còn mở

1. **Hoàn tiền:** còn áp dụng trong trường hợp nào, hay bỏ khỏi service 7.
2. **Hình thức học online:** lớp trực tuyến theo lịch, tự học qua video, hay cả hai.
3. **Nền tảng họp online** và **chat theo lớp**: chưa quyết định.
4. **Học phí học online:** có khác học phí offline không.
5. **Chi tiết chatbot/RAG:** để giai đoạn sau.
