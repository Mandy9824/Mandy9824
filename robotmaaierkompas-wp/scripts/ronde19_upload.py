#!/usr/bin/env python3
"""Ronde 19: Navimow-messenprijs op #236 en #18, en bronlabels op de kostenpagina (#18).

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde19_upload.py          (proefdraai, schrijft niets)
          python3 scripts/ronde19_upload.py --schrijf
Publiceert niets: beide pagina's moeten concept zijn en blijven dat.
"""
import base64, json, os, re, sys, urllib.request, urllib.error

SITE = 'https://robotmaaierkompas.nl/wp-json/wp/v2/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
SCHRIJF = '--schrijf' in sys.argv
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()
NIEUW = 'ongeveer 25 euro per verpakking (het aantal messen is niet bevestigd)'
OUD = {236: 'ongeveer 25 euro voor 12', 18: 'ongeveer 25 euro voor 12 stuks'}


def api(path, data=None):
    req = urllib.request.Request(SITE + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:300]!r}')


def is_handleiding(url):
    # Handleidingen zijn pdf's of downloads uit het documentarchief van de fabrikant.
    return bool(re.search(r'\.pdf(\?|$)|/tdrdownload/', url, re.I))


def labels(raw):
    def li(m):
        url, chip = m.group(1), m.group(3)
        if chip not in ('Handleiding', 'Fabrikant'):
            return m.group(0)  # bijv. "Handleiding (kopie op mansier.com)" of "Eigen methode"
        goed = 'Handleiding' if is_handleiding(url) else 'Fabrikant'
        return m.group(0).replace(f'<span class="rmk-chip">{chip}</span>', f'<span class="rmk-chip">{goed}</span>')
    def ol(m):
        return re.sub(r'<li><div><a href="([^"]+)">(.*?)</a><div class="rmk-sources__meta"><span class="rmk-chip">([^<]+)</span>.*?</li>', li, m.group(0), flags=re.S)
    return re.sub(r'<ol class="rmk-sources">.*?</ol>', ol, raw, flags=re.S)


fout = False
for pid in (236, 18):
    p = api(f'pages/{pid}?context=edit')
    if p['status'] != 'draft':
        sys.exit(f'#{pid} heeft status {p["status"]}, geen concept. Niets gewijzigd.')
    raw = p['content']['raw']
    nieuw = raw
    if NIEUW not in nieuw:
        n = nieuw.count(OUD[pid])
        if n != 1:
            sys.exit(f'#{pid}: oude Navimow-tekst {n} keer gevonden, verwacht 1. Niets gewijzigd.')
        nieuw = nieuw.replace(OUD[pid], NIEUW)
    if pid == 18:
        nieuw = labels(nieuw)
    oud_chips = re.findall(r'href="([^"]+)">[^<]*</a><div class="rmk-sources__meta"><span class="rmk-chip">([^<]+)<', raw)
    nw_chips = re.findall(r'href="([^"]+)">[^<]*</a><div class="rmk-sources__meta"><span class="rmk-chip">([^<]+)<', nieuw)
    gewijzigd = [(u, a, b) for (u, a), (_, b) in zip(oud_chips, nw_chips) if a != b]
    print(f'#{pid} {p["slug"]}: Navimow {"al aangepast" if NIEUW in raw else "aanpassen"}, labels gewijzigd {len(gewijzigd)}')
    for u, a, b in gewijzigd:
        print(f'   {a} -> {b}: {u[:90]}')
    if SCHRIJF and nieuw != raw:
        api(f'pages/{pid}', {'content': nieuw})
    if SCHRIJF:
        q = api(f'pages/{pid}?context=edit')
        r = q['content']['raw']
        rest = [m for m in ('voor 12 stuks', '25 euro voor 12') if m in r]
        print(f'   controle: status {q["status"]}, nieuwe tekst {r.count(NIEUW)}x, oude tekst {rest or "weg"}')
        fout |= q['status'] != 'draft' or r.count(NIEUW) != 1 or bool(rest)
sys.exit(1 if fout else 0)
