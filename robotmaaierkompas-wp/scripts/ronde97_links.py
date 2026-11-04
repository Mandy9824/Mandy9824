#!/usr/bin/env python3
"""Ronde 97, KLAARGEZET: alle links rond /robotmaaier-rtk-lidar-camera/. Pas draaien als Mandy meldt dat die pagina
gepubliceerd is. Weigert zolang robotmaaier-rtk-lidar-camera (#470) geen status publish heeft.
1. Pagina 1 (#11 /robotmaaier-zonder-draad/), direct na "Meer over RTK of begrenzingsdraad lees je op de pagina ...":
   "Hoe werkt zonder draad? Zie RTK, LiDAR of camera." (tekst Mandy; link op "RTK, LiDAR of camera").
2. Zonder-grensdraad-pagina (#17), direct na de lijst met de drie technieken (na de LiDAR-regel): dezelfde zin.
3. "Meer lezen", als laatste regel: alle merkpagina's (Navimow #264, Husqvarna #20, Gardena #21, Stihl #22, Worx #24,
   Mova/Dreame #351, Eufy #366), kleine tuin #16, grote tuin #15 en Husqvarna of Gardena #461:
   "RTK, LiDAR of camera: hoe navigeert een robotmaaier zonder draad?" (tekst Mandy; link op "RTK, LiDAR of camera").
4. Nieuwe pagina (#470), "Meer lezen" (na de Husqvarna-of-Gardena-regel): pagina 1, zonder grensdraad, de zeven
   merkpagina's, kleine en grote tuin, met dezelfde teksten als op de andere pagina's.
Alle pagina's behalve #470 zijn gepubliceerd en deels met de hand gewijzigd: alleen gerichte vervangingen, nooit opnieuw
bouwen. Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde97_links.py [--schrijf]
          python3 scripts/ronde97_links.py --proef-concept   (alleen de ankers controleren terwijl #470 nog concept is)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
PID_NIEUW = 470
SLUG = 'robotmaaier-rtk-lidar-camera'
RL = f'/{SLUG}/'
A = f'<a href="{RL}">RTK, LiDAR of camera</a>'
ZIN = f'<p>Hoe werkt zonder draad? Zie {A}.</p>'
ML = f'<li>{A}: hoe navigeert een robotmaaier zonder draad?</li></ul>'

P1_ANKER = '<p>Meer over RTK of begrenzingsdraad lees je op de pagina <a href="/robotmaaier-zonder-grensdraad/">robotmaaier zonder begrenzingsdraad</a>.</p>'
ZG_ANKER = ('<li><strong>LiDAR:</strong> een laser meet afstanden tot objecten, zodat de maaier een kaart maakt zonder satellieten. '
            'Dat vraagt geen antenne of correctiedata.</li></ul>')
L = {  # laatste regel van "Meer lezen" (met </ul>) zoals die op 4 november 2026 live stond
    'grote': '<li><a href="/robotmaaier-grote-tuin/">Robotmaaier voor een grote tuin</a>: modellen van 1.000 tot 3.000 m².</li></ul>',
    'kleine': '<li><a href="/robotmaaier-kleine-tuin/">Robotmaaier voor een kleine tuin</a>: vijftien modellen tot 600 m².</li></ul>',
    'hg': '<li><a href="/husqvarna-of-gardena-robotmaaier/">Husqvarna of Gardena robotmaaier</a>? De twee merken vergeleken.</li></ul>',
}
NIEUW_ML = ('<li><a href="/robotmaaier-zonder-draad/">Robotmaaier zonder draad</a>: tien modellen vergeleken.</li>'
            '<li><a href="/robotmaaier-zonder-grensdraad/">Robotmaaier zonder grensdraad</a>: hoe het werkt en wanneer je het kiest.</li>'
            '<li><a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>: alle modellen die nu nieuw te koop zijn.</li>'
            '<li><a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>: de Automower-modellen vergeleken.</li>'
            '<li><a href="/gardena-robotmaaier/">Gardena robotmaaier</a>: de Sileno-modellen vergeleken.</li>'
            '<li><a href="/stihl-robotmaaier/">Stihl robotmaaier</a>: de iMOW-modellen vergeleken.</li>'
            '<li><a href="/worx-robotmaaier/">Worx robotmaaier</a>: de Landroid-modellen vergeleken.</li>'
            '<li><a href="/mova-dreame-robotmaaier/">Mova of Dreame robotmaaier</a>: de LiDAR-modellen vergeleken.</li>'
            '<li><a href="/eufy-robotmaaier/">Eufy robotmaaier</a>: de E15, E18 en C15 vergeleken.</li>'
            '<li><a href="/robotmaaier-kleine-tuin/">Robotmaaier voor een kleine tuin</a>: vijftien modellen tot 600 m².</li>'
            '<li><a href="/robotmaaier-grote-tuin/">Robotmaaier voor een grote tuin</a>: modellen van 1.000 tot 3.000 m².</li>')
NIEUWE_LINKS = re.findall(r'href="([^"]+)"', NIEUW_ML)
STAPPEN = [  # (pagina, anker, vervanging, omschrijving, link die er nog niet mag staan)
    (11, P1_ANKER, P1_ANKER + '\n' + ZIN, 'pagina 1, na "Meer over RTK of begrenzingsdraad"', RL),
    (17, ZG_ANKER, ZG_ANKER + '\n' + ZIN, 'zonder grensdraad, na de drie technieken', RL),
    (264, L['grote'], L['grote'][:-5] + ML, 'Navimow-pagina, Meer lezen', RL),
    (20, L['hg'], L['hg'][:-5] + ML, 'Husqvarna-pagina, Meer lezen', RL),
    (21, L['hg'], L['hg'][:-5] + ML, 'Gardena-pagina, Meer lezen', RL),
    (22, L['grote'], L['grote'][:-5] + ML, 'Stihl-pagina, Meer lezen', RL),
    (24, L['grote'], L['grote'][:-5] + ML, 'Worx-pagina, Meer lezen', RL),
    (351, L['grote'], L['grote'][:-5] + ML, 'Mova/Dreame-pagina, Meer lezen', RL),
    (366, L['grote'], L['grote'][:-5] + ML, 'Eufy-pagina, Meer lezen', RL),
    (16, L['grote'], L['grote'][:-5] + ML, 'kleine-tuinpagina, Meer lezen', RL),
    (15, L['kleine'], L['kleine'][:-5] + ML, 'grote-tuinpagina, Meer lezen', RL),
    (461, L['grote'], L['grote'][:-5] + ML, 'Husqvarna-of-Gardena-pagina, Meer lezen', RL),
    (PID_NIEUW, L['hg'], L['hg'][:-5] + NIEUW_ML + '</ul>', 'nieuwe pagina, Meer lezen', None),
]

doel = api(f'wp/v2/pages?slug={SLUG}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['id'] != PID_NIEUW or (doel[0]['status'] != 'publish' and not PROEF_CONCEPT):
    sys.exit(f'{SLUG} is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
ids = sorted({s[0] for s in STAPPEN})
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid in ids:
    if pid != PID_NIEUW and pag[pid]['status'] != 'publish':
        meld.append(f'#{pid} {pag[pid]["slug"]}: status {pag[pid]["status"]}, verwacht publish.')
for pid, was, wordt, wat, link in STAPPEN:
    # "Meer lezen"-ankers moeten binnen het blok Meer lezen staan
    if link and raw[pid].count(link):
        meld.append(f'#{pid} {wat}: link staat er al.')
    elif raw[pid].count(was) != 1:
        meld.append(f'#{pid} {wat}: anker {raw[pid].count(was)} keer gevonden (verwacht 1).')
    elif 'Meer lezen' in wat and not re.search(r'Meer lezen</h2>\s*<ul>(?:(?!</ul>).)*' + re.escape(was), raw[pid], re.S):
        meld.append(f'#{pid} {wat}: anker staat niet in het blok Meer lezen.')
    else:
        raw[pid] = raw[pid].replace(was, wordt, 1)
        print(f'  #{pid} {wat}: regel toegevoegd')
# Nieuwe pagina: in "Meer lezen" mag nog geen van de nieuwe links staan
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
pad = f'backups/ronde97-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
