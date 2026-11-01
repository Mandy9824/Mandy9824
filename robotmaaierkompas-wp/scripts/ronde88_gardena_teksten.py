#!/usr/bin/env python3
"""Ronde 88, stap 3: alleen beste_voor, pluspunten, minpunten en analyse van M054 en M055 (Gardena smart SILENO max 1200
en free 1500) uit modellen-teksten-gardena-2026.json (in scripts/modellen_teksten.json en modellen_analyse.json), via de
dataroute. De waarden komen uit de omzetting (excel_naar_json.py --uit). Alle andere velden en modellen en de algemene
velden blijven ongewijzigd; het script weigert anders. Wachtwoord alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde88_gardena_teksten.py <omzetting.json> [--schrijf]
"""
import copy, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if a.endswith('.json'))
IDS = ('M054', 'M055')
VELDEN = ('beste_voor', 'pluspunten', 'minpunten', 'analyse')
D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(D, 'modellen_teksten.json'), encoding='utf-8'))
A = json.load(open(os.path.join(D, 'modellen_analyse.json'), encoding='utf-8'))
live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    if m['id'] in IDS:
        o = omz[m['id']]
        assert [o[k] for k in VELDEN] == [T[m['id']]['beste_voor'], T[m['id']]['pluspunten'], T[m['id']]['minpunten'], A[m['id']]['analyse']]
        for k in VELDEN:
            print(f'{m["id"]} {k}: {json.dumps(m.get(k), ensure_ascii=False)[:60]} -> {json.dumps(o[k], ensure_ascii=False)[:60]}')
            m[k] = copy.deepcopy(o[k])
gelijk = all((a == b) if a['id'] not in IDS else
             ({k: x for k, x in a.items() if k not in VELDEN} == {k: x for k, x in b.items() if k not in VELDEN})
             for a, b in zip(live['modellen'], nieuw['modellen'])) and len(live['modellen']) == len(nieuw['modellen']) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
print('Alleen de vier tekstvelden van M054 en M055 veranderen, de rest gelijk:', gelijk)
if not gelijk:
    sys.exit('Andere gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
pad = f'backups/modellen-voor-ronde88-teksten-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
