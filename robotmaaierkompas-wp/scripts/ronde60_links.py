#!/usr/bin/env python3
"""Ronde 60, KLAARGEZET: alle links rond /worx-robotmaaier/. Pas draaien als Mandy meldt dat die pagina gepubliceerd is.
Weigert zolang worx-robotmaaier (#24) geen status publish heeft.
1. Hub (#10), "Meer lezen": regel na de Stihl-regel: "Alle Worx Landroid-modellen vergeleken: zie Worx robotmaaier."
2. Pagina 1 (#11), onder "De modellen een voor een": dezelfde zin na de Stihl-zin.
3. Navimow- (#264), Husqvarna- (#20), Gardena- (#21) en Stihl-pagina (#22), "Meer lezen":
   "Worx robotmaaier: de Landroid-modellen vergeleken."
4. Worx-pagina (#24), "Meer lezen": Segway Navimow, Husqvarna, Gardena en Stihl, met dezelfde teksten als op de andere
   merkpagina's.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde60_links.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
WL = '<a href="/worx-robotmaaier/">Worx robotmaaier</a>'
SL = '<a href="/stihl-robotmaaier/">Stihl robotmaaier</a>'
GL = '<a href="/gardena-robotmaaier/">Gardena robotmaaier</a>'
HL = '<a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>'
NL = '<a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>'
ZIN = f'Alle Worx Landroid-modellen vergeleken: zie {WL}.'
ML = f'<li>{WL}: de Landroid-modellen vergeleken.</li></ul>'
STIHL_ZIN = f'Alle Stihl iMOW-modellen vergeleken: zie {SL}.'
STIHL_ML = f'<li>{SL}: de iMOW-modellen vergeleken.</li></ul>'
GARD_ML = f'<li>{GL}: de Sileno-modellen vergeleken.</li></ul>'
GRENS_ML = ('<li><a href="/robotmaaier-zonder-grensdraad/">Robotmaaier zonder grensdraad</a>: '
            'hoe het werkt en wanneer je het kiest.</li></ul>')
STAPPEN = [
    (10, f'<li>{STIHL_ZIN}</li>', f'<li>{STIHL_ZIN}</li><li>{ZIN}</li>', 'hub, Meer lezen', '/worx-robotmaaier/'),
    (11, f'<p>{STIHL_ZIN}</p>', f'<p>{STIHL_ZIN}</p>\n<p>{ZIN}</p>', 'pagina 1, De modellen een voor een', '/worx-robotmaaier/'),
    (264, STIHL_ML, STIHL_ML[:-5] + ML, 'Navimow-pagina, Meer lezen', '/worx-robotmaaier/'),
    (20, STIHL_ML, STIHL_ML[:-5] + ML, 'Husqvarna-pagina, Meer lezen', '/worx-robotmaaier/'),
    (21, STIHL_ML, STIHL_ML[:-5] + ML, 'Gardena-pagina, Meer lezen', '/worx-robotmaaier/'),
    (22, GARD_ML, GARD_ML[:-5] + ML, 'Stihl-pagina, Meer lezen', '/worx-robotmaaier/'),
    (24, GRENS_ML, GRENS_ML[:-5] + f'<li>{NL}: alle modellen die nu nieuw te koop zijn.</li>'
     f'<li>{HL}: de Automower-modellen vergeleken.</li><li>{GL}: de Sileno-modellen vergeleken.</li>' + STIHL_ML,
     'Worx-pagina, Meer lezen', '/segway-navimow-robotmaaier/'),
]

doel = api('wp/v2/pages?slug=worx-robotmaaier&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['status'] != 'publish' or doel[0]['id'] != 24:
    sys.exit(f'worx-robotmaaier is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
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
pad = f'backups/ronde60-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
