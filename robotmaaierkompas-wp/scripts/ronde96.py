#!/usr/bin/env python3
"""Ronde 96, MET DE HAND (zonder thema-zip):
1. /husqvarna-of-gardena-robotmaaier/ (#461), keuzetabel rij "Een alarm": Gardena-cel "Niet genoemd" ->
   "Nee volgens de productpagina's van Gardena" (gezocht mét de rij; moet precies 1x voorkomen).
2. Modelgegevens M071, M072, M055 (dataroute), alleen de tekstvelden analyse en minpunten:
   "een diefstalalarm noemt Gardena niet" -> "volgens de productpagina's van Gardena heeft hij geen diefstalalarm";
   minpunt "Geen diefstalalarm genoemd" -> "Geen diefstalalarm volgens de productpagina's van Gardena".
   Per model en veld moet de zoektekst precies 1x voorkomen, anders wordt dat veld niet gewijzigd en gemeld.
   Ook in scripts/modellen_teksten.json en scripts/modellen_analyse.json (zelfde regel: precies 1x per model/veld).
Het script weigert als er in de modelgegevens iets anders verandert dan deze velden.
Gebruik:  python3 scripts/ronde96.py            (proefdraai)
          python3 scripts/ronde96.py --schrijf
"""
import copy, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
from ronde88_lib import pas_toe

SCHRIJF = '--schrijf' in sys.argv
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(D))

R = '<th scope="row">'
STAPPEN = [(f'{R}Een alarm</th><td>Ja</td><td>Niet genoemd</td>',
            f'{R}Een alarm</th><td>Ja</td><td>Nee volgens de productpagina\'s van Gardena</td>',
            'keuzetabel, Een alarm (Gardena)')]
print('== Pagina #461')
p = api('wp/v2/pages/461?context=edit')
assert p['status'] == 'publish' and p['slug'] == 'husqvarna-of-gardena-robotmaaier'
_, meld = pas_toe(461, STAPPEN, False, 'r96')

MODELLEN = ['M071', 'M072', 'M055']
A_OUD, A_NIEUW = 'een diefstalalarm noemt Gardena niet', "volgens de productpagina's van Gardena heeft hij geen diefstalalarm"
M_OUD, M_NIEUW = 'Geen diefstalalarm genoemd', "Geen diefstalalarm volgens de productpagina's van Gardena"
info = []  # meldingen die niet blokkeren (zoektekst niet gevonden: niets gegokt)


def vervang_model(m, waar):
    """Past analyse en minpunten van één model aan (in place). Geeft lijst van gewijzigde velden."""
    gewijzigd = []
    n = (m.get('analyse') or '').count(A_OUD)
    if n == 1:
        m['analyse'] = m['analyse'].replace(A_OUD, A_NIEUW)
        gewijzigd.append('analyse')
    else:
        info.append(f'{waar} {m.get("id", "")} analyse: "{A_OUD}" {n} keer (verwacht 1); niet gewijzigd.')
    mp = m.get('minpunten') or []
    n = mp.count(M_OUD) + sum(M_OUD in x and x != M_OUD for x in mp)
    if n == 1 and M_OUD in mp:
        m['minpunten'] = [M_NIEUW if x == M_OUD else x for x in mp]
        gewijzigd.append('minpunten')
    else:
        info.append(f'{waar} {m.get("id", "")} minpunten: "{M_OUD}" {n} keer (verwacht 1); niet gewijzigd. '
                    f'Minpunten: {mp}')
    return gewijzigd


print('\n== Modelgegevens (dataroute)')
live = api('rmk/v1/modellen')['data']
elders = [(m['id'], k) for m in live['modellen'] for k, v in m.items()
          if (A_OUD in json.dumps(v, ensure_ascii=False) or M_OUD in json.dumps(v, ensure_ascii=False)) and m['id'] not in MODELLEN]
if elders:
    info.append(f'Zoektekst ook buiten M071/M072/M055: {elders} (niet gewijzigd).')
nieuw = copy.deepcopy(live)
for m in nieuw['modellen']:
    if m['id'] in MODELLEN:
        g = vervang_model(m, 'live')
        print(f'  {m["id"]}: gewijzigd {g or "niets"}')
for a, b in zip(live['modellen'], nieuw['modellen']):
    if a != b:
        assert a['id'] in MODELLEN and {k for k in set(a) | set(b) if a.get(k) != b.get(k)} <= {'analyse', 'minpunten'}, a['id']
assert len(live['modellen']) == len(nieuw['modellen'])
assert {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}

print('\n== Repository-bestanden')
BEST = {}
for naam in ('modellen_teksten.json', 'modellen_analyse.json'):
    pad = os.path.join(D, naam)
    t = json.load(open(pad, encoding='utf-8'))
    for i in MODELLEN:
        if i not in t:
            info.append(f'{naam}: {i} ontbreekt.')
            continue
        e = dict(t[i], id=i)
        heeft = [k for k in ('analyse', 'minpunten') if k in t[i]]
        g = []
        if 'analyse' in heeft:
            n = t[i]['analyse'].count(A_OUD)
            if n == 1:
                t[i]['analyse'] = t[i]['analyse'].replace(A_OUD, A_NIEUW); g.append('analyse')
            else:
                info.append(f'{naam} {i} analyse: {n} keer; niet gewijzigd.')
        if 'minpunten' in heeft:
            if t[i]['minpunten'].count(M_OUD) == 1:
                t[i]['minpunten'] = [M_NIEUW if x == M_OUD else x for x in t[i]['minpunten']]; g.append('minpunten')
            else:
                info.append(f'{naam} {i} minpunten: "{M_OUD}" 0 keer; niet gewijzigd.')
        # na de wijziging moet het bestand gelijk zijn aan de bedoelde live gegevens
        lm = next(m for m in nieuw['modellen'] if m['id'] == i)
        for k in heeft:
            if t[i][k] != lm.get(k):
                meld.append(f'{naam} {i} {k} wijkt af van de (bedoelde) live gegevens.')
        print(f'  {naam} {i}: gewijzigd {g or "niets"}')
    BEST[pad] = t

print('\nMeldingen (blokkerend):' if meld else '\nGeen blokkerende meldingen.')
for m in meld:
    print('  - ' + m)
print('Niet gevonden / niet gewijzigd:' if info else 'Alles precies 1x gevonden.')
for m in info:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')

pas_toe(461, STAPPEN, True, 'r96')
pad = f'backups/modellen-voor-ronde96-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie modelgegevens:', pad, '| opgeslagen:', api('rmk/v1/modellen', nieuw))  # leegt ook LiteSpeed
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
for pad_b, t in BEST.items():
    open(pad_b, 'w', encoding='utf-8').write(json.dumps(t, ensure_ascii=False, indent=2))  # zelfde opmaak als voorheen
