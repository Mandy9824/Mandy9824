#!/usr/bin/env python3
"""Ronde 100: conceptpagina's robotmaaier-diefstal-verzekering en robotmaaier-egels (uit scripts/ronde100/*.json)
aanmaken of bijwerken (van ronde97_pagina.py).

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde100_pagina.py           (proefdraai, schrijft niets)
          python3 scripts/ronde100_pagina.py --schrijf
Publiceert niets: een nieuwe pagina wordt een concept; een bestaande pagina wordt alleen bijgewerkt als die een concept is.
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api as _api

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde100')
SCHRIJF = '--schrijf' in sys.argv
api = lambda path, data=None: _api('wp/v2/' + path, data)
ok = True
for naam in ('diefstal-verzekering.json', 'egels.json'):
    p = json.load(open(os.path.join(D, naam), encoding='utf-8'))
    c = p['content']
    assert p['status'] == 'draft'
    assert not re.search(r'bol\.com|/ga/|rel="[^"]*sponsored|\{\{|coolblue|amazon', c, re.I)
    res = api(f'pages?slug={p["slug"]}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
    if len(res) > 1:
        sys.exit(f'{p["slug"]}: {len(res)} pagina\'s gevonden.')
    if res and res[0]['status'] != 'draft':
        sys.exit(f'{p["slug"]} heeft status {res[0]["status"]}, geen concept. Niets gewijzigd.')
    print(f'{p["slug"]}: ' + (f'bijwerken (id {res[0]["id"]}, concept)' if res else 'nieuw concept aanmaken'))
    if not SCHRIJF:
        continue
    if res:  # kopie van het bestaande concept (ook als revisie in WordPress)
        os.makedirs('backups', exist_ok=True)
        oud = api(f'pages/{res[0]["id"]}?context=edit')
        json.dump({k: oud[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta')},
                  open(f'backups/ronde100-pagina{res[0]["id"]}-voor-{time.strftime("%Y%m%d-%H%M%S")}.json', 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
    data = {'title': p['title'], 'slug': p['slug'], 'content': c, 'meta': p['meta'], 'status': 'draft', 'parent': 0}
    pid = api(f'pages/{res[0]["id"]}' if res else 'pages', data)['id']
    q = api(f'pages/{pid}?context=edit')
    raw = q['content']['raw']
    plain = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
    kaarten = re.findall(r'<article class="rmk-product".*?data-model="(M\d+)"', raw, re.S)
    iv = re.findall(r'\[(?!rmk_)[^\]]*\]', plain) + re.findall(r'\{\{', plain)
    meta = q.get('meta', {})
    meta_ok = all(meta.get(k) == v for k, v in p['meta'].items())
    print(f'  id {pid}, status {q["status"]}, slug {q["slug"]}, ouder {q["parent"]}, kaarten {kaarten}, invulvelden {iv or "geen"}, '
          f'metabeschrijving en kruimeltitel gezet: {meta_ok}')
    ok &= q['status'] == 'draft' and kaarten == p['kaarten'] and not iv and meta_ok and q['slug'] == p['slug']
sys.exit(0 if ok else 1)
