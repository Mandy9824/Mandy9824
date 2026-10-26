#!/usr/bin/env python3
"""Ronde 62: Husqvarna-pagina (#20, gepubliceerd): sectie over GPS en drie extra veelgestelde vragen.
1. Nieuwe sectie (H2 "Husqvarna robotmaaier met GPS: welke Automower heeft het?") direct vóór "Waar op te letten".
2. Drie vragen achteraan in de veelgestelde vragen.
3. Inhoudsopgave: de pagina heeft er geen (gecontroleerd), dus niets toe te voegen.
Elk anker moet precies één keer voorkomen en de nieuwe kop mag er nog niet staan; anders schrijft het script niets.
De pagina houdt haar status. Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute.
Gebruik:  python3 scripts/ronde62_husqvarna.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PID = 20
KOP = 'Husqvarna robotmaaier met GPS: welke Automower heeft het?'
ALINEA = ("Alleen de Automower 410VE NERA heeft GPS-tracking en een geofence-melding standaard, dankzij de ingebouwde 4G. "
          "De 305E en 310E NERA hebben volgens Husqvarna's productpagina geen GPS-volgsysteem; hun GeoFence geeft wel een "
          "sirene en een melding in de app, maar alleen binnen wifi-bereik. De 305 met draad heeft standaard geen GPS en geen "
          "GeoFence; met de losse Connect Kit (329 euro, door een dealer in te bouwen) komen GPS-positie, alarm in de app en "
          "GeoFence erbij.")
VRAGEN = [
    ('Welke Husqvarna Automower heeft GPS?',
     'De Automower 410VE NERA heeft GPS-tracking standaard. Bij de 305E en 310E NERA is er geen GPS-volgsysteem; '
     'de 305 met draad krijgt GPS pas met de Connect Kit (329 euro).'),
    ('Is er een Husqvarna robotmaaier zonder draad?',
     'Ja: de modellen met NERA in de naam (305E, 310E en 410VE) werken zonder begrenzingsdraad, met EPOS. '
     'De Automower 305 werkt met draad.'),
    ('Waar kan ik een Husqvarna Automower kopen?',
     'Husqvarna verkoopt de Automower via onafhankelijke dealers; sommige modellen, zoals de 305E en 310E NERA, ook via '
     'de webshop van Husqvarna NL. Dealers bepalen hun eigen prijzen en voorraad, dus controleer de beschikbaarheid.'),
]
WAAR = ('<!-- wp:html -->\n<section class="rmk-container rmk-section--tight rmk-column"><div class="rmk-prose">\n'
        '<h2 id="waar-op-te-letten">Waar op te letten</h2>')
SECTIE = ('<!-- wp:html -->\n<section class="rmk-container rmk-section--tight rmk-column"><div class="rmk-prose">\n'
          f'<h2 id="husqvarna-robotmaaier-met-gps-welke-automower-heeft-het">{KOP}</h2>\n<p>{ALINEA}</p>\n'
          '</div></section>\n<!-- /wp:html -->\n\n')
FAQ_SLOT = ('<details><summary>Is de Automower 105 nog te koop?</summary><div><p>Bij Husqvarna NL staat hij als niet meer leverbaar.</p></div></details>\n'
            '</div>')
NIEUWE_VRAGEN = ''.join(f'\n  <details><summary>{v}</summary><div><p>{a}</p></div></details>' for v, a in VRAGEN)
STAPPEN = [
    (WAAR, SECTIE + WAAR, 'sectie GPS vóór "Waar op te letten"'),
    (FAQ_SLOT, FAQ_SLOT[:-len('\n</div>')] + NIEUWE_VRAGEN + '\n</div>', 'drie vragen achteraan in de FAQ'),
]

p = api(f'wp/v2/pages/{PID}?context=edit')
raw = oud = p['content']['raw']
meld = []
if KOP in raw or any(v in raw for v, _ in VRAGEN):
    meld.append('De nieuwe kop of een van de nieuwe vragen staat er al.')
for was, wordt, wat in STAPPEN:
    n = raw.count(was)
    if n != 1:
        meld.append(f'{wat}: anker {n} keer gevonden (verwacht 1).')
    else:
        raw = raw.replace(was, wordt, 1)
        print(f'  {wat}: toegevoegd')
for t in ('In deze gids', 'rmk-toc', 'Inhoudsopgave'):
    if t in oud:
        meld.append(f'Er lijkt toch een inhoudsopgave te zijn ("{t}"); niet bijgewerkt.')
print(f'#{PID} status {p["status"]}')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde62-husqvarna-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({'id': PID, 'status': p['status'], 'content': oud}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api(f'wp/v2/pages/{PID}', {'content': raw})
q = api(f'wp/v2/pages/{PID}?context=edit')
print(f'#{PID} opgeslagen; status {q["status"]} (was {p["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
