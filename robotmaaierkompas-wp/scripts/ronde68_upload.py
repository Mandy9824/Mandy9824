#!/usr/bin/env python3
"""Ronde 68: modelgegevens M059 tot en met M064 (Mova) bijwerken via de dataroute /rmk/v1/modellen.

- Alle andere live modellen (M001-M058) en de algemene velden blijven ONGEWIJZIGD (het script weigert anders).
- M059-M064 (stonden live als niveau basis) worden vervangen door de omzetting (excel_naar_json.py --uit <json>).
  M059, M060, M063 en M064 krijgen de teksten uit modellen-teksten-mova.json (in scripts/modellen_teksten.json en
  modellen_analyse.json) en zijn geen niveau basis meer; M061 en M062 blijven basis.
- Geen van de zes staat in de bladen Bol of Coolblue: geen EAN, blok bol, blok coolblue of prijs (gecontroleerd).
  Id, slug, naam en fabrikantpagina moeten gelijk blijven.
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde68_upload.py <omzetting.json>            (proefdraai)
          python3 scripts/ronde68_upload.py <omzetting.json> --schrijf
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
BIJWERKEN = [f'M{n:03d}' for n in range(59, 65)]
MET_TEKST = ['M059', 'M060', 'M063', 'M064']
D = os.path.dirname(os.path.abspath(__file__))
TEKSTEN = json.load(open(os.path.join(D, 'modellen_teksten.json'), encoding='utf-8'))
ANALYSE = json.load(open(os.path.join(D, 'modellen_analyse.json'), encoding='utf-8'))

live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
L = {m['id']: m for m in live['modellen']}
if any(i not in L for i in BIJWERKEN):
    sys.exit(f'Niet live: {[i for i in BIJWERKEN if i not in L]}. Niets gewijzigd.')

for i in BIJWERKEN:
    m = omz[i]
    for k in ('id', 'slug', 'naam', 'fabrikant_url'):
        assert L[i].get(k) == m.get(k), f'{i}: {k} zou veranderen'
    assert m['fabrikant_url'].startswith('https://nl.mova.tech/'), f'{i}: geen fabrikantpagina'
    assert not m.get('ean') and not m.get('bol') and not m.get('prijs') and 'coolblue' not in m, f'{i}: onverwacht winkelgegeven'
    assert (m.get('niveau') == 'basis') == (i not in MET_TEKST), f'{i}: niveau {m.get("niveau")}'
for i in MET_TEKST:
    m = omz[i]
    assert (m.get('beste_voor'), m.get('pluspunten'), m.get('minpunten'), m.get('analyse')) == (
        TEKSTEN[i]['beste_voor'], TEKSTEN[i]['pluspunten'], TEKSTEN[i]['minpunten'], ANALYSE[i]['analyse']), f'{i}: teksten wijken af'

nieuw = copy.deepcopy(live)
nieuw['modellen'] = [omz[m['id']] if m['id'] in BIJWERKEN else m for m in live['modellen']]
ongewijzigd = [m['id'] for m in live['modellen'] if m['id'] not in BIJWERKEN]
gelijk = all(L[i] == next(x for x in nieuw['modellen'] if x['id'] == i) for i in ongewijzigd) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
for i in BIJWERKEN:
    m = omz[i]
    gewijzigd = sorted(k for k in set(m) | set(L[i]) if m.get(k) != L[i].get(k))
    print(f'{i} {m["naam"]}: {m.get("niveau") or "volledig"}, fabrikant {m["fabrikant_url"]}; velden: {", ".join(gewijzigd) or "geen"}')
print(f'{len(ongewijzigd)} live modellen en algemene velden ongewijzigd: {gelijk}; totaal {len(nieuw["modellen"])} modellen')
if not gelijk:
    sys.exit('Bestaande gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
json.dump(live, open('backups/modellen-voor-ronde68.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
