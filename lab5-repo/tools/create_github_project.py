#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo GitHub Project (v2) và các issue từ LAB5_backlog_import.csv bằng GitHub CLI (gh).

Chuẩn bị (một lần):
    gh auth login
    gh auth refresh -s project,repo        # cấp quyền Project cho gh
    (cần gh >= 2.40; repo đích phải tồn tại và bạn có quyền ghi)

Chạy thử, chỉ in lệnh, không tạo gì:
    python3 create_github_project.py --repo OWNER/REPO --owner @me --dry-run

Chạy thật:
    python3 create_github_project.py --repo OWNER/REPO --owner @me
    (thêm --with-status để đặt trạng thái Sprint 1 giống báo cáo mẫu: Done, In Progress;
     task Done sẽ được đóng issue)

Sau khi chạy xong, vào trang Project và tạo thủ công các view (CLI không tạo được view):
    1) Board: nhóm theo Status
    2) Table: hiện các cột Story Point, Estimate (h), Sprint, Role, Epic, Level
    3) (tuỳ chọn) Insights: biểu đồ burndown theo Sprint
"""
import argparse
import csv
import json
import os
import shlex
import subprocess
import sys
import time

LABEL_COLORS = {'epic': '1F6FEB', 'type': '6E7781', 'role': '8250DF', 'sprint': '0E8A16',
                'priority': 'D93F0B', 'constraint': 'B60205'}


TRANSIENT = ('connectex', 'timeout', 'timed out', 'connection', 'EOF', '502', '503', '504',
             'secondary rate limit', 'rate limit', 'temporarily', 'TLS', 'reset by peer')
RETRIES = 6


def gh(args, dry, fail_ok=False):
    cmd = ['gh'] + args
    if dry:
        print('$ ' + ' '.join(shlex.quote(a) for a in cmd))
        return ''
    msg = ''
    for attempt in range(1, RETRIES + 1):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=90)
        except subprocess.TimeoutExpired:
            msg = 'timeout: lệnh gh chạy quá 90 giây'
            if attempt < RETRIES:
                print(f'  Quá 90 giây không phản hồi, thử lại lần {attempt}/{RETRIES - 1}...', flush=True)
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
        print('  (bỏ qua) ' + (msg.splitlines()[0] if msg else ''))
        return ''
    sys.exit('Lỗi khi chạy: ' + ' '.join(cmd[:4]) + ' ...\n' + msg +
             '\n\nKiểm tra mạng rồi chạy lại đúng lệnh cũ: script sẽ bỏ qua phần đã tạo và làm tiếp.')


def parse_json(text, default):
    try:
        return json.loads(text) if text else default
    except json.JSONDecodeError:
        return default


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True, help='OWNER/REPO chứa issue')
    ap.add_argument('--owner', default='@me', help='chủ sở hữu Project: @me hoặc tên tổ chức')
    ap.add_argument('--title', default='LAB-5 Backlog Kho lạnh Yuki (Product B)')
    ap.add_argument('--csv', default=os.path.join(here, 'LAB5_backlog_import.csv'))
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--with-status', action='store_true')
    ap.add_argument('--sleep', type=float, default=1.0, help='giây nghỉ giữa các issue (tránh giới hạn tốc độ)')
    a = ap.parse_args()
    dry = a.dry_run

    with open(a.csv, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    print(f'Đọc {len(rows)} dòng từ {a.csv}', flush=True)

    # 1) nhãn
    print('Bước 1/5: tạo nhãn (khoảng 1 phút)...', flush=True)
    labels = sorted({l for r in rows for l in r['labels'].split(';') if l})
    for l in labels:
        color = LABEL_COLORS.get(l.split(':')[0], 'C5DEF5')
        if l.startswith('sprint-'):
            color = LABEL_COLORS['sprint']
        gh(['label', 'create', l, '--repo', a.repo, '--color', color, '--force'], dry, fail_ok=True)

    # 2) project (dùng lại nếu đã có project cùng tên)
    print('Bước 2/5: kiểm tra hoặc tạo project...', flush=True)
    number, pid = None, None
    out = gh(['project', 'list', '--owner', a.owner, '--limit', '100', '--format', 'json'], dry)
    for pj in parse_json(out, {'projects': []}).get('projects', []):
        if pj.get('title') == a.title:
            number, pid = str(pj['number']), pj['id']
            print(f'Dùng lại project đã có: #{number}')
            break
    if number is None:
        out = gh(['project', 'create', '--owner', a.owner, '--title', a.title, '--format', 'json'], dry)
        pj = parse_json(out, {'number': 0, 'id': 'DRY_PROJECT_ID'})
        number, pid = str(pj['number']), pj['id']
        print(f'Đã tạo project #{number}')
    gh(['project', 'link', number, '--owner', a.owner, '--repo', a.repo], dry, fail_ok=True)

    # 3) field
    print('Bước 3/5: tạo các field (Story Point, Estimate, Sprint...)...', flush=True)
    epics = sorted({r['epic'] for r in rows})
    fields = [('Story Point', 'NUMBER', None), ('Estimate (h)', 'NUMBER', None),
              ('Sprint', 'SINGLE_SELECT', 'Sprint 1,Sprint 2,Sprint 3,Sprint 4'),
              ('Role', 'SINGLE_SELECT', 'BE,FE,QA'),
              ('Priority', 'SINGLE_SELECT', 'Must,Should,Could'),
              ('Epic', 'SINGLE_SELECT', ','.join(epics)),
              ('Level', 'SINGLE_SELECT', 'Epic,Task,Subtask')]
    out = gh(['project', 'field-list', number, '--owner', a.owner, '--format', 'json'], dry)
    existing = {f['name'] for f in parse_json(out, {'fields': []}).get('fields', [])}
    for name, dtype, opts in fields:
        if name in existing:
            continue
        cmd = ['project', 'field-create', number, '--owner', a.owner, '--name', name, '--data-type', dtype]
        if opts:
            cmd += ['--single-select-options', opts]
        gh(cmd, dry)

    out = gh(['project', 'field-list', number, '--owner', a.owner, '--format', 'json'], dry)
    fl = parse_json(out, {'fields': []})['fields']
    F = {f['name']: {'id': f['id'], 'opts': {o['name']: o['id'] for o in f.get('options', [])}} for f in fl}

    def fid(name):
        return F.get(name, {}).get('id', 'DRY_' + name.upper().replace(' ', '_'))

    def set_number(item, name, value):
        if value == '' or value is None:
            return
        gh(['project', 'item-edit', '--id', item, '--project-id', pid, '--field-id', fid(name), '--number', str(value)], dry)

    def set_select(item, name, option):
        if not option:
            return
        oid = F.get(name, {}).get('opts', {}).get(option, 'DRY_OPT' if dry else None)
        if oid is None:
            print(f'  Cảnh báo: field {name} không có lựa chọn {option}')
            return
        gh(['project', 'item-edit', '--id', item, '--project-id', pid, '--field-id', fid(name),
            '--single-select-option-id', oid], dry)

    # 4) issue + item (bỏ qua phần đã tạo từ lần chạy trước)
    issue_no, issue_url, children, body_of = {}, {}, {}, {}
    fake = 100
    existing_issues = {}
    out = gh(['issue', 'list', '--repo', a.repo, '--state', 'all', '--limit', '1000',
              '--json', 'number,title,url,state'], dry)
    for it in parse_json(out, []):
        if it['title'].startswith('[') and ']' in it['title']:
            existing_issues[it['title'][1:it['title'].index(']')]] = it
    out = gh(['project', 'item-list', number, '--owner', a.owner, '--limit', '1000', '--format', 'json'], dry)
    existing_items = {}
    for it in parse_json(out, {'items': []}).get('items', []):
        num = (it.get('content') or {}).get('number')
        if num:
            existing_items[num] = it['id']
    if existing_issues:
        print(f'Đã có {len(existing_issues)} issue từ lần chạy trước, sẽ bỏ qua và làm tiếp.')
    print('Bước 4/5: tạo issue và đưa vào board...', flush=True)
    for idx, r in enumerate(rows, 1):
        print(f"  [{idx}/{len(rows)}] {r['id']}", flush=True)
        title = f"[{r['id']}] {r['title']}"
        body = r['body']
        if r['parent'] and r['parent'] in issue_no:
            body += f"\n\n**Thuộc:** #{issue_no[r['parent']]}"
        body_of[r['id']] = body
        if r['id'] in existing_issues:
            ex = existing_issues[r['id']]
            n, url, state = ex['number'], ex['url'], ex['state']
        else:
            cmd = ['issue', 'create', '--repo', a.repo, '--title', title, '--body', body]
            if r['labels']:
                cmd += ['--label', ','.join(r['labels'].split(';'))]
            res = gh(cmd, dry)
            url = res.splitlines()[-1] if res else f'https://github.com/{a.repo}/issues/{fake}'
            n = int(url.rstrip('/').split('/')[-1])
            state = 'OPEN'
            if not dry:
                time.sleep(a.sleep)
        fake += 1
        issue_no[r['id']], issue_url[r['id']] = n, url
        if r['parent']:
            children.setdefault(r['parent'], []).append(r)
        if n in existing_items:
            item = existing_items[n]
        else:
            out = gh(['project', 'item-add', number, '--owner', a.owner, '--url', url, '--format', 'json'], dry)
            item = parse_json(out, {'id': 'DRY_ITEM'})['id']
        set_number(item, 'Story Point', r['story_point'])
        set_number(item, 'Estimate (h)', r['hours'])
        set_select(item, 'Sprint', r['sprint'])
        set_select(item, 'Role', r['role'])
        set_select(item, 'Priority', r['priority'])
        set_select(item, 'Epic', r['epic'])
        set_select(item, 'Level', r['level'])
        status = r['status'] if a.with_status else 'Todo'
        set_select(item, 'Status', status)
        if a.with_status and status == 'Done' and r['level'] != 'Epic' and state != 'CLOSED':
            gh(['issue', 'close', str(n), '--repo', a.repo], dry, fail_ok=True)

    print('Bước 5/5: cập nhật danh sách công việc con...', flush=True)
    # 5) danh sách công việc con trong issue cha (GitHub hiển thị tiến độ)
    for pid_row, kids in children.items():
        lines = []
        for k in kids:
            mark = 'x' if (a.with_status and k['status'] == 'Done') else ' '
            lines.append(f"- [{mark}] #{issue_no[k['id']]} {k['title']}")
        new_body = body_of[pid_row] + '\n\n**Công việc con:**\n' + '\n'.join(lines)
        gh(['issue', 'edit', str(issue_no[pid_row]), '--repo', a.repo, '--body', new_body], dry)

    print('\nXong. Mở Project: gh project view %s --owner %s --web' % (number, a.owner))
    print('Tạo các view Board (nhóm theo Status) và Table (Story Point, Estimate, Sprint, Role) trên giao diện web.')


if __name__ == '__main__':
    main()
