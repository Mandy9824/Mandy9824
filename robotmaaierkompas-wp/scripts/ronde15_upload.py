#!/usr/bin/env python3
"""Ronde 15: mesjespagina als concept plaatsen en drie korte tekstwijzigingen doorvoeren.

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde15_upload.py          (proefdraai, schrijft niets)
          python3 scripts/ronde15_upload.py --schrijf
Publiceert niets: de nieuwe pagina krijgt status draft, bestaande pagina's houden hun status.
"""
import base64, json, os, re, sys, urllib.request, urllib.error

SITE = 'https://robotmaaierkompas.nl/wp-json/wp/v2/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde15')
SCHRIJF = '--schrijf' in sys.argv
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()


def api(path, data=None, method=None):
    req = urllib.request.Request(SITE + path, method=method or ('POST' if data is not None else 'GET'),
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{method or "GET"} {path}: {e.code} {e.read()[:300]!r}')


def invulvelden(html):
    plain = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    return re.findall(r'\[(?!rmk_)[^\]]*\]', plain) + re.findall(r'Alfa|Beta|gepeild', plain)


# 1. Tekstwijzigingen op bestaande pagina's
for w in json.load(open(os.path.join(D, 'wijzigingen.json'))):
    p = api(f'pages/{w["id"]}?context=edit')
    assert p['slug'] == w['slug'], (w['id'], p['slug'])
    raw = p['content']['raw']
    if w['nieuw'] in raw:
        print(f'{w["slug"]}: al aangepast'); continue
    n = raw.count(w['oud'])
    if n != 1:
        sys.exit(f'{w["slug"]}: oude tekst {n} keer gevonden, verwacht 1. Niets gewijzigd.')
    print(f'{w["slug"]}: aanpassen (status blijft {p["status"]})')
    if SCHRIJF:
        api(f'pages/{w["id"]}', {'content': raw.replace(w['oud'], w['nieuw'])})

# 2. Mesjespagina als concept
m = json.load(open(os.path.join(D, 'mesjes.json')))
bestaand = api(f'pages?slug={m["slug"]}&status=publish,draft,pending,private,future&context=edit')
body = {'title': m['title'], 'content': m['content'], 'slug': m['slug'], 'status': 'draft', 'meta': m['meta']}
if bestaand:
    pid = bestaand[0]['id']
    if bestaand[0]['status'] != 'draft':
        sys.exit(f'{m["slug"]} bestaat al met status {bestaand[0]["status"]}; niets gewijzigd.')
    print(f'{m["slug"]}: bijwerken (id {pid}, concept)')
    if SCHRIJF:
        api(f'pages/{pid}', body)
else:
    print(f'{m["slug"]}: nieuw concept')
    if SCHRIJF:
        pid = api('pages', body)['id']
        print('  id', pid)

# 3. Controle na het plaatsen
if SCHRIJF:
    alle = {}
    for pg in range(1, 5):
        res = api(f'pages?per_page=100&page={pg}&status=publish,draft&context=edit&_fields=id,slug,status,link,parent')
        for x in res:
            alle[x['id']] = x
        if len(res) < 100:
            break
    paden = {re.sub(r'^https?://[^/]+', '', x['link']) for x in alle.values()} | {'/'}
    # concepten hebben een ?page_id=-link; bouw hun pad uit slug en ouder
    def pad(x):
        s = [x['slug']]
        while x.get('parent'):
            x = alle.get(x['parent'], {}); s.insert(0, x.get('slug', ''))
        return '/' + '/'.join(s) + '/'
    paden |= {pad(x) for x in alle.values()}
    fout = False
    for pid_ in [w['id'] for w in json.load(open(os.path.join(D, 'wijzigingen.json')))] + [pid]:
        p = api(f'pages/{pid_}?context=edit')
        raw = p['content']['raw']
        links = set(re.findall(r'href="(/[^"#?]*)', raw))
        mis = sorted(l for l in links if l not in paden)
        iv = invulvelden(raw)
        print(f'{p["slug"]}: status {p["status"]}, interne links {len(links)}, ontbrekend {mis or "geen"}, invulvelden {iv or "geen"}')
        fout |= bool(mis or iv)
        if p['id'] == pid and p['status'] != 'draft':
            sys.exit('Mesjespagina is geen concept!')
    sys.exit(1 if fout else 0)
