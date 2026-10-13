#!/usr/bin/env python3
"""Elke rmk-route geeft zonder inloggen 401 of 404 (lijst voor 1.3.6, punt c). Veilig tegen de live site:
zonder inloggegevens en zonder cookies kan een POST niets wijzigen.

Gebruik:  python3 tests/rmk-routes-test.py [https://robotmaaierkompas.nl] [--na-136]
Met --na-136 moeten /noindex en (zonder RMK_BOUW_ACTIVE) /paginas, /seo en /huisstijl 404 geven.
"""
import json, re, sys, urllib.request, urllib.error

SITE = next((a for a in sys.argv[1:] if a.startswith('http')), 'https://robotmaaierkompas.nl').rstrip('/')
NA_136 = '--na-136' in sys.argv
BEKEND = ['/rmk/v1', '/rmk/v1/status', '/rmk/v1/modellen', '/rmk/v1/bol-status', '/rmk/v1/noindex',
          '/rmk/v1/paginas', '/rmk/v1/seo', '/rmk/v1/huisstijl']
WEG_IN_136 = {'/rmk/v1/noindex', '/rmk/v1/paginas', '/rmk/v1/seo', '/rmk/v1/huisstijl'}


def vraag(pad, methode='GET'):
    req = urllib.request.Request(SITE + '/wp-json' + pad, method=methode, data=b'' if methode == 'POST' else None,
                                 headers={'User-Agent': 'rmk-routetest', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()[:400]
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:400]


routes = set(BEKEND)
for index in ('', '/rmk/v1'):
    st, body = vraag(index or '/')
    if st == 200:
        try:
            routes |= {r for r in json.loads(body if index else vraag('/')[1] or b'{}').get('routes', {}) if r.startswith('/rmk/')}
        except ValueError:
            pass
fout = 0
for pad in sorted(routes):
    for methode in ('GET', 'POST'):
        st, body = vraag(pad, methode)
        code = (re.search(rb'"code":"([^"]+)"', body) or [None, b''])[1].decode()
        ok = st in (401, 404)
        if NA_136 and pad in WEG_IN_136:
            ok = st == 404 and code == 'rest_no_route'
        gegevens = bool(re.search(rb'"(modellen|blog_public|laatste_ronde|constanten_aanwezig|meta)"', body))
        ok = ok and not gegevens
        fout += 0 if ok else 1
        print(f"{'OK  ' if ok else 'FOUT'} {methode:4} {pad:22} {st} {code}")
print(f'{fout} fout(en)')
sys.exit(1 if fout else 0)
