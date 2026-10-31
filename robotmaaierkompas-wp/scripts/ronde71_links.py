#!/usr/bin/env python3
"""Ronde 71, KLAARGEZET: alle links rond /robotmaaier-kleine-tuin/. Pas draaien als Mandy meldt dat die pagina gepubliceerd is.
Weigert zolang robotmaaier-kleine-tuin (#16) geen status publish heeft.
1. Hub (#10), "Meer lezen": regel na de Eufy-regel: "Op zoek naar een robotmaaier voor een kleine tuin? Zie Robotmaaier kleine tuin."
2. Pagina 1 (#11), onder "De modellen een voor een": dezelfde zin na de Eufy-zin.
3. Navimow- (#264), Husqvarna- (#20), Gardena- (#21), Stihl- (#22), Worx- (#24), Mova/Dreame- (#351) en Eufy-pagina (#366),
   "Meer lezen", als laatste regel: "Robotmaaier voor een kleine tuin: twaalf modellen tot 600 m²."
4. Kleine-tuinpagina (#16), "Meer lezen" (na Robotmaaier kosten): de merkpagina's waarvan een model op de pagina staat, in
   de volgorde van de tabel: Segway Navimow, Mova of Dreame, Worx, Eufy, Stihl, Husqvarna (met dezelfde teksten als op de
   andere merkpagina's). Roborock heeft (nog) geen merkpagina.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde71_links.py [--schrijf]
          python3 scripts/ronde71_links.py --proef-concept   (alleen de ankers controleren terwijl #16 nog concept is)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
PID_NIEUW = 16
SLUG = 'robotmaaier-kleine-tuin'
KL = '/robotmaaier-kleine-tuin/'
EL = '<a href="/eufy-robotmaaier/">Eufy robotmaaier</a>'
EUFY_ZIN = f'Alle Eufy-robotmaaiers vergeleken: zie {EL}.'
ZIN = f'Op zoek naar een robotmaaier voor een kleine tuin? Zie <a href="{KL}">Robotmaaier kleine tuin</a>.'
KML = f'<li><a href="{KL}">Robotmaaier voor een kleine tuin</a>: twaalf modellen tot 600 m².</li></ul>'
EUFY_ML = f'<li>{EL}: de E15, E18 en C15 vergeleken.</li></ul>'
MOVA_ML = '<li><a href="/mova-dreame-robotmaaier/">Mova of Dreame robotmaaier</a>: de LiDAR-modellen vergeleken.</li></ul>'
KOSTEN_ML = '<li><a href="/robotmaaier-kosten/">Robotmaaier kosten</a>: wat het echt kost, met verborgen kosten.</li></ul>'
MERKEN = ('<li><a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>: alle modellen die nu nieuw te koop zijn.</li>'
          '<li><a href="/mova-dreame-robotmaaier/">Mova of Dreame robotmaaier</a>: de LiDAR-modellen vergeleken.</li>'
          '<li><a href="/worx-robotmaaier/">Worx robotmaaier</a>: de Landroid-modellen vergeleken.</li>'
          f'<li>{EL}: de E15, E18 en C15 vergeleken.</li>'
          '<li><a href="/stihl-robotmaaier/">Stihl robotmaaier</a>: de iMOW-modellen vergeleken.</li>'
          '<li><a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>: de Automower-modellen vergeleken.</li>')
MERK_LINKS = ['/segway-navimow-robotmaaier/', '/mova-dreame-robotmaaier/', '/worx-robotmaaier/', '/eufy-robotmaaier/',
              '/stihl-robotmaaier/', '/husqvarna-robotmaaier/']
STAPPEN = [
    (10, f'<li>{EUFY_ZIN}</li>', f'<li>{EUFY_ZIN}</li><li>{ZIN}</li>', 'hub, Meer lezen', KL),
    (11, f'<p>{EUFY_ZIN}</p>', f'<p>{EUFY_ZIN}</p>\n<p>{ZIN}</p>', 'pagina 1, De modellen een voor een', KL),
    (264, EUFY_ML, EUFY_ML[:-5] + KML, 'Navimow-pagina, Meer lezen', KL),
    (20, EUFY_ML, EUFY_ML[:-5] + KML, 'Husqvarna-pagina, Meer lezen', KL),
    (21, EUFY_ML, EUFY_ML[:-5] + KML, 'Gardena-pagina, Meer lezen', KL),
    (22, EUFY_ML, EUFY_ML[:-5] + KML, 'Stihl-pagina, Meer lezen', KL),
    (24, EUFY_ML, EUFY_ML[:-5] + KML, 'Worx-pagina, Meer lezen', KL),
    (351, EUFY_ML, EUFY_ML[:-5] + KML, 'Mova/Dreame-pagina, Meer lezen', KL),
    (366, MOVA_ML, MOVA_ML[:-5] + KML, 'Eufy-pagina, Meer lezen', KL),
    (PID_NIEUW, KOSTEN_ML, KOSTEN_ML[:-5] + MERKEN + '</ul>', 'Kleine-tuinpagina, Meer lezen', '/segway-navimow-robotmaaier/'),
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
# Kleine-tuinpagina: geen van de merklinks mag er al staan
for l in MERK_LINKS:
    if l in pag[PID_NIEUW]['content']['raw']:
        meld.append(f'#{PID_NIEUW} Kleine-tuinpagina: link naar {l} staat er al.')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde71-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
