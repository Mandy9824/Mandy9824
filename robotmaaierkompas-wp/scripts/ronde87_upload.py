#!/usr/bin/env python3
"""Ronde 87: modelgegevens via de dataroute /rmk/v1/modellen. Alleen dit verandert:

- M066-M072 (Husqvarna Automower 308V, 312V, Aspire R6V, 430V NERA, 450V NERA; Gardena smart SILENO sense 400 en 600)
  nieuw uit de omzetting (excel_naar_json.py --uit), met fabrikantpagina (kolom Fabrikantpagina) en de teksten uit
  modellen-teksten-husqvarna-2026.json (in scripts/modellen_teksten.json en modellen_analyse.json). Geen van de zeven
  staat in de bladen Bol, Coolblue of Amazon: geen EAN, blok bol, coolblue of amazon (het script controleert dat).
- M010 (Husqvarna Automower 410VE NERA): alleen beschikbaarheid "nieuw" -> "uitlopend" (zoals in het blad Modellen).
Alle andere modellen, de andere velden van M010 en de algemene velden blijven ongewijzigd; het script weigert anders.
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde87_upload.py <omzetting.json> <modeldata.xlsx>            (proefdraai)
          python3 scripts/ronde87_upload.py <omzetting.json> <modeldata.xlsx> --schrijf
"""
import copy, json, os, sys, time
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON, XLSX = [a for a in sys.argv[1:] if not a.startswith('--')][:2]
NIEUW = [f'M{n:03d}' for n in range(66, 73)]
D = os.path.dirname(os.path.abspath(__file__))
TEKSTEN = json.load(open(os.path.join(D, 'modellen_teksten.json'), encoding='utf-8'))
ANALYSE = json.load(open(os.path.join(D, 'modellen_analyse.json'), encoding='utf-8'))

wb = openpyxl.load_workbook(XLSX, data_only=True)
def ids(blad):
    return {str(r[0]).strip() for r in wb[blad].iter_rows(min_row=2, values_only=True) if r[0]}
WINKELBLADEN = {b: ids(b) for b in ('Bol', 'Coolblue', 'Amazon')}
ws = wb['Modellen']
kop = [c.value for c in ws[1]]
RIJ = {r[0]: dict(zip(kop, r)) for r in ws.iter_rows(min_row=2, values_only=True) if r[0]}

live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
L = {m['id']: m for m in live['modellen']}
if any(i in L for i in NIEUW):
    sys.exit(f'Er staan al nieuwe modellen live: {[i for i in NIEUW if i in L]}. Niets gewijzigd.')

for i in NIEUW:
    m, rij = omz[i], RIJ[i]
    assert m['naam'] == f'{rij["Merk"]} {rij["Model"]}', f'{i}: naam'
    assert m.get('fabrikant_url') == rij['Fabrikantpagina (URL)'] and m['fabrikant_url'].startswith(
        ('https://www.husqvarna.com/nl/', 'https://www.gardena.com/nl/')), f'{i}: fabrikantpagina'
    assert m.get('beschikbaarheid') == 'nieuw', f'{i}: beschikbaarheid'
    for blad, s in WINKELBLADEN.items():
        assert i not in s, f'{i} staat in het blad {blad}: script aanpassen'
    assert not m.get('ean') and not m.get('bol') and 'coolblue' not in m and 'amazon' not in m, f'{i}: onverwacht winkelgegeven'
    assert (m.get('beste_voor'), m.get('pluspunten'), m.get('minpunten'), m.get('analyse')) == (
        TEKSTEN[i]['beste_voor'], TEKSTEN[i]['pluspunten'], TEKSTEN[i]['minpunten'], ANALYSE[i]['analyse']), f'{i}: teksten wijken af'

assert RIJ['M010']['Beschikbaarheid (nieuw / uitlopend / uitverkocht)'] == 'uitlopend'
assert L['M010']['beschikbaarheid'] == 'nieuw', 'M010 is live niet "nieuw"'

nieuw = copy.deepcopy(live)
N = {m['id']: m for m in nieuw['modellen']}
N['M010']['beschikbaarheid'] = 'uitlopend'
nieuw['modellen'] += [copy.deepcopy(omz[i]) for i in NIEUW]

a, b = copy.deepcopy(L['M010']), copy.deepcopy(N['M010'])
a.pop('beschikbaarheid'); b.pop('beschikbaarheid')
gelijk = a == b and all(L[i] == N[i] for i in L if i != 'M010') and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'} and \
    [m['id'] for m in nieuw['modellen']] == [m['id'] for m in live['modellen']] + NIEUW
for i in NIEUW:
    m = omz[i]
    print(f'{i} {m["naam"]}: {m.get("niveau") or "volledig"}, slug {m["slug"]}, fabrikant {m["fabrikant_url"]}, '
          f'verbinding {m.get("verbinding") or "-"}, teksten ja')
print('M010: beschikbaarheid nieuw -> uitlopend')
print(f'{len(L) - 1} andere live modellen, de andere velden van M010 en de algemene velden ongewijzigd: {gelijk}; '
      f'totaal {len(nieuw["modellen"])} modellen')
if not gelijk:
    sys.exit('Bestaande gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
pad = f'backups/modellen-voor-ronde87-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
