#!/usr/bin/env python3
"""Ronde 71: modelgegevens via de dataroute /rmk/v1/modellen. Alleen dit verandert:

- M056 en M057 (Roborock RockNeo Q105/Q110, stonden al live): vervangen door de omzetting (excel_naar_json.py --uit);
  het verschil met live mag ALLEEN de teksten zijn (beste_voor, pluspunten, minpunten, analyse uit
  modellen-teksten-roborock.json, nu in scripts/modellen_teksten.json en modellen_analyse.json).
- M061 en M062 (Mova LiDAX Ultra 1600/2000 AWD): alleen specs.vierwielaandrijving (was leeg) = de omzetting ("ja").
- M004 en M005 (Mova LiDAX Ultra 800/1200): alleen specs.app_rating.waarde 2.7 -> 2.9 (bron, status, datum blijven).
- M065 (Mova ViAX 300, beschikbaarheid "uitverkocht"): de omzetter slaat uitverkochte modellen over; daarom als leeg
  record zoals M019 (ronde 43): naam, slug, merk, model, beschikbaarheid "uitverkocht", fabrikantpagina uit de kolom
  Fabrikantpagina. Geen specificaties, scores, prijs, EAN of teksten. Staat op geen enkele pagina.
Alle andere modellen en de algemene velden blijven ongewijzigd; het script weigert als er meer verandert.
Gedraaid op 31 oktober 2026 (toen nog onder de werknaam ronde68_upload.py; kopie backups/modellen-voor-ronde68.json).
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde71_upload.py <omzetting.json> <modeldata.xlsx>            (proefdraai)
          python3 scripts/ronde71_upload.py <omzetting.json> <modeldata.xlsx> --schrijf
"""
import copy, json, os, sys
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON, XLSX = [a for a in sys.argv[1:] if not a.startswith('--')][:2]
TEKSTVELDEN = {'beste_voor', 'pluspunten', 'minpunten', 'analyse'}
D = os.path.dirname(os.path.abspath(__file__))
TEKSTEN = json.load(open(os.path.join(D, 'modellen_teksten.json'), encoding='utf-8'))
ANALYSE = json.load(open(os.path.join(D, 'modellen_analyse.json'), encoding='utf-8'))

live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
L = {m['id']: m for m in live['modellen']}
if 'M065' in L:
    sys.exit('M065 staat al live. Niets gewijzigd.')
nieuw = copy.deepcopy(live)
N = {m['id']: m for m in nieuw['modellen']}

# M056, M057: alleen de teksten
for i in ('M056', 'M057'):
    verschil = sorted(k for k in set(omz[i]) | set(L[i]) if omz[i].get(k) != L[i].get(k))
    assert set(verschil) <= TEKSTVELDEN, f'{i}: meer dan de teksten zou veranderen: {verschil}'
    assert (omz[i]['beste_voor'], omz[i]['pluspunten'], omz[i]['minpunten'], omz[i]['analyse']) == (
        TEKSTEN[i]['beste_voor'], TEKSTEN[i]['pluspunten'], TEKSTEN[i]['minpunten'], ANALYSE[i]['analyse']), f'{i}: teksten wijken af'
    assert not any(L[i].get(k) for k in TEKSTVELDEN), f'{i}: had al teksten'
    N[i].update({k: copy.deepcopy(omz[i][k]) for k in TEKSTVELDEN})
    print(f'{i} {L[i]["naam"]}: teksten toegevoegd ({", ".join(verschil)})')
# M061, M062: vierwielaandrijving
for i in ('M061', 'M062'):
    assert L[i]['specs'].get('vierwielaandrijving') is None, f'{i}: vierwielaandrijving was niet leeg'
    v = omz[i]['specs']['vierwielaandrijving']
    assert v['waarde'] == 'ja' and v['bron'] and v['datum'], f'{i}: omzetting geeft geen bron/ja'
    N[i]['specs']['vierwielaandrijving'] = copy.deepcopy(v)
    print(f'{i} {L[i]["naam"]}: vierwielaandrijving leeg -> ja ({v["status"]}, {v["datum"]})')
# M004, M005: app-rating
for i in ('M004', 'M005'):
    assert L[i]['specs']['app_rating']['waarde'] == 2.7 and omz[i]['specs']['app_rating']['waarde'] == 2.9, i
    N[i]['specs']['app_rating']['waarde'] = 2.9
    print(f'{i} {L[i]["naam"]}: app-rating 2.7 -> 2.9')
# M065: leeg record
ws = openpyxl.load_workbook(XLSX, data_only=True)['Modellen']
kop = [c.value for c in ws[1]]
rij = dict(zip(kop, next(r for r in ws.iter_rows(min_row=2, values_only=True) if r[0] == 'M065')))
assert rij['Beschikbaarheid (nieuw / uitlopend / uitverkocht)'] == 'uitverkocht'
leeg = copy.deepcopy(L['M019'])
m065 = {**leeg, 'id': 'M065', 'slug': 'mova-viax-300', 'naam': f'{rij["Merk"]} {rij["Model"]}', 'merk': rij['Merk'],
        'model': rij['Model'], 'specs': {}, 'beschikbaarheid': 'uitverkocht', 'fabrikant_url': rij['Fabrikantpagina (URL)']}
assert m065['naam'] == 'Mova ViAX 300' and m065['fabrikant_url'].startswith('https://')
assert not any(m065.get(k) for k in ('ean', 'prijs', 'verbinding', 'beste_voor', 'analyse', 'pluspunten', 'minpunten', 'reviews'))
assert all(v is None for v in m065['scores'].values()) and all(v == {'waarde': None, 'bron': None, 'datum': None} for v in m065['kosten'].values())
nieuw['modellen'].append(m065)
print(f'M065 {m065["naam"]}: leeg record, beschikbaarheid uitverkocht, fabrikant {m065["fabrikant_url"]}')

# Controle: verder niets anders
GEWIJZIGD = {'M056', 'M057', 'M061', 'M062', 'M004', 'M005'}
ongewijzigd = [m['id'] for m in live['modellen'] if m['id'] not in GEWIJZIGD]
gelijk = all(L[i] == N[i] for i in ongewijzigd) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'} and \
    [m['id'] for m in nieuw['modellen']] == [m['id'] for m in live['modellen']] + ['M065']
for i in ('M061', 'M062', 'M004', 'M005'):
    a, b = copy.deepcopy(L[i]), copy.deepcopy(N[i])
    a['specs'].pop('vierwielaandrijving' if i in ('M061', 'M062') else 'app_rating', None)
    b['specs'].pop('vierwielaandrijving' if i in ('M061', 'M062') else 'app_rating', None)
    gelijk = gelijk and a == b
    if i in ('M004', 'M005'):
        x, y = dict(L[i]['specs']['app_rating']), dict(N[i]['specs']['app_rating'])
        x.pop('waarde'); y.pop('waarde'); gelijk = gelijk and x == y
print(f'{len(ongewijzigd)} andere live modellen en algemene velden ongewijzigd, alleen de genoemde velden anders: {gelijk}; '
      f'totaal {len(nieuw["modellen"])} modellen')
if not gelijk:
    sys.exit('Bestaande gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
json.dump(live, open('backups/modellen-voor-ronde71.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '(M065 specs komt terug als [] in plaats van {}, zoals bij M019)')
