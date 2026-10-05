# Danh sách service — Hệ thống quản lý trung tâm Ling IELTS

> Tài liệu tổng hợp kiến trúc nghiệp vụ và các quyết định đã thảo luận. Các service là những khối chức năng ở mức tổng quan, không đồng nhất với module hay sản phẩm cụ thể.
> Nền móng: dữ liệu khảo sát nghiệp vụ (100+ học viên, 6 giáo viên, 10+ phòng, khóa 3 tháng, 2 buổi/tuần).

## 1. Cấu trúc kiến trúc tổng thể

| Phần | Vai trò | Nội dung |
| --- | --- | --- |
| **1. Client** | Điểm tương tác giữa người dùng và hệ thống | Giao diện quản trị cho quản lý/nhân sự; các kênh người dùng khác chỉ đưa vào khi nằm trong phạm vi triển khai |
| **Biên** | Xác thực và phân quyền | Kiểm soát danh tính, vai trò và phạm vi dữ liệu; là năng lực dùng chung cho các kênh được hệ thống hỗ trợ |
| **2. Services** | Các năng lực nghiệp vụ và dùng chung của hệ thống | Service nghiệp vụ, service dùng chung, dữ liệu và tích hợp với hệ thống ngoài |
| **3. Infrastructure** | Nơi hệ thống chạy và được vận hành | Máy chủ, mạng, triển khai, giám sát, sao lưu và CI/CD |

**Yêu cầu trực tiếp:** số hóa quy trình quản lý thông tin học viên, xếp lịch giảng dạy giáo viên, phân bổ phòng học và theo dõi dòng tiền thu học phí. Phạm vi kiến trúc lõi còn bao gồm các service liên quan đến quản lý và số hóa dữ liệu của tổ chức; các phần mở rộng được phân biệt riêng bên dưới.

## 2. Service nghiệp vụ

| # | Service | Chức năng chính | Dữ liệu làm chủ | Phạm vi |
| --- | --- | --- | --- | --- |
| 1 | **Học viên** | Hồ sơ học viên và phụ huynh, test đầu vào, xếp lớp theo cấp độ, lịch sử cấp độ; ghi nhận việc rút khóa khi phát sinh | Học viên, phụ huynh, kết quả test đầu vào, cấp độ, lịch sử | Lõi |
| 2 | **Giáo viên** | Hồ sơ, hợp đồng và đơn giá, lịch rảnh, yêu cầu nghỉ dạy và phê duyệt, tính lương tháng | Giáo viên, hợp đồng, yêu cầu nghỉ, bảng lương | Lõi |
| 3 | **Phòng học** | Danh mục và loại phòng, phân bổ, cảnh báo trùng, thống kê sử dụng | Phòng, lịch sử sử dụng phòng | Lõi |
| 4 | **Học liệu và chương trình đào tạo** | Chương trình, khóa/cấp độ và số buổi thuộc lõi dữ liệu; có thể đính kèm PDF. Kho video và ngân hàng đề được xem là phần mở rộng | Chương trình, tài liệu, đề | mở rộng |
| 6 | **Lịch học và buổi học** | Xếp lịch, mở/đóng lớp, điểm danh, xử lý giáo viên nghỉ (lùi lịch, đổi giáo viên, dạy bù), ghi nhận buổi dạy thực tế; buổi có thuộc tính hình thức tại phòng hoặc online | Lịch, buổi học, điểm danh, buổi dạy thực tế | Lõi |
| 7 | **Tài chính** | Học phí, giảm giá, ghi nhận thu, hoàn tiền, hóa đơn và biên lai, chi trả lương giáo viên | Khoản thu, khoản chi, hóa đơn, hoàn tiền | Lõi |
| 8 | **Kết quả học tập** | Kiểm tra tuần và tháng, điểm số, tổng kết cuối khóa, đề xuất và xử lý chuyển cấp | Điểm, tổng kết, đề xuất chuyển cấp | Lõi |
| 9 | **Phụ thu** | Tính phụ thu khi chuyển cấp, ghi nhận thanh toán phụ thu | Khoản phụ thu | Lõi |
| 10 | **Bài tập và kiểm tra online** | Giao bài, làm bài, nộp bài; Listening/Reading chấm tự động, Writing/Speaking giáo viên chấm | Bài giao, bài nộp, điểm chấm | Mở rộng |

