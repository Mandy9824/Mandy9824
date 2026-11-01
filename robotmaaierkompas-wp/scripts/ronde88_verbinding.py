#!/usr/bin/env python3
"""Ronde 88: alleen het veld "verbinding" van M066-M072 (M069, M070, M071, M072 ingebouwd = chip 4G; M066-M068 wifi), via de dataroute.
Waarden uit de omzetting (excel_naar_json.py --uit <json>) met de nieuwe regels in scripts/verbinding_toewijzing.json.
Per model moet het bronveld precies één regel hebben in het blad Bronnen. Alle andere velden en modellen en de
algemene velden blijven ongewijzigd; het script weigert anders. Wachtwoord alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde88_verbinding.py <omzetting.json> <modeldata.xlsx> [--schrijf]
"""
import copy, json, os, sys, time
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if a.endswith('.json'))
XLSX = next(a for a in sys.argv[1:] if a.endswith('.xlsx'))
VERWACHT = {'M069': 'ingebouwd', 'M070': 'ingebouwd', 'M066': 'wifi', 'M067': 'wifi', 'M068': 'wifi', 'M071': 'ingebouwd', 'M072': 'ingebouwd'}
D = os.path.dirname(os.path.abspath(__file__))
tw = {t['model']: t for t in json.load(open(os.path.join(D, 'verbinding_toewijzing.json'), encoding='utf-8'))['toewijzingen']}

rijen = [r for r in openpyxl.load_workbook(XLSX, data_only=True, read_only=True)['Bronnen'].iter_rows(min_row=2, values_only=True) if r[0]]
for mid in VERWACHT:
    n = sum(1 for r in rijen if r[0] == mid and str(r[1] or '').strip().lower() == tw[mid]['bronveld'].strip().lower())
    print(f'{mid}: bronveld "{tw[mid]["bronveld"]}": {n} regel(s)')
    if n != 1:
        sys.exit(f'{mid}: niet precies één bronregel. Niets gewijzigd.')

live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    if m['id'] in VERWACHT:
        v = omz[m['id']].get('verbinding')
        assert v and v['extra'] == VERWACHT[m['id']], f'{m["id"]}: verbinding in de omzetting {v}'
        assert m.get('verbinding') is None, f'{m["id"]}: had al een verbinding'
        print(f'{m["id"]} {m["naam"]}: verbinding {m.get("verbinding")} -> {v["extra"]} ("{v["tekst"]}", {v["status"]}, {v["datum"]})')
        m['verbinding'] = copy.deepcopy(v)
gelijk = all((a == b) if a['id'] not in VERWACHT else
             ({k: x for k, x in a.items() if k != 'verbinding'} == {k: x for k, x in b.items() if k != 'verbinding'})
             for a, b in zip(live['modellen'], nieuw['modellen'])) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
print('Alleen "verbinding" van deze modellen verandert, de rest gelijk:', gelijk)
if not gelijk:
    sys.exit('Andere gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
pad = f'backups/modellen-voor-ronde88-verbinding-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
