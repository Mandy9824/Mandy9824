#!/usr/bin/env python3
"""Ronde 82, KLAARGEZET: alle links rond /robotmaaier-grote-tuin/. Pas draaien als Mandy meldt dat die pagina gepubliceerd is.
Weigert zolang robotmaaier-grote-tuin (#15) geen status publish heeft.
1. Hub (#10), "Meer lezen": regel na de kleine-tuinregel: "Op zoek naar een robotmaaier voor een grote tuin? Zie Robotmaaier grote tuin."
2. Pagina 1 (#11), onder "De modellen een voor een": dezelfde zin na de kleine-tuinzin.
3. Kleine-tuinpagina (#16), "Meer lezen", als laatste regel: "Robotmaaier voor een grote tuin: modellen van 1.000 tot 3.000 m²."
4. Navimow- (#264), Husqvarna- (#20), Gardena- (#21), Stihl- (#22), Worx- (#24), Mova/Dreame- (#351) en Eufy-pagina (#366),
   "Meer lezen", als laatste regel (na de kleine-tuinregel): dezelfde zin.
5. Grote-tuinpagina (#15), "Meer lezen" (na Robotmaaier kosten): de merkpagina's waarvan een model op de pagina staat, in de
   volgorde waarin het merk op de pagina voorkomt (Segway Navimow, Mova of Dreame, Husqvarna, Eufy, Gardena, Worx, Stihl),
   met dezelfde teksten als op de andere merkpagina's, en daarna de kleine-tuinpagina. Roborock en Ecovacs hebben geen merkpagina.
Pagina 1 en de hub zijn met de hand gewijzigd (rondes 78, 79): alleen gerichte vervangingen, nooit opnieuw bouwen.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde82_links.py [--schrijf]
          python3 scripts/ronde82_links.py --proef-concept   (alleen de ankers controleren terwijl #15 nog concept is)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
PID_NIEUW = 15
SLUG = 'robotmaaier-grote-tuin'
GL = '/robotmaaier-grote-tuin/'
KL = '/robotmaaier-kleine-tuin/'
KLEINE_ZIN = f'Op zoek naar een robotmaaier voor een kleine tuin? Zie <a href="{KL}">Robotmaaier kleine tuin</a>.'
ZIN = f'Op zoek naar een robotmaaier voor een grote tuin? Zie <a href="{GL}">Robotmaaier grote tuin</a>.'
KML = f'<li><a href="{KL}">Robotmaaier voor een kleine tuin</a>: twaalf modellen tot 600 m².</li>'
GML = f'<li><a href="{GL}">Robotmaaier voor een grote tuin</a>: modellen van 1.000 tot 3.000 m².</li>'
HUSQ_ML = '<li><a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>: de Automower-modellen vergeleken.</li></ul>'
KOSTEN_ML = '<li><a href="/robotmaaier-kosten/">Robotmaaier kosten</a>: wat het echt kost, met verborgen kosten.</li></ul>'
MERKEN = ('<li><a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>: alle modellen die nu nieuw te koop zijn.</li>'
          '<li><a href="/mova-dreame-robotmaaier/">Mova of Dreame robotmaaier</a>: de LiDAR-modellen vergeleken.</li>'
          '<li><a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>: de Automower-modellen vergeleken.</li>'
          '<li><a href="/eufy-robotmaaier/">Eufy robotmaaier</a>: de E15, E18 en C15 vergeleken.</li>'
          '<li><a href="/gardena-robotmaaier/">Gardena robotmaaier</a>: de Sileno-modellen vergeleken.</li>'
          '<li><a href="/worx-robotmaaier/">Worx robotmaaier</a>: de Landroid-modellen vergeleken.</li>'
          '<li><a href="/stihl-robotmaaier/">Stihl robotmaaier</a>: de iMOW-modellen vergeleken.</li>' + KML)
NIEUWE_LINKS = ['/segway-navimow-robotmaaier/', '/mova-dreame-robotmaaier/', '/husqvarna-robotmaaier/', '/eufy-robotmaaier/',
                '/gardena-robotmaaier/', '/worx-robotmaaier/', '/stihl-robotmaaier/', KL]
STAPPEN = [
    (10, f'<li>{KLEINE_ZIN}</li>', f'<li>{KLEINE_ZIN}</li><li>{ZIN}</li>', 'hub, Meer lezen', GL),
    (11, f'<p>{KLEINE_ZIN}</p>', f'<p>{KLEINE_ZIN}</p>\n<p>{ZIN}</p>', 'pagina 1, De modellen een voor een', GL),
    (16, HUSQ_ML, HUSQ_ML[:-5] + GML + '</ul>', 'kleine-tuinpagina, Meer lezen', GL),
    (264, KML + '</ul>', KML + GML + '</ul>', 'Navimow-pagina, Meer lezen', GL),
    (20, KML + '</ul>', KML + GML + '</ul>', 'Husqvarna-pagina, Meer lezen', GL),
    (21, KML + '</ul>', KML + GML + '</ul>', 'Gardena-pagina, Meer lezen', GL),
    (22, KML + '</ul>', KML + GML + '</ul>', 'Stihl-pagina, Meer lezen', GL),
    (24, KML + '</ul>', KML + GML + '</ul>', 'Worx-pagina, Meer lezen', GL),
    (351, KML + '</ul>', KML + GML + '</ul>', 'Mova/Dreame-pagina, Meer lezen', GL),
    (366, KML + '</ul>', KML + GML + '</ul>', 'Eufy-pagina, Meer lezen', GL),
    (PID_NIEUW, KOSTEN_ML, KOSTEN_ML[:-5] + MERKEN + '</ul>', 'grote-tuinpagina, Meer lezen', '/segway-navimow-robotmaaier/'),
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
# Grote-tuinpagina: in "Meer lezen" mag nog geen van de nieuwe links staan (de tekstlink naar de Stihl-pagina onder
# "Met draad" staat er wel, en hoort er te staan)
ml = re.search(r'<h2 id="meer-lezen">Meer lezen</h2>\s*<ul>.*?</ul>', pag[PID_NIEUW]['content']['raw'], re.S)
if not ml:
    meld.append(f'#{PID_NIEUW} grote-tuinpagina: "Meer lezen" niet gevonden.')
else:
    for l in NIEUWE_LINKS:
        if l in ml.group(0):
            meld.append(f'#{PID_NIEUW} grote-tuinpagina, Meer lezen: link naar {l} staat er al.')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde82-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
