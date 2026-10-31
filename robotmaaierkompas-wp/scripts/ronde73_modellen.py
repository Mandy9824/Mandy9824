#!/usr/bin/env python3
"""Ronde 73: alleen deze velden in de live modelgegevens (dataroute /rmk/v1/modellen):
- M004 en M005: analyse en minpunten (app-rating 2,7 -> 2,9; aangepast in scripts/modellen_analyse.json en
  modellen_teksten.json); pluspunten en beste_voor ongewijzigd.
- M056 en M053: verbinding "module" (Losse 4G-module), M046: verbinding "wifi" (scripts/verbinding_toewijzing.json).
Waarden uit de omzetting (excel_naar_json.py --uit <json>). Alle andere velden en modellen en de algemene velden blijven
ongewijzigd; het script weigert anders. Wachtwoord alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde73_modellen.py <omzetting.json> [--schrijf]
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
TEKST = {'M004': ['analyse', 'minpunten'], 'M005': ['analyse', 'minpunten']}
VERB = {'M056': 'module', 'M046': 'wifi', 'M053': 'module'}
live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    i = m['id']
    if i in TEKST:
        o = omz[i]
        assert '2,7' in m['analyse'] and '2,9' in o['analyse'] and o['analyse'] == m['analyse'].replace('2,7', '2,9'), f'{i}: analyse'
        assert o['minpunten'] == [x.replace('2,7', '2,9') for x in m['minpunten']] != m['minpunten'], f'{i}: minpunten'
        assert o['pluspunten'] == m['pluspunten'] and o['beste_voor'] == m['beste_voor'], f'{i}: andere tekst wijkt af'
        for k in TEKST[i]:
            m[k] = copy.deepcopy(o[k])
        print(f'{i} {m["naam"]}: analyse en minpunten 2,7 -> 2,9')
    if i in VERB:
        v = omz[i].get('verbinding')
        assert v and v['extra'] == VERB[i] and v['bron'].startswith('https://'), f'{i}: verbinding {v}'
        assert m.get('verbinding') is None, f'{i}: had al een verbinding'
        m['verbinding'] = v
        print(f'{i} {m["naam"]}: verbinding {v["extra"]} ("{v["tekst"]}", {v["status"]}, {v["datum"]})')
for a, b in zip(live['modellen'], nieuw['modellen']):
    d = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    verwacht = sorted(TEKST.get(a['id'], []) + (['verbinding'] if a['id'] in VERB else []))
    assert d == verwacht, f'{a["id"]}: {d}'
assert {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
zonder = [m['id'] for m in nieuw['modellen'] if not m.get('verbinding') and m.get('scores') and any(v is not None for v in m['scores'].values())]
print(f'Alleen de genoemde velden anders; {len(nieuw["modellen"])} modellen. Modellen met een score zonder verbinding: {zonder}')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
json.dump(live, open('backups/modellen-voor-ronde73.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Opgeslagen (LiteSpeed geleegd):', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld (behalve M019/M065 specs [] i.p.v. {}):',
      all(x == y for x, y in zip(na['modellen'], nieuw['modellen']) if x['id'] not in ('M019', 'M065')))
