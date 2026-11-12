---
name: swp-scoring
description: Chấm SWP (điểm kích thước) cho issue của backlog theo Scope × Complexity, đối chiếu với giờ ước lượng và dựng báo cáo HTML. Dùng khi cần ước lượng hoặc review điểm cho backlog GitHub Project, hoặc khi phải ghi SWP lên field của Project.
---

# swp-scoring

**Lưu ý nguồn gốc.** Skill chấm SWP chính thức của chương trình không có trong tay người làm bài, nên đây là skill tự đặt cho bài LAB-5. Cách hiểu SWP ở đây: điểm kích thước của một issue, suy ra từ hai điểm Scope và Complexity. Thang chấm và bậc quy đổi chưa được hiệu chỉnh bằng dữ liệu năng suất thực tế.

## Đầu vào

- `tools/LAB5_backlog_import.csv`: backlog (cột `id`, `level`, `epic`, `parent`, `title`, `hours`).
- `skills/swp-scoring/scores-input.csv`: điểm `scope`, `complexity` và `reason` cho mỗi **issue lá** (task không có sub-issue và mọi sub-issue).

## Thang chấm

Mỗi issue lá được chấm hai điểm nguyên từ 1 đến 5.

| Điểm | Scope (phạm vi) | Complexity (độ phức tạp và bất định) |
|---|---|---|
| 1 | Một thành phần, một thay đổi nhỏ | Cơ học, không có nhánh logic |
| 2 | Một lớp, một luồng nhỏ | Logic đơn giản, vài điều kiện |
| 3 | Hai lớp, một luồng đầy đủ | Nhiều nhánh hoặc ràng buộc, validation theo điều kiện |
| 4 | Ba lớp hoặc nhiều luồng liên quan | Quy tắc nhiều biến, giao dịch, đồng thời, ca biên khó |
| 5 | Cắt ngang nhiều module | Thuật toán hoặc ràng buộc ngoài còn mơ hồ |

Tích Scope × Complexity quy ra SWP: 1 đến 2 → 1; 3 đến 4 → 2; 5 đến 6 → 3; 7 đến 9 → 5; 10 đến 15 → 8; 16 đến 25 → 13.

Issue có sub-issue lấy SWP bằng tổng các sub-issue; epic bằng tổng các issue con. Giờ ước lượng được ước độc lập (xem `estimate.md`), không đổi từ SWP.

## Quy trình

1. **Chấm lần đầu.** Đọc tiêu đề và tiêu chí chấp nhận của từng issue lá, chấm Scope và Complexity, ghi lý do ngắn vào `reason`. Không chấm theo giờ đã ước; chấm xong mới đối chiếu.
2. **Tính SWP và dựng báo cáo.**
   ```
   python skills/swp-scoring/build_report.py \
       --backlog tools/LAB5_backlog_import.csv \
       --scores skills/swp-scoring/scores-input.csv \
       --out swp-report
   ```
   Kết quả: `swp-report/index.html` (báo cáo) và `swp-report/swp-scores.csv` (SWP của mọi issue và epic).
3. **Đối chiếu với giờ.** Với mỗi mức SWP, tính trung vị giờ; issue lệch quá 50% so với trung vị bị đánh dấu "lệch giờ" để xem lại. Issue nằm đúng ở ngưỡng ±50% cũng được kiểm thủ công.
4. **Review bởi người.** Người làm bài xem báo cáo và các issue gần ngưỡng, quyết định giữ hoặc sửa điểm; mỗi lần sửa ghi lý do vào `estimate.md`. Giá trị sau review là giá trị ghi vào field "SWP (đã review)".

## Ghi SWP lên GitHub Project

Một agent (hoặc người làm bài) có `gh` đã đăng nhập chạy:

```
python tools/upgrade_project.py --repo OWNER/REPO --owner '@me' --project 1 \
    --swp-csv swp-report/swp-scores.csv
```

Script đặt giá trị của cột `swp` vào field số "SWP (đã review)" cho từng item. Trợ lý AI trong cuộc trò chuyện không có quyền ghi vào GitHub, nên bước này do người làm bài chạy.

## Giới hạn

- Thang chấm do người làm bài tự đặt, chưa kiểm chứng bằng năng suất thực tế.
- Điểm do AI chấm lần đầu dựa trên mô tả issue; mô tả mơ hồ cho điểm kém tin cậy.
- Đối chiếu SWP với giờ chỉ phát hiện lệch nội bộ giữa hai ước lượng của cùng nhóm.
