#!/usr/bin/env python3
"""Ronde 16: hub beste-robotmaaier (versie 2) als concept bijwerken. Draai eerst ronde15_upload.py.

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde16_upload.py          (proefdraai, schrijft niets)
          python3 scripts/ronde16_upload.py --schrijf
Publiceert niets: de pagina moet een concept zijn en blijft dat.
"""
import base64, json, os, re, sys, urllib.request, urllib.error

SITE = 'https://robotmaaierkompas.nl/wp-json/wp/v2/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde16')
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


h = json.load(open(os.path.join(D, 'hub.json')))
c = h['content']
assert 'ruim 3.000 euro' in c and 'rond 3.000 euro' not in c
assert not re.search(r'bol\.com|/ga/|rel="[^"]*sponsored', c, re.I)
res = api(f'pages?slug={h["slug"]}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(res) != 1:
    sys.exit(f'{h["slug"]}: {len(res)} pagina\'s gevonden, verwacht 1.')
pid, st = res[0]['id'], res[0]['status']
if st != 'draft':
    sys.exit(f'{h["slug"]} heeft status {st}, geen concept. Niets gewijzigd.')
print(f'{h["slug"]}: bijwerken (id {pid}, concept)')
if not SCHRIJF:
    sys.exit(0)
api(f'pages/{pid}', {'title': h['title'], 'content': c, 'meta': h['meta'], 'status': 'draft'})

# Controle
p = api(f'pages/{pid}?context=edit')
raw = p['content']['raw']
plain = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
iv = re.findall(r'\[(?!rmk_)[^\]]*\]', plain) + re.findall(r'Alfa|Beta|gepeild|\{\{', plain)
kaarten = re.findall(r'<article class="rmk-product"[^>]*>.*?data-model="(M\d+)"', raw, re.S)
groepen = len(re.findall(r'<ol class="rmk-sources">', raw))
bol = bool(re.search(r'bol\.com', raw, re.I))
aff = bool(re.search(r'/ga/|sponsored', raw))
print(f'status {p["status"]}, kaarten {kaarten}, brongroepen {groepen}, invulvelden {iv or "geen"}, '
      f'Bol {bol}, affiliate {aff}')
ok = p['status'] == 'draft' and kaarten == ['M002', 'M010', 'M005', 'M008', 'M011'] and groepen == 6 and not iv and not bol and not aff
sys.exit(0 if ok else 1)
