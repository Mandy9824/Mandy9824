#!/usr/bin/env python3
"""Ronde 63: conceptpagina mova-dreame-robotmaaier (uit scripts/ronde63/mova-dreame.json) aanmaken of bijwerken.

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde63_pagina.py           (proefdraai, schrijft niets)
          python3 scripts/ronde63_pagina.py --schrijf
Publiceert niets: een nieuwe pagina wordt een concept; een bestaande pagina wordt alleen bijgewerkt als die een concept is.
"""
import base64, json, os, re, sys, urllib.request, urllib.error

SITE = 'https://robotmaaierkompas.nl/wp-json/wp/v2/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde63')
SCHRIJF = '--schrijf' in sys.argv
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()


def api(path, data=None):
    req = urllib.request.Request(SITE + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:300]!r}')


p = json.load(open(os.path.join(D, 'mova-dreame.json'), encoding='utf-8'))
c = p['content']
assert p['status'] == 'draft'
assert not re.search(r'bol\.com|/ga/|rel="[^"]*sponsored|\{\{', c, re.I)
res = api(f'pages?slug={p["slug"]}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(res) > 1:
    sys.exit(f'{p["slug"]}: {len(res)} pagina\'s gevonden.')
if res and res[0]['status'] != 'draft':
    sys.exit(f'{p["slug"]} heeft status {res[0]["status"]}, geen concept. Niets gewijzigd.')
print(f'{p["slug"]}: ' + (f'bijwerken (id {res[0]["id"]}, concept)' if res else 'nieuw concept aanmaken'))
if not SCHRIJF:
    sys.exit(0)
if res:  # kopie van het bestaande concept (ook als revisie in WordPress)
    os.makedirs('backups', exist_ok=True)
    oud = api(f'pages/{res[0]["id"]}?context=edit')
    json.dump({k: oud[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta')},
              open(f'backups/ronde63-pagina{res[0]["id"]}-voor.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
data = {'title': p['title'], 'slug': p['slug'], 'content': c, 'meta': p['meta'], 'status': 'draft', 'parent': 0}
pid = api(f'pages/{res[0]["id"]}' if res else 'pages', data)['id']

# Controle (ingelogd, weergegeven inhoud)
q = api(f'pages/{pid}?context=edit')
raw, html = q['content']['raw'], q['content']['rendered']
plain = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
kaarten = re.findall(r'<article class="rmk-product".*?data-model="(M\d+)"', raw, re.S)
iv = re.findall(r'\[(?!rmk_)[^\]]*\]', plain) + re.findall(r'\{\{', plain)
meta_ok = q.get('meta', {}).get('_yoast_wpseo_metadesc') == p['meta']['_yoast_wpseo_metadesc']
print(f'id {pid}, status {q["status"]}, slug {q["slug"]}, ouder {q["parent"]}, kaarten {kaarten}, invulvelden {iv or "geen"}, '
      f'metabeschrijving gezet: {meta_ok}')
sys.exit(0 if q['status'] == 'draft' and kaarten == ['M004', 'M005', 'M008'] and not iv and meta_ok else 1)
