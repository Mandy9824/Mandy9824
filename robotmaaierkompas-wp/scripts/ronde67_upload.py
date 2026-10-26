#!/usr/bin/env python3
"""Ronde 67: modelgegevens M007, M050 tot en met M064 (dataroute /rmk/v1/modellen).

- Alle andere live modellen (M001-M049 zonder M007) en de algemene velden blijven ONGEWIJZIGD.
- M007 en M050-M058 (stonden al live) worden vervangen door de omzetting (excel_naar_json.py --uit <json>): nu met
  EAN en het blok "bol" (EAN, productlink, afbeelding uit het blad Bol), de fabrikantpagina en voor M007, M052 en M053
  de teksten uit modellen-teksten-eufy.json (in scripts/modellen_teksten.json en modellen_analyse.json).
  Id, slug, naam en het blok coolblue moeten gelijk blijven.
- M059-M064 (Mova LiDAX Ultra 1600, Ultra 1000/1600/2000 AWD, ViAX 250/500) nieuw, niveau basis, met fabrikantpagina;
  geen EAN, Bol, Coolblue of prijs (ze staan niet in de bladen Bol en Coolblue).
Het script weigert als er meer verandert dan dit. Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde67_upload.py <omzetting.json>            (proefdraai)
          python3 scripts/ronde67_upload.py <omzetting.json> --schrijf
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
BIJWERKEN = ['M007'] + [f'M{n:03d}' for n in range(50, 59)]
NIEUW = [f'M{n:03d}' for n in range(59, 65)]
MET_BOL = ['M007', 'M050', 'M051', 'M052', 'M053', 'M054', 'M055', 'M056', 'M057', 'M058']
TEKSTEN_EUFY = ['M007', 'M052', 'M053']
D = os.path.dirname(os.path.abspath(__file__))
TEKSTEN = json.load(open(os.path.join(D, 'modellen_teksten.json'), encoding='utf-8'))
ANALYSE = json.load(open(os.path.join(D, 'modellen_analyse.json'), encoding='utf-8'))

live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
L = {m['id']: m for m in live['modellen']}
if any(i in L for i in NIEUW):
    sys.exit(f'Er staan al nieuwe modellen live: {[i for i in NIEUW if i in L]}. Niets gewijzigd.')
if any(i not in L for i in BIJWERKEN):
    sys.exit(f'Niet live: {[i for i in BIJWERKEN if i not in L]}. Niets gewijzigd.')

for i in BIJWERKEN:
    m = omz[i]
    for k in ('id', 'slug', 'naam', 'coolblue'):
        assert L[i].get(k) == m.get(k), f'{i}: {k} zou veranderen'
    assert m.get('fabrikant_url', '').startswith('https://'), f'{i}: geen fabrikantpagina'
    assert not m.get('prijs'), f'{i}: onverwachte prijs'
for i in MET_BOL:
    b = omz[i].get('bol') or {}
    assert omz[i].get('ean') and b.get('product_url', '').startswith('https://www.bol.com/nl/nl/p/'), f'{i}: geen Bol-blok'
    assert (b.get('afbeelding') or {}).get('url', '').startswith('https://media.s-bol.com/'), f'{i}: geen Bol-afbeelding'
for i in NIEUW:
    m = omz[i]
    assert m.get('fabrikant_url', '').startswith('https://nl.mova.tech/'), f'{i}: geen fabrikantpagina'
    assert m.get('niveau') == 'basis', f'{i}: niet niveau basis'
    assert not m.get('ean') and not m.get('bol') and not m.get('prijs') and 'coolblue' not in m, f'{i}: onverwacht winkelgegeven'
for i in TEKSTEN_EUFY:
    m = omz[i]
    assert (m.get('beste_voor'), m.get('pluspunten'), m.get('minpunten'), m.get('analyse')) == (
        TEKSTEN[i]['beste_voor'], TEKSTEN[i]['pluspunten'], TEKSTEN[i]['minpunten'], ANALYSE[i]['analyse']), f'{i}: teksten wijken af'

nieuw = copy.deepcopy(live)
nieuw['modellen'] = [omz[m['id']] if m['id'] in BIJWERKEN else m for m in live['modellen']] + [omz[i] for i in NIEUW]
ongewijzigd = [m['id'] for m in live['modellen'] if m['id'] not in BIJWERKEN]
gelijk = all(L[i] == next(x for x in nieuw['modellen'] if x['id'] == i) for i in ongewijzigd) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
for i in BIJWERKEN + NIEUW:
    m = omz[i]
    gewijzigd = sorted(k for k in set(m) | set(L.get(i, {})) if m.get(k) != L.get(i, {}).get(k)) if i in L else ['nieuw']
    print(f'{i} {m["naam"]}: {m.get("niveau") or "volledig"}, EAN {m.get("ean") or "-"}, '
          f'coolblue {"ja" if m.get("coolblue") else "nee"}, fabrikant {m["fabrikant_url"]}; velden: {", ".join(gewijzigd)}')
print(f'{len(ongewijzigd)} live modellen en algemene velden ongewijzigd: {gelijk}; totaal {len(nieuw["modellen"])} modellen')
if not gelijk:
    sys.exit('Bestaande gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
json.dump(live, open('backups/modellen-voor-ronde67.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
