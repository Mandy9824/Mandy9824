#!/usr/bin/env python3
"""Ronde 22, na de upload van thema 1.3.5: de tijdelijke aanvullende CSS weghalen.

1.3.5 bevat de tabelregels voor de methodepagina (ronde 20) en de instelling RMK_AFFILIATE_ACTIVE
(vervangt de CSS-truc .rmk-affnote uit ronde 21). Dit script haalt die twee blokken pas uit de
aanvullende CSS als het actieve thema live 1.3.5 (of hoger) is.

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde22_na_upload.py          (proefdraai, schrijft niets)
          python3 scripts/ronde22_na_upload.py --schrijf
"""
import base64, json, os, re, sys, urllib.request, urllib.error

SITE = 'https://robotmaaierkompas.nl/wp-json/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
SCHRIJF = '--schrijf' in sys.argv
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()
# De twee blokken zoals ze in ronde 20 en 21 zijn toegevoegd (commentaar tot en met de laatste regel).
BLOKKEN = [
    r'/\* Ronde 20:.*?\.rmk-split > \.rmk-split__main > \.rmk-prose \{ min-width: 0; max-width: 100%; \}',
    r'/\* Ronde 21:.*?\.rmk-affnote \{ display: none !important; \}',
]


def api(path, data=None):
    req = urllib.request.Request(SITE + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:300]!r}')


thema = api('wp/v2/themes?status=active')[0]
versie = thema.get('version', '')
print(f'Actief thema: {thema["stylesheet"]} {versie}')
if tuple(int(x) for x in re.findall(r'\d+', versie)[:3]) < (1, 3, 5):
    sys.exit('Thema 1.3.5 is nog niet actief. Niets gewijzigd.')

gs_id = thema['_links']['wp:user-global-styles'][0]['href'].rstrip('/').split('/')[-1]
gs = api(f'wp/v2/global-styles/{gs_id}?context=edit')
css = (gs.get('styles') or {}).get('css') or ''
nieuw = css
for b in BLOKKEN:
    n = len(re.findall(b, nieuw, re.S))
    print(f'Blok {b[:14]}…: {n} keer gevonden')
    if n > 1:
        sys.exit('Blok meer dan één keer gevonden. Niets gewijzigd.')
    nieuw = re.sub(b, '', nieuw, flags=re.S)
nieuw = re.sub(r'\n{3,}', '\n\n', nieuw).strip()
print('Aanvullende CSS daarna:', repr(nieuw) if nieuw else '(leeg)')
if SCHRIJF and nieuw != css:
    styles = dict(gs.get('styles') or {})
    styles['css'] = nieuw
    api(f'wp/v2/global-styles/{gs_id}', {'styles': styles})
    print('Opgeslagen:', repr(api(f'wp/v2/global-styles/{gs_id}?context=edit')['styles'].get('css') or ''))
