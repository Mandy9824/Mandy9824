#!/usr/bin/env python3
"""Ronde 52, KLAARGEZET: alle links rond /stihl-robotmaaier/. Pas draaien als Mandy meldt dat die pagina gepubliceerd is.
Weigert zolang stihl-robotmaaier (#22) geen status publish heeft.
1. Hub (#10), "Meer lezen": regel na de Gardena-regel: "Alle Stihl iMOW-modellen vergeleken: zie Stihl robotmaaier."
2. Pagina 1 (#11), onder "De modellen een voor een": dezelfde zin na de Gardena-zin.
3. Navimow- (#264), Husqvarna- (#20) en Gardena-pagina (#21), "Meer lezen": "Stihl robotmaaier: de iMOW-modellen vergeleken."
4. Stihl-pagina (#22), "Meer lezen": "Husqvarna robotmaaier: de Automower-modellen vergeleken." en
   "Gardena robotmaaier: de Sileno-modellen vergeleken."
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde52_links.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
SL = '<a href="/stihl-robotmaaier/">Stihl robotmaaier</a>'
GL = '<a href="/gardena-robotmaaier/">Gardena robotmaaier</a>'
HL = '<a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>'
NL = '<a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>'
ZIN = f'Alle Stihl iMOW-modellen vergeleken: zie {SL}.'
ML = f'<li>{SL}: de iMOW-modellen vergeleken.</li></ul>'
GARD_ZIN = f'Alle Gardena Sileno-modellen, met beschikbaarheid en kosten: zie {GL}.'
GARD_ML = f'<li>{GL}: de Sileno-modellen vergeleken.</li></ul>'
NAV_ML = f'<li>{NL}: alle modellen die nu nieuw te koop zijn.</li></ul>'
MES_ML = '<li><a href="/robotmaaier-mesjes/">Robotmaaier mesjes</a>: prijzen en vervangtermijnen.</li></ul>'
STAPPEN = [
    (10, f'<li>{GARD_ZIN}</li>', f'<li>{GARD_ZIN}</li><li>{ZIN}</li>', 'hub, Meer lezen', '/stihl-robotmaaier/'),
    (11, f'<p>{GARD_ZIN}</p>', f'<p>{GARD_ZIN}</p>\n<p>{ZIN}</p>', 'pagina 1, De modellen een voor een', '/stihl-robotmaaier/'),
    (264, GARD_ML, GARD_ML[:-5] + ML, 'Navimow-pagina, Meer lezen', '/stihl-robotmaaier/'),
    (20, GARD_ML, GARD_ML[:-5] + ML, 'Husqvarna-pagina, Meer lezen', '/stihl-robotmaaier/'),
    (21, NAV_ML, NAV_ML[:-5] + ML, 'Gardena-pagina, Meer lezen', '/stihl-robotmaaier/'),
    (22, MES_ML, MES_ML[:-5] + f'<li>{HL}: de Automower-modellen vergeleken.</li><li>{GL}: de Sileno-modellen vergeleken.</li></ul>',
     'Stihl-pagina, Meer lezen', '/husqvarna-robotmaaier/'),
]

doel = api('wp/v2/pages?slug=stihl-robotmaaier&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['status'] != 'publish' or doel[0]['id'] != 22:
    sys.exit(f'stihl-robotmaaier is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
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
pad = f'backups/ronde52-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
