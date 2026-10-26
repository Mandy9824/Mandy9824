#!/usr/bin/env python3
"""Ronde 64: conceptpagina mova-dreame-robotmaaier (#351, concept) aanvullen.
1. Na de alinea "Het korte antwoord.": alinea "Mova en Dreame: één groep, twee merken."
2. Veelgestelde vragen, vooraan: "Is Mova hetzelfde als Dreame?" en "Wat is een Dreame Mova LiDAX Ultra 1200?"
3. Bronnen: eigen kopje "Mova en Dreame" met het persbericht (Business Wire, 21 oktober 2024), vóór het kopje Scoremodel.
Werkt op de live inhoud (het auteursblok is in de editor omgezet; scripts/ronde63/mova-dreame.json is dus niet de bron).
Elk anker moet precies één keer voorkomen en de nieuwe teksten mogen er nog niet staan; anders schrijft het script niets.
Weigert als #351 geen concept is, behalve met --gepubliceerd (ronde 65: de pagina is gepubliceerd zonder deze ronde;
dan blijft ze gepubliceerd). Met --schrijf: eerst een kopie in backups/, dan opslaan (status blijft gelijk),
LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde64_mova_dreame.py [--gepubliceerd] [--schrijf]
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
TOEGESTAAN = ('draft', 'publish') if '--gepubliceerd' in sys.argv else ('draft',)
PID = 351
ALINEA = ('<p><strong>Mova en Dreame: één groep, twee merken.</strong> Mova is een merk van de Dreame-groep. '
          'De LiDAX Ultra-modellen zijn van Mova, de A1 Pro is van Dreame zelf. Winkels en prijsvergelijkers schrijven een '
          'Mova daarom vaak als "Dreame Mova", maar het zijn aparte productlijnen met eigen modellen, apps en garantie.</p>')
VRAGEN = [
    ('Is Mova hetzelfde als Dreame?',
     'Mova is een merk van de Dreame-groep. De techniek lijkt op elkaar, maar de LiDAX Ultra-modellen zijn van Mova en de '
     'A1 Pro van Dreame zelf, met eigen apps (MOVAhome en Dreamehome) en eigen garantie.'),
    ('Wat is een Dreame Mova LiDAX Ultra 1200?',
     'Dat is de Mova LiDAX Ultra 1200: een model van Mova, het merk van de Dreame-groep. De Dreame A1 Pro is een ander '
     'model, van Dreame zelf.'),
]
FAQ = '<div class="rmk-faq">\n'
NIEUWE_VRAGEN = ''.join(f'  <details><summary>{v}</summary><div><p>{a}</p></div></details>\n' for v, a in VRAGEN)
SCOREKOP = ('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">'
            'Scoremodel</h3></div>\n<!-- /wp:html -->\n\n')
BRON = ('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">'
        'Mova en Dreame</h3></div>\n<!-- /wp:html -->\n\n'
        '<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n'
        '<div class="wp-block-group rmk-container rmk-block rmk-column"><!-- wp:html -->\n<ol class="rmk-sources">\n'
        '  <li><div><a href="https://www.businesswire.com/news/home/20241021856800/de">Persbericht van Mova en Dreame '
        '(Business Wire, 21 oktober 2024)</a><div class="rmk-sources__meta"><span class="rmk-chip">Persbericht</span></div></div></li>\n'
        '</ol>\n<!-- /wp:html --></div>\n<!-- /wp:group -->\n\n')

p = api(f'wp/v2/pages/{PID}?context=edit')
if p['status'] not in TOEGESTAAN or p['slug'] != 'mova-dreame-robotmaaier':
    sys.exit(f'#{PID} is {p["slug"]} met status {p["status"]}; verwacht {TOEGESTAAN}. Niets gewijzigd.')
raw = oud = p['content']['raw']
meld = []
for t in ('één groep, twee merken', VRAGEN[0][0], VRAGEN[1][0], 'businesswire.com'):
    if t in raw:
        meld.append(f'"{t}" staat er al.')
# 1. de alinea "Het korte antwoord." (van <p> tot en met </p>)
kort = re.findall(r'<p><strong>Het korte antwoord\.</strong>.*?</p>', raw, re.S)
stappen = []
if len(kort) == 1:
    stappen.append((kort[0], kort[0] + '\n' + ALINEA, 'alinea na "Het korte antwoord."'))
else:
    meld.append(f'alinea "Het korte antwoord.": {len(kort)} keer gevonden (verwacht 1).')
stappen += [(FAQ, FAQ + NIEUWE_VRAGEN, 'twee vragen vooraan in de FAQ'),
            (SCOREKOP, BRON + SCOREKOP, 'bron persbericht vóór Scoremodel')]
for was, wordt, wat in stappen:
    n = raw.count(was)
    if n != 1:
        meld.append(f'{wat}: anker {n} keer gevonden (verwacht 1).')
    else:
        raw = raw.replace(was, wordt, 1)
        print(f'  {wat}: toegevoegd')
print(f'#{PID} status {p["status"]}')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde64-pagina351-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({k: p[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta')}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api(f'wp/v2/pages/{PID}', {'content': raw})
q = api(f'wp/v2/pages/{PID}?context=edit')
print(f'#{PID} opgeslagen; status {q["status"]} (was {p["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw}; '
      f'metabeschrijving ongewijzigd: {q["meta"].get("_yoast_wpseo_metadesc") == p["meta"].get("_yoast_wpseo_metadesc")}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
