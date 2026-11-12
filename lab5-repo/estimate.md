# Estimate: Kho lạnh Yuki (Product B)

## 1. Báo cáo HTML của skill chấm SWP

Báo cáo nằm ở [`swp-report/index.html`](swp-report/index.html); bảng SWP của mọi issue ở [`swp-report/swp-scores.csv`](swp-report/swp-scores.csv). Skill chấm là skill tự đặt, mô tả ở [`skills/swp-scoring/SKILL.md`](skills/swp-scoring/SKILL.md) (skill chấm SWP chính thức không có trong tay người làm bài). GitHub hiển thị file HTML dưới dạng mã nguồn, nên cần tải về hoặc mở bằng GitHub Pages để xem báo cáo dạng trang.

## 2. Issue mẫu skill chọn để kiểm

Quy tắc đối chiếu là giờ lệch quá 50% so với trung vị cùng mức SWP; kết quả là **không có issue nào vượt ngưỡng**. Tám issue nằm đúng ở ngưỡng ±50% nên skill chọn sáu issue trong đó để kiểm thủ công (hai nhóm: giờ thấp hơn trung vị và giờ cao hơn trung vị).

| Issue | Skill chấm (Scope × Complexity → SWP) | Chốt | Lý do |
|---|---|---|---|
| #42 E4-T05, sub-issue khóa advisory | 2 × 4 = 8 → SWP 5; ước 3 giờ (trung vị mức 5 là 6 giờ, thấp hơn 50%) | Giữ SWP 5, giữ 3 giờ | Phần khó là độ bất định (Complexity 4): mã ít nhưng sai thì lỗi chỉ lộ khi chạy đồng thời. Giờ đủ cho việc cài đặt; rủi ro được theo dõi ở R-05 trong progress-report.md |
| #44 E4-T05, sub-issue test hai phiên song song | 1 × 3 = 3 → SWP 2; ước 2 giờ (trung vị mức 2 là 4 giờ, thấp hơn 50%) | Giữ SWP 2, giữ 2 giờ | Phần khó đã tách sang sub-issue khóa advisory; kịch bản test đã rõ nên 2 giờ đủ |
| #2 E1-T01, repo, CI và hai môi trường | 3 × 1 = 3 → SWP 2; ước 6 giờ (cao hơn trung vị mức 2 là 50%) | Giữ SWP 2, giữ 6 giờ | Việc cơ học (Complexity 1) nhưng nhiều thành phần cấu hình (Scope 3), nên tốn giờ hơn điểm kích thước; chênh do khối lượng, không do độ khó |
| #5 E1-T04, màn quản lý SKU | 2 × 2 = 4 → SWP 2; ước 6 giờ (cao hơn 50%) | Giữ SWP 2, giữ 6 giờ | Màn CRUD có nhiều field bắt buộc kèm ba thuộc tính phân loại; thời gian dồn vào form và validation |
| #35 E4-T02, bước V1 (trạng thái lô) | 1 × 1 = 1 → SWP 1; ước 3 giờ (trung vị mức 1 là 2 giờ, cao hơn 50%) | Giữ SWP 1, giữ 3 giờ | Logic một điều kiện nhưng phải nối vào engine cấp phát và viết test, tối thiểu 3 giờ |
| #49 E4-T07, bước V5 (truy xuất) | 1 × 2 = 2 → SWP 1; ước 3 giờ (cao hơn 50%) | Giữ SWP 1, giữ 3 giờ | Điều kiện phụ thuộc loại sản phẩm (gạo, bò), cần ca test cho từng loại |

Không sửa issue nào sau khi kiểm: mọi chênh đều giải thích được bằng khối lượng cấu hình, độ bất định hoặc test đi kèm, và nằm trong biên ±50%.

## 3. Cách quy ra giờ

**Cách đã chọn.** Giờ được ước trực tiếp cho từng issue (từ dưới lên). SWP do skill chấm độc lập rồi ghi vào field "SWP (đã review)" để đối chiếu, không dùng làm hệ số đổi ra giờ.

**Vì sao.** SWP đo độ lớn tương đối của issue, còn giờ cần để lập capacity và so sánh với estimate LAB-1 (đơn vị người-ngày). Chưa có dữ liệu năng suất thực tế của nhóm để suy ra hệ số đổi từ SWP sang giờ, nên ước trực tiếp ít sai lệch hơn một hệ số đặt tay.

