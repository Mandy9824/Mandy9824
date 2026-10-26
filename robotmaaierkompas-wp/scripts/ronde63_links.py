#!/usr/bin/env python3
"""Ronde 63, KLAARGEZET: alle links rond /mova-dreame-robotmaaier/. Pas draaien als Mandy meldt dat die pagina gepubliceerd is.
Weigert zolang mova-dreame-robotmaaier (#351) geen status publish heeft.
1. Hub (#10), "Meer lezen": regel na de Worx-regel:
   "Mova en Dreame: de LiDAR-robotmaaiers vergeleken, zie Mova of Dreame robotmaaier."
2. Pagina 1 (#11), onder "De modellen een voor een": dezelfde zin na de Worx-zin.
3. Navimow- (#264), Husqvarna- (#20), Gardena- (#21), Stihl- (#22) en Worx-pagina (#24), "Meer lezen":
   "Mova of Dreame robotmaaier: de LiDAR-modellen vergeleken."
4. Mova/Dreame-pagina (#351), "Meer lezen": Segway Navimow en Worx, met dezelfde teksten als op de andere merkpagina's.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde63_links.py [--schrijf]
          python3 scripts/ronde63_links.py --proef-concept   (alleen de ankers controleren terwijl #351 nog concept is)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
PID_NIEUW = 351
ML_ = '<a href="/mova-dreame-robotmaaier/">Mova of Dreame robotmaaier</a>'
WL = '<a href="/worx-robotmaaier/">Worx robotmaaier</a>'
SL = '<a href="/stihl-robotmaaier/">Stihl robotmaaier</a>'
NL = '<a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>'
ZIN = f'Mova en Dreame: de LiDAR-robotmaaiers vergeleken, zie {ML_}.'
ML = f'<li>{ML_}: de LiDAR-modellen vergeleken.</li></ul>'
WORX_ZIN = f'Alle Worx Landroid-modellen vergeleken: zie {WL}.'
WORX_ML = f'<li>{WL}: de Landroid-modellen vergeleken.</li></ul>'
STIHL_ML = f'<li>{SL}: de iMOW-modellen vergeleken.</li></ul>'
MES_ML = '<li><a href="/robotmaaier-mesjes/">Robotmaaier mesjes</a>: prijzen en vervangtermijnen.</li></ul>'
STAPPEN = [
    (10, f'<li>{WORX_ZIN}</li>', f'<li>{WORX_ZIN}</li><li>{ZIN}</li>', 'hub, Meer lezen', '/mova-dreame-robotmaaier/'),
    (11, f'<p>{WORX_ZIN}</p>', f'<p>{WORX_ZIN}</p>\n<p>{ZIN}</p>', 'pagina 1, De modellen een voor een', '/mova-dreame-robotmaaier/'),
    (264, WORX_ML, WORX_ML[:-5] + ML, 'Navimow-pagina, Meer lezen', '/mova-dreame-robotmaaier/'),
    (20, WORX_ML, WORX_ML[:-5] + ML, 'Husqvarna-pagina, Meer lezen', '/mova-dreame-robotmaaier/'),
    (21, WORX_ML, WORX_ML[:-5] + ML, 'Gardena-pagina, Meer lezen', '/mova-dreame-robotmaaier/'),
    (22, WORX_ML, WORX_ML[:-5] + ML, 'Stihl-pagina, Meer lezen', '/mova-dreame-robotmaaier/'),
    (24, STIHL_ML, STIHL_ML[:-5] + ML, 'Worx-pagina, Meer lezen', '/mova-dreame-robotmaaier/'),
    (PID_NIEUW, MES_ML, MES_ML[:-5] + f'<li>{NL}: alle modellen die nu nieuw te koop zijn.</li>' + WORX_ML,
     'Mova/Dreame-pagina, Meer lezen', '/segway-navimow-robotmaaier/'),
]

doel = api('wp/v2/pages?slug=mova-dreame-robotmaaier&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['id'] != PID_NIEUW or (doel[0]['status'] != 'publish' and not PROEF_CONCEPT):
    sys.exit(f'mova-dreame-robotmaaier is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
ids = sorted({s[0] for s in STAPPEN})
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid, was, wordt, wat, link in STAPPEN:
    if raw[pid].count(link):
        meld.append(f'#{pid} {wat}: link staat er al.')
    elif raw[pid].count(was) != 1:
        meld.append(f'#{pid} {wat}: anker {raw[pid].count(was)} keer gevonden (verwacht 1).')
    else:
        raw[pid] = raw[pid].replace(was, wordt, 1)
        print(f'  #{pid} {wat}: regel toegevoegd')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde63-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
