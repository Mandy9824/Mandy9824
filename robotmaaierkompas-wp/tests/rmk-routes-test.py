#!/usr/bin/env python3
"""Elke rmk-route zonder inloggen (lijst voor 1.3.6 punt c, uitgebreid in 1.3.7). Veilig tegen de live site:
zonder inloggegevens en zonder cookies kan een POST niets wijzigen.

- Alle rmk-routes geven 401 of 404 en geen gegevens, BEHALVE GET /rmk/v1/bol-prijs (1.3.7): die mag zonder inloggen
  antwoorden, maar alleen met de toegestane velden (prijs, tijdstip, verkoper, EAN) en met
  Cache-Control: no-store en CDN-Cache-Control: no-store.
- Met --na-136: /noindex, /paginas, /seo en /huisstijl moeten 404 rest_no_route geven.
- Met --na-137: /bol-prijs (GET) moet 200 geven en /bol-ronde 401; zonder deze vlag mogen beide ook nog 404 zijn.
- 1.3.10: /bol-prijs mag een deel "coolblue" hebben, per model ALLEEN model, prijs, tijdstip en winkel ("Coolblue").
  /coolblue-ronde en /coolblue-status zijn alleen voor beheerders. Met --na-1310 moeten die 401 geven (anders mag ook 404).
  Zo blijft /bol-prijs de enige rmk-route die zonder inloggen gegevens geeft.

Gebruik:  python3 tests/rmk-routes-test.py [https://robotmaaierkompas.nl] [--na-136] [--na-137] [--na-1310]
"""
import json, re, sys, urllib.request, urllib.error

SITE = next((a for a in sys.argv[1:] if a.startswith('http')), 'https://robotmaaierkompas.nl').rstrip('/')
NA_136 = '--na-136' in sys.argv
NA_137 = '--na-137' in sys.argv
NA_1310 = '--na-1310' in sys.argv
BEKEND = ['/rmk/v1', '/rmk/v1/status', '/rmk/v1/modellen', '/rmk/v1/bol-status', '/rmk/v1/bol-ronde', '/rmk/v1/bol-prijs',
          '/rmk/v1/coolblue-ronde', '/rmk/v1/coolblue-status',
          '/rmk/v1/noindex', '/rmk/v1/paginas', '/rmk/v1/seo', '/rmk/v1/huisstijl']
COOLBLUE_ROUTES = {'/rmk/v1/coolblue-ronde', '/rmk/v1/coolblue-status'}
COOLBLUE_VELDEN = {'model', 'prijs', 'tijdstip', 'winkel'}
WEG_IN_136 = {'/rmk/v1/noindex', '/rmk/v1/paginas', '/rmk/v1/seo', '/rmk/v1/huisstijl'}
PRIJS_VELDEN = {'status', 'model', 'ean', 'prijs', 'prijs_tekst', 'verkoper', 'partner', 'tijd', 'tijd_tekst', 'geldig_tot'}
PRIJS_QUERY = '?modellen=M001,M002,M004,M005,M006,M007,M008,M011,M015,M016,M017,M018'


def vraag(pad, methode='GET'):
    req = urllib.request.Request(SITE + '/wp-json' + pad, method=methode, data=b'' if methode == 'POST' else None,
                                 headers={'User-Agent': 'rmk-routetest', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()[:20000], {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:2000], {k.lower(): v for k, v in e.headers.items()}


def prijs_ok(st, body, hd):
    """GET /bol-prijs: 200 met alleen toegestane velden en no-store, of (vóór 1.3.7) 404."""
    if st == 404 and not NA_137:
        return True, 'nog niet aanwezig'
    if st != 200:
        return False, f'verwacht 200, kreeg {st}'
    try:
        d = json.loads(body)
    except ValueError:
        return False, 'geen JSON'
    fouten = []
    if set(d) - {'bron', 'modellen', 'coolblue'}:
        fouten.append(f'extra velden {set(d) - {"bron", "modellen", "coolblue"}}')
    for mid, v in (d.get('coolblue') or {}).items():
        if not re.fullmatch(r'M\d{3,4}', mid) or set(v) != COOLBLUE_VELDEN or v.get('model') != mid or v.get('winkel') != 'Coolblue':
            fouten.append(f'coolblue {mid}: velden {sorted(v)}')
    for mid, v in (d.get('modellen') or {}).items():
        if not re.fullmatch(r'M\d{3,4}', mid) or set(v) - PRIJS_VELDEN:
            fouten.append(f'{mid}: {set(v) - PRIJS_VELDEN}')
    if re.search(rb'partner\.bol\.com|awin1\.com|awin\.com|apikey|bynder|in_stock|hash|secret|client_id|token|access_|password', body, re.I):
        fouten.append('verboden tekst in het antwoord')
    if 'no-store' not in hd.get('cache-control', '') or 'no-store' not in hd.get('cdn-cache-control', ''):
        fouten.append(f'cache: {hd.get("cache-control")} / {hd.get("cdn-cache-control")}')
    return not fouten, '; '.join(fouten) or f'{len(d.get("modellen") or {})} modellen, coolblue {len(d.get("coolblue") or {}) if "coolblue" in d else "-"}, cache-control {hd.get("cache-control")}, cdn {hd.get("x-hcdn-cache-status")}'


routes = set(BEKEND)
st, body, _ = vraag('/')
if st == 200:
    try:
        routes |= {r for r in json.loads(body).get('routes', {}) if r.startswith('/rmk/')}
    except ValueError:
        pass
fout = 0
for pad in sorted(routes):
    for methode in ('GET', 'POST'):
        if pad == '/rmk/v1/bol-prijs' and methode == 'GET':
            st, body, hd = vraag(pad + PRIJS_QUERY)
            ok, info = prijs_ok(st, body, hd)
            fout += 0 if ok else 1
            print(f"{'OK  ' if ok else 'FOUT'} {methode:4} {pad:22} {st} {info}")
            continue
        st, body, hd = vraag(pad, methode)
        code = (re.search(rb'"code":"([^"]+)"', body) or [None, b''])[1].decode()
        ok = st in (401, 404)
        if NA_136 and pad in WEG_IN_136:
            ok = st == 404 and code == 'rest_no_route'
        if NA_137 and pad == '/rmk/v1/bol-ronde':
            ok = st == 401 if methode == 'POST' else st in (401, 404)
        if NA_1310 and pad in COOLBLUE_ROUTES:
            ok = st == 401 if (methode == 'POST') == (pad == '/rmk/v1/coolblue-ronde') else st in (401, 404)
        gegevens = bool(re.search(rb'"(modellen|blog_public|laatste_ronde|constanten_aanwezig|meta|prijs)"', body))
        ok = ok and not gegevens
        fout += 0 if ok else 1
        print(f"{'OK  ' if ok else 'FOUT'} {methode:4} {pad:22} {st} {code}")
print(f'{fout} fout(en)')
sys.exit(1 if fout else 0)