**Quy tắc áp dụng nhất quán.**
1. Giờ ước lượng là giờ làm trực tiếp của một người cho một issue, gồm viết mã, unit test và sửa lỗi nhỏ; không gồm review của người khác và họp.
2. Làm tròn đến 1 giờ; một issue không quá 8 giờ. Issue ước lượng 7 đến 8 giờ và có ít nhất hai phần logic độc lập thì tách sub-issue; giờ các sub-issue cộng đúng bằng issue cha.
3. Một ngày công bằng 7 giờ, cùng quy ước với estimate LAB-1, để hai bảng so sánh được.
4. Chỉ epic E5 (lập lịch giao và giờ lái xe) có dự phòng 15% giờ, vì tham số nghiệp vụ chưa được khách xác nhận (G-01 trong PREMISE.md). Dự phòng này không cộng vào tổng giờ ở mục 4. Các epic khác không có dự phòng, khác với estimate LAB-1 (dự phòng 15 đến 30% trong từng task).
5. Issue của QA và các việc kiểm thử tính vào giờ của epic chứa nó, nhưng được tách theo Role để so với dòng QA của LAB-1 ở mục 5.
6. Sau khi có SWP: issue nào có giờ lệch hơn 50% so với trung vị giờ của cùng mức SWP thì được xem lại; issue nằm đúng ở ngưỡng ±50% cũng được kiểm thủ công. Kết quả ghi ở bảng mục 2.

## 4. Tổng theo epic

| Epic | Số issue | Tổng SWP | Tổng giờ | Ghi chú |
|---|---|---|---|---|
| E1 #1 Nền tảng và danh mục | 10 issue + 3 sub-issue | 33 | 61 | Gồm 4 giờ QA (dữ liệu mẫu) |
| E2 #15 Nhập kho | 7 issue + 3 sub-issue | 27 | 45 | Gồm 6 giờ QA |
| E3 #26 Tồn kho và vòng đời lô | 6 issue | 24 | 36 | Gồm 4 giờ QA |
| E4 #33 Xuất hàng và kiểm lô | 12 issue + 9 sub-issue | 57 | 71 | Gồm 8 giờ QA; thêm E4-T12 theo P-11 |
| E5 #54 Lập lịch giao và giờ lái xe | 14 issue + 3 sub-issue | 61 | 80 | Gồm 11 giờ QA; thêm E5-T13, E5-T14 theo P-10; dự phòng riêng 15% (khoảng 12 giờ), chưa tính vào tổng |
| E6 #70 HACCP và truy xuất | 7 issue | 29 | 42 | Gồm 4 giờ QA |
| E7 #78 Phân quyền, audit, bảo mật | 4 issue | 15 | 21 | Gồm 2 giờ QA |
| E8 #83 Kiểm thử, triển khai, tài liệu | 6 issue | 23 | 37 | Gồm 23 giờ QA |
| **Tổng** | **66 issue + 18 sub-issue** | **269** | **393** | Tương đương khoảng 56 ngày công (7 giờ/ngày); giờ QA của toàn bộ epic là 62 |

## 5. So với estimate LAB-1

Nguồn LAB-1: file `YCL-2026-01_Effort_Estimation_v2` (1.299 người-ngày, tức 9.093 giờ ở 7 giờ/ngày). Số liệu từng phần được cộng từ sheet `01_Server` (cột Backend, Frontend, Design theo nhóm chức năng FG-01 đến FG-11), sheet hạ tầng và sheet tổng hợp. Với LAB-5, cột giờ chỉ gồm giờ phát triển (Backend và Frontend) của epic tương ứng; giờ QA được so ở dòng riêng.

