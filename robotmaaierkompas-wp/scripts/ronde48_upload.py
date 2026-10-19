#!/usr/bin/env python3
"""Ronde 48: Gardena-modellen M023, M024 en M025 in de live modelgegevens (dataroute /rmk/v1/modellen).

- De 21 live modellen en de algemene velden (gegenereerd, algemeen, ...) blijven ONGEWIJZIGD (ook M011 met zijn
  teksten en Bol-blok).
- M023 (Sileno Minimo 250), M024 (Minimo 500) en M025 (City 250) komen uit de omzetting van het Excel-bestand
  (excel_naar_json.py --uit <json>), met de fabrikantpagina-URL en de teksten uit modellen-teksten-gardena.json
  (via scripts/modellen_teksten.json en modellen_analyse.json). Geen EAN, geen Bol, geen prijs.
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde48_upload.py <omzetting.json>            (proefdraai)
          python3 scripts/ronde48_upload.py <omzetting.json> --schrijf
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
NIEUW = ('M023', 'M024', 'M025')
TEKSTEN = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modellen_teksten.json'), encoding='utf-8'))
ANALYSE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modellen_analyse.json'), encoding='utf-8'))

live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
ids = [m['id'] for m in live['modellen']]
if any(i in ids for i in NIEUW):
    sys.exit(f'Er staan al Gardena-modellen live: {[i for i in ids if i in NIEUW]}. Niets gewijzigd.')
for i in NIEUW:
    m = omz[i]
    assert m.get('fabrikant_url', '').startswith('https://www.gardena.com/nl/'), i
    assert m.get('beste_voor') == TEKSTEN[i]['beste_voor'] and m.get('pluspunten') == TEKSTEN[i]['pluspunten'] \
        and m.get('minpunten') == TEKSTEN[i]['minpunten'] and m.get('analyse') == ANALYSE[i]['analyse'], f'{i}: teksten wijken af'
    assert not m.get('ean') and not m.get('bol') and not m.get('prijs'), f'{i}: onverwacht Bol- of prijsgegeven'
    assert m.get('beschikbaarheid') == 'uitlopend', i

nieuw = copy.deepcopy(live)
nieuw['modellen'] = live['modellen'] + [omz[i] for i in NIEUW]
for i in NIEUW:
    m = omz[i]
    print(f'{i} {m["naam"]}: beschikbaarheid {m["beschikbaarheid"]}, scores {m["scores"]}, fabrikant {m["fabrikant_url"]}')
gelijk = all(a == b for a, b in zip(live['modellen'], nieuw['modellen'])) and {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
print(f'{len(live["modellen"])} live modellen en algemene velden ongewijzigd: {gelijk}; totaal {len(nieuw["modellen"])} modellen')
if not gelijk:
    sys.exit('Bestaande gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
json.dump(live, open('backups/modellen-voor-ronde48.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
