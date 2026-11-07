#!/usr/bin/env python3
"""Ronde 102, KLAARGEZET: alle links rond /robotmaaier-kopen-waar-op-letten/ (#508).
Pas draaien als Mandy meldt dat de pagina gepubliceerd is. Weigert zolang #508 geen status publish heeft.
1. Hub (#10), "Meer lezen", en pagina 1 (#11), onder "De modellen een voor een": een regel direct na de egelregel:
   "Wat moet je weten voor je koopt? Zie Robotmaaier kopen: waar let je op?" (tekst Mandy).
2. "Meer lezen", als laatste regel, met dezelfde zin: de zeven merkpagina's (Navimow #264, Husqvarna #20, Gardena #21,
   Stihl #22, Worx #24, Mova/Dreame #351, Eufy #366), kleine tuin #16, grote tuin #15, Husqvarna of Gardena #461,
   RTK #470, diefstal #489 en egels #490.
3. Kopen-pagina (#508), "Meer lezen" (na de laatste regel): alle pagina's uit de lijst interne links van de md die daar
   nog niet staan, met dezelfde teksten als op de andere pagina's.
Alle pagina's behalve #508 zijn gepubliceerd en deels met de hand gewijzigd: alleen gerichte vervangingen, nooit
opnieuw bouwen. Elk anker (en elk blok "Meer lezen") moet precies één keer voorkomen; anders schrijft het script niets.
Pagina's houden hun status. Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute
(modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde102_links.py [--schrijf]
          python3 scripts/ronde102_links.py --proef-concept   (alleen de ankers controleren terwijl #508 concept is)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
NIEUW_ID, NIEUW_SLUG = 508, 'robotmaaier-kopen-waar-op-letten'
KL = f'/{NIEUW_SLUG}/'
K_ZIN = f'Wat moet je weten voor je koopt? Zie <a href="{KL}">Robotmaaier kopen: waar let je op?</a>'
E_ZIN = '<a href="/robotmaaier-egels/">Robotmaaier en egels</a>: advies, regels en welke maaiers egels noemen.'
# Interne links uit de md (zelfde teksten als op de andere pagina's)
MD_LINKS = [
    ('/beste-robotmaaier/', '<a href="/beste-robotmaaier/">Beste robotmaaier</a>: onze selectie per situatie.'),
    ('/robotmaaier-zonder-draad/', '<a href="/robotmaaier-zonder-draad/">Robotmaaier zonder draad</a>: tien modellen vergeleken.'),
    ('/robotmaaier-zonder-grensdraad/', '<a href="/robotmaaier-zonder-grensdraad/">Robotmaaier zonder grensdraad</a>: hoe het werkt en wanneer je het kiest.'),
    ('/robotmaaier-kleine-tuin/', '<a href="/robotmaaier-kleine-tuin/">Robotmaaier voor een kleine tuin</a>: vijftien modellen tot 600 m².'),
    ('/robotmaaier-grote-tuin/', '<a href="/robotmaaier-grote-tuin/">Robotmaaier voor een grote tuin</a>: modellen van 1.000 tot 3.000 m².'),
    ('/robotmaaier-rtk-lidar-camera/', '<a href="/robotmaaier-rtk-lidar-camera/">RTK, LiDAR of camera</a>: hoe navigeert een robotmaaier zonder draad?'),
    ('/husqvarna-of-gardena-robotmaaier/', '<a href="/husqvarna-of-gardena-robotmaaier/">Husqvarna of Gardena robotmaaier</a>? De twee merken vergeleken.'),
    ('/robotmaaier-kosten/', '<a href="/robotmaaier-kosten/">Robotmaaier kosten</a>: wat het echt kost, met verborgen kosten.'),
    ('/robotmaaier-mesjes/', '<a href="/robotmaaier-mesjes/">Robotmaaier mesjes</a>: prijzen en vervangtermijnen.'),
    ('/segway-navimow-robotmaaier/', '<a href="/segway-navimow-robotmaaier/">Segway Navimow robotmaaier</a>: alle modellen die nu nieuw te koop zijn.'),
    ('/husqvarna-robotmaaier/', '<a href="/husqvarna-robotmaaier/">Husqvarna robotmaaier</a>: de Automower-modellen vergeleken.'),
    ('/gardena-robotmaaier/', '<a href="/gardena-robotmaaier/">Gardena robotmaaier</a>: de Sileno-modellen vergeleken.'),
    ('/stihl-robotmaaier/', '<a href="/stihl-robotmaaier/">Stihl robotmaaier</a>: de iMOW-modellen vergeleken.'),
    ('/worx-robotmaaier/', '<a href="/worx-robotmaaier/">Worx robotmaaier</a>: de Landroid-modellen vergeleken.'),
    ('/mova-dreame-robotmaaier/', '<a href="/mova-dreame-robotmaaier/">Mova of Dreame robotmaaier</a>: de LiDAR-modellen vergeleken.'),
    ('/eufy-robotmaaier/', '<a href="/eufy-robotmaaier/">Eufy robotmaaier</a>: de E15, E18 en C15 vergeleken.'),
    ('/hoe-we-beoordelen/', '<a href="/hoe-we-beoordelen/">Hoe we beoordelen</a>: scoremodel, bronnen en statussen.'),
]
ML = re.compile(r'(Meer lezen</h2>\s*<ul>)(.*?)(</ul>)', re.S)
LAATSTE = [(264, 'Navimow-pagina'), (20, 'Husqvarna-pagina'), (21, 'Gardena-pagina'), (22, 'Stihl-pagina'), (24, 'Worx-pagina'),
           (351, 'Mova/Dreame-pagina'), (366, 'Eufy-pagina'), (16, 'kleine tuin'), (15, 'grote tuin'),
           (461, 'Husqvarna of Gardena'), (470, 'RTK-pagina'), (489, 'diefstalpagina'), (490, 'egelpagina')]

doel = api(f'wp/v2/pages?slug={NIEUW_SLUG}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['id'] != NIEUW_ID or (doel[0]['status'] != 'publish' and not PROEF_CONCEPT):
    sys.exit(f'{NIEUW_SLUG} is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
ids = [10, 11] + [p for p, _ in LAATSTE] + [NIEUW_ID]
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid in ids:
    if pid != NIEUW_ID and pag[pid]['status'] != 'publish':
        meld.append(f'#{pid} {pag[pid]["slug"]}: status {pag[pid]["status"]}, verwacht publish.')
    if pid != NIEUW_ID and f'href="{KL}"' in raw[pid]:
        meld.append(f'#{pid} {pag[pid]["slug"]}: link naar de kopen-pagina staat er al.')


def na_anker(pid, was, wordt, wat):
    n = raw[pid].count(was)
    if n != 1:
        meld.append(f'#{pid} {wat}: anker {n} keer gevonden (verwacht 1).')
    else:
        raw[pid] = raw[pid].replace(was, wordt)
        print(f'  #{pid} {wat}: regel toegevoegd')


def meer_lezen(pid, regels, wat):
    blokken = ML.findall(raw[pid])
    if len(blokken) != 1:
        meld.append(f'#{pid} {wat}: {len(blokken)} blokken "Meer lezen" (verwacht 1).')
        return
    raw[pid] = ML.sub(lambda m: m.group(1) + m.group(2) + ''.join(f'<li>{r}</li>' for r in regels) + m.group(3), raw[pid], count=1)
    print(f'  #{pid} {wat}: {len(regels)} regel(s) onder Meer lezen')


na_anker(10, f'<li>{E_ZIN}</li>', f'<li>{E_ZIN}</li><li>{K_ZIN}</li>', 'hub, Meer lezen, na de egelregel')
if 'Meer lezen' in raw[10] and not re.search(r'Meer lezen</h2>\s*<ul>(?:(?!</ul>).)*' + re.escape(K_ZIN), raw[10], re.S) and not meld:
    meld.append('#10: de egelregel staat niet in het blok Meer lezen.')
na_anker(11, f'<p>{E_ZIN}</p>', f'<p>{E_ZIN}</p>\n<p>{K_ZIN}</p>', 'pagina 1, De modellen een voor een, na de egelregel')
for pid, wat in LAATSTE:
    meer_lezen(pid, [K_ZIN], f'{wat}, Meer lezen (laatste regel)')
blok = ML.search(raw[NIEUW_ID])
al = set(re.findall(r'href="([^"]+)"', blok.group(2))) if blok else set()
meer_lezen(NIEUW_ID, [t for u, t in MD_LINKS if u not in al], 'kopen-pagina, Meer lezen')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde102-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
