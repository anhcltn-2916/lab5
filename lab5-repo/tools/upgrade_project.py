#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nâng cấp GitHub Project đã tạo (từ create_github_project.py) theo đề LAB-5 mới:

  1. Biến các issue con thành sub-issue thật của GitHub (epic -> issue -> sub-issue).
  2. Tạo field Iteration (Sprint 1 đến Sprint 4) và gán cho từng issue theo cột sprint.
  3. Tạo field "SWP (đã review)" (kiểu số); điền giá trị nếu có file --swp-csv (cột id,swp).
  4. Bổ sung ghi chú "Cập nhật theo PREMISE.md" vào một số issue bị ảnh hưởng.

Chạy thử (chỉ in lệnh):
    python upgrade_project.py --repo anhcltn-2916/lab5 --owner '@me' --project 1 --dry-run

Chạy thật:
    python upgrade_project.py --repo anhcltn-2916/lab5 --owner '@me' --project 1

Có thể chạy lại nhiều lần: phần đã làm được bỏ qua.
Nếu bước tạo Iteration báo lỗi, tạo tay trên web (Project > Settings > New field > Iteration,
đặt tên Iteration), rồi chạy lại script.
"""
import argparse
import csv
import json
import os
import shlex
import subprocess
import sys
import time

TRANSIENT = ('connectex', 'timeout', 'timed out', 'connection', 'EOF', '502', '503', '504',
             'rate limit', 'temporarily', 'TLS', 'reset by peer')
RETRIES = 6
NOTE = '**Cập nhật theo PREMISE.md:**'

PATCHES = {
    'E1-T03': 'Theo G-07: danh mục không có cột trạng thái ngừng hoạt động trong phạm vi LAB-5; schema khớp bảng đã tạo ở LAB-2.',
    'E3-T01': 'Theo H-02 (P-05): số lượng và vị trí nằm trên lô, mỗi lô một vị trí; không có bảng stock.',
    'E4-T01': 'Theo P-07: tên trạng thái phiếu là DRAFT, BUSINESS_REVIEW, ALLOCATED, ASSIGNED_TO_TRIP, DELIVERED, CANCELLED.',
    'E4-T04': 'Theo H-01 và G-02: so với delivery_history, lô giao gần nhất theo thời điểm giao; không dùng bảng watermark.',
    'E4-T05': 'Theo H-01: khóa advisory theo cặp khách × SKU thay cho khóa dòng watermark.',
    'E5-T12': 'Phạm vi bổ sung (task-breakdown.md mục 4): chốt cách tính giờ bị ràng buộc khi một ngày có nhiều chuyến và khi chuyến qua nửa đêm.',
}


def gh(args, dry, fail_ok=False, stdin=None):
    cmd = ['gh'] + args
    if dry:
        print('$ ' + ' '.join(shlex.quote(a) for a in cmd), flush=True)
        return ''
    msg = ''
    for attempt in range(1, RETRIES + 1):
        try:
            res = subprocess.run(cmd, input=stdin, capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=90)
        except subprocess.TimeoutExpired:
            msg = 'timeout: lệnh gh chạy quá 90 giây'
            if attempt < RETRIES:
                print(f'  Quá 90 giây, thử lại lần {attempt}/{RETRIES - 1}...', flush=True)
                continue
            break
        if res.returncode == 0:
            return res.stdout.strip()
        msg = (res.stderr or res.stdout).strip()
        if any(t.lower() in msg.lower() for t in TRANSIENT) and attempt < RETRIES:
            wait = min(60, 5 * attempt)
            print(f'  Lỗi mạng, thử lại lần {attempt}/{RETRIES - 1} sau {wait} giây...', flush=True)
            time.sleep(wait)
            continue
        break
    if fail_ok:
        print('  (bỏ qua) ' + (msg.splitlines()[0] if msg else ''), flush=True)
        return ''
    sys.exit('Lỗi khi chạy: ' + ' '.join(cmd[:4]) + ' ...\n' + msg +
             '\n\nKiểm tra mạng rồi chạy lại đúng lệnh cũ: script bỏ qua phần đã làm.')


def parse_json(text, default):
    try:
        return json.loads(text) if text else default
    except json.JSONDecodeError:
        return default


def graphql(query, variables, dry, fail_ok=False):
    payload = json.dumps({'query': query, 'variables': variables})
    out = gh(['api', 'graphql', '--input', '-'], dry, fail_ok=fail_ok, stdin=payload)
    return parse_json(out, {})


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--owner', default='@me')
    ap.add_argument('--project', required=True, help='số của project, ví dụ 1')
    ap.add_argument('--csv', default=os.path.join(here, 'LAB5_backlog_import.csv'))
    ap.add_argument('--swp-csv', help='file csv có cột id,swp để điền field SWP')
    ap.add_argument('--start-date', default='2026-10-12', help='ngày bắt đầu Sprint 1 (yyyy-mm-dd)')
    ap.add_argument('--days', type=int, default=14, help='độ dài mỗi iteration (ngày lịch)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--sleep', type=float, default=0.5)
    a = ap.parse_args()
    dry = a.dry_run
    repo, owner, num = a.repo, a.owner, a.project

    with open(a.csv, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    print(f'Đọc {len(rows)} dòng từ {a.csv}', flush=True)

    # số issue theo mã
    issue_no = {}
    out = gh(['issue', 'list', '--repo', repo, '--state', 'all', '--limit', '1000', '--json', 'number,title'], dry)
    for it in parse_json(out, []):
        t = it['title']
        if t.startswith('[') and ']' in t:
            issue_no[t[1:t.index(']')]] = it['number']
    if dry and not issue_no:
        issue_no = {r['id']: i for i, r in enumerate(rows, 1)}
    missing = [r['id'] for r in rows if r['id'] not in issue_no]
    if missing and not dry:
        sys.exit('Thiếu issue trên repo cho các mã: ' + ', '.join(missing[:10]) + ' ... Chạy create_github_project.py trước.')

    # project
    out = gh(['project', 'view', num, '--owner', owner, '--format', 'json'], dry)
    pid = parse_json(out, {}).get('id', 'DRY_PROJECT_ID')

    def field_list():
        o = gh(['project', 'field-list', num, '--owner', owner, '--format', 'json'], dry)
        return {f['name']: f for f in parse_json(o, {'fields': []}).get('fields', [])}

    fields = field_list()

    # --- 1) field SWP
    print('Bước 1/5: field "SWP (đã review)"...', flush=True)
    if 'SWP (đã review)' not in fields:
        gh(['project', 'field-create', num, '--owner', owner, '--name', 'SWP (đã review)', '--data-type', 'NUMBER'], dry)

    # --- 2) field Iteration
    print('Bước 2/5: field Iteration (Sprint 1 đến Sprint 4)...', flush=True)
    if 'Iteration' not in fields:
        import datetime
        d0 = datetime.date.fromisoformat(a.start_date)
        its = [{'title': f'Sprint {k}', 'startDate': (d0 + datetime.timedelta(days=a.days * (k - 1))).isoformat(),
                'duration': a.days} for k in range(1, 5)]
        q = ('mutation($p:ID!,$n:String!,$c:ProjectV2IterationFieldConfigurationInput!){'
             'createProjectV2Field(input:{projectId:$p,dataType:ITERATION,name:$n,iterationConfiguration:$c})'
             '{projectV2Field{... on ProjectV2IterationField{id name}}}}')
        graphql(q, {'p': pid, 'n': 'Iteration',
                    'c': {'startDate': its[0]['startDate'], 'duration': a.days, 'iterations': its}}, dry, fail_ok=True)
    fields = field_list()
    iter_field_id, iter_ids = 'DRY_ITER_FIELD', {}
    q = ('query($p:ID!){node(id:$p){... on ProjectV2{fields(first:50){nodes{... on ProjectV2IterationField{'
         'id name configuration{iterations{id title startDate} completedIterations{id title startDate}}}}}}}}')
    data = graphql(q, {'p': pid}, dry)
    for nd in (((data.get('data') or {}).get('node') or {}).get('fields') or {}).get('nodes', []):
        if nd and nd.get('name') == 'Iteration':
            iter_field_id = nd['id']
            cfg = nd.get('configuration') or {}
            lst = (cfg.get('iterations') or []) + (cfg.get('completedIterations') or [])
            lst.sort(key=lambda x: x['startDate'])
            for k, itx in enumerate(lst, 1):
                iter_ids[f'Sprint {k}'] = itx['id']
    if not dry and not iter_ids:
        print('  Chưa tìm thấy field Iteration. Tạo tay trên web (Project > Settings > New field > Iteration) '
              'rồi chạy lại script.', flush=True)

    # --- 3) item của project
    out = gh(['project', 'item-list', num, '--owner', owner, '--limit', '1000', '--format', 'json'], dry)
    item_of = {}
    for it in parse_json(out, {'items': []}).get('items', []):
        n = (it.get('content') or {}).get('number')
        if n:
            item_of[n] = it['id']

    print('Bước 3/5: gán Iteration cho từng issue...', flush=True)
    for r in rows:
        if not r['sprint'] or not iter_ids and not dry:
            continue
        item = item_of.get(issue_no[r['id']], 'DRY_ITEM')
        label = r['sprint'].replace('sprint-', 'Sprint ').title()
        iid = iter_ids.get(label, 'DRY_ITER')
        gh(['project', 'item-edit', '--id', item, '--project-id', pid, '--field-id', iter_field_id,
            '--iteration-id', iid], dry)
        if not dry:
            time.sleep(a.sleep)

    # --- 4) sub-issue
    print('Bước 4/5: tạo quan hệ sub-issue (epic > issue > sub-issue)...', flush=True)
    idcache = {}

    def db_id(n):
        if n not in idcache:
            o = gh(['api', f'repos/{repo}/issues/{n}', '--jq', '.id'], dry)
            idcache[n] = o or 'DRY_ID'
        return idcache[n]

    for idx, r in enumerate(rows, 1):
        if not r['parent']:
            continue
        print(f"  [{idx}/{len(rows)}] {r['id']} -> {r['parent']}", flush=True)
        child, parent = issue_no[r['id']], issue_no[r['parent']]
        gh(['api', '-X', 'POST', f'repos/{repo}/issues/{parent}/sub_issues', '-F', f'sub_issue_id={db_id(child)}'],
           dry, fail_ok=True)
        if not dry:
            time.sleep(a.sleep)

    # --- 5) SWP và ghi chú
    print('Bước 5/5: điền SWP (nếu có) và ghi chú PREMISE...', flush=True)
    if a.swp_csv:
        fid = fields.get('SWP (đã review)', {}).get('id', 'DRY_SWP_FIELD')
        with open(a.swp_csv, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                n = issue_no.get(r['id'])
                if n and r.get('swp', '') != '':
                    gh(['project', 'item-edit', '--id', item_of.get(n, 'DRY_ITEM'), '--project-id', pid,
                        '--field-id', fid, '--number', str(r['swp'])], dry)
    for code, text in PATCHES.items():
        n = issue_no.get(code)
        if not n:
            continue
        body = gh(['issue', 'view', str(n), '--repo', repo, '--json', 'body', '--jq', '.body'], dry)
        if NOTE in body:
            continue
        gh(['issue', 'edit', str(n), '--repo', repo, '--body', f'{body}\n\n{NOTE} {text}'], dry)

    print('\nXong. Kiểm tra trên web: Project có cột Iteration, SWP (đã review), và issue cha hiển thị sub-issue.')
    print('Đề yêu cầu Project và repo đều public: Settings > Visibility (Project), Settings > Danger Zone (repo).')


if __name__ == '__main__':
    main()
