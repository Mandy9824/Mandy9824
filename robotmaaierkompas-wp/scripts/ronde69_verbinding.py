#!/usr/bin/env python3
"""Ronde 69: alleen het veld "verbinding" (chip Verbinding op de kaarten) van M059, M060 (4G) en M063, M064 (module).

Waarden uit de omzetting (excel_naar_json.py --uit <json>, met scripts/verbinding_toewijzing.json). Alle andere velden en
modellen en de algemene velden blijven ongewijzigd; het script weigert anders. Wachtwoord alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde69_verbinding.py <omzetting.json> [--schrijf]
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
DOEL = {'M059': 'ingebouwd', 'M060': 'ingebouwd', 'M063': 'module', 'M064': 'module'}
live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    if m['id'] in DOEL:
        v = omz[m['id']].get('verbinding')
        assert v and v['extra'] == DOEL[m['id']] and v['bron'].startswith('https://'), f'{m["id"]}: verbinding {v}'
        assert m.get('verbinding') is None, f'{m["id"]}: had al een verbinding'
        m['verbinding'] = v
        print(f'{m["id"]} {m["naam"]}: verbinding {v["extra"]} ("{v["tekst"]}", {v["status"]}, {v["datum"]})')
# alleen die vier velden anders
for a, b in zip(live['modellen'], nieuw['modellen']):
    d = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    assert d == (['verbinding'] if a['id'] in DOEL else []), f'{a["id"]}: {d}'
assert {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
print(f'Alleen verbinding van {sorted(DOEL)} anders; {len(nieuw["modellen"])} modellen')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
json.dump(live, open('backups/modellen-voor-ronde69.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Opgeslagen (LiteSpeed geleegd):', api('rmk/v1/modellen', nieuw))
print('Live na upload gelijk aan bedoeld:', api('rmk/v1/modellen')['data'] == nieuw)
