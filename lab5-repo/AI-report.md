# AI report: cách dùng AI trong bài LAB-5

Toàn bộ bài được làm trong một cuộc trò chuyện dài với Claude (giao diện chat của Anthropic). Báo cáo này ghi lại việc đã xảy ra, không ghi những việc không làm.

## 1. Skill, prompt và cách dùng AI cho từng việc

**Skill đã dùng.** Skill chấm SWP chính thức không có trong tay người làm bài, nên đã dùng skill tự đặt `skills/swp-scoring` (thang Scope × Complexity, script tính SWP và dựng báo cáo HTML), viết trong chính cuộc trò chuyện. Ngoài ra AI dùng khả năng tạo file có sẵn (bảng tính xlsx, Markdown, CSV, script Python, biểu đồ) để làm sản phẩm.

| Việc | Prompt thực tế (rút gọn) | Cách AI làm | Kết quả |
|---|---|---|---|
| Break task | "tôi có bài tập lab 5, hãy phân tích và hoàn thành output tốt nhất", kèm ảnh đề và các tài liệu LAB-4 đã làm trước đó trong cuộc trò chuyện | Đọc đề, lập bản đồ ràng buộc nghiệp vụ, chia thành epic theo module kiến trúc, mỗi task không quá 8 giờ, tách riêng từng quy tắc giờ lái xe | 8 epic, 63 task, 18 subtask ban đầu; sau khi đối chiếu LAB-1 thành 66 task |
| Đổi đề | "đề bài của lab 5 đã bị thay đổi mà tôi không biết ... tôi muốn giúp tôi hoàn thành lần lượt tất cả các yêu cầu" | Phân tích đề mới, so với sản phẩm cũ, lập thứ tự làm theo mức phụ thuộc giữa các file | Danh sách việc, thứ tự: PREMISE, task-breakdown, SWP và estimate, Project, progress-report, AI-report, README |
| Chấm SWP | "tôi không có skill SWP", sau đó "giữ nguyên hết" | Đề xuất tự viết skill; chấm Scope và Complexity cho 78 issue lá kèm lý do; script tính SWP, đối chiếu với giờ, dựng báo cáo HTML | `swp-report/`, 269 SWP; người làm bài xem tổng hợp và quyết định giữ nguyên |
| Quy giờ | Không có prompt riêng, làm trong cùng chuỗi | Ước giờ trực tiếp cho từng issue theo khối lượng làm việc; chọn cách ước trực tiếp thay vì đổi từ SWP vì chưa có dữ liệu năng suất; đối chiếu với file estimate LAB-1 do người làm bài gửi | `estimate.md` mục 3 và 5 |
| Báo cáo tiến độ | Không có prompt riêng; theo yêu cầu của đề | Dựng một sprint giả lập (trạng thái từng task, burndown theo giờ, việc phát sinh giữa sprint, rủi ro trễ có số issue cụ thể); số liệu do AI đặt ra và được ghi rõ là giả lập | `progress-report.md`, biểu đồ burndown |
| Ghi SWP và đưa backlog lên Project | "tạo github project như thế nào", sau đó là các ảnh lỗi khi chạy | AI **không có quyền** ghi vào GitHub nên không dùng agent ghi trực tiếp. AI viết hai script bằng GitHub CLI (`tools/create_github_project.py` tạo issue và Project, `tools/upgrade_project.py` tạo sub-issue, Iteration và ghi SWP từ `swp-report/swp-scores.csv`); người làm bài chạy trên máy | 92 issue, field Story Point, Estimate, SWP, Iteration |

## 2. Review output của AI

Phần lớn việc kiểm chéo do chính AI thực hiện trong lúc làm; người làm bài review ở các điểm quyết định, kiểm số liệu trên board và chạy thử script. Bảng dưới liệt kê các vấn đề thật đã phát hiện.

