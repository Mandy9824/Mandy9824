#!/usr/bin/env python3
"""Ronde 43: Husqvarna-modellen M019 tot en met M022 in de live modelgegevens (dataroute /rmk/v1/modellen).

- De 17 live modellen en de algemene velden (gegenereerd, algemeen, ...) blijven ONGEWIJZIGD (ook M010 en zijn teksten).
- M020 (305E NERA), M021 (305) en M022 (310E NERA) komen uit de omzetting van het Excel-bestand
  (excel_naar_json.py --uit <json>), met de fabrikantpagina-URL en de teksten uit modellen-teksten-husqvarna.json
  (via scripts/modellen_teksten.json en modellen_analyse.json).
- M019 (Automower 105): niet leverbaar; de omzetter slaat zulke modellen over. Hier alleen als leeg record
  (zoals M013): naam, slug, fabrikantpagina (de ondersteuningspagina "Niet meer leverbaar"), beschikbaarheid
  "niet leverbaar", geen specificaties, scores, prijs of teksten. Geen kaart; staat op geen enkele pagina.
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde43_upload.py <omzetting.json>            (proefdraai)
          python3 scripts/ronde43_upload.py <omzetting.json> --schrijf
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
NIEUW = ('M020', 'M021', 'M022')

live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
ids = [m['id'] for m in live['modellen']]
if any(i in ids for i in NIEUW + ('M019',)):
    sys.exit(f'Er staan al Husqvarna-modellen live: {[i for i in ids if i in NIEUW + ("M019",)]}. Niets gewijzigd.')
for i in NIEUW:
    m = omz[i]
    assert m.get('fabrikant_url', '').startswith('https://www.husqvarna.com/nl/'), i
    assert m.get('beste_voor') and m.get('analyse') and m.get('pluspunten') and m.get('minpunten'), f'{i}: teksten ontbreken'
    assert not m.get('ean') and not m.get('bol'), f'{i}: onverwacht Bol-gegeven'

leeg = copy.deepcopy(next(m for m in live['modellen'] if m['id'] == 'M013'))
m019 = {**leeg, 'id': 'M019', 'slug': 'husqvarna-automower-105', 'naam': 'Husqvarna Automower 105', 'merk': 'Husqvarna',
        'model': 'Automower 105', 'specs': {}, 'beschikbaarheid': 'niet leverbaar',
        'fabrikant_url': 'https://www.husqvarna.com/nl/ondersteuning/robotic-lawn-mowers/automower-105/'}
for k in m019['kosten']:
    m019['kosten'][k] = {'waarde': None, 'bron': None, 'datum': None}

nieuw = copy.deepcopy(live)
nieuw['modellen'] = live['modellen'] + [m019] + [omz[i] for i in NIEUW]
for i in ('M019',) + NIEUW:
    m = next(x for x in nieuw['modellen'] if x['id'] == i)
    print(f'{i} {m["naam"]}: beschikbaarheid {m["beschikbaarheid"]}, scores {m["scores"]}, fabrikant {m["fabrikant_url"]}')
gelijk = all(a == b for a, b in zip(live['modellen'], nieuw['modellen'])) and {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
print(f'{len(live["modellen"])} live modellen en algemene velden ongewijzigd: {gelijk}; totaal {len(nieuw["modellen"])} modellen')
if not gelijk:
    sys.exit('Bestaande gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
json.dump(live, open('backups/modellen-voor-ronde43.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
