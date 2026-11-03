#!/usr/bin/env python3
"""Ronde 93, KLAARGEZET: alle links rond /husqvarna-of-gardena-robotmaaier/. Pas draaien als Mandy meldt dat die pagina
gepubliceerd is. Weigert zolang husqvarna-of-gardena-robotmaaier (#461) geen status publish heeft.
1. Husqvarna- (#20) en Gardena-pagina (#21), "Meer lezen", als laatste regel (na de grote-tuinregel):
   "Husqvarna of Gardena robotmaaier? De twee merken vergeleken." (tekst Mandy; de link op "Husqvarna of Gardena robotmaaier").
2. Hub (#10), "Meer lezen": dezelfde regel na de grote-tuinregel.
3. Pagina 1 (#11), onder "De modellen een voor een": dezelfde zin na de grote-tuinzin.
4. Nieuwe pagina (#461), "Meer lezen" (na de Stihl-regel): Husqvarna, Gardena, kleine tuin en grote tuin, met dezelfde
   teksten als op de andere pagina's.
Alle zes pagina's zijn gepubliceerd en (behalve #461) met de hand gewijzigd: alleen gerichte vervangingen, nooit opnieuw bouwen.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde93_links.py [--schrijf]
          python3 scripts/ronde93_links.py --proef-concept   (alleen de ankers controleren terwijl #461 nog concept is)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
PID_NIEUW = 461
SLUG = 'husqvarna-of-gardena-robotmaaier'
HG = f'/{SLUG}/'
GL = '/robotmaaier-grote-tuin/'
KL = '/robotmaaier-kleine-tuin/'
ZIN = f'<a href="{HG}">Husqvarna of Gardena robotmaaier</a>? De twee merken vergeleken.'
GROTE_ZIN = f'Op zoek naar een robotmaaier voor een grote tuin? Zie <a href="{GL}">Robotmaaier grote tuin</a>.'
GML = f'<li><a href="{GL}">Robotmaaier voor een grote tuin</a>: modellen van 1.000 tot 3.000 m².</li></ul>'
STIHL_ML = '<li><a href="/stihl-robotmaaier/">Stihl robotmaaier</a>: de iMOW-modellen vergeleken.</li></ul>'
NIEUW_ML = ('<li><a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>: de Automower-modellen vergeleken.</li>'
            '<li><a href="/gardena-robotmaaier/">Gardena robotmaaier</a>: de Sileno-modellen vergeleken.</li>'
            f'<li><a href="{KL}">Robotmaaier voor een kleine tuin</a>: vijftien modellen tot 600 m².</li>'
            f'<li><a href="{GL}">Robotmaaier voor een grote tuin</a>: modellen van 1.000 tot 3.000 m².</li>')
NIEUWE_LINKS = ['/husqvarna-robotmaaier/', '/gardena-robotmaaier/', KL, GL]
STAPPEN = [
    (20, GML, GML[:-5] + f'<li>{ZIN}</li></ul>', 'Husqvarna-pagina, Meer lezen', HG),
    (21, GML, GML[:-5] + f'<li>{ZIN}</li></ul>', 'Gardena-pagina, Meer lezen', HG),
    (10, f'<li>{GROTE_ZIN}</li>', f'<li>{GROTE_ZIN}</li><li>{ZIN}</li>', 'hub, Meer lezen', HG),
    (11, f'<p>{GROTE_ZIN}</p>', f'<p>{GROTE_ZIN}</p>\n<p>{ZIN}</p>', 'pagina 1, De modellen een voor een', HG),
    (PID_NIEUW, STIHL_ML, STIHL_ML[:-5] + NIEUW_ML + '</ul>', 'Husqvarna-of-Gardena-pagina, Meer lezen', '/husqvarna-robotmaaier/'),
]

doel = api(f'wp/v2/pages?slug={SLUG}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['id'] != PID_NIEUW or (doel[0]['status'] != 'publish' and not PROEF_CONCEPT):
    sys.exit(f'{SLUG} is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
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
# Nieuwe pagina: in "Meer lezen" mag nog geen van de vier nieuwe links staan
ml = re.search(r'<h2 id="meer-lezen">Meer lezen</h2>\s*<ul>.*?</ul>', pag[PID_NIEUW]['content']['raw'], re.S)
if not ml:
    meld.append(f'#{PID_NIEUW}: "Meer lezen" niet gevonden.')
else:
    for l in NIEUWE_LINKS:
        if l in ml.group(0):
            meld.append(f'#{PID_NIEUW}, Meer lezen: link naar {l} staat er al.')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde93-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