| Bước review | Ai review | Vấn đề phát hiện | Xử lý |
|---|---|---|---|
| Đối chiếu từng yêu cầu của đề với sản phẩm (người làm bài hỏi "chúng ta đang làm đúng đề bài ko") | Người làm bài hỏi, AI đối chiếu | Board chưa có người phụ trách; task bị chặn không có trạng thái riêng trên board | Hướng dẫn gán Assignees; dùng nhãn `blocked` |
| Tự kiểm công thức trong bảng tính báo cáo | AI | Hệ số giờ thực tế trên ước lượng ra 1,85 thay vì 1,07 do tham chiếu ô sai; tốc độ đốt tính nhầm ngày | Sửa công thức, tính lại và kiểm số |
| Chạy thử script ở chế độ không tạo gì (dry-run) | AI | Lệnh tạo issue không được in ra ở chế độ chạy thử, nên bản đầu không kiểm tra được | Sửa script, in đủ lệnh |
| Chạy thật trên máy | Người làm bài | PowerShell hiểu sai `@me`; mất mạng giữa chừng làm script dừng; chạy lại thì có nguy cơ tạo trùng | Đặt `@me` trong dấu nháy; thêm tự thử lại và bỏ qua phần đã tạo; thêm in tiến trình |
| Đếm issue trên GitHub | Người làm bài | Số issue Closed nhiều hơn dự kiến lúc script còn chạy | AI giải thích do tùy chọn đặt trạng thái; số cuối khớp 76 Open và 13 Closed |
| Đối chiếu spec LAB-4 với schema LAB-2 | AI, người làm bài gửi schema | Spec LAB-4 lệch schema ở hợp đồng giao (NULL), đơn vị số lượng, vai trò, bảng watermark, bảng tồn, trạng thái phiếu, truy xuất | Chín dòng sửa P-01 đến P-09 trong `PREMISE.md` |
| So backlog với estimate LAB-1 | AI, người làm bài gửi file | Bản LAB-4 chỉ có bốn quy tắc giờ lái trong khi LAB-1 liệt kê tám; LAB-4 dùng FIFO còn LAB-1 dùng FEFO; một giá trị từng bị ghi là "giả định" thực ra đã có trong LAB-1 | Thêm 3 issue (#90 đến #92), thêm P-10 và P-11, sửa G-01 |
| Chốt quyết định thiết kế (bỏ bảng watermark, bỏ bảng tồn, đổi tên trạng thái, gộp truy xuất, cách so 日付逆転) | Người làm bài | AI đề xuất theo mặc định | Người làm bài trả lời "đồng ý hết" |
| Review điểm SWP | Người làm bài | AI chấm lần đầu; không issue nào vượt ngưỡng lệch 50% so với trung vị cùng mức, tám issue nằm đúng ở ±50% | Kiểm thủ công sáu issue, giữ nguyên; người làm bài quyết định giữ nguyên toàn bộ điểm |

Điểm SWP chưa được đối chiếu với dữ liệu năng suất thực tế, và người làm bài chưa đọc lại từng lý do chấm của 78 issue.

## 3. Điểm đặc biệt trong cách dùng AI

**Chỗ cho là hiệu quả.**
- Đối chiếu nhiều tài liệu một lúc: đọc file estimate LAB-1 (52 chức năng, tiếng Nhật) và so với backlog phát hiện được ba chỗ thiếu mà nếu làm tay dễ bỏ qua.
- Sinh script tạo 92 issue, sub-issue và field cho Project, thay vì nhập tay; script có tự thử lại khi mất mạng.
- Sửa lặp nhanh khi đề đổi giữa chừng: phân tích lại, nêu rõ phần dùng lại được và phần phải làm mới.

**Chỗ chưa tốt, cần cải thiện khi làm thật.**
- AI từng ghi một giá trị là "giả định" trong khi nguồn đã có trong tài liệu LAB-1; chỉ khi người làm bài đưa tài liệu nguồn mới sửa được. Cần luôn cho AI đủ tài liệu gốc.
- Số liệu Sprint 1 do AI tạo nên dễ bị hiểu nhầm là số thật; phải ghi nhãn giả lập ở mọi nơi.
- Skill SWP tự đặt, chưa hiệu chỉnh; điểm do AI chấm nên cần người có kinh nghiệm review từng lý do, việc này chưa làm hết trong giới hạn thời gian.
- Script GitHub chưa được thử với GitHub thật trước khi giao, nên lần chạy đầu gặp lỗi; AI không đọc được Google Drive, Google Sheets hay GitHub riêng tư nên file phải chuyển tay.
- Cuộc trò chuyện rất dài (nhiều bài lab xen kẽ); chi tiết ở phần đầu dễ lệch khi đề bài đổi, cần tách mỗi bài một cuộc trò chuyện.

**Chưa có ý tưởng.** Cách hiệu chỉnh quan hệ giữa SWP và giờ bằng dữ liệu năng suất thật của nhóm; cách cho một agent ghi trực tiếp lên Project mà vẫn kiểm soát được quyền hạn và có người duyệt từng thay đổi.
