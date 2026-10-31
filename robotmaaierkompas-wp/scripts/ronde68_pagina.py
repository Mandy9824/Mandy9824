#!/usr/bin/env python3
"""Ronde 68: inhoud van de gepubliceerde pagina /mova-dreame-robotmaaier/ (#351) vervangen door scripts/ronde68/mova.json.

Behoudt slug, status (publish), bovenliggende pagina en de Yoast-kruimeltitel; zet titel, inhoud en de metabeschrijving
uit de md. Maakt eerst een kopie in backups/ (niet in git). Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde68_pagina.py           (proefdraai, schrijft niets)
          python3 scripts/ronde68_pagina.py --schrijf
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

PID, SLUG = 351, 'mova-dreame-robotmaaier'
KAARTEN = ['M059', 'M060', 'M004', 'M005', 'M008', 'M064', 'M063']
SCHRIJF = '--schrijf' in sys.argv
p = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde68', 'mova.json'), encoding='utf-8'))
c = p['content']
assert p['slug'] == SLUG
assert not re.search(r'bol\.com|/ga/|rel="[^"]*sponsored|\{\{', c, re.I)
oud = api(f'wp/v2/pages/{PID}?context=edit')
if oud['slug'] != SLUG or oud['status'] != 'publish':
    sys.exit(f'#{PID}: slug {oud["slug"]}, status {oud["status"]} (verwacht {SLUG}, publish). Niets gewijzigd.')
print(f'#{PID} {oud["slug"]} ({oud["status"]}), laatst gewijzigd {oud["modified"]}: inhoud {len(oud["content"]["raw"])} -> {len(c)} tekens')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
fn = time.strftime(f'backups/ronde68-pagina{PID}-voor-%Y%m%d-%H%M%S.json')
json.dump({k: oud[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta', 'modified', 'template', 'menu_order')},
          open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', fn)
api(f'wp/v2/pages/{PID}', {'title': p['title'], 'content': c, 'status': 'publish', 'slug': SLUG, 'parent': oud['parent'],
                           'meta': {'_yoast_wpseo_metadesc': p['meta']['_yoast_wpseo_metadesc']}})

q = api(f'wp/v2/pages/{PID}?context=edit')
raw = q['content']['raw']
plain = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
kaarten = re.findall(r'<article class="rmk-product".*?data-model="(M\d+)"', raw, re.S)
iv = re.findall(r'\[(?!rmk_)[^\]]*\]', plain) + re.findall(r'\{\{', plain)
m = q.get('meta', {})
ok = (q['status'] == 'publish' and q['slug'] == SLUG and q['parent'] == oud['parent'] and raw == c and kaarten == KAARTEN and not iv
      and m.get('_yoast_wpseo_metadesc') == p['meta']['_yoast_wpseo_metadesc']
      and m.get('_yoast_wpseo_bctitle') == oud['meta'].get('_yoast_wpseo_bctitle'))
print(f'status {q["status"]}, slug {q["slug"]}, ouder {q["parent"]}, inhoud gelijk {raw == c}, kaarten {kaarten}, '
      f'invulvelden {iv or "geen"}, metabeschrijving {m.get("_yoast_wpseo_metadesc")!r}, kruimeltitel {m.get("_yoast_wpseo_bctitle")!r}')
sys.exit(0 if ok else 1)
