#!/usr/bin/env python3
"""Ronde 78: alleen de teksten van M058 (Ecovacs GOAT A3000 LiDAR Pro) in de live modelgegevens (dataroute /rmk/v1/modellen).

Velden: beste_voor, pluspunten, minpunten en analyse, uit modellen-teksten-ecovacs.json (toegevoegd aan
scripts/modellen_teksten.json en modellen_analyse.json), via de omzetting (excel_naar_json.py --uit <json>).
De omzetting moet voor M058 verder precies gelijk zijn aan live; alle andere modellen, alle andere velden van M058
en de algemene velden blijven ongewijzigd. Het script weigert anders. Wachtwoord alleen uit RMK_WP_APP_PASSWORD.
Opslaan via de dataroute leegt ook de LiteSpeed-cache.
Gebruik:  python3 scripts/ronde78_m058_teksten.py <omzetting.json> [--schrijf]
"""
import copy, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
ID, VELDEN = 'M058', ('beste_voor', 'pluspunten', 'minpunten', 'analyse')
D = os.path.dirname(os.path.abspath(__file__))
TEKSTEN = json.load(open(os.path.join(D, 'modellen_teksten.json'), encoding='utf-8'))[ID]
ANALYSE = json.load(open(os.path.join(D, 'modellen_analyse.json'), encoding='utf-8'))[ID]

live = api('rmk/v1/modellen')['data']
o = next(m for m in json.load(open(BRON, encoding='utf-8'))['modellen'] if m['id'] == ID)
L = next(m for m in live['modellen'] if m['id'] == ID)
assert (o['beste_voor'], o['pluspunten'], o['minpunten'], o['analyse']) == (
    TEKSTEN['beste_voor'], TEKSTEN['pluspunten'], TEKSTEN['minpunten'], ANALYSE['analyse']), 'teksten in de omzetting wijken af'
anders = sorted(k for k in set(o) | set(L) if o.get(k) != L.get(k) and k not in VELDEN)
if anders:
    sys.exit(f'{ID}: ook andere velden zouden veranderen ({", ".join(anders)}). Niets gewijzigd.')
if any(L.get(k) for k in VELDEN):
    sys.exit(f'{ID}: heeft live al teksten. Niets gewijzigd.')

nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    if m['id'] == ID:
        for k in VELDEN:
            m[k] = copy.deepcopy(o[k])
gelijk = all(a == b for a, b in zip(live['modellen'], nieuw['modellen']) if a['id'] != ID) and \
    len(live['modellen']) == len(nieuw['modellen']) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
print(f'{ID} {L["naam"]}: {", ".join(VELDEN)} leeg -> tekst; overige {len(live["modellen"]) - 1} modellen en algemene velden ongewijzigd: {gelijk}')
if not gelijk:
    sys.exit('Bestaande gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
pad = f'backups/modellen-voor-ronde78-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
