#!/usr/bin/env python3
"""Ronde 65: op de Mova/Dreame-pagina (#351, gepubliceerd) de twee regels onder "Meer lezen" terugzetten
(Segway Navimow en Worx, uit scripts/ronde63_links.py). Een editortab met de oude versie heeft ze bij het opslaan
weggehaald (revisie 363). De andere zeven pagina's van het linkscript hebben hun regel nog en blijven ongemoeid.
Het anker moet precies één keer voorkomen en de links mogen er nog niet staan; anders schrijft het script niets.
De pagina houdt haar status. Met --schrijf: eerst een kopie in backups/, dan opslaan, LiteSpeed legen via de dataroute.
Gebruik:  python3 scripts/ronde65_mova_links_herstel.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PID = 351
MES_ML = '<li><a href="/robotmaaier-mesjes/">Robotmaaier mesjes</a>: prijzen en vervangtermijnen.</li></ul>'
NIEUW = ('<li><a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>: alle modellen die nu nieuw te koop zijn.</li>'
         '<li><a href="/worx-robotmaaier/">Worx robotmaaier</a>: de Landroid-modellen vergeleken.</li></ul>')

p = api(f'wp/v2/pages/{PID}?context=edit')
raw = oud = p['content']['raw']
meld = []
if p['slug'] != 'mova-dreame-robotmaaier':
    meld.append(f'#{PID} heeft slug {p["slug"]}.')
for link in ('/segway-navimow-robotmaaier/', '/worx-robotmaaier/'):
    if link in raw:
        meld.append(f'{link} staat er al.')
if raw.count(MES_ML) != 1:
    meld.append(f'anker "Robotmaaier mesjes" {raw.count(MES_ML)} keer gevonden (verwacht 1).')
if not meld:
    raw = raw.replace(MES_ML, MES_ML[:-5] + NIEUW, 1)
    print('  Meer lezen: Navimow en Worx toegevoegd')
print(f'#{PID} status {p["status"]}')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde65-pagina351-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({'id': PID, 'status': p['status'], 'content': oud}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api(f'wp/v2/pages/{PID}', {'content': raw})
q = api(f'wp/v2/pages/{PID}?context=edit')
print(f'#{PID} opgeslagen; status {q["status"]} (was {p["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
