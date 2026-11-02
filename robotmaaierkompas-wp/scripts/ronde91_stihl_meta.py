#!/usr/bin/env python3
"""Ronde 91: alleen de Yoast-metabeschrijving van /stihl-robotmaaier/ (#22) vervangen.

Inhoud, titel en status blijven gelijk (het script controleert dat). Met --schrijf: eerst een kopie in backups/,
dan opslaan, controle in de live HTML (openbaar adres, cache omzeild), LiteSpeed legen via de dataroute.
Gebruik:  python3 scripts/ronde91_stihl_meta.py [--schrijf]
"""
import html, json, os, re, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PID = 22
URL = 'https://robotmaaierkompas.nl/stihl-robotmaaier/'
NIEUW = ('Geen draadloze Stihl, wel negen iMOW-modellen met draad: installatiekit 87 of 229 euro, '
         '4G bij de EVO. Welke past bij 500 tot 5.000 m²?')


def live_meta():
    req = urllib.request.Request(f'{URL}?nocache={int(time.time())}', headers={'Cache-Control': 'no-cache', 'User-Agent': 'Mozilla/5.0 rmk-controle'})
    with urllib.request.urlopen(req, timeout=60) as r:
        h = r.read().decode('utf-8')
    return {n: [html.unescape(v) for v in re.findall(rf'<meta (?:name|property)="{re.escape(n)}" content="([^"]*)"', h)]
            for n in ('description', 'og:description', 'twitter:description')}


p = api(f'wp/v2/pages/{PID}?context=edit')
if p['slug'] != 'stihl-robotmaaier':
    sys.exit(f'#{PID} heeft slug {p["slug"]}. Niets gewijzigd.')
oud = p['meta'].get('_yoast_wpseo_metadesc')
print(f'#{PID} status {p["status"]}\n  oud:   {oud}\n  nieuw: {NIEUW} ({len(NIEUW)} tekens)')
print('Live vooraf:', live_meta())
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde91-pagina22-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({k: p[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta', 'modified')},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api(f'wp/v2/pages/{PID}', {'meta': {'_yoast_wpseo_metadesc': NIEUW}})
q = api(f'wp/v2/pages/{PID}?context=edit')
print(f'opgeslagen: status {q["status"]} (was {p["status"]}); metabeschrijving gezet: {q["meta"].get("_yoast_wpseo_metadesc") == NIEUW}; '
      f'inhoud gelijk: {q["content"]["raw"] == p["content"]["raw"]}; titel gelijk: {q["title"]["raw"] == p["title"]["raw"]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
time.sleep(3)
m = live_meta()
print('Live na afloop:', m)
print('Live meta description precies goed:', m['description'] == [NIEUW])
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
