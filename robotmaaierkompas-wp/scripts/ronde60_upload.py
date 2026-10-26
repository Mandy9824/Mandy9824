#!/usr/bin/env python3
"""Ronde 60: modelgegevens M046 tot en met M058 en M007 (dataroute /rmk/v1/modellen).

- Alle andere live modellen (M001-M045 zonder M007) en de algemene velden blijven ONGEWIJZIGD.
- M007 (Eufy E18): de live versie had alleen het blok coolblue; nu de kernvelden uit de omzetting (niveau basis),
  met fabrikantpagina. Het blok coolblue blijft gelijk.
- M046-M058 (Worx, Eufy, Gardena, Roborock, Ecovacs) nieuw uit de omzetting (excel_naar_json.py --uit <json>), met
  fabrikantpagina; M046 en M047 met de teksten uit modellen-teksten-worx.json. Geen EAN, Bol of prijs.
  M052-M058 met het blok coolblue uit het blad Coolblue (zichtbaar pas als een model een kaart krijgt).
Het script weigert als er meer verandert dan dit. Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde60_upload.py <omzetting.json>            (proefdraai)
          python3 scripts/ronde60_upload.py <omzetting.json> --schrijf
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
NIEUW = [f'M{n:03d}' for n in range(46, 59)]
D = os.path.dirname(os.path.abspath(__file__))
TEKSTEN = json.load(open(os.path.join(D, 'modellen_teksten.json'), encoding='utf-8'))
ANALYSE = json.load(open(os.path.join(D, 'modellen_analyse.json'), encoding='utf-8'))

live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
L = {m['id']: m for m in live['modellen']}
if any(i in L for i in NIEUW):
    sys.exit(f'Er staan al nieuwe modellen live: {[i for i in NIEUW if i in L]}. Niets gewijzigd.')

# M007: alleen de kernvelden komen erbij; naam, slug en coolblue blijven
m7 = omz['M007']
for k in ('id', 'slug', 'naam', 'merk', 'model', 'coolblue', 'kosten', 'scores', 'reviews_gelezen', 'ean', 'prijs', 'bol'):
    assert L['M007'].get(k) == m7.get(k), f'M007: {k} zou veranderen'
assert m7['fabrikant_url'].startswith('https://www.eufy.com/nl/') and m7.get('niveau') == 'basis', 'M007'
for i in NIEUW:
    m = omz[i]
    assert m.get('fabrikant_url', '').startswith('https://'), f'{i}: geen fabrikantpagina'
    assert not m.get('ean') and not m.get('bol') and not m.get('prijs'), f'{i}: onverwacht Bol- of prijsgegeven'
    assert ('coolblue' in m) == (i >= 'M052'), f'{i}: blok coolblue onverwacht'
for i in ('M046', 'M047'):
    m = omz[i]
    assert (m.get('beste_voor'), m.get('pluspunten'), m.get('minpunten'), m.get('analyse')) == (
        TEKSTEN[i]['beste_voor'], TEKSTEN[i]['pluspunten'], TEKSTEN[i]['minpunten'], ANALYSE[i]['analyse']), f'{i}: teksten wijken af'

nieuw = copy.deepcopy(live)
nieuw['modellen'] = [omz['M007'] if m['id'] == 'M007' else m for m in live['modellen']] + [omz[i] for i in NIEUW]
ongewijzigd = [m['id'] for m in live['modellen'] if m['id'] != 'M007']
gelijk = all(L[i] == next(x for x in nieuw['modellen'] if x['id'] == i) for i in ongewijzigd) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
for i in ['M007'] + NIEUW:
    m = omz[i]
    print(f'{i} {m["naam"]}: {m.get("niveau") or "volledig"}, beschikbaarheid {m.get("beschikbaarheid")}, '
          f'coolblue {"ja" if m.get("coolblue") else "nee"}, fabrikant {m["fabrikant_url"]}')
print(f'{len(ongewijzigd)} live modellen en algemene velden ongewijzigd: {gelijk}; M007 kernvelden; '
      f'totaal {len(nieuw["modellen"])} modellen')
if not gelijk:
    sys.exit('Bestaande gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
json.dump(live, open('backups/modellen-voor-ronde60.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