Service Phòng học online (số 5 trong danh sách cũ) đã được loại bỏ. Online không còn là một service hay quy trình riêng mà chỉ là thuộc tính hình thức của buổi học trong service Lịch học và buổi học. Các số service còn lại được giữ nguyên để không làm thay đổi những tham chiếu đã dùng trước đó.

Các service nghiệp vụ từ 1 đến 9, ngoại trừ service 5 đã loại bỏ, thuộc kiến trúc lõi theo quyết định gộp các năng lực quản lý, vận hành và số hóa dữ liệu của trung tâm. Bốn quy trình trong yêu cầu là trọng tâm trực tiếp; các nghiệp vụ như lương, kết quả, chuyển cấp, phụ thu và hoàn tiền là các nghiệp vụ lõi liên quan nhưng không phải nội dung trực tiếp được nêu trong yêu cầu. Service 10 và phần kho tài liệu/đề chuyên sâu là hướng mở rộng.

## 3. Service dùng chung

| Service | Chức năng chính | Phạm vi / trạng thái |
| --- | --- | --- |
| **Báo cáo** | Tổng hợp dữ liệu từ nhiều service, gồm thu học phí, sử dụng phòng, điểm danh và kết quả | Lõi |
| **Chatbot** | Hỏi đáp theo role trên dữ liệu nghiệp vụ; chi tiết RAG để sau | Mở rộng, ngoài phạm vi hiện tại |

**Chat theo lớp không phải service của hệ thống.** Trao đổi giữa giáo viên, học viên và phụ huynh diễn ra trên Zalo ngoài hệ thống; không lưu hay xử lý nội dung chat, không dùng Raven. Zalo không phải một client ERP. Nếu sau này có tích hợp Zalo để gửi thông báo hoặc nhận yêu cầu cho chatbot thì đó là tích hợp riêng, cần quyết định sau.

## 4. Thành phần nền tảng

| Thành phần | Vai trò |
| --- | --- |
| **Xác thực và phân quyền** | Xác định người dùng và quyền thao tác/đọc dữ liệu theo vai trò. Nếu có cổng dành cho phụ huynh thì phải thiết kế quyền để phụ huynh chỉ xem được con mình |
| **Lưu trữ** | Lưu dữ liệu nghiệp vụ và file đính kèm. PDF theo hồ sơ/khóa có thể thuộc nhu cầu lõi; kho video và bản ghi dung lượng lớn cần đánh giá riêng |
| **Tích hợp** | Cầu nối tới dịch vụ ngoài khi có nhu cầu, ví dụ Zalo để gửi thông báo; không để service nghiệp vụ phụ thuộc trực tiếp vào nhà cung cấp |

## 5. Quy tắc nghiệp vụ đã chốt

### Học phí
- Học phí tính theo cấp độ; có thể có giảm giá.
- Đóng đủ 100% trước khi vào lớp, không cho nợ.
- Học phí khóa online và tại phòng như nhau.
- Các khóa có cùng tổng số buổi; phụ thu và hoàn tiền tính theo buổi, không theo ngày lịch.
- Mức giảm được áp dụng khi chuyển cấp. Lưu quy tắc giảm (phần trăm hoặc số tiền cố định) và lý do để tính nhất quán.

### Chuyển cấp và phụ thu
- Đủ điều kiện khi một tháng liên tục kiểm tra tuần và tháng đều vượt cấp hiện tại, hoặc giáo viên đề xuất giữa kỳ; quản lý phê duyệt.
- **Phụ thu = (Học phí cấp mới sau giảm − Học phí cấp cũ sau giảm) × (Số buổi còn lại / Tổng số buổi khóa).**
- Học viên đồng ý thì chuyển lớp; từ chối thì giữ lớp và lưu lịch sử đề xuất.
- Mức giảm được áp dụng cả khi chuyển cấp.

