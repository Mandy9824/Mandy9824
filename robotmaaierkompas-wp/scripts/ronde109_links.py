#!/usr/bin/env python3
"""Ronde 109, KLAARGEZET (niet gedraaid): links naar /robotmaaier-gps/ (#559).
Pas draaien als Mandy meldt dat de pagina gepubliceerd is. Weigert zolang #559 geen status publish heeft.
1. "Meer lezen", als laatste regel: RTK #470, diefstal #489, Husqvarna #20, Navimow #264, Gardena #21, Worx #24 en
   Mova/Dreame #351: "Wil je weten welke maaier GPS heeft? Zie Robotmaaier met GPS: welke modellen hebben het echt?"
2. Pagina 1 /robotmaaier-zonder-draad/ (#11) heeft geen blok "Meer lezen". Daar komt dezelfde zin als eigen alinea
   onder "De modellen een voor een", direct na de hellingregel (ronde 106), tussen de andere leesverwijzingen.
Alle pagina's zijn gepubliceerd en deels met de hand gewijzigd (#470, #489): alleen gerichte vervangingen, nooit
opnieuw bouwen. Elk anker (en elk blok "Meer lezen") moet precies één keer voorkomen en er mag nog geen link naar de
GPS-pagina staan; anders schrijft het script niets. Pagina's houden hun status. Met --schrijf: kopie in backups/,
opslaan, controle, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde109_links.py [--schrijf]
          python3 scripts/ronde109_links.py --proef-concept   (alleen de ankers controleren terwijl #559 concept is)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
NIEUW_ID, NIEUW_SLUG = 559, 'robotmaaier-gps'
GL = f'/{NIEUW_SLUG}/'
G_ZIN = f'Wil je weten welke maaier GPS heeft? Zie <a href="{GL}">Robotmaaier met GPS: welke modellen hebben het echt?</a>'
H_ZIN = 'Is je tuin steil? Zie <a href="/robotmaaier-helling/">Robotmaaier voor hellingen: welke kan hoe steil?</a>'
ML = re.compile(r'(Meer lezen</h2>\s*<ul>)(.*?)(</ul>)', re.S)
LAATSTE = [(470, 'RTK-pagina'), (489, 'diefstalpagina'), (20, 'Husqvarna-pagina'), (264, 'Navimow-pagina'),
           (21, 'Gardena-pagina'), (24, 'Worx-pagina'), (351, 'Mova/Dreame-pagina')]

doel = api(f'wp/v2/pages?slug={NIEUW_SLUG}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['id'] != NIEUW_ID:
    sys.exit(f'{NIEUW_SLUG}: verwacht precies pagina #{NIEUW_ID}, gevonden {doel}. Niets gewijzigd.')
if doel[0]['status'] != 'publish' and not PROEF_CONCEPT:
    sys.exit(f'{NIEUW_SLUG} (#{NIEUW_ID}) heeft status {doel[0]["status"]}, is (nog) niet gepubliceerd. Niets gewijzigd.')
ids = [p for p, _ in LAATSTE] + [11]
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid in ids:
    if pag[pid]['status'] != 'publish':
        meld.append(f'#{pid} {pag[pid]["slug"]}: status {pag[pid]["status"]}, verwacht publish.')
    if f'href="{GL}' in raw[pid] or 'robotmaaierkompas.nl' + GL in raw[pid]:
        meld.append(f'#{pid} {pag[pid]["slug"]}: link naar de GPS-pagina staat er al.')


def meer_lezen(pid, regel, wat):
    blokken = ML.findall(raw[pid])
    if len(blokken) != 1:
        meld.append(f'#{pid} {wat}: {len(blokken)} blokken "Meer lezen" (verwacht 1).')
        return
    raw[pid] = ML.sub(lambda m: m.group(1) + m.group(2) + f'<li>{regel}</li>' + m.group(3), raw[pid], count=1)
    print(f'  #{pid} {wat}: regel toegevoegd')


for pid, wat in LAATSTE:
    meer_lezen(pid, G_ZIN, f'{wat}, Meer lezen (laatste regel)')
n = raw[11].count(f'<p>{H_ZIN}</p>')
if ML.search(raw[11]):
    meld.append('#11 pagina 1: heeft nu wel een blok "Meer lezen"; script nakijken.')
if n != 1:
    meld.append(f'#11 pagina 1: anker (hellingregel) {n} keer gevonden (verwacht 1).')
else:
    raw[11] = raw[11].replace(f'<p>{H_ZIN}</p>', f'<p>{H_ZIN}</p>\n<p>{G_ZIN}</p>')
    print('  #11 pagina 1, De modellen een voor een, na de hellingregel: regel toegevoegd')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(1 if meld else 0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde109-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'modified': p['modified'], 'content': p['content']['raw']} for pid, p in pag.items()},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
ok = True
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    goed = q['content']['raw'] == raw[pid] and q['status'] == pag[pid]['status'] and q['content']['raw'].count(f'href="{GL}"') == 1
    ok &= goed
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld en 1 link: {goed}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
sys.exit(0 if ok else 1)
