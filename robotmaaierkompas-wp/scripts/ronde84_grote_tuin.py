#!/usr/bin/env python3
"""Ronde 84: gerichte wijzigingen op /robotmaaier-grote-tuin/ (#15, gepubliceerd). Bouwt niets opnieuw uit de md.
De pagina is MET DE HAND gewijzigd (deze ronde): niet opnieuw bouwen met ronde82_bouw.py, anders gaan deze wijzigingen
en de links van ronde 83 verloren.
1. Tabel "Modellen zonder score": rij Cramer AiConic 2 achteraan; "zes" -> "zeven" (korte antwoord, "Wat we nog niet
   weten") en in de Yoast-metabeschrijving "zes zonder score" -> "zeven zonder score".
2. Keuzetabel: 310E NERA bij 1.500-1.600 m², Worx Landroid 4WD WR342E bij 2.000 m² (zonder score), Navimow X420 bij 4G.
3. FAQ "Welke grote maaier heeft 4G ingebouwd?": Navimow X420.
4. "LiDAR en netwerk-RTK" -> "LiDAR met camera en netwerk-RTK (volgens Navimow)" (beide tabellen).
Elke zoektekst moet precies het verwachte aantal keren voorkomen; anders schrijft het script niets. Status blijft publish.
Gebruik:  python3 scripts/ronde84_grote_tuin.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PID = 15
WR342E_RIJ = ('<tr><th scope="row">Worx Landroid 4WD WR342E</th><td>2.000 m²</td><td>84%</td><td>RTK via de cloud met camera</td>'
              '<td>niet bekend</td><td>Wifi en Bluetooth</td></tr>')
AICONIC = ('<tr><th scope="row">Cramer AiConic 2</th><td>2.000 m²</td><td>45%</td><td>RTK met camera</td>'
           '<td>niet bekend</td><td>4G, Bluetooth en wifi</td></tr>')
STAPPEN = [  # (zoek, vervang, verwacht aantal, omschrijving)
    (WR342E_RIJ + '</tbody>', WR342E_RIJ + AICONIC + '</tbody>', 1, 'tabel zonder score: rij Cramer AiConic 2'),
    ('een score hebben, plus zes zonder score en', 'een score hebben, plus zeven zonder score en', 1, 'korte antwoord: zes -> zeven'),
    ('<li>De zes modellen zonder score hebben we', '<li>De zeven modellen zonder score hebben we', 1, 'Wat we nog niet weten: zes -> zeven'),
    ('<td>Mova LiDAX Ultra 1600, Husqvarna Automower 410VE NERA of Gardena Sileno Free 1500</td>',
     '<td>Mova LiDAX Ultra 1600, Husqvarna Automower 410VE NERA, Husqvarna Automower 310E NERA of Gardena Sileno Free 1500</td>', 1,
     'keuzetabel 1.500-1.600 m²: 310E NERA'),
    ('zonder score ook de Navimow i220 LiDAR Pro, de Navimow X420 en de Mova LiDAX Ultra 2000 AWD</td>',
     'zonder score ook de Navimow i220 LiDAR Pro, de Navimow X420, de Mova LiDAX Ultra 2000 AWD en de Worx Landroid 4WD WR342E</td>', 1,
     'keuzetabel 2.000 m²: Worx WR342E'),
    ('<th scope="row">4G en GPS ingebouwd</th><td>Navimow i210 en i220 Pro, Mova',
     '<th scope="row">4G en GPS ingebouwd</th><td>Navimow i210 en i220 Pro, Navimow X420, Mova', 1, 'keuzetabel 4G: Navimow X420'),
    ('<p>De Navimow i210 en i220 Pro, de Mova LiDAX Ultra 1600 en AWD-modellen,',
     '<p>De Navimow i210 en i220 Pro, de Navimow X420, de Mova LiDAX Ultra 1600 en AWD-modellen,', 1, 'FAQ 4G: Navimow X420'),
    ('<td>LiDAR en netwerk-RTK</td>', '<td>LiDAR met camera en netwerk-RTK (volgens Navimow)</td>', 2, 'tabellen: navigatie i210/i220 Pro'),
]
META_OUD, META_NIEUW = 'Elf modellen met score en zes zonder score', 'Elf modellen met score en zeven zonder score'

q = api(f'wp/v2/pages/{PID}?context=edit')
if q['status'] != 'publish' or q['slug'] != 'robotmaaier-grote-tuin':
    sys.exit(f'#{PID}: status {q["status"]}, slug {q["slug"]}. Niets gewijzigd.')
raw = q['content']['raw']
meta = q['meta']['_yoast_wpseo_metadesc']
meld = []
for zoek, vervang, n, wat in STAPPEN:
    c = raw.count(zoek)
    if c != n:
        meld.append(f'{wat}: {c} keer gevonden (verwacht {n}).')
    else:
        raw = raw.replace(zoek, vervang)
        print(f'  {wat}: {n}x vervangen')
if 'Cramer AiConic 2' in q['content']['raw']:
    meld.append('Cramer AiConic 2 staat al op de pagina.')
if meta.count(META_OUD) != 1:
    meld.append(f'metabeschrijving: "{META_OUD}" {meta.count(META_OUD)} keer gevonden (verwacht 1).')
else:
    meta = meta.replace(META_OUD, META_NIEUW)
    print('  metabeschrijving: zes -> zeven')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde84-pagina15-schrijf-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({k: q[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta', 'modified')}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api(f'wp/v2/pages/{PID}', {'content': raw, 'meta': {'_yoast_wpseo_metadesc': meta}})
n = api(f'wp/v2/pages/{PID}?context=edit')
print(f'#{PID} opgeslagen; status {n["status"]}; inhoud zoals bedoeld: {n["content"]["raw"] == raw}; '
      f'metabeschrijving zoals bedoeld: {n["meta"]["_yoast_wpseo_metadesc"] == meta}')