| Phần (chức năng/epic) | LAB-1 (giờ) | LAB-5 (giờ) | Chênh (giờ) | Vì sao |
|---|---|---|---|---|
| Danh mục và nền tảng: FG-01 so với E1 | 371 (53 ngày) | 57 | -314 | LAB-1 có vòng đời master (tạo, duyệt, kích hoạt, ngừng dùng), tách người đề xuất và người duyệt (F-006) và danh mục thiết bị (F-005); LAB-4 không có các phần này, LAB-5 chỉ làm danh mục, ngưỡng nhiệt và hợp đồng |
| Nhập kho: FG-02 so với E2 | 399 (57 ngày) | 39 | -360 | LAB-1 có lịch hẹn nhập (F-008), chụp và đính ảnh khi kiểm (F-009), duyệt phân tán khi lệch số lượng (F-010), tự động cách ly (F-012), gán dải nhiệt tạm (F-013); LAB-4 chỉ có một form nhập một lô kèm cách ly hoặc từ chối |
| Tồn kho và lô: FG-03 so với E3 | 322 (46 ngày) | 32 | -290 | LAB-1 có gợi ý vị trí cất hàng (F-015), kiểm kê mù (F-017), nhật ký di chuyển (F-016); LAB-4 chỉ có xem tồn, trạng thái lô và job quá hạn |
| Xuất hàng: FG-04 so với E4 | 749 (107 ngày) | 63 | -686 | LAB-1 còn gom việc lấy hàng (F-022), kiểm và xếp hàng bằng mã vạch (F-023), kiểm tra trước xuất (F-024), bằng chứng giao hàng trên thiết bị tài xế (F-025), trả hàng và khiếu nại (F-026); LAB-4 chỉ có phần kiểm lô và chọn lô. Thêm 3 giờ cho E4-T12 theo P-11 |
| Lập lịch giao và giờ lái: FG-05 so với E5 | 525 (75 ngày) | 69 | -456 | LAB-1 có công bố tuyến có phiên bản (F-030), nghỉ chèn trong lịch trình (F-029), tách sự kiện khách quan khỏi báo cáo tuân thủ (F-031); LAB-5 có đủ các quy tắc giờ lái sau P-10 (thêm 10 giờ) nhưng không có công bố tuyến |
| HACCP và truy xuất: FG-06 và FG-07 so với E6 | 749 (107 ngày) | 38 | -711 | LAB-1 có nhập dữ liệu logger (F-032), hàng đợi cảnh báo theo SLA (F-034), ca sai lệch (F-035), thu hồi sản phẩm (F-038, F-039); LAB-4 chỉ có ghi nhiệt độ, hành động khắc phục và tra cứu truy xuất |
| Phân quyền và audit: FG-10 so với E7 | 259 (37 ngày) | 19 | -240 | LAB-1 có đăng nhập một lần, MFA, thiết bị dùng chung (F-048); LAB-4 chỉ có ma trận quyền theo vai trò và nhật ký audit |
| Báo cáo: FG-08 | 161 (23 ngày) | 0 | -161 | Không có trong LAB-4, không có issue |
| Giao diện ngoài: FG-09 | 245 (35 ngày) | 0 | -245 | Không có trong LAB-4 (tích hợp ERP, bản đồ, email nằm ngoài phạm vi), không có issue |
| Chuyển đổi dữ liệu: FG-11 | 280 (40 ngày) | 0 | -280 | Không có trong LAB-4, không có issue |
| Thiết kế cơ bản, hạ tầng, bằng chứng phi chức năng, chuyển đổi, đào tạo so với E8 | 1.029 (147 ngày) | 14 | -1.015 | LAB-1 gồm cả hạ tầng và đào tạo, tính cho hệ thống thật; LAB-5 chỉ có CI, triển khai và tài liệu cho phạm vi LAB-4 |
| QA (kiểm thử thủ công và tự động) | 2.142 (306 ngày) | 62 | -2.080 | LAB-1 tính QA theo từng chức năng của 52 chức năng; LAB-5 có QA cho phạm vi nhỏ hơn nhiều |
| Quản lý dự án và BrSE | 1.862 (266 ngày) | 0 | -1.862 | LAB-1 tính chi phí quản lý (khoảng 10% tổng) và BrSE (khoảng 12% tổng); LAB-5 chưa tính hai vai trò này |
| **Tổng** | **9.093** | **393** | **-8.700** | LAB-5 bằng khoảng 4% LAB-1 |

**Đọc bảng.** Chênh lệch lớn do hai nguyên nhân chính. Một là phạm vi: LAB-1 ước cho 52 chức năng của hệ thống hoàn chỉnh (11 nhóm FG, kèm hạ tầng, chuyển đổi dữ liệu và đào tạo), còn LAB-5 chỉ chia từ bản thiết kế LAB-4 (5 màn hình lõi, 6 module); ba nhóm FG-08, FG-09, FG-11 không có issue nào. Hai là mức chi tiết: LAB-1 ước theo từng chức năng và có dự phòng 15 đến 30% trong mỗi task, còn LAB-5 ước theo issue nhỏ cho một sản phẩm thử, chỉ dự phòng cho E5. Phần chênh do thay đổi ở PREMISE.md nhỏ: P-10 thêm 10 giờ cho E5 và P-11 thêm 3 giờ cho E4.
