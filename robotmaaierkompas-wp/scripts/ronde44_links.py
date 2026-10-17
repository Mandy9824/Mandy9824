#!/usr/bin/env python3
"""Ronde 44, KLAARGEZET: alle links rond /husqvarna-robotmaaier/. Pas draaien als Mandy meldt dat die pagina gepubliceerd is.
Vervangt scripts/ronde43_links.py (die drie regels zitten hier ook in). Weigert zolang husqvarna-robotmaaier geen status publish heeft.
1. Hub (#10), "Meer lezen": regel na de Navimow-regel.
2. Pagina 1 (#11), onder "De modellen een voor een": zin na de Navimow-zin.
3. Mesjespagina (#236), onder "Husqvarna robotmaaier mesjes": "Welke Automower past bij welke tuin? Zie Husqvarna robotmaaier."
4. Kosten (#18), sectie C5: "Meer over de Automower-modellen lees je op Husqvarna robotmaaier." aan het einde van het punt
   over de Husqvarna 305E en 310E NERA onder "Antenne, gateway of dekking".
5. Navimow-pagina (#264), "Meer lezen": "Husqvarna robotmaaier: de Automower-modellen vergeleken."
6. Husqvarna-pagina (#20), "Meer lezen": "Segway Navimow robotmaaier: alle modellen die nu nieuw te koop zijn."
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde44_links.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
HL = '<a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>'
NAV_LI = '<li>Alle Segway Navimow-modellen die nu nieuw te koop zijn, met kosten: zie <a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>.</li>'
NAV_P = '<p>Alle Segway Navimow-modellen die nu nieuw te koop zijn, met kosten: zie <a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>.</p>'
MES_P = ('<p>Voor de Automower 305E en 310E NERA noemt Husqvarna Endurance-messen (26,99 euro) en Classic-messen (22,99 euro); '
         'de messen van de hoofdschijf gaan volgens Husqvarna 3 tot 6 weken mee.</p>')
KOST_LI = '<li>Husqvarna Automower 305E en 310E NERA: wifi-dekking over het hele gazon nodig; zonder wifi een Connect Kit of een referentiestation.</li>'
KOST_ML = '<li><a href="/robotmaaier-kosten/">Robotmaaier kosten</a>: wat het echt kost, met verborgen kosten.</li></ul>'
MES_ML = '<li><a href="/robotmaaier-mesjes/">Robotmaaier mesjes</a>: prijzen en vervangtermijnen.</li></ul>'
STAPPEN = [
    (10, NAV_LI, NAV_LI + f'<li>Alle Husqvarna Automower-modellen die nu nieuw te koop zijn, met kosten: zie {HL}.</li>', 'hub, Meer lezen', '/husqvarna-robotmaaier/'),
    (11, NAV_P, NAV_P + f'\n<p>Alle Husqvarna Automower-modellen die nu nieuw te koop zijn, met kosten: zie {HL}.</p>', 'pagina 1, De modellen een voor een', '/husqvarna-robotmaaier/'),
    (236, MES_P, MES_P + f'\n<p>Welke Automower past bij welke tuin? Zie {HL}.</p>', 'mesjespagina', '/husqvarna-robotmaaier/'),
    (18, KOST_LI, KOST_LI[:-5] + f' Meer over de Automower-modellen lees je op {HL}.</li>', 'kosten C5', '/husqvarna-robotmaaier/'),
    (264, KOST_ML, KOST_ML[:-5] + f'<li>{HL}: de Automower-modellen vergeleken.</li></ul>', 'Navimow-pagina, Meer lezen', '/husqvarna-robotmaaier/'),
    (20, MES_ML, MES_ML[:-5] + '<li><a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>: alle modellen die nu nieuw te koop zijn.</li></ul>',
     'Husqvarna-pagina, Meer lezen', '/segway-navimow-robotmaaier/'),
]

doel = api('wp/v2/pages?slug=husqvarna-robotmaaier&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['status'] != 'publish':
    sys.exit(f'husqvarna-robotmaaier is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
ids = sorted({s[0] for s in STAPPEN})
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid, was, wordt, wat, link in STAPPEN:
    if raw[pid].count(link) and link == '/husqvarna-robotmaaier/':
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
pad = f'backups/ronde44-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
