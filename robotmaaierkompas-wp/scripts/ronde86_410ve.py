#!/usr/bin/env python3
"""Ronde 86: uitlopende Husqvarna Automower 410VE NERA (M010), gerichte toevoegingen via de API (MET DE HAND; niets bouwen).
1. Husqvarna-pagina (#20): onder de modellentabel ("De Husqvarna Automower-modellen naast elkaar"), na het bijschrift.
2. Pagina 1 (#11): zin over de i105E vervangen.
3. Hub (#10): "Waarom deze" van de Husqvarna-keuze aangevuld.
4. Grote-tuinpagina (#15): "Waarom deze" bij de 410VE NERA aangevuld; punt onder "Wat we nog niet weten".
Kopie van alle vier pagina's vooraf in backups/. Elke zoektekst moet precies één keer voorkomen; anders schrijft het
script niets. Pagina's houden hun status.
Gebruik:  python3 scripts/ronde86_410ve.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
UIT = ' Hij loopt uit: controleer de beschikbaarheid.'
BIJSCHRIFT_20 = ("<p>Oppervlak en helling volgens de handleidingen en productpagina's van Husqvarna NL. Het geluid is het geluidsvermogen "
                 '(LWA). Functiescore: wat deze maaier kan. Hoe we scoren: zie <a href="/hoe-we-beoordelen/#scoremodel">Hoe we beoordelen</a>.</p>')
ZIN_20 = ('<p>De Automower 410VE NERA loopt uit: Husqvarna NL toont hem alleen nog als ondersteuningspagina en een dealer had hem '
          'op 1 november nog op voorraad. Controleer de beschikbaarheid voor je kiest.</p>')
HUB_410 = ('Je hebt wel mobiele of wifidekking over het hele gazon nodig, en de prijs ligt boven de 3.000 euro.</p>')
GT_410 = '<p><strong>Waarom deze:</strong> tot 1.500 m² met camera en 4G ingebouwd. De prijs ligt boven de 3.000 euro.</p>'
GT_WWNW = 'maar zonder handleiding is er geen score.</li></ul>'
STAPPEN = [  # (pagina, zoek, vervang, omschrijving)
    (20, BIJSCHRIFT_20, BIJSCHRIFT_20 + '\n' + ZIN_20, 'Husqvarna-pagina: zin onder de modellentabel'),
    (11, 'De Navimow i105E loopt uit: controleer de beschikbaarheid voor je kiest.',
     'De Navimow i105E en de Husqvarna Automower 410VE NERA lopen uit: controleer de beschikbaarheid voor je kiest.', 'pagina 1: zin uitlopers'),
    (10, HUB_410, HUB_410[:-4] + UIT + '</p>', 'hub: Waarom deze (Husqvarna 410VE NERA)'),
    (15, GT_410, GT_410[:-4] + UIT + '</p>', 'grote tuin: Waarom deze (410VE NERA)'),
    (15, GT_WWNW, GT_WWNW[:-5] + '<li>De Husqvarna Automower 410VE NERA loopt uit.</li></ul>', 'grote tuin: Wat we nog niet weten'),
]
ids = [20, 11, 10, 15]
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde86-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {k: p[k] for k in ('id', 'status', 'slug', 'title', 'content', 'meta', 'modified')} for pid, p in pag.items()},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid, zoek, vervang, wat in STAPPEN:
    n = raw[pid].count(zoek)
    if n != 1:
        meld.append(f'#{pid} {wat}: {n} keer gevonden (verwacht 1).')
    else:
        raw[pid] = raw[pid].replace(zoek, vervang)
        print(f'  #{pid} {wat}: vervangen')
for pid, tekst in ((20, 'De Automower 410VE NERA loopt uit'), (11, 'lopen uit'), (15, '410VE NERA loopt uit')):
    if tekst in pag[pid]['content']['raw']:
        meld.append(f'#{pid}: "{tekst}" staat er al.')
if UIT.strip() in pag[10]['content']['raw']:
    meld.append('#10: "Hij loopt uit" staat er al.')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
