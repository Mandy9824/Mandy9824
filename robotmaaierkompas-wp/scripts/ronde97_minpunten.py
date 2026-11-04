#!/usr/bin/env python3
"""Ronde 97: modelgegevens (dataroute), ALLEEN het veld minpunten van M071, M072 en M055:
  M071, M072: "Geen diefstalalarm" -> "Geen diefstalalarm volgens de productpagina's van Gardena"
  M055:       "Geen GPS-tracking en geen diefstalalarm" -> "Geen GPS-tracking; geen diefstalalarm volgens de productpagina's van Gardena"
Elk minpunt moet precies 1x (als heel minpunt) voorkomen, anders schrijft het script niets.
Hetzelfde in scripts/modellen_teksten.json (daar moeten de minpunten daarna gelijk zijn aan live).
Weigert als er in de modelgegevens iets anders verandert dan deze drie velden. Kopie vooraf in backups/ (niet in git).
Gebruik:  python3 scripts/ronde97_minpunten.py            (proefdraai)
          python3 scripts/ronde97_minpunten.py --schrijf
"""
import copy, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(D))
G = "volgens de productpagina's van Gardena"
REGELS = {
    'M071': ('Geen diefstalalarm', f'Geen diefstalalarm {G}'),
    'M072': ('Geen diefstalalarm', f'Geen diefstalalarm {G}'),
    'M055': ('Geen GPS-tracking en geen diefstalalarm', f'Geen GPS-tracking; geen diefstalalarm {G}'),
}
meld = []


def vervang(mp, wie):
    oud, wordt = REGELS[wie[1]]
    if mp.count(oud) != 1:
        meld.append(f'{wie[0]} {wie[1]}: minpunt "{oud}" {mp.count(oud)} keer (verwacht 1). Minpunten: {mp}')
        return mp
    return [wordt if x == oud else x for x in mp]


live = api('rmk/v1/modellen')['data']
nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    if m['id'] in REGELS:
        m['minpunten'] = vervang(m.get('minpunten') or [], ('live', m['id']))
assert {m['id'] for m in live['modellen']} >= set(REGELS), 'model ontbreekt live'
for a, b in zip(live['modellen'], nieuw['modellen']):
    if a != b:
        verschil = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
        assert a['id'] in REGELS and verschil == {'minpunten'}, (a['id'], verschil)
        print(f'{a["id"]} {a["naam"]}:\n  was   {a["minpunten"]}\n  wordt {b["minpunten"]}')
assert len(live['modellen']) == len(nieuw['modellen'])
assert {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
# andere modellen met een vergelijkbaar minpunt: alleen melden
for m in live['modellen']:
    for x in m.get('minpunten') or []:
        if 'diefstalalarm' in x.lower() and m['id'] not in REGELS:
            print(f'  (niet gewijzigd, niet gevraagd) {m["id"]}: "{x}"')

pad_t = os.path.join(D, 'modellen_teksten.json')
t = json.load(open(pad_t, encoding='utf-8'))
for i in REGELS:
    if i not in t or 'minpunten' not in t[i]:
        meld.append(f'modellen_teksten.json: {i} zonder minpunten.')
        continue
    t[i]['minpunten'] = vervang(t[i]['minpunten'], ('modellen_teksten.json', i))
    lm = next(m for m in nieuw['modellen'] if m['id'] == i)
    if t[i]['minpunten'] != lm['minpunten']:
        meld.append(f'modellen_teksten.json {i}: minpunten wijken af van de bedoelde live gegevens.')

print('\nMeldingen:' if meld else '\nGeen meldingen.')
for x in meld:
    print('  - ' + x)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/modellen-voor-ronde97-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie modelgegevens:', pad, '| opgeslagen:', api('rmk/v1/modellen', nieuw))  # leegt ook LiteSpeed
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
open(pad_t, 'w', encoding='utf-8').write(json.dumps(t, ensure_ascii=False, indent=2))
