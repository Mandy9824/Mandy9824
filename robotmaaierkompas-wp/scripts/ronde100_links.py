#!/usr/bin/env python3
"""Ronde 100, KLAARGEZET: alle links rond /robotmaaier-diefstal-verzekering/ (#489) en /robotmaaier-egels/ (#490).
Pas draaien als Mandy meldt dat beide pagina's gepubliceerd zijn. Weigert zolang een van de twee geen status publish heeft.
1. Hub (#10), "Meer lezen", en pagina 1 (#11), onder "De modellen een voor een": twee regels direct na de Eufy-regel:
   "Robotmaaier gestolen? Zie Diefstalbeveiliging, GPS en verzekering." en
   "Robotmaaier en egels: advies, regels en welke maaiers egels noemen." (teksten Mandy).
   De kopen-pagina (/robotmaaier-kopen-waar-op-letten/) bestaat niet (4 november 2026): daar niets (zie bouwlogboek).
2. "Meer lezen", als laatste regel, op de zeven merkpagina's (Navimow #264, Husqvarna #20, Gardena #21, Stihl #22,
   Worx #24, Mova/Dreame #351, Eufy #366) en de RTK-pagina (#470): de diefstalzin.
3. Diefstalpagina (#489) en egelpagina (#490), "Meer lezen" (na de laatste regel): de andere nieuwe pagina, de RTK-pagina
   en de zeven merkpagina's uit de md, met dezelfde teksten als op de andere pagina's. Geen link naar de kopen-pagina.
Alle pagina's behalve #489/#490 zijn gepubliceerd en deels met de hand gewijzigd: alleen gerichte vervangingen, nooit
opnieuw bouwen. Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde100_links.py [--schrijf]
          python3 scripts/ronde100_links.py --proef-concept   (alleen de ankers controleren terwijl #489/#490 concept zijn)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
NIEUW = {489: 'robotmaaier-diefstal-verzekering', 490: 'robotmaaier-egels'}
DL, EGL = '/robotmaaier-diefstal-verzekering/', '/robotmaaier-egels/'
D_ZIN = f'Robotmaaier gestolen? Zie <a href="{DL}">Diefstalbeveiliging, GPS en verzekering</a>.'
E_ZIN = f'<a href="{EGL}">Robotmaaier en egels</a>: advies, regels en welke maaiers egels noemen.'
EUFY = 'Alle Eufy-robotmaaiers vergeleken: zie <a href="/eufy-robotmaaier/">Eufy robotmaaier</a>.'
RTK_ML = '<li><a href="/robotmaaier-rtk-lidar-camera/">RTK, LiDAR of camera</a>: hoe navigeert een robotmaaier zonder draad?</li></ul>'
GROOT_ML = '<li><a href="/robotmaaier-grote-tuin/">Robotmaaier voor een grote tuin</a>: modellen van 1.000 tot 3.000 m².</li></ul>'
KOSTEN_ML = '<li><a href="/robotmaaier-kosten/">Robotmaaier kosten</a>: wat het echt kost, met verborgen kosten.</li></ul>'
ZD_ML = '<li><a href="/robotmaaier-zonder-draad/">Robotmaaier zonder draad</a>: tien modellen vergeleken.</li></ul>'
MERKEN_ML = ('<li><a href="/robotmaaier-rtk-lidar-camera/">RTK, LiDAR of camera</a>: hoe navigeert een robotmaaier zonder draad?</li>'
             '<li><a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>: alle modellen die nu nieuw te koop zijn.</li>'
             '<li><a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>: de Automower-modellen vergeleken.</li>'
             '<li><a href="/gardena-robotmaaier/">Gardena robotmaaier</a>: de Sileno-modellen vergeleken.</li>'
             '<li><a href="/stihl-robotmaaier/">Stihl robotmaaier</a>: de iMOW-modellen vergeleken.</li>'
             '<li><a href="/worx-robotmaaier/">Worx robotmaaier</a>: de Landroid-modellen vergeleken.</li>'
             '<li><a href="/mova-dreame-robotmaaier/">Mova of Dreame robotmaaier</a>: de LiDAR-modellen vergeleken.</li>'
             '<li><a href="/eufy-robotmaaier/">Eufy robotmaaier</a>: de E15, E18 en C15 vergeleken.</li></ul>')
MERK_LINKS = tuple(re.findall(r'href="([^"]+)"', MERKEN_ML))
STAPPEN = [  # (pagina, anker, vervanging, omschrijving, links die er nog niet mogen staan)
    (10, f'<li>{EUFY}</li>', f'<li>{EUFY}</li><li>{D_ZIN}</li><li>{E_ZIN}</li>', 'hub, Meer lezen, na Eufy', (DL, EGL)),
    (11, f'<p>{EUFY}</p>', f'<p>{EUFY}</p>\n<p>{D_ZIN}</p>\n<p>{E_ZIN}</p>', 'pagina 1, De modellen een voor een, na Eufy', (DL, EGL)),
] + [(pid, RTK_ML, RTK_ML[:-5] + f'<li>{D_ZIN}</li></ul>', f'{wat}, Meer lezen', (DL,)) for pid, wat in (
    (264, 'Navimow-pagina'), (20, 'Husqvarna-pagina'), (21, 'Gardena-pagina'), (22, 'Stihl-pagina'), (24, 'Worx-pagina'),
    (351, 'Mova/Dreame-pagina'), (366, 'Eufy-pagina'))] + [
    (470, GROOT_ML, GROOT_ML[:-5] + f'<li>{D_ZIN}</li></ul>', 'RTK-pagina, Meer lezen', (DL,)),
    (489, KOSTEN_ML, KOSTEN_ML[:-5] + f'<li>{E_ZIN}</li>' + MERKEN_ML, 'diefstalpagina, Meer lezen', (EGL,) + MERK_LINKS),
    (490, ZD_ML, ZD_ML[:-5] + f'<li>{D_ZIN}</li>' + MERKEN_ML, 'egelpagina, Meer lezen', (DL,) + MERK_LINKS),
]

for pid, slug in NIEUW.items():
    doel = api(f'wp/v2/pages?slug={slug}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
    if len(doel) != 1 or doel[0]['id'] != pid or (doel[0]['status'] != 'publish' and not PROEF_CONCEPT):
        sys.exit(f'{slug} is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
ids = sorted({s[0] for s in STAPPEN})
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid in ids:
    if pid not in NIEUW and pag[pid]['status'] != 'publish':
        meld.append(f'#{pid} {pag[pid]["slug"]}: status {pag[pid]["status"]}, verwacht publish.')
for pid, was, wordt, wat, links in STAPPEN:
    ml = re.search(r'Meer lezen</h2>\s*<ul>.*?</ul>', raw[pid], re.S)
    al = [l for l in links if (ml.group(0) if pid in NIEUW and ml else raw[pid]).count(f'href="{l}"')]
    if al:
        meld.append(f'#{pid} {wat}: link staat er al: {al}.')
    elif raw[pid].count(was) != 1:
        meld.append(f'#{pid} {wat}: anker {raw[pid].count(was)} keer gevonden (verwacht 1).')
    elif 'Meer lezen' in wat and not re.search(r'Meer lezen</h2>\s*<ul>(?:(?!</ul>).)*' + re.escape(was), raw[pid], re.S):
        meld.append(f'#{pid} {wat}: anker staat niet in het blok Meer lezen.')
    else:
        raw[pid] = raw[pid].replace(was, wordt, 1)
        print(f'  #{pid} {wat}: regel(s) toegevoegd')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde100-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
