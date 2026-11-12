# PREMISE: tiền đề của backlog LAB-5

Backlog trong repo này được chia từ bản LAB-4 nộp ngày 08/10/2026 (5 file: ADR, Architecture Design, Database diagram, screen spec, Wireframe) và **có thay đổi so với bản đó**. Các thay đổi nằm ở ba phần dưới. Mã spec lấy theo tên file và mục của bản LAB-4; mã `P-xx`, `G-xx`, `H-xx` được các file khác trong repo dùng để trỏ về. Số `#n` là số issue trên GitHub Project.

## 1. Spec thêm, bỏ, sửa so với LAB-4

| # | Spec (mã/file LAB-4) | Thêm/Bỏ/Sửa | Trước → sau | Vì sao | Issue bị ảnh hưởng |
|---|---|---|---|---|---|
| P-01 | screen spec S3 (S3-03, S3-13, bước V4); Database diagram bảng `customer_rule` | Sửa | Trước: quy tắc giao theo khách, giá trị ONE_THIRD, ONE_HALF, NONE; thiếu cấu hình thì coi là NONE. Sau: theo cặp khách × SKU, giá trị ONE_THIRD, ONE_HALF, LABEL_ONLY; NULL là chưa cấu hình và đơn chuyển sang BUSINESS_REVIEW | Khi đối chiếu với schema LAB-2 (comment BR-DELWIN-01): NONE gộp "không áp dụng" với "chưa cấu hình", trong khi hợp đồng chưa cấu hình không được tự suy ra. Câu hỏi QA-008 ở LAB-1 vẫn chưa có trả lời | #8 E1-T07, #13 E1-T09, #34 E4-T01, #45 E4-T06 |
| P-02 | screen spec S1-09, S3-05, S3-15, S2-14, mã lỗi E02, E08, E28; Wireframe W1 | Sửa | Trước: số lượng tính bằng kg, 3 chữ số thập phân. Sau: số nguyên theo đơn vị đóng gói (`pack_unit`) | Schema LAB-2 lưu `quantity` kiểu số nguyên và có `sku.pack_unit`; khi break E2-T01 không có chỗ lưu số thập phân | #16 E2-T01, #22 E2-T04, #23 E2-T05, #52 E4-T10 |
| P-03 | screen spec mục 0.1 (vai trò) | Sửa | Trước: 5 vai trò tự đặt (Thủ kho, Điều phối, QC, Quản lý, Admin). Sau: ánh xạ sang mã vai trò LAB-1: Điều phối ≈ 受注担当 (ROLE-006), Thủ kho ≈ 庫内作業者 (ROLE-002), QC ≈ 品質管理 (ROLE-003); Quản lý và Admin chưa ánh xạ | Prototype LAB-2 lưu vai trò dạng `role_code` ROLE-001..008; khi break E1-T02 và E7-T02 không thể gán quyền cho vai trò chưa có mã | #3 E1-T02, #80 E7-T02, #81 E7-T03 |
| P-04 | ADR-002; Database diagram bảng `customer_product_watermark` | Sửa (bỏ bảng) | Trước: bảng watermark lưu hạn lớn nhất đã giao, khóa dòng khi xác nhận lấy hàng. Sau: không có bảng dẫn xuất; so với `delivery_history` bất biến theo cặp khách × SKU, có chỉ mục theo (khách, SKU, thời điểm giao giảm dần), khóa advisory theo cặp khi xác nhận | Khi break E4-T04, E4-T05 và E4-T09 thấy bảng watermark là một nguồn sự thật thứ hai phải đồng bộ với lịch sử giao. Schema LAB-2 (comment BR-DATE-01) dùng lịch sử bất biến và không có cột nào cho ngày hôm nay | #37 E4-T04, #41 E4-T05, #51 E4-T09, #88 E8-T05 |
| P-05 | Database diagram bảng `stock` | Bỏ | Trước: tồn theo (lô, vị trí) ở bảng `stock`. Sau: số lượng và vị trí nằm trên lô, mỗi lô một vị trí | Prototype LAB-2 đặt `lot.quantity` và `lot.location_id`; quy mô Yuki chưa cần tách một lô nhiều vị trí, bớt một bảng và một lớp join khi break E3-T02 và E4-T05 | #27 E3-T01, #28 E3-T02, #41 E4-T05 |
| P-06 | Database diagram | Thêm bảng `allocation_exclusion` | Trước: lý do lô bị loại chỉ tính lúc hiển thị. Sau: lưu từng lô bị loại kèm bước (1 đến 6) và lý do | Screen spec S3 yêu cầu hiện lý do chặn từng lô; khi break E4-T10 thấy nếu không lưu thì không truy vết được. Schema LAB-2 đã làm điều này (comment nhắc RFP P.26) | #50 E4-T08, #52 E4-T10 |
| P-07 | screen spec S3 (trạng thái phiếu xuất), S4 | Sửa | Trước: DRAFT, PICKED, ASSIGNED_TO_TRIP, DELIVERED, CANCELLED. Sau: thêm BUSINESS_REVIEW, đổi tên PICKED thành ALLOCATED: DRAFT, BUSINESS_REVIEW, ALLOCATED, ASSIGNED_TO_TRIP, DELIVERED, CANCELLED | Cần chỗ cho đơn thiếu hợp đồng (P-01) và tên trạng thái phải khớp enum `order_status` đã tạo ở LAB-2 | #34 E4-T01, #64 E5-T09 |
| P-08 | screen spec S1; Database diagram `receiving_line` | Sửa | Trước: cách ly hoặc từ chối chọn trên form nhập một lô, lý do chỉ kiểm ở ứng dụng (E11). Sau: kết quả ACCEPTED, REJECTED, HOLD ghi theo từng dòng nhập; `reason_code` bắt buộc khi REJECTED hoặc HOLD, ràng buộc CHECK ở database | Phiếu nhập có nhiều dòng với nhiệt độ khác nhau; schema LAB-2 đặt kết quả kiểm ở từng dòng và dùng CHECK `reason_required` | #17 E2-T02 |
| P-09 | Database diagram bảng `trace_record`, cột `product.traceability_level` | Sửa | Trước: bảng `trace_record` riêng, `traceability_level` là MANDATORY hoặc OPTIONAL. Sau: cột `lot.trace_ref` (văn bản) và `sku.trace_lane` (RICE, BEEF, INTERNAL, NONE); mã cá thể bò phải đúng 10 chữ số | Schema LAB-2 có CHECK mã bò 10 chữ số; khi chỉ bắt buộc truy xuất cho gạo và bò thì E2-T03 và E6-T05 không cần bảng riêng | #21 E2-T03, #49 E4-T07, #75 E6-T05 |
| P-10 | screen spec S4 (quy tắc giờ lái H1 đến H4); Architecture mục 6.3 | Thêm | Trước: bốn quy tắc giờ lái (giờ bị ràng buộc trong ngày, nghỉ giữa hai ca, lái liên tục, lũy kế tháng và năm). Sau: thêm quy tắc lái trung bình (tối đa 9 giờ/ngày tính trung bình 2 ngày, tối đa 44 giờ/tuần tính trung bình 2 tuần) và giới hạn giờ tăng ca trong năm (tối đa 960 giờ); giờ bị ràng buộc mỗi ngày mặc định 13 giờ, tối đa 15 giờ | Khi so với estimate LAB-1 (chức năng F-028 liệt kê 8 ràng buộc về giờ lái) thấy bản LAB-4 chỉ có bốn quy tắc, thiếu ba ràng buộc | #91 E5-T13, #92 E5-T14, #59 E5-T04, #69 E5-T11 |
| P-11 | screen spec S3 (thứ tự gợi ý lô); Architecture R8 | Sửa | Trước: gợi ý lô theo vào trước ra trước (FIFO). Sau: gợi ý theo hạn sớm trước (FEFO), cùng hạn thì lô vào trước | Estimate LAB-1 (F-021, bước 6) dùng FEFO; FIFO thuần có thể gợi ý lô hạn xa trước lô hạn gần | #90 E4-T12, #52 E4-T10 |

