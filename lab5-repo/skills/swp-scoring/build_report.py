#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tính SWP từ điểm Scope và Complexity rồi dựng báo cáo HTML.

Dùng:
    python build_report.py --backlog ../../tools/LAB5_backlog_import.csv \
        --scores scores-input.csv --out ../../swp-report

Đầu vào:
    backlog  : CSV backlog (cột id, level, epic, parent, title, hours)
    scores   : CSV điểm (cột id, scope, complexity, reason), chỉ cho issue lá
               (task không có sub-issue, và mọi sub-issue)
Đầu ra (thư mục --out):
    index.html     báo cáo
    swp-scores.csv bảng SWP cho mọi issue và epic (cột id, swp dùng cho upgrade_project.py --swp-csv)
"""
import argparse
import csv
import html
import os
import statistics

BUCKETS = [(2, 1), (4, 2), (6, 3), (9, 5), (15, 8), (25, 13)]  # (tích tối đa, SWP)


def swp_of(product):
    for top, v in BUCKETS:
        if product <= top:
            return v
    return BUCKETS[-1][1]


def fmt(x):
    return f'{x:.1f}'.replace('.', ',') if isinstance(x, float) else str(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--backlog', required=True)
    ap.add_argument('--scores', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tolerance', type=float, default=0.5, help='ngưỡng lệch giờ so với trung vị cùng mức SWP')
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.backlog, encoding='utf-8')))
    sc = {r['id']: r for r in csv.DictReader(open(a.scores, encoding='utf-8'))}
    by_id = {r['id']: r for r in rows}
    kids = {}
    for r in rows:
        if r['parent']:
            kids.setdefault(r['parent'], []).append(r['id'])

    leaf = [r for r in rows if r['level'] != 'Epic' and r['id'] not in kids]
    for r in leaf:
        if r['id'] not in sc:
            raise SystemExit('Thiếu điểm cho ' + r['id'])
        s, c = int(sc[r['id']]['scope']), int(sc[r['id']]['complexity'])
        assert 1 <= s <= 5 and 1 <= c <= 5, r['id']
        r['_s'], r['_c'], r['_p'] = s, c, s * c
        r['_swp'] = swp_of(s * c)
        r['_h'] = float(r['hours'])

    # trung vị giờ theo mức SWP
    med = {}
    for b in {r['_swp'] for r in leaf}:
        med[b] = statistics.median(r['_h'] for r in leaf if r['_swp'] == b)
    for r in leaf:
        m = med[r['_swp']]
        r['_dev'] = (r['_h'] - m) / m
        r['_flag'] = abs(r['_dev']) > a.tolerance

    # tổng cho issue cha và epic
    total_swp, total_h = {}, {}

    def agg(i):
        if i in total_swp:
            return
        if i not in kids:
            total_swp[i] = by_id[i]['_swp']
            total_h[i] = by_id[i]['_h']
            return
        s = h = 0
        for k in kids[i]:
            agg(k)
            s += total_swp[k]
            h += total_h[k]
        total_swp[i], total_h[i] = s, h

    for r in rows:
        agg(r['id'])

    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, 'swp-scores.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['id', 'swp', 'level', 'epic', 'hours', 'scope', 'complexity'])
        for r in rows:
            leafrow = r['id'] not in kids and r['level'] != 'Epic'
            w.writerow([r['id'], total_swp[r['id']], r['level'], r['epic'], total_h[r['id']],
                        r['_s'] if leafrow else '', r['_c'] if leafrow else ''])

    # ---------------- HTML
    e = html.escape
    epics = [r for r in rows if r['level'] == 'Epic']
    tasks = [r for r in rows if r['level'] == 'Task']
    grand_swp = sum(total_swp[r['id']] for r in epics)
    grand_h = sum(total_h[r['id']] for r in epics)
    dist = {}
    for r in leaf:
        dist[r['_swp']] = dist.get(r['_swp'], 0) + 1
    flagged = sorted([r for r in leaf if r['_flag']], key=lambda r: -abs(r['_dev']))

    ep_rows = ''
    for r in epics:
        n_task = sum(1 for t in tasks if t['epic'] == r['id'])
        ep_rows += (f"<tr><td>{e(r['id'])}</td><td>{e(r['title'])}</td><td class='n'>{n_task}</td>"
                    f"<td class='n'>{total_swp[r['id']]}</td><td class='n'>{fmt(total_h[r['id']])}</td>"
                    f"<td class='n'>{fmt(total_h[r['id']] / total_swp[r['id']])}</td></tr>")
    dist_rows = ''
    for b in sorted(dist):
        width = int(dist[b] / max(dist.values()) * 100)
        dist_rows += (f"<tr><td>SWP {b}</td><td class='n'>{dist[b]}</td><td class='n'>{fmt(med[b])}</td>"
                      f"<td><div class='bar' style='width:{width}%'></div></td></tr>")
    flag_rows = ''
    for r in flagged:
        flag_rows += (f"<tr><td>{e(r['id'])}</td><td>{e(r['title'])}</td><td class='n'>{r['_swp']}</td>"
                      f"<td class='n'>{fmt(r['_h'])}</td><td class='n'>{fmt(med[r['_swp']])}</td>"
                      f"<td class='n'>{r['_dev'] * 100:+.0f}%</td></tr>")
    all_rows = ''
    for r in rows:
        if r['level'] == 'Epic':
            continue
        isleaf = r['id'] not in kids
        cls = ' class="sub"' if r['level'] == 'Subtask' else ''
        if isleaf:
            all_rows += (f"<tr{cls}><td>{e(r['id'])}</td><td>{e(r['title'])}</td><td class='n'>{r['_s']}</td>"
                         f"<td class='n'>{r['_c']}</td><td class='n'>{r['_p']}</td><td class='n'><b>{r['_swp']}</b></td>"
                         f"<td class='n'>{fmt(r['_h'])}</td><td>{e(sc[r['id']]['reason'])}{' <span class=flag>lệch giờ</span>' if r['_flag'] else ''}</td></tr>")
        else:
            all_rows += (f"<tr{cls}><td>{e(r['id'])}</td><td>{e(r['title'])}</td><td colspan='3' class='n'>tổng các sub-issue</td>"
                         f"<td class='n'><b>{total_swp[r['id']]}</b></td><td class='n'>{fmt(total_h[r['id']])}</td><td></td></tr>")

    page = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Báo cáo chấm SWP: Kho lạnh Yuki (Product B)</title>
<style>
:root{{--bg:#fff;--ink:#1f2328;--mut:#59636e;--line:#d0d7de;--acc:#2f5bea;--soft:#f6f8fa;--warn:#9a6700}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0d1117;--ink:#e6edf3;--mut:#9da7b3;--line:#30363d;--acc:#7aa2ff;--soft:#161b22;--warn:#d29922}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,'Segoe UI',sans-serif}}
main{{max-width:1040px;margin:0 auto;padding:32px 20px 64px}}
h1{{font-size:26px;margin:0 0 6px}} h2{{font-size:19px;margin:36px 0 10px}}
p.lead{{color:var(--mut);margin:0 0 18px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:18px 0}}
.card{{border:1px solid var(--line);border-radius:8px;padding:12px 14px;background:var(--soft)}}
.card b{{display:block;font-size:24px}} .card span{{color:var(--mut);font-size:13px}}
table{{border-collapse:collapse;width:100%;font-size:13.5px;margin:8px 0}}
th,td{{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}}
th{{background:var(--soft);font-weight:600}} td.n,th.n{{text-align:right;white-space:nowrap}}
tr.sub td{{color:var(--mut)}} .bar{{height:10px;background:var(--acc);border-radius:3px}}
.flag{{color:var(--warn);font-size:12px;border:1px solid var(--warn);border-radius:10px;padding:0 6px}}
.wrap{{overflow-x:auto}} .note{{border-left:3px solid var(--acc);padding:6px 12px;background:var(--soft);margin:12px 0}}
</style></head><body><main>
<h1>Báo cáo chấm SWP</h1>
<p class="lead">Kho lạnh Yuki (Product B) · {len(leaf)} issue được chấm, {len(rows)} issue và epic trong backlog · tạo bằng <code>skills/swp-scoring</code></p>

<div class="note">Skill chấm SWP chính thức của chương trình không có, nên đây là skill tự đặt: SWP = điểm kích thước từ Scope × Complexity. Cách chấm do người làm bài định nghĩa (mục 1), điểm do AI chấm lần đầu và người làm bài review.</div>

<div class="cards">
<div class="card"><b>{grand_swp}</b><span>tổng SWP của backlog</span></div>
<div class="card"><b>{fmt(grand_h)}</b><span>tổng giờ ước lượng</span></div>
<div class="card"><b>{len(leaf)}</b><span>issue lá được chấm</span></div>
<div class="card"><b>{len(flagged)}</b><span>issue lệch giờ cần xem lại</span></div>
</div>

<h2>1. Cách chấm</h2>
<p>Mỗi issue lá (task không có sub-issue, và mọi sub-issue) được chấm hai điểm từ 1 đến 5, nhân với nhau, rồi quy ra SWP theo bậc.</p>
<div class="wrap"><table>
<tr><th>Điểm</th><th>Scope (phạm vi)</th><th>Complexity (độ phức tạp và bất định)</th></tr>
<tr><td class="n">1</td><td>Một thành phần, một thay đổi nhỏ</td><td>Cơ học, không có nhánh logic</td></tr>
<tr><td class="n">2</td><td>Một lớp, một luồng nhỏ (một API hoặc một màn đơn giản)</td><td>Logic đơn giản, vài điều kiện</td></tr>
<tr><td class="n">3</td><td>Hai lớp, một luồng đầy đủ (ví dụ API và cơ sở dữ liệu, hoặc API và giao diện)</td><td>Nhiều nhánh hoặc ràng buộc, có validation theo điều kiện</td></tr>
<tr><td class="n">4</td><td>Ba lớp hoặc nhiều luồng liên quan</td><td>Quy tắc nghiệp vụ nhiều biến, giao dịch, đồng thời, hoặc ca biên khó</td></tr>
<tr><td class="n">5</td><td>Cắt ngang nhiều module</td><td>Thuật toán hoặc ràng buộc ngoài còn mơ hồ, bất định cao</td></tr>
</table></div>
<p>Bậc quy đổi: tích 1 đến 2 → SWP 1; 3 đến 4 → 2; 5 đến 6 → 3; 7 đến 9 → 5; 10 đến 15 → 8; 16 đến 25 → 13. Issue có sub-issue lấy SWP bằng tổng các sub-issue; epic bằng tổng các issue con.</p>

<h2>2. Tổng theo epic</h2>
<div class="wrap"><table>
<tr><th>Epic</th><th>Tên</th><th class="n">Số issue</th><th class="n">SWP</th><th class="n">Giờ</th><th class="n">Giờ mỗi SWP</th></tr>
{ep_rows}
<tr><td></td><td><b>Tổng</b></td><td class="n"><b>{len(tasks)}</b></td><td class="n"><b>{grand_swp}</b></td><td class="n"><b>{fmt(grand_h)}</b></td><td class="n"><b>{fmt(grand_h / grand_swp)}</b></td></tr>
</table></div>

<h2>3. Phân bố SWP và đối chiếu với giờ</h2>
<p>Với mỗi mức SWP, bảng cho trung vị giờ ước lượng. Issue có giờ lệch quá {int(a.tolerance * 100)}% so với trung vị cùng mức bị đánh dấu để xem lại.</p>
<div class="wrap"><table>
<tr><th>Mức</th><th class="n">Số issue</th><th class="n">Trung vị giờ</th><th>Phân bố</th></tr>
{dist_rows}
</table></div>
<h2>4. Issue lệch giờ cần xem lại</h2>
<div class="wrap"><table>
<tr><th>Issue</th><th>Tiêu đề</th><th class="n">SWP</th><th class="n">Giờ</th><th class="n">Trung vị cùng mức</th><th class="n">Lệch</th></tr>
{flag_rows}
</table></div>

<h2>5. Điểm chi tiết từng issue</h2>
<div class="wrap"><table>
<tr><th>Issue</th><th>Tiêu đề</th><th class="n">Scope</th><th class="n">Compl.</th><th class="n">Tích</th><th class="n">SWP</th><th class="n">Giờ</th><th>Lý do chấm</th></tr>
{all_rows}
</table></div>

<h2>6. Giới hạn</h2>
<ul>
<li>Thang chấm và bậc quy đổi do người làm bài tự đặt, chưa được kiểm chứng bằng dữ liệu năng suất thực tế.</li>
<li>Điểm Scope và Complexity do AI chấm lần đầu theo mô tả issue; độ tin cậy phụ thuộc mô tả đó.</li>
<li>Giờ ước lượng và SWP đều là ước lượng của cùng một nhóm làm bài, nên đối chiếu giữa hai số chỉ phát hiện lệch nội bộ, không chứng minh ước lượng đúng.</li>
</ul>
</main></body></html>"""
    with open(os.path.join(a.out, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page)

    print('leaf', len(leaf), 'swp', grand_swp, 'hours', grand_h, 'flagged', len(flagged))
    for r in epics:
        print(r['id'], total_swp[r['id']], total_h[r['id']])
    for r in flagged:
        print('flag', r['id'], r['_swp'], r['_h'], med[r['_swp']], f"{r['_dev']*100:+.0f}%")


if __name__ == '__main__':
    main()
