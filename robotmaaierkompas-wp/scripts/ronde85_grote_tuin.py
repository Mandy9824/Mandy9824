#!/usr/bin/env python3
"""Ronde 85: één gerichte vervanging op /robotmaaier-grote-tuin/ (#15, gepubliceerd; MET DE HAND gewijzigd, niet opnieuw bouwen).
"De zeven modellen zonder score hebben we alleen op basisniveau uitgezocht." ->
"Zes van de zeven modellen zonder score hebben we op basisniveau uitgezocht; de Cramer AiConic 2 is breder uitgezocht,
maar zonder handleiding is er geen score."
Kopie vooraf in backups/. Komt de zin niet precies één keer voor, dan schrijft het script niets. Status blijft publish.
Gebruik:  python3 scripts/ronde85_grote_tuin.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PID = 15
OUD = 'De zeven modellen zonder score hebben we alleen op basisniveau uitgezocht.'
NIEUW = ('Zes van de zeven modellen zonder score hebben we op basisniveau uitgezocht; de Cramer AiConic 2 is breder '
         'uitgezocht, maar zonder handleiding is er geen score.')

q = api(f'wp/v2/pages/{PID}?context=edit')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde85-pagina15-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({k: q[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta', 'modified')}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad, '| status', q['status'], '| gewijzigd', q['modified'])
if q['status'] != 'publish' or q['slug'] != 'robotmaaier-grote-tuin':
    sys.exit(f'#{PID}: status {q["status"]}, slug {q["slug"]}. Niets gewijzigd.')
raw = q['content']['raw']
n = raw.count(OUD)
print(f'Zin gevonden: {n} keer (verwacht 1); nieuwe zin al aanwezig: {NIEUW in raw}')
if n != 1 or NIEUW in raw:
    sys.exit('Niets gewijzigd.')
raw = raw.replace(OUD, NIEUW)
if not SCHRIJF:
    sys.exit(0)
api(f'wp/v2/pages/{PID}', {'content': raw})
na = api(f'wp/v2/pages/{PID}?context=edit')
print(f'#{PID} opgeslagen; status {na["status"]}; inhoud zoals bedoeld: {na["content"]["raw"] == raw}; '
      f'metabeschrijving ongewijzigd: {na["meta"]["_yoast_wpseo_metadesc"] == q["meta"]["_yoast_wpseo_metadesc"]}')