## 2. Giả định bổ sung

Mỗi giả định chỉ lấp chỗ để ngỏ, không ghi đè nội dung RFP đã nêu rõ.

| # | Giả định | Chỗ spec/RFP để ngỏ | Ảnh hưởng tới issue/estimate |
|---|---|---|---|
| G-01 | Thời lượng nghỉ bắt buộc sau 4 giờ lái liên tục là 30 phút; các mức giờ lái còn lại lấy theo estimate LAB-1 (F-028) và đều cấu hình được | LAB-1 nêu lái liên tục tối đa 4 giờ và phải chèn nghỉ nhưng không nêu thời lượng nghỉ | #55 E5-T12, #57 E5-T02, #61 E5-T06. Estimate: dự phòng 15% cho epic E5 (#54) |
| G-02 | Quy tắc 日付逆転 so với lô giao gần nhất theo thời điểm giao (khớp chỉ mục của `delivery_history`) | LAB-4 chỉ nói so với lô đã giao trước đó, chưa nói lô gần nhất hay hạn lớn nhất | #37 E4-T04 (subtask truy vấn, 3 giờ), #41 E4-T05, #88 E8-T05. Đổi sang hạn lớn nhất chỉ ảnh hưởng subtask truy vấn |
| G-03 | Sức chứa vị trí đo cùng đơn vị với số lượng (đơn vị đóng gói) | Bản LAB-4 ghi sức chứa còn lại tính bằng kg; schema chỉ có `capacity` số nguyên, không ghi đơn vị | #23 E2-T05 |
| G-04 | Ngưỡng ví dụ ba dải nhiệt: Thường 15 đến 25°C, Mát 0 đến 10°C, Đông từ -15°C trở xuống | Yuki tự công bố ngưỡng riêng, đề không cho số | #7 E1-T06, #17 E2-T02, #72 E6-T02 |
| G-05 | Duyệt ngoại lệ lô hạn NGON NHẤT đã quá hạn đi qua trạng thái BUSINESS_REVIEW, chưa làm màn duyệt riêng | Spec S3 (E22) nói cần Quản lý duyệt nhưng LAB-4 không có màn hay luồng duyệt | #36 E4-T03; nếu cần màn riêng thì phải thêm issue mới |
| G-06 | Nhóm 4 người (2 BE, 1 FE, 1 QA), 5 giờ tập trung mỗi ngày, sprint 2 tuần | Đề và LAB-4 không nói về nhóm thực hiện | Capacity và cách chia sprint trong estimate |
| G-07 | Danh mục nhà cung cấp, vị trí, xe, tài xế không có trạng thái ngừng hoạt động trong phạm vi LAB-5; bỏ điều kiện chỉ chọn đối tượng đang hoạt động ở màn nhập hàng và lập lịch | Screen spec S1 và S4 đặt validation chỉ chọn đối tượng đang hoạt động, nhưng Database diagram không có cột trạng thái cho các bảng đó | #4 E1-T03, #6 E1-T05, #16 E2-T01, #63 E5-T08 |
| G-08 | Ngày hạn vẫn còn hợp lệ trong cả ngày đó; lô chỉ bị coi là quá hạn từ ngày hôm sau | Screen spec S2, S3 (E21, E22) dùng "quá hạn" nhưng không nói có tính ngày hạn hay không | #30 E3-T04, #36 E4-T03, #29 E3-T03 |

