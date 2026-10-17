#!/usr/bin/env python3
# VERVANGEN door scripts/ronde44_links.py (ronde 44): het mesjes-anker hieronder klopt niet meer na sectie B. Niet meer draaien.
"""Ronde 43, KLAARGEZET: links naar /husqvarna-robotmaaier/. Pas draaien na het bericht van Mandy.

Weigert zolang de pagina husqvarna-robotmaaier niet gepubliceerd is.
- Hub (#10), "Meer lezen": regel direct na de Navimow-regel.
- Pagina 1 (#11), onder "De modellen een voor een": zin direct na de Navimow-zin.
- Mesjespagina (#236), onder "Husqvarna robotmaaier mesjes": "Welke Automower past bij welke tuin? Zie Husqvarna robotmaaier."
  direct na de alinea over de 305E NERA.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde43_links.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
LINK = '<a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>'
NAV_LI = '<li>Alle Segway Navimow-modellen die nu nieuw te koop zijn, met kosten: zie <a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>.</li>'
NAV_P = '<p>Alle Segway Navimow-modellen die nu nieuw te koop zijn, met kosten: zie <a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>.</p>'
MES_P = ('<p>Voor de Automower 305E NERA noemt Husqvarna Endurance-messen (26,99 euro) en Classic-messen (22,99 euro); '
         'de messen van de hoofdschijf gaan volgens Husqvarna 3 tot 6 weken mee.</p>')
STAPPEN = [
    (10, NAV_LI, NAV_LI + f'<li>Alle Husqvarna Automower-modellen die nu nieuw te koop zijn, met kosten: zie {LINK}.</li>', 'hub, Meer lezen'),
    (11, NAV_P, NAV_P + f'\n<p>Alle Husqvarna Automower-modellen die nu nieuw te koop zijn, met kosten: zie {LINK}.</p>', 'pagina 1, De modellen een voor een'),
    (236, MES_P, MES_P + f'\n<p>Welke Automower past bij welke tuin? Zie {LINK}.</p>', 'mesjespagina, Husqvarna robotmaaier mesjes'),
]

doel = api('wp/v2/pages?slug=husqvarna-robotmaaier&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['status'] != 'publish':
    sys.exit(f'husqvarna-robotmaaier is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in (10, 11, 236)}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid, was, wordt, wat in STAPPEN:
    if '/husqvarna-robotmaaier/' in raw[pid]:
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
pad = f'backups/ronde43-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in (10, 11, 236):
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
