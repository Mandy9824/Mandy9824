#!/usr/bin/env python3
"""Ronde 48, KLAARGEZET: alle links rond /gardena-robotmaaier/. Pas draaien als Mandy meldt dat die pagina gepubliceerd is.
Weigert zolang gardena-robotmaaier geen status publish heeft.
1. Hub (#10), "Meer lezen": regel na de Husqvarna-regel.
2. Pagina 1 (#11), onder "De modellen een voor een": zin na de Husqvarna-zin.
3. Navimow-pagina (#264), "Meer lezen": "Gardena robotmaaier: de Sileno-modellen vergeleken."
4. Husqvarna-pagina (#20), "Meer lezen": "Gardena robotmaaier: de Sileno-modellen vergeleken."
5. Gardena-pagina (#21), "Meer lezen": "Husqvarna robotmaaier: de Automower-modellen vergeleken." en
   "Segway Navimow robotmaaier: alle modellen die nu nieuw te koop zijn."
De mesjespagina (#236) heeft geen Gardena-gedeelte (Gardena staat alleen onder "Wat we nog niet weten"): daar geen regel.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde48_links.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
GL = '<a href="/gardena-robotmaaier/">Gardena robotmaaier</a>'
HL = '<a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>'
NL = '<a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>'
ZIN = f'Alle Gardena Sileno-modellen, met beschikbaarheid en kosten: zie {GL}.'
HUSQ_LI = f'<li>Alle Husqvarna Automower-modellen die nu nieuw te koop zijn, met kosten: zie {HL}.</li>'
HUSQ_P = f'<p>Alle Husqvarna Automower-modellen die nu nieuw te koop zijn, met kosten: zie {HL}.</p>'
NAV_ML = f'<li>{HL}: de Automower-modellen vergeleken.</li></ul>'
HUSQ_ML = f'<li>{NL}: alle modellen die nu nieuw te koop zijn.</li></ul>'
MES_ML = '<li><a href="/robotmaaier-mesjes/">Robotmaaier mesjes</a>: prijzen en vervangtermijnen.</li></ul>'
STAPPEN = [
    (10, HUSQ_LI, HUSQ_LI + f'<li>{ZIN}</li>', 'hub, Meer lezen', '/gardena-robotmaaier/'),
    (11, HUSQ_P, HUSQ_P + f'\n<p>{ZIN}</p>', 'pagina 1, De modellen een voor een', '/gardena-robotmaaier/'),
    (264, NAV_ML, NAV_ML[:-5] + f'<li>{GL}: de Sileno-modellen vergeleken.</li></ul>', 'Navimow-pagina, Meer lezen', '/gardena-robotmaaier/'),
    (20, HUSQ_ML, HUSQ_ML[:-5] + f'<li>{GL}: de Sileno-modellen vergeleken.</li></ul>', 'Husqvarna-pagina, Meer lezen', '/gardena-robotmaaier/'),
    (21, MES_ML, MES_ML[:-5] + f'<li>{HL}: de Automower-modellen vergeleken.</li><li>{NL}: alle modellen die nu nieuw te koop zijn.</li></ul>',
     'Gardena-pagina, Meer lezen', '/husqvarna-robotmaaier/'),
]

doel = api('wp/v2/pages?slug=gardena-robotmaaier&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['status'] != 'publish' or doel[0]['id'] != 21:
    sys.exit(f'gardena-robotmaaier is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
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
pad = f'backups/ronde48-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
