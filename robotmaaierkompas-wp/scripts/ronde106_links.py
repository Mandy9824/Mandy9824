#!/usr/bin/env python3
"""Ronde 106, KLAARGEZET (niet gedraaid): links naar /robotmaaier-helling/ (#531).
Pas draaien als Mandy meldt dat de pagina gepubliceerd is. Weigert zolang #531 geen status publish heeft.
1. "Meer lezen", als laatste regel: Stihl #22, Husqvarna #20, Mova/Dreame #351, Navimow #264, grote tuin #15 en
   kleine tuin #16: "Is je tuin steil? Zie Robotmaaier voor hellingen: welke kan hoe steil?"
2. Pagina 1 /robotmaaier-zonder-draad/ (#11), onder "De modellen een voor een": dezelfde zin als eigen alinea direct
   na de regel naar de kopen-pagina (ronde 103), zoals de egel- en kopenregel daar ook staan.
Alle pagina's zijn gepubliceerd en deels met de hand gewijzigd: alleen gerichte vervangingen, nooit opnieuw bouwen.
Elk anker (en elk blok "Meer lezen") moet precies één keer voorkomen en er mag nog geen link naar de hellingpagina
staan; anders schrijft het script niets. Pagina's houden hun status. Met --schrijf: kopie in backups/, opslaan,
LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde106_links.py [--schrijf]
          python3 scripts/ronde106_links.py --proef-concept   (alleen de ankers controleren terwijl #531 concept is)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PROEF_CONCEPT = '--proef-concept' in sys.argv and not SCHRIJF
NIEUW_ID, NIEUW_SLUG = 531, 'robotmaaier-helling'
HL = f'/{NIEUW_SLUG}/'
H_ZIN = f'Is je tuin steil? Zie <a href="{HL}">Robotmaaier voor hellingen: welke kan hoe steil?</a>'
K_ZIN = 'Wat moet je weten voor je koopt? Zie <a href="/robotmaaier-kopen-waar-op-letten/">Robotmaaier kopen: waar let je op?</a>'
ML = re.compile(r'(Meer lezen</h2>\s*<ul>)(.*?)(</ul>)', re.S)
LAATSTE = [(22, 'Stihl-pagina'), (20, 'Husqvarna-pagina'), (351, 'Mova/Dreame-pagina'), (264, 'Navimow-pagina'),
           (15, 'grote tuin'), (16, 'kleine tuin')]

doel = api(f'wp/v2/pages?slug={NIEUW_SLUG}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['id'] != NIEUW_ID or (doel[0]['status'] != 'publish' and not PROEF_CONCEPT):
    sys.exit(f'{NIEUW_SLUG} is (nog) niet gepubliceerd: {doel}. Niets gewijzigd.')
ids = [p for p, _ in LAATSTE] + [11]
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid in ids:
    if pag[pid]['status'] != 'publish':
        meld.append(f'#{pid} {pag[pid]["slug"]}: status {pag[pid]["status"]}, verwacht publish.')
    if f'href="{HL}"' in raw[pid]:
        meld.append(f'#{pid} {pag[pid]["slug"]}: link naar de hellingpagina staat er al.')


def meer_lezen(pid, regel, wat):
    blokken = ML.findall(raw[pid])
    if len(blokken) != 1:
        meld.append(f'#{pid} {wat}: {len(blokken)} blokken "Meer lezen" (verwacht 1).')
        return
    raw[pid] = ML.sub(lambda m: m.group(1) + m.group(2) + f'<li>{regel}</li>' + m.group(3), raw[pid], count=1)
    print(f'  #{pid} {wat}: regel toegevoegd')


for pid, wat in LAATSTE:
    meer_lezen(pid, H_ZIN, f'{wat}, Meer lezen (laatste regel)')
n = raw[11].count(f'<p>{K_ZIN}</p>')
if n != 1:
    meld.append(f'#11 pagina 1: anker (kopenregel) {n} keer gevonden (verwacht 1).')
else:
    raw[11] = raw[11].replace(f'<p>{K_ZIN}</p>', f'<p>{K_ZIN}</p>\n<p>{H_ZIN}</p>')
    print('  #11 pagina 1, De modellen een voor een, na de kopenregel: regel toegevoegd')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde106-links-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
