# Task breakdown: Kho lạnh Yuki (Product B)

Backlog được chia từ bản LAB-4 nộp ngày 08/10/2026, kèm các thay đổi ghi ở [PREMISE.md](PREMISE.md). Số `#n` là số issue trên GitHub Project. Mã `P-xx`, `G-xx`, `H-xx` trỏ về các dòng trong PREMISE.md.

## 1. Nguyên tắc chia task

**Độ hạt.** Mỗi issue do một người làm xong trong tối đa một ngày công (không quá 8 giờ ước lượng) và có tiêu chí chấp nhận kiểm chứng được độc lập. Dừng chia khi issue đạt hai điều kiện đó. Tách sub-issue khi issue ước lượng 7 đến 8 giờ và chứa ít nhất hai phần logic độc lập (ví dụ truy vấn dữ liệu, so sánh, rồi test); sáu issue lớn nhất (#8, #17, #37, #41, #45, #65) được tách thành ba sub-issue. Mỗi ràng buộc nghiệp vụ đặc thù là một issue riêng, không gộp chung với việc thông thường; test của ràng buộc đặc thù cũng là issue riêng của QA.

**Định nghĩa xong.** Một issue chỉ chuyển sang Done khi: mã chạy được ở môi trường thử nghiệm; có test cho các ca đặc thù của issue; tiêu chí chấp nhận trong mô tả đạt; người khác (không phải người viết) đã review. Với issue của QA, tài liệu hoặc bộ test phải nằm trong repo.

**Cách dùng epic → issue → sub-issue trên Project.**
- **Epic** là issue có nhãn `type:epic`, gom theo module kiến trúc (E1 đến E8). Epic không có ước lượng riêng, tổng SWP và giờ của epic là tổng các issue con.
- **Issue** là đơn vị giao việc, có người phụ trách, Iteration, SWP (đã review), giờ ước lượng, Role, Priority và Epic.
- **Sub-issue** là sub-issue thật của GitHub, nằm dưới issue cha; tiến độ của issue cha tính theo sub-issue đã đóng. Sub-issue có ước lượng riêng và cộng đúng bằng issue cha.

## 2. Spec → issue

| Spec (LAB-4) | Epic | Issue/sub-issue | Phần spec chưa thành issue và vì sao |
|---|---|---|---|
| Wireframe W1, screen spec S1 (nhập hàng) | E2 #15 | #16 E2-T01 (API phiếu nhập), #17 E2-T02 (+ #18 đến #20, nhiệt độ ngoài ngưỡng), #21 E2-T03 (truy xuất), #22 E2-T04 (màn W1), #23 E2-T05 (vị trí và sức chứa), #24 E2-T06 (màn duyệt QC), #25 E2-T07 (test) | Điều kiện chỉ chọn nhà cung cấp đang hoạt động: bỏ theo G-07 |
| Wireframe W2, screen spec S2 (tồn kho) | E3 #26 | #27 E3-T01 (trạng thái lô), #28 E3-T02 (API tồn), #29 E3-T03 (màn W2), #30 E3-T04 (job quá hạn), #31 E3-T05 (hủy lô), #32 E3-T06 (test) | Phân trang 20 dòng và làm mới tình trạng mỗi 5 phút gộp vào #29, quá nhỏ để thành issue riêng |
| Wireframe W3, screen spec S3 (xuất hàng, V1 đến V6) | E4 #33 | #34 E4-T01 (phiếu xuất), #35 E4-T02 (V1), #36 E4-T03 (V2), #37 E4-T04 (+ #38 đến #40, V3), #41 E4-T05 (+ #42 đến #44, khóa chống race), #45 E4-T06 (+ #46 đến #48, V4), #49 E4-T07 (V5), #50 E4-T08 (lưu lý do loại lô), #51 E4-T09 (lịch sử giao), #52 E4-T10 (màn W3), #53 E4-T11 (test), #90 E4-T12 (sắp xếp FEFO) | Duyệt ngoại lệ lô hạn NGON NHẤT đã quá hạn: chưa có màn riêng, xử lý theo G-05 |
| Wireframe W4, screen spec S4 (lập lịch giao, H1 đến H4) | E5 #54 | #55 E5-T12 (làm rõ tham số), #56 E5-T01 (mô hình dữ liệu), #57 E5-T02 (tham số giờ lái), #58 E5-T03 (giờ kết thúc), #59 đến #62 (H1 đến H4), #63 E5-T08 (xe đúng dải, không trùng chuyến), #64 E5-T09 (màn W4), #65 E5-T10 (+ #66 đến #68, gợi ý xử lý), #69 E5-T11 (test), #91 E5-T13 (lái trung bình), #92 E5-T14 (tăng ca trong năm) | Không có |
| Wireframe W5, screen spec S5 (HACCP, truy xuất) | E6 #70 | #71 E6-T01 (bảng chỉ thêm), #72 E6-T02 (API ghi nhiệt độ), #73 E6-T03 (màn W5), #74 E6-T04 (hành động khắc phục), #75 E6-T05 (tra cứu truy xuất), #76 E6-T06 (import CSV), #77 E6-T07 (test) | Không có |
| Screen spec mục 0.1, Architecture mục 7, ADR-003 (vai trò, phân quyền, audit, cấu hình) | E7 #78 | #79 E7-T01 (audit), #80 E7-T02 (ma trận quyền), #81 E7-T03 (ánh xạ vai trò), #82 E7-T04 (rà soát bảo mật) | Không có |
| Architecture mục 8, ADR-001 (triển khai, ranh giới module) | E8 #83 | #84 E8-T01 (CI kiểm ranh giới module), #85 E8-T02 (UAT), #86 E8-T03 (triển khai, sao lưu), #87 E8-T04 (tài liệu), #88 E8-T05 (hiệu năng), #89 E8-T06 (test plan) | Không có |
| Database diagram (bảng danh mục), screen spec mục 0.2 và 0.5 (định dạng, mã lỗi) | E1 #1 | #2 E1-T01 (repo, CI cơ bản), #3 E1-T02 (xác thực), #4 E1-T03 (migration danh mục), #5 E1-T04 và #6 E1-T05 (màn danh mục), #7 E1-T06 (ngưỡng nhiệt), #8 E1-T07 (+ #9 đến #11, thỏa thuận khách × SKU), #12 E1-T08 (dữ liệu mẫu), #13 E1-T09 (hợp đồng thiếu), #14 E1-T10 (khung giao diện, thông báo lỗi) | Từng mã lỗi E01 đến E43 không có issue riêng, được gắn vào issue của màn hình dùng mã đó |
| Architecture mục 1 (ngoài phạm vi) | Không có | Không có | Tối ưu tuyến đường, cảm biến thời gian thực, tích hợp ERP, ứng dụng di động: nằm ngoài phạm vi LAB-4 nên không thành issue |

## 3. Hạng mục chịu ràng buộc đặc thù của đề

**Giới hạn giờ lái xe tải từ 2024** (module lập lịch giao, epic E5 #54). Epic này tách thành 14 issue và có dự phòng 15% giờ trong estimate vì tham số chưa được chốt (G-01).

| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Tham số giờ lái chưa được khách xác nhận | #55 E5-T12 | Thời lượng nghỉ chưa chốt (G-01) và các mức giờ cần xác nhận với khách; là rủi ro lớn nhất của epic, làm trước các issue kiểm giờ lái |
| Tham số giờ lái là cấu hình có ngày hiệu lực | #57 E5-T02 | Quy định có thể đổi, không hard-code (ADR-003); đổi tham số không cần deploy |
| Giờ bị ràng buộc tối đa mỗi ngày (H1) | #59 E5-T04 | Quy tắc, tham số và ca test biên riêng; gộp chung thì mỗi lần tham số đổi phải sửa cả khối |
| Nghỉ tối thiểu giữa hai ca (H2) | #60 E5-T05 | Phụ thuộc ca liền trước, có thể qua ngày, cách tính khác H1 |
| Lái liên tục và nghỉ bắt buộc (H3) | #61 E5-T06 | Việc chèn nghỉ làm đổi giờ kết thúc dự kiến, ảnh hưởng #58 |
| Giờ lũy kế tháng và năm (H4) | #62 E5-T07 | Cần dữ liệu nhiều chuyến và xử lý qua ranh giới tháng, ưu tiên Should |
| Lái trung bình 9 giờ/ngày và 44 giờ/tuần | #91 E5-T13 | Tính trung bình trên cửa sổ nhiều ngày, khác cách tính H1 đến H4; thiếu ở bản LAB-4 (P-10) |
| Giới hạn giờ tăng ca trong năm | #92 E5-T14 | Quy tắc lũy kế năm riêng, dùng dữ liệu giờ tăng ca chứ không phải giờ bị ràng buộc; thiếu ở bản LAB-4 (P-10) |
| Tính giờ kết thúc dự kiến | #58 E5-T03 | Đầu vào chung của H1 đến H4; sai ở đây thì mọi kiểm tra sai theo |
| Gợi ý xử lý khi vượt giới hạn | #65 E5-T10 (+ #66 đến #68) | Chỉ có giá trị khi H1 đến H4 đã đúng; tách để có thể hoãn mà không ảnh hưởng phần kiểm |
| Kiểm thử bộ quy tắc giờ lái | #69 E5-T11 | Ca biên (qua nửa đêm, nhiều chuyến một ngày) cần tách khỏi test thông thường |
| Màn lập lịch hiển thị lỗi theo từng quy tắc | #64 E5-T09 | Giao diện phụ thuộc kết quả H1 đến H4, làm sau cùng trong epic |

**Các ràng buộc nghiệp vụ đặc thù khác của Product B** (cũng tách thành issue riêng):

| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Hai loại hạn (ngon nhất, tiêu thụ an toàn) | #36 E4-T03, #29 E3-T03, #30 E3-T04 | Quy tắc chặn khác nhau theo loại hạn, nếu gộp sẽ không phân biệt được hai loại |
| Thứ tự gợi ý FEFO | #90 E4-T12 | Quy tắc sắp xếp riêng, khác FIFO của bản LAB-4 (P-11); test độc lập |
| Cấm giao lô hạn cũ hơn lô đã giao cho cùng khách | #37 E4-T04 (+ #38 đến #40), #41 E4-T05 (+ #42 đến #44), #51 E4-T09 | Quy tắc so theo từng khách × SKU, cần khóa chống race, là lỗi nghiêm trọng nhất của đề; tách phần kiểm, phần khóa và phần ghi lịch sử |
| Hạn giao theo tập quán 1/3, 1/2 | #8 E1-T07 (+ #9 đến #11), #45 E4-T06 (+ #46 đến #48), #34 E4-T01 | Khác hạn pháp lý; giá trị NULL chuyển đơn sang BUSINESS_REVIEW (P-01) |
| Truy xuất gạo và bò | #21 E2-T03, #49 E4-T07, #75 E6-T05 | Chỉ bắt buộc cho gạo và bò, các sản phẩm khác không áp dụng |
| Ba dải nhiệt có ngưỡng riêng | #7 E1-T06, #17 E2-T02 (+ #18 đến #20), #72 E6-T02 | Ngưỡng do công ty tự công bố, có ngày hiệu lực |
| Nhật ký HACCP chỉ thêm | #71 E6-T01, #72 E6-T02, #73 E6-T03, #74 E6-T04, #77 E6-T07 | Yêu cầu ghi chép tuân thủ, quyền cơ sở dữ liệu chặn sửa và xóa |

## 4. Chỗ hở hoặc mâu thuẫn của spec LAB-4 phát hiện khi break

| Spec | Chỗ hở/mâu thuẫn | Xử lý |
|---|---|---|
| screen spec S3 (V4) và Database diagram `customer_rule` | Giá trị NONE gộp "không áp dụng" với "chưa cấu hình" | Đã sửa thiết kế (P-01) |
| screen spec S1-09, S3-05, S3-15 | Số lượng tính bằng kg thập phân, không khớp dữ liệu thật dùng số nguyên theo đơn vị đóng gói | Đã sửa thiết kế (P-02) |
| screen spec mục 0.1 | 5 vai trò tự đặt, chưa có mã vai trò ROLE-001..008 của LAB-1 | Đã sửa thiết kế (P-03); phần Quản lý và Admin còn lại được theo dõi ở #81 |
| ADR-002, Database diagram `customer_product_watermark` | Bảng watermark là nguồn sự thật thứ hai phải đồng bộ với lịch sử giao | Đã sửa thiết kế (P-04) |
| Database diagram `stock` | Tách tồn theo (lô, vị trí) chưa có nhu cầu thực | Đã sửa thiết kế (P-05) |
| Database diagram | Không lưu lý do lô bị loại dù screen spec S3 yêu cầu hiện lý do | Đã sửa thiết kế (P-06) |
| screen spec S3 (trạng thái phiếu) | Thiếu trạng thái cho đơn chưa có hợp đồng; tên PICKED không khớp enum đã tạo | Đã sửa thiết kế (P-07) |
| screen spec S1 (xử lý nhiệt độ) | Xử lý chọn ở mức form một lô, không phản ánh phiếu nhập nhiều dòng | Đã sửa thiết kế (P-08) |
| Database diagram `trace_record` | Bảng riêng không cần thiết khi chỉ gạo và bò bắt buộc | Đã sửa thiết kế (P-09) |
| screen spec S4 (H1 đến H4) | Chỉ có bốn quy tắc giờ lái, thiếu lái trung bình (9 giờ/ngày, 44 giờ/tuần) và giới hạn tăng ca 960 giờ/năm so với estimate LAB-1 | Đã sửa thiết kế (P-10) |
| screen spec S4 (nghỉ bắt buộc) | Không nêu thời lượng nghỉ sau 4 giờ lái liên tục | Giả định (G-01) và tạo issue làm rõ #55 |
| screen spec S3 và Architecture R8 (thứ tự gợi ý lô) | FIFO, trong khi estimate LAB-1 dùng FEFO | Đã sửa thiết kế (P-11) |
| screen spec S4 (H1, H2) | Không nói cách tính giờ bị ràng buộc khi một ngày có nhiều chuyến hoặc chuyến qua nửa đêm | Tạo issue làm rõ: bổ sung vào phạm vi #55; ca biên được kiểm ở #69 |
| screen spec S3 (V3) | Chưa nói so với lô giao gần nhất hay hạn lớn nhất đã giao | Giả định (G-02) |
| screen spec S3 (E22) | Cần Quản lý duyệt ngoại lệ nhưng không có màn hay luồng duyệt | Giả định (G-05) |
| screen spec S1 (sức chứa E08) | Sức chứa tính bằng kg, trong khi schema chỉ có số nguyên không ghi đơn vị | Giả định (G-03) |
| screen spec S1, S4 (validation) | Chỉ chọn đối tượng đang hoạt động, nhưng Database diagram không có cột trạng thái | Giả định (G-07) |
| screen spec S2, S3 (E21, E22) | Không nói ngày hạn có còn hợp lệ trong cả ngày hay không | Giả định (G-08) |
| screen spec S5 (đóng sự cố) | Ghi chú nói quyền đóng sự cố do QC nhưng chính sách chưa chốt với khách | Để mở: không chặn #74 vì quyền đóng sự cố chỉ là một dòng trong ma trận quyền #80, dễ đổi khi khách trả lời |
