#!/usr/bin/env python3
"""Ronde 63: Husqvarna-pagina (#20, gepubliceerd): de sectie "Husqvarna robotmaaier met GPS: welke Automower heeft het?"
(ronde 62) verplaatsen naar direct vóór de kop "Veelgestelde vragen". Verder niets.
Het sectieblok en de FAQ-kop moeten elk precies één keer voorkomen; anders schrijft het script niets. Na de verplaatsing
controleert het dat de inhoud alleen in volgorde verschilt (zelfde tekens, zelfde blokken).
De pagina houdt haar status. Met --schrijf: eerst een kopie in backups/, dan opslaan, LiteSpeed legen via de dataroute.
Gebruik:  python3 scripts/ronde63_husqvarna.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PID = 20
# Begin van het blok dat scripts/ronde62_husqvarna.py plaatste; het blok loopt tot en met de eerstvolgende
# "<!-- /wp:html -->" en de witregel erna
KOP = 'Husqvarna robotmaaier met GPS: welke Automower heeft het?'
BEGIN = ('<!-- wp:html -->\n<section class="rmk-container rmk-section--tight rmk-column"><div class="rmk-prose">\n'
          f'<h2 id="husqvarna-robotmaaier-met-gps-welke-automower-heeft-het">{KOP}</h2>\n<p>')
FAQ_KOP = ('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h2 style="font-size: var(--rmk-fs-xl)">Veelgestelde vragen</h2></div>\n'
           '<!-- /wp:html -->\n\n')

p = api(f'wp/v2/pages/{PID}?context=edit')
raw = oud = p['content']['raw']
meld = []
SECTIE = ''
if raw.count(BEGIN) == 1:
    i = raw.index(BEGIN)
    SECTIE = raw[i:raw.index('<!-- /wp:html -->\n\n', i) + len('<!-- /wp:html -->\n\n')]
    assert SECTIE.count('<h2') == 1 and SECTIE.count('<!-- wp:html -->') == 1, 'sectieblok onverwacht'
for wat, s in (('sectie GPS', SECTIE), ('kop Veelgestelde vragen', FAQ_KOP)):
    if raw.count(s) != 1:
        meld.append(f'{wat}: {raw.count(s)} keer gevonden (verwacht 1).')
if not meld:
    if raw.index(SECTIE) < raw.index(FAQ_KOP):
        meld.append('De sectie staat al vóór de veelgestelde vragen.')
    else:
        raw = raw.replace(SECTIE, '', 1)
        raw = raw.replace(FAQ_KOP, SECTIE + FAQ_KOP, 1)
        assert sorted(oud) == sorted(raw) and len(oud) == len(raw)
        assert raw.index(SECTIE) + len(SECTIE) == raw.index(FAQ_KOP)
        print('  sectie GPS: verplaatst naar direct vóór "Veelgestelde vragen"')
print(f'#{PID} status {p["status"]}')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde63-husqvarna-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({'id': PID, 'status': p['status'], 'content': oud}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api(f'wp/v2/pages/{PID}', {'content': raw})
q = api(f'wp/v2/pages/{PID}?context=edit')
print(f'#{PID} opgeslagen; status {q["status"]} (was {p["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
