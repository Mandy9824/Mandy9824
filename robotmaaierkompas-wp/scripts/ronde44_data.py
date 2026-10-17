#!/usr/bin/env python3
"""Ronde 44, sectie D en aanvulling 1: modelgegevens via de dataroute.
- M020, M022: verbinding "Wifi" (extra wifi); M021: "Bluetooth" (extra bluetooth), uit de omzetting van het Excel-bestand
  (excel_naar_json.py met scripts/verbinding_toewijzing.json).
- M010: alleen het minpunt "IPX5" weg.
Al het andere blijft gelijk; het script controleert dat alleen deze velden veranderen.
Gebruik:  python3 scripts/ronde44_data.py <omzetting.json> [--schrijf]
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
omz = {m['id']: m for m in json.load(open(next(a for a in sys.argv[1:] if not a.startswith('--')), encoding='utf-8'))['modellen']}
live = api('rmk/v1/modellen')['data']
nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    if m['id'] in ('M020', 'M021', 'M022'):
        m['verbinding'] = omz[m['id']]['verbinding']
        print(f'{m["id"]}: verbinding {m["verbinding"]["tekst"]} ({m["verbinding"]["extra"]})')
    if m['id'] == 'M010':
        if m['minpunten'].count('IPX5') != 1:
            sys.exit(f'M010: minpunt "IPX5" {m["minpunten"].count("IPX5")} keer gevonden. Niets gewijzigd.')
        m['minpunten'].remove('IPX5')
        print('M010: minpunt "IPX5" weg ->', m['minpunten'])
# alleen de bedoelde velden mogen verschillen
for a, b in zip(live['modellen'], nieuw['modellen']):
    vers = [k for k in set(a) | set(b) if a.get(k) != b.get(k)]
    toegestaan = {'M010': ['minpunten'], 'M020': ['verbinding'], 'M021': ['verbinding'], 'M022': ['verbinding']}.get(a['id'], [])
    if sorted(vers) != sorted(toegestaan):
        sys.exit(f'{a["id"]}: onverwachte verschillen {vers}. Niets gewijzigd.')
assert {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
print('Alleen de bedoelde velden veranderen.')
if not SCHRIJF:
    sys.exit(0)
print('Opgeslagen (LiteSpeed geleegd):', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('M010 minpunten live:', next(m for m in na['modellen'] if m['id'] == 'M010')['minpunten'])
print('Verbinding live:', {m['id']: (m['verbinding'] or {}).get('tekst') for m in na['modellen'] if m['id'] in ('M020', 'M021', 'M022')})
