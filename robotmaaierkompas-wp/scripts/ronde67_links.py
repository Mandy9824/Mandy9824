#!/usr/bin/env python3
"""Ronde 67, KLAARGEZET: alle links rond /eufy-robotmaaier/. Pas draaien als Mandy meldt dat die pagina gepubliceerd is.
Weigert zolang eufy-robotmaaier (#366) geen status publish heeft.
1. Hub (#10), "Meer lezen": regel na de Mova/Dreame-regel: "Alle Eufy-robotmaaiers vergeleken: zie Eufy robotmaaier."
2. Pagina 1 (#11), onder "De modellen een voor een": dezelfde zin na de Mova/Dreame-zin.
3. Navimow- (#264), Husqvarna- (#20), Gardena- (#21), Stihl- (#22), Worx-pagina (#24) (de Mova/Dreame-pagina #351 niet meer: die link staat er sinds ronde 68 al),
   "Meer lezen": "Eufy robotmaaier: de E15, E18 en C15 vergeleken."
4. Eufy-pagina (#366), "Meer lezen" (na de Worx-regel): Segway Navimow en Mova of Dreame, met dezelfde teksten als op
   de andere merkpagina's.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde67_links.py [--schrijf]
          python3 scripts/ronde67_links.py --proef-concept   (alleen de ankers controleren terwijl #366 nog concept is)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
PID_NIEUW = 366
EL = '<a href="/eufy-robotmaaier/">Eufy robotmaaier</a>'
ML_ = '<a href="/mova-dreame-robotmaaier/">Mova of Dreame robotmaaier</a>'
WL = '<a href="/worx-robotmaaier/">Worx robotmaaier</a>'
NL = '<a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>'
ZIN = f'Alle Eufy-robotmaaiers vergeleken: zie {EL}.'
EML = f'<li>{EL}: de E15, E18 en C15 vergeleken.</li></ul>'
MOVA_ZIN = f'Mova en Dreame: de LiDAR-robotmaaiers vergeleken, zie {ML_}.'
MOVA_ML = f'<li>{ML_}: de LiDAR-modellen vergeleken.</li></ul>'
WORX_ML = f'<li>{WL}: de Landroid-modellen vergeleken.</li></ul>'
STAPPEN = [
    (10, f'<li>{MOVA_ZIN}</li>', f'<li>{MOVA_ZIN}</li><li>{ZIN}</li>', 'hub, Meer lezen', '/eufy-robotmaaier/'),
    (11, f'<p>{MOVA_ZIN}</p>', f'<p>{MOVA_ZIN}</p>\n<p>{ZIN}</p>', 'pagina 1, De modellen een voor een', '/eufy-robotmaaier/'),
    (264, MOVA_ML, MOVA_ML[:-5] + EML, 'Navimow-pagina, Meer lezen', '/eufy-robotmaaier/'),
    (20, MOVA_ML, MOVA_ML[:-5] + EML, 'Husqvarna-pagina, Meer lezen', '/eufy-robotmaaier/'),
    (21, MOVA_ML, MOVA_ML[:-5] + EML, 'Gardena-pagina, Meer lezen', '/eufy-robotmaaier/'),
    (22, MOVA_ML, MOVA_ML[:-5] + EML, 'Stihl-pagina, Meer lezen', '/eufy-robotmaaier/'),
    (24, MOVA_ML, MOVA_ML[:-5] + EML, 'Worx-pagina, Meer lezen', '/eufy-robotmaaier/'),
    (PID_NIEUW, WORX_ML, WORX_ML[:-5] + f'<li>{NL}: alle modellen die nu nieuw te koop zijn.</li>' + MOVA_ML,
     'Eufy-pagina, Meer lezen', '/segway-navimow-robotmaaier/'),
]

doel = api('wp/v2/pages?slug=eufy-robotmaaier&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['id'] != PID_NIEUW or (doel[0]['status'] != 'publish' and not PROEF_CONCEPT):
    sys.exit(f'eufy-robotmaaier is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
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
# Eufy-pagina: ook de link naar Mova/Dreame moet er nog niet staan
if '/mova-dreame-robotmaaier/' in pag[PID_NIEUW]['content']['raw']:
    meld.append(f'#{PID_NIEUW} Eufy-pagina, Meer lezen: link naar Mova/Dreame staat er al.')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde67-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