### Rút khóa và hoàn tiền
- Hoàn tiền áp dụng khi học viên kết thúc khóa trước khi khóa học kết thúc.
- Mốc tính là buổi đầu tiên học viên thông báo nghỉ; buổi đó được tính vào số buổi còn lại.
- **Hoàn tiền = Học phí khóa hiện tại sau giảm × (Số buổi còn lại / Tổng số buổi khóa).**
- Nếu học viên đã chuyển cấp và trả phụ thu thì dùng học phí sau giảm của cấp hiện tại (cấp mới).
- Số buổi còn lại lấy theo lịch hiện hành, gồm buổi dạy bù đã xếp lại. Lưu đầu vào tính toán và yêu cầu quản lý phê duyệt trước khi chi.
- Phụ thu và hoàn tiền dùng chung nguồn học phí áp dụng sau giảm.

### Lịch, phòng và giáo viên nghỉ
- Không trùng giờ giáo viên; không trùng giờ trong cùng một phòng.
- Giáo viên nghỉ: thứ tự xử lý **lùi lịch → đổi giáo viên → dạy bù → học online**. Quản lý phê duyệt.
- Chỉ có hai hình thức của buổi học: **tại phòng** và **online**. Đây chỉ là thuộc tính của buổi trong service Lịch học và buổi học, không có service Phòng học online hay quy trình nghiệp vụ riêng.
- Giáo viên quyết định hình thức mặc định cho lớp; hình thức có thể được xác định/đổi ở từng buổi.
- Các quy tắc điểm danh, tính số buổi, học phí và lương giống nhau giữa hai hình thức. Phân bổ phòng vật lý chỉ áp dụng cho buổi diễn ra tại phòng.

### Lương giáo viên
- **Lương tháng = Số buổi dạy thực tế trong tháng × đơn giá cố định.**
- Nghỉ rồi dạy bù không làm đổi số buổi; buổi bù và buổi online tính như buổi thường.
- Buổi được tính cho giáo viên thực tế đứng lớp, kể cả giáo viên thay thế.
- Chi trả theo tháng (tạm ghi nhận).

### Bài kiểm tra online (phần mở rộng)
| Kỹ năng | Cách chấm |
| --- | --- |
| Listening, Reading | Tự động theo đáp án, quy đổi band |
| Writing | Giáo viên chấm tay theo tiêu chí IELTS |
| Speaking | Giáo viên chấm trực tiếp hoặc chấm bản ghi âm |

### Phạm vi đã loại
- Tuyển sinh và tư vấn.
- Bảo lưu, danh sách chờ và các quy trình phức tạp của lớp.
- Chat theo lớp trong hệ thống.

## 6. Phân tầng và luồng dữ liệu giữa các service

| Tầng | Service |
| --- | --- |
| Dữ liệu gốc | 1 Học viên, 2 Giáo viên, 3 Phòng học, phần chương trình của 4 Học liệu |
| Vận hành | 6 Lịch và buổi học |
| Kết quả và tiền | 8 Kết quả học tập, 9 Phụ thu, 7 Tài chính |
| Dùng chung | Thông báo, Báo cáo, Chatbot (mở rộng) |
| Mở rộng | 10 Bài tập và kiểm tra online, kho video/ngân hàng đề |

**Luồng chính**
- `1 + 2 + 3 → 6`: hồ sơ học viên, giáo viên và phòng là dữ liệu đầu vào cho xếp lịch.
- `6 → 3`: phân bổ và cập nhật sử dụng phòng; buổi online không chiếm phòng vật lý.
- `6 → 2 → 7`: buổi dạy thực tế → tổng hợp lương → chi trả.
- `4 → 7/8`: chương trình, cấp độ và số buổi làm căn cứ cho học phí, phụ thu, hoàn tiền và kết quả đào tạo.
- `8 → 9 → 7`: đề xuất chuyển cấp → phụ thu → ghi nhận thu.
- `2 → 6`: yêu cầu nghỉ đã được duyệt thì lịch được xử lý lại.
- Service Thông báo nhận sự kiện từ nghiệp vụ để phát tin; Báo cáo chỉ đọc dữ liệu tổng hợp, không làm chủ dữ liệu nghiệp vụ.

