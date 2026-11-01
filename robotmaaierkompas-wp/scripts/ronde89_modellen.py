#!/usr/bin/env python3
"""Ronde 89: modelgegevens via de dataroute, alleen deze velden (waarden uit de omzetting excel_naar_json.py --uit):
- M054: analyse en minpunten (kaart en zones; GPS-tracking ook met de gateway niet), verbinding bluetooth (chip);
- M055: minpunten ("Weinig reviews gelezen (2 bij Coolblue): geen betrouwbaarheidsscore");
- M025: verbinding bluetooth (chip). M055 houdt geen verbinding (geen chip).
Per chip moet het bronveld precies één regel in het blad Bronnen hebben. Alle andere velden en modellen en de algemene
velden blijven ongewijzigd; het script weigert anders. Gebruik:  python3 scripts/ronde89_modellen.py <omzetting.json> <xlsx> [--schrijf]
"""
import copy, json, os, sys, time
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if a.endswith('.json')); XLSX = next(a for a in sys.argv[1:] if a.endswith('.xlsx'))
VELDEN = {'M054': ('analyse', 'minpunten', 'verbinding'), 'M055': ('minpunten',), 'M025': ('verbinding',)}
D = os.path.dirname(os.path.abspath(__file__))
tw = {t['model']: t for t in json.load(open(os.path.join(D, 'verbinding_toewijzing.json'), encoding='utf-8'))['toewijzingen']}
rijen = [r for r in openpyxl.load_workbook(XLSX, data_only=True, read_only=True)['Bronnen'].iter_rows(min_row=2, values_only=True) if r[0]]
for mid in ('M025', 'M054'):
    n = sum(1 for r in rijen if r[0] == mid and str(r[1] or '').strip().lower() == tw[mid]['bronveld'].strip().lower())
    print(f'{mid}: bronveld "{tw[mid]["bronveld"]}": {n} regel(s)')
    if n != 1:
        sys.exit('Niet precies één bronregel. Niets gewijzigd.')
assert 'M055' not in tw
live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    for k in VELDEN.get(m['id'], ()):
        if k == 'verbinding':
            assert m.get('verbinding') is None and omz[m['id']]['verbinding']['extra'] == 'bluetooth'
        print(f'{m["id"]} {k}: {json.dumps(m.get(k), ensure_ascii=False)[:150]}\n      -> {json.dumps(omz[m["id"]][k], ensure_ascii=False)[:150]}')
        m[k] = copy.deepcopy(omz[m['id']][k])
assert next(m for m in nieuw['modellen'] if m['id'] == 'M055').get('verbinding') is None
gelijk = len(live['modellen']) == len(nieuw['modellen']) and all(
    {k: v for k, v in a.items() if k not in VELDEN.get(a['id'], ())} == {k: v for k, v in b.items() if k not in VELDEN.get(b['id'], ())}
    for a, b in zip(live['modellen'], nieuw['modellen'])) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
print('Alleen de genoemde velden veranderen:', gelijk)
if not gelijk:
    sys.exit('Andere gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
pad = f'backups/modellen-voor-ronde89-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad, '| opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
