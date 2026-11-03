#!/usr/bin/env python3
"""Ronde 92: alleen de Yoast-metabeschrijving van /stihl-robotmaaier/ (#22) vervangen.

Kopie vooraf in backups/ (niet in git). Daarna LiteSpeed legen via de dataroute (modelgegevens ongewijzigd terugzetten).
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde92_stihl_meta.py            (proefdraai)
          python3 scripts/ronde92_stihl_meta.py --schrijf
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

PID = 22
OUD = ('Geen draadloze Stihl, wel negen iMOW-modellen met draad: installatiekit 87 of 229 euro, 4G bij de EVO. '
       'Welke past bij 500 tot 5.000 m²?')
NIEUW = ('Geen draadloze Stihl, wel negen iMOW-modellen met draad: installatiekit 87 of 229 euro, mobiel bij 3 EVO en 4 EVO. '
         'Welke past bij 500 tot 5.000 m²?')
SCHRIJF = '--schrijf' in sys.argv

p = api(f'wp/v2/pages/{PID}?context=edit')
nu = p['meta'].get('_yoast_wpseo_metadesc')
print(f'#{PID} {p["slug"]} status {p["status"]}; metabeschrijving nu: {nu!r}')
if p['slug'] != 'stihl-robotmaaier' or p['status'] != 'publish':
    sys.exit('Onverwachte pagina of status. Niets gewijzigd.')
if nu == NIEUW:
    sys.exit('Staat al goed. Niets gewijzigd.')
if nu != OUD:
    sys.exit('Huidige metabeschrijving wijkt af van de verwachte. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde92-pagina{PID}-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({k: p[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta', 'modified')},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api(f'wp/v2/pages/{PID}', {'meta': {'_yoast_wpseo_metadesc': NIEUW}})
q = api(f'wp/v2/pages/{PID}?context=edit')
print('Na opslaan: status', q['status'], '| meta gelijk:', q['meta'].get('_yoast_wpseo_metadesc') == NIEUW,
      '| inhoud gelijk:', q['content']['raw'] == p['content']['raw'], '| titel gelijk:', q['title']['raw'] == p['title']['raw'])
data = api('rmk/v1/modellen')['data']
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', data))
print('Modelgegevens na legen gelijk:', api('rmk/v1/modellen')['data'] == data)
