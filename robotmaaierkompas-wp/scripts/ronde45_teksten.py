#!/usr/bin/env python3
"""Ronde 45, zonder thema-zip.
(a) Navimow-pagina (#264), "Meer lezen": "acht modellen vergeleken" -> "tien modellen vergeleken".
(b) Mesjespagina (#236): de zin over andere Husqvarna-modellen noemt ook de 310E NERA.
Elke "Was"-tekst moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
STAPPEN = [
    (264, 'a', 'Robotmaaier zonder draad</a>: acht modellen vergeleken.', 'Robotmaaier zonder draad</a>: tien modellen vergeleken.'),
    (236, 'b', 'Voor andere Husqvarna-modellen dan de 410VE NERA en de 305E NERA hebben we de mesjes nog niet uitgezocht.',
     'Voor andere Husqvarna-modellen dan de 410VE NERA, 305E NERA en 310E NERA hebben we de mesjes nog niet uitgezocht.'),
]
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in (236, 264)}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid, wat, was, wordt in STAPPEN:
    n = raw[pid].count(was)
    if n != 1:
        meld.append(f'#{pid} {wat}: "Was" {n} keer gevonden (verwacht 1).')
        continue
    raw[pid] = raw[pid].replace(was, wordt, 1)
    print(f'  #{pid} {wat}: toegepast')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde45-teksten-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in (236, 264):
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