**Nguyên tắc**
1. Mỗi dữ liệu chỉ có một service làm chủ; service khác chỉ đọc hoặc nhận sự kiện.
2. Luồng nghiệp vụ chính đi theo các tầng; các sự kiện ngược chiều không làm phát sinh quyền ghi tùy tiện vào service khác.
3. Service 6 làm chủ số buổi dạy thực tế; service 2 dùng dữ liệu đó để tính lương.
4. Chat Zalo giữa người với người nằm ngoài hệ thống; không có luồng chat hay lưu nội dung hội thoại trong kiến trúc.

## 7. Cách thể hiện trên sơ đồ

- Giữ ba phần tổng thể: **Client**, **Services** (gồm các block nghiệp vụ, dùng chung, data và external phù hợp) và **Infrastructure**; thể hiện xác thực/phân quyền ở biên Client–Services.
- Giữ service ở mức vai trò/chức năng kiến trúc. Không đổi tên service thành sản phẩm hoặc module của giải pháp.
- Phân biệt lõi và hướng mở rộng bằng màu hoặc kiểu đường viền riêng.
- Zalo, nếu cần chú thích, nằm ngoài ranh giới hệ thống và chỉ thể hiện như nền tảng trò chuyện giữa người với người; không vẽ thành service chat hoặc client ERP.
- Kiểm tra online, kho nội dung mở rộng và chatbot chỉ thể hiện như các khối mở rộng, chưa gắn với sản phẩm cụ thể.

## 8. Định hướng giải pháp — tách biệt với kiến trúc

ERPNext v16 là **một giải pháp được lựa chọn/định hướng để triển khai các năng lực ERP lõi**, không phải tên gọi của toàn bộ kiến trúc và không thay thế các service trong sơ đồ. Ở bước ánh xạ giải pháp, mới xác định service nào được ERPNext đáp ứng sẵn, service nào cần cấu hình, tùy biến hoặc triển khai riêng. Việc dùng ERPNext không làm thay đổi ranh giới, trách nhiệm hay luồng dữ liệu của các service đã mô tả.

| Nội dung | Định hướng |
| --- | --- |
| Phạm vi phù hợp để đánh giá ERPNext | Quản lý học viên, giáo viên, phòng, lịch, tài chính và các nghiệp vụ số hóa khác trong lõi |
| Cần kiểm chứng khi chọn giải pháp | Service nào được nền tảng đáp ứng sẵn, service nào cần cấu hình hoặc tùy biến |
| Ngoài giải pháp ERP lõi / có thể triển khai riêng | Kiểm tra online, kho video/ngân hàng đề, chatbot/RAG, tích hợp Zalo |
| Trò chuyện người với người | Tiếp tục dùng Zalo ngoài hệ thống theo quyết định đã thống nhất |

Khả năng ERPNext lưu file PDF là một lựa chọn triển khai cho nhu cầu đính kèm tài liệu; không làm thay đổi việc dữ liệu chương trình và tài liệu được sở hữu bởi service Học liệu. Kho video/bản ghi dung lượng lớn và quyền truy cập theo lớp cần được đánh giá riêng.

## 9. Các điểm còn mở / chưa chốt

1. **Kho video và ngân hàng đề:** chưa quyết định triển khai; nếu có thì chọn cách lưu và thiết kế quyền.
3. **Phản hồi đề xuất chuyển cấp:** cách học viên xác nhận/từ chối và cách ghi nhận vào service nghiệp vụ chưa chốt.
4. **Chatbot/RAG và kiểm tra online:** ngoài phạm vi hiện tại, để xem xét ở giai đoạn sau.
5. **Lựa chọn giải pháp:** ERPNext là một giải pháp cần đánh giá; cần kiểm chứng mức đáp ứng của từng service, không suy ra từ sơ đồ kiến trúc.
