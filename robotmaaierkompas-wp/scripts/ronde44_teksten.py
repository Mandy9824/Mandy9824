#!/usr/bin/env python3
"""Ronde 44 (tekstwijzigingen-husqvarna-ronde.md, secties A, B, C1-C4, en de aanvulling op de Husqvarna-pagina).
A  hub (#10): FAQ-zin over modellen met begrenzingsdraad.
B  mesjespagina (#236): alinea 305E -> 305E en 310E NERA.
C1 kosten (#18): metabeschrijving.  C2: korte antwoord ("acht" weg).  C3: drie rijen vóór Gardena in "Verbinding en
   antidiefstal".  C4: punt na de 410VE NERA onder "Antenne, gateway of dekking".
Husqvarna-concept (#20): "de opvolger in ons overzicht" -> "het meest vergelijkbare model met draad in ons overzicht".
C5 (link op de kostenpagina) pas na publicatie van de Husqvarna-pagina: zie scripts/ronde44_links.py.
Elke "Was"-tekst moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
GARDENA = '<tr><th scope="row">Gardena Smart Sileno Free 800</th><td>Geen 4G en geen abonnement, en ook geen GPS-tracking</td></tr>'
LI_410 = ('<li>Husqvarna Automower 410VE NERA: je hebt mobiele of wifidekking over het hele gazon nodig. Anders heb je een '
          'referentiestation nodig (adviesprijs 309 euro).</li>')
STAPPEN = [
    (10, 'A', 'Modellen met begrenzingsdraad, zoals de Husqvarna Automower 105 en 305 en de Gardena Sileno Minimo, voegen we toe.',
     'Modellen met begrenzingsdraad, zoals de Husqvarna Automower 305 (zie de pagina Husqvarna robotmaaier) en de Gardena Sileno Minimo, voegen we toe.'),
    (236, 'B', 'Voor de Automower 305E NERA noemt Husqvarna Endurance-messen (26,99 euro)',
     'Voor de Automower 305E en 310E NERA noemt Husqvarna Endurance-messen (26,99 euro)'),
    (18, 'C2', 'Bij de acht modellen die wij hebben uitgezocht', 'Bij de modellen die wij hebben uitgezocht'),
    (18, 'C3', GARDENA,
     '<tr><th scope="row">Navimow i205 AWD, i210 LiDAR Pro, i220 LiDAR Pro en X420</th><td>4G ingebouwd met een jaar gratis data, daarna 29,99 euro per jaar volgens Navimow</td></tr>'
     '<tr><th scope="row">Husqvarna Automower 305E en 310E NERA</th><td>Geen abonnement; wifi-dekking over het hele gazon nodig, anders een Connect Kit (209 euro, alleen via een dealer) of een referentiestation (309 euro)</td></tr>'
     '<tr><th scope="row">Husqvarna Automower 305 (met draad)</th><td>Alleen Bluetooth; GPS, alarm en GeoFence vragen een Connect Kit van 329 euro (alleen via een dealer); de draadset kost 94,99 tot 239 euro</td></tr>'
     + GARDENA),
    (18, 'C4', LI_410, LI_410 + '<li>Husqvarna Automower 305E en 310E NERA: wifi-dekking over het hele gazon nodig; zonder wifi een Connect Kit of een referentiestation.</li>'),
    (20, 'Husqvarna 105', 'dan is de 305 met draad de opvolger in ons overzicht', 'dan is de 305 met draad het meest vergelijkbare model met draad in ons overzicht'),
]
META = (18, 'De prijs van de maaier is maar een deel. Wat kosten verbinding, antidiefstal en messen? Acht modellen, met bron en datum.',
        'De prijs van de maaier is maar een deel. Wat kosten verbinding, antidiefstal en messen? Meer dan tien modellen, met bron en datum.')

pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in (10, 18, 20, 236)}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid, wat, was, wordt in STAPPEN:
    n = raw[pid].count(was)
    if n != 1:
        meld.append(f'#{pid} {wat}: "Was" {n} keer gevonden (verwacht 1).')
        continue
    raw[pid] = raw[pid].replace(was, wordt, 1)
    print(f'  #{pid} {wat}: toegepast')
meta_ok = pag[18]['meta'].get('_yoast_wpseo_metadesc') == META[1]
print('  #18 C1 metabeschrijving:', 'toegepast' if meta_ok else 'NIET gevonden')
if not meta_ok:
    meld.append('#18 C1: metabeschrijving is niet de "Was"-tekst.')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde44-teksten-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw'], 'meta': p.get('meta')} for pid, p in pag.items()},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in (10, 18, 20, 236):
    body = {'content': raw[pid]}
    if pid == 18:
        body['meta'] = {'_yoast_wpseo_metadesc': META[2]}
    api(f'wp/v2/pages/{pid}', body)
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}'
          + (f'; meta {q["meta"].get("_yoast_wpseo_metadesc")!r}' if pid == 18 else ''))
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
