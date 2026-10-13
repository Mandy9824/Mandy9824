#!/usr/bin/env python3
"""Ronde 30 (thema 1.3.6): EAN, Bol-product-URL, Bol-afbeelding en fabrikantpagina in de live modelgegevens.

Neemt uit de omzetting van het Excel-bestand (excel_naar_json.py --uit <json>) per bestaand model ALLEEN de velden
fabrikant_url, ean en bol over; al het andere (prijzen, scores, teksten, specificaties) blijft zoals het live staat.
Het blok "bol" gaat alleen mee als thema 1.3.6 (of hoger) actief is: 1.3.5 weigert elke "bol.com" in de gegevens.

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde30_upload.py <gegenereerd.json>            (proefdraai)
          python3 scripts/ronde30_upload.py <gegenereerd.json> --schrijf
"""
import base64, copy, json, os, re, sys, urllib.request, urllib.error

ROOT = 'https://robotmaaierkompas.nl/wp-json/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()
VELDEN = ('fabrikant_url', 'ean', 'bol')


def api(path, data=None):
    req = urllib.request.Request(ROOT + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data, ensure_ascii=False).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:400]!r}')


thema = api('wp/v2/themes?status=active')[0]
versie = tuple(int(x) for x in re.findall(r'\d+', thema.get('version', ''))[:3])
met_bol = versie >= (1, 3, 6)
print(f'Actief thema {thema["stylesheet"]} {thema.get("version")}: blok "bol" ' + ('gaat mee' if met_bol else 'gaat NIET mee (eerst 1.3.6 activeren)'))

gen = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
live = api('rmk/v1/modellen')['data']
nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    g = gen.get(m['id'])
    if not g:
        print(f'{m["id"]}: niet in de omzetting, ongewijzigd')
        continue
    for v in VELDEN:
        if v == 'bol' and not met_bol:
            continue
        if g.get(v) != m.get(v):
            print(f'{m["id"]} {v}: {json.dumps(m.get(v), ensure_ascii=False)[:90]} -> {json.dumps(g.get(v), ensure_ascii=False)[:90]}')
            m[v] = g.get(v)
# Controle: verder niets veranderd
for a, b in zip(live['modellen'], nieuw['modellen']):
    extra = [k for k in set(a) | set(b) if a.get(k) != b.get(k) and k not in VELDEN]
    assert not extra, (a['id'], extra)
assert {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
if nieuw == live:
    print('Niets te doen.')
    sys.exit(0)
if not SCHRIJF:
    sys.exit(0)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
verschil = [(x['id'], k) for x, y in zip(na['modellen'], nieuw['modellen']) for k in set(x) | set(y)
            if json.dumps(x.get(k), sort_keys=True).replace('.0,', ',').replace('.0}', '}') != json.dumps(y.get(k), sort_keys=True).replace('.0,', ',').replace('.0}', '}')]
print('Live gelijk aan wat verstuurd is (op notatie 10.0/10 na):', not verschil, verschil[:5])
