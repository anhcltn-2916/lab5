[README.md](https://github.com/user-attachments/files/34723825/README.md)
# Backlog Kho lạnh Yuki (Product B): LAB-5

- **Tên dự án:** Hệ thống quản lý chuỗi kho lạnh thực phẩm, Kho lạnh Yuki
- **Đề:** Product B (chuỗi kho lạnh thực phẩm)

## Tổng quan

- **Backlog được chia từ bản LAB-4 nào:** bản nộp ngày 08/10/2026 (5 file: ADR, Architecture Design, Database diagram, screen spec, Wireframe).
- **PREMISE.md có thay đổi so với LAB-4:** có. 11 dòng spec thêm, bỏ, sửa (P-01 đến P-11), 8 giả định bổ sung (G-01 đến G-08) và 5 hướng đã chốt (H-01 đến H-05). Chi tiết ở [PREMISE.md](PREMISE.md).
- **Số epic:** 8 (E1 đến E8), gồm 66 issue và 18 sub-issue, tổng 269 SWP và 393 giờ ước lượng.
- **Sprint giả lập đã chạy:** Sprint 1 (12/10/2026 đến 23/10/2026), báo cáo tính đến hết ngày làm việc thứ 7. Xem [progress-report.md](progress-report.md). Số liệu sprint là giả lập.

## Link

- **Repo:** https://github.com/anhcltn-2916/lab5
- **GitHub Project:** https://github.com/users/anhcltn-2916/projects/1
- **Báo cáo HTML của skill chấm SWP:** [swp-report/index.html](swp-report/index.html) (tải về để xem dạng trang; GitHub hiển thị file HTML dưới dạng mã nguồn)
- **Đã mở thử bằng cửa sổ ẩn danh (không đăng nhập):** repo, Project và báo cáo HTML, ngày [ĐIỀN NGÀY MỞ THỬ].

## Cấu trúc repo

| File/thư mục | Nội dung |
|---|---|
| [README.md](README.md) | Mô tả repo, link, cấu trúc và bảng Spec → epic |
| [PREMISE.md](PREMISE.md) | Tiền đề: thay đổi so với LAB-4, giả định bổ sung, hướng đã chốt |
| [task-breakdown.md](task-breakdown.md) | Nguyên tắc chia task, bảng Spec → issue, hạng mục ràng buộc đặc thù, chỗ hở của spec |
| [estimate.md](estimate.md) | Ước lượng: SWP đã review, cách quy ra giờ, tổng theo epic, so với estimate LAB-1 |
| [progress-report.md](progress-report.md) | Báo cáo tiến độ Sprint 1: trạng thái, burndown, rủi ro trễ |
| [AI-report.md](AI-report.md) | Cách dùng AI trong bài: skill, prompt, review, điểm đặc biệt |
| [swp-report/](swp-report/) | Báo cáo HTML của skill chấm SWP và bảng `swp-scores.csv` |
| [skills/](skills/) | Skill tự đặt `swp-scoring` (mô tả, điểm chấm đầu vào, script dựng báo cáo) |
| [images/](images/) | Ảnh biểu đồ burndown dùng trong báo cáo tiến độ |
| [tools/](tools/) | Backlog dạng CSV và hai script GitHub CLI dùng để tạo Project, issue, sub-issue, Iteration |

Nội dung repo do người làm bài tự viết cho bài tập; không chép tài liệu RFP, không có dữ liệu thật, dữ liệu cá nhân hay khóa bí mật.

## Spec → epic

| Spec (mã/file LAB-4, hoặc dòng PREMISE) | Epic trên Project | Ghi chú |
|---|---|---|
| Wireframe W1, screen spec S1 (nhập hàng) | #15 E2: Nhập kho | Ngưỡng nhiệt ba dải; truy xuất bắt buộc gạo và bò |
| Wireframe W2, screen spec S2 (tồn kho) | #26 E3: Tồn kho và vòng đời lô | Hai loại hạn: ngon nhất và tiêu thụ an toàn |
| Wireframe W3, screen spec S3 (xuất hàng, kiểm lô V1 đến V6) | #33 E4: Xuất hàng và kiểm lô | Ràng buộc đặc thù: cấm giao lô hạn cũ hơn lô đã giao cho cùng khách, hạn giao 1/3 và 1/2, hai loại hạn, truy xuất |
| Wireframe W4, screen spec S4 (lập lịch giao hàng) | #54 E5: Lập lịch giao và giờ lái xe | Ràng buộc đặc thù: giới hạn giờ lái xe tải từ 2024, tách riêng từng quy tắc |
| Wireframe W5, screen spec S5 (HACCP, truy xuất) | #70 E6: HACCP và truy xuất | Nhật ký nhiệt độ chỉ thêm, không sửa, không xóa |
| Screen spec mục 0.1, Architecture mục 7, ADR-003 (vai trò, phân quyền, audit) | #78 E7: Phân quyền, audit, bảo mật | Ánh xạ vai trò LAB-1 (P-03) |
| Architecture mục 8, ADR-001 (triển khai, kiểm thử) | #83 E8: Kiểm thử, triển khai, tài liệu | Kiểm tra ranh giới module trong CI |
| Database diagram (bảng danh mục), screen spec mục 0 (định dạng, mã lỗi) | #1 E1: Nền tảng và danh mục | Thỏa thuận khách × SKU, NULL là chưa cấu hình (P-01) |
| PREMISE P-06 (bảng lưu lý do lô bị loại) | #33 E4 | Issue #50 |
| PREMISE P-10 (thêm hai quy tắc giờ lái) | #54 E5 | Issue #91, #92 |
| PREMISE P-11 (FEFO thay FIFO) | #33 E4 | Issue #90 |