## 3. Hướng đã chốt

| # | Vấn đề | Các phương án ở LAB-4 | Phương án chốt | Vì sao |
|---|---|---|---|---|
| H-01 | Chặn 日付逆転 bằng gì | ADR-002: bảng watermark; truy vấn lịch sử giao mỗi lần; chỉ kiểm ở giao diện | Truy vấn `delivery_history` có chỉ mục, kèm khóa advisory theo cặp khách × SKU | Một nguồn sự thật bất biến, khớp BR-DATE-01. Rủi ro hiệu năng được kiểm bằng #88 E8-T05; nếu đo thấy chậm thì quay lại bảng watermark |
| H-02 | Nơi lưu tồn kho | Bảng `stock` theo (lô, vị trí) | Số lượng và vị trí nằm trên lô | Bớt một bảng; chấp nhận hạn chế mỗi lô một vị trí vì chưa có nhu cầu tách lô |
| H-03 | Tên trạng thái phiếu sau khi chọn lô | PICKED | ALLOCATED | Khớp enum `order_status` của LAB-2 |
| H-04 | Lưu thông tin truy xuất | Bảng `trace_record` | Cột `lot.trace_ref` và `sku.trace_lane` | Truy xuất chỉ bắt buộc cho gạo và bò, một cột đủ dùng |
| H-05 | Cách thể hiện việc con trên Project | LAB-4 không nói; backlog bản trước dùng issue riêng gắn nhãn subtask | Sub-issue thật của GitHub dưới issue cha | Project cần thể hiện epic, issue, sub-issue |
