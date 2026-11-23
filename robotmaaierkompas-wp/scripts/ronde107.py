#!/usr/bin/env python3
"""Ronde 107: Stihl-pagina #22, de tekst van de alinea "Het korte antwoord." gericht vervangen.
"<strong>Het korte antwoord.</strong> " blijft staan; alleen de tekst daarna tot </p> wordt vervangen.
De oude tekst moet precies gelijk zijn aan OUD en precies één keer voorkomen; anders schrijft het script niets.
Pagina houdt zijn status. Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute.
Gebruik:  python3 scripts/ronde107.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PID = 22
KOP = '<p><strong>Het korte antwoord.</strong> '
OUD = (KOP + 'Nee: Stihl verkoopt in Nederland negen iMOW-robotmaaiers en ze werken allemaal met begrenzingsdraad. '
       'Een draadloze Stihl hebben we niet gevonden. Wil je geen draad aanleggen, kijk dan naar '
       '<a href="/robotmaaier-zonder-draad/">robotmaaier zonder draad</a>. Kies je toch een Stihl, dan bepaalt je '
       'gazon het model: de iMOW 3 is er voor 500 m², de 4 voor 1.000 m², de 5 voor 1.500 m², de 6 EVO voor '
       '3.000 m² en de 7 voor 5.000 m². De EVO-varianten halen 45% helling in plaats van 40%. Let op: de '
       'installatiekit met draad zit niet in de doos en kost 87 of 229 euro.</p>')
NIEUW = (KOP + 'Nee: alle negen iMOW-robotmaaiers die Stihl in Nederland verkoopt werken met begrenzingsdraad. '
         'Wil je geen draad, kijk dan bij onze <a href="/robotmaaier-zonder-draad/">robotmaaiers zonder draad</a>. '
         'Heb je een helling? De iMOW EVO-modellen halen 45% en volgens Stihl met een Upgrade Kit 50 of 55%; zie '
         '<a href="/robotmaaier-helling/">robotmaaier voor hellingen</a> voor de vergelijking.</p>')

p = api(f'wp/v2/pages/{PID}?context=edit')
raw = p['content']['raw']
meld = []
if p['status'] != 'publish':
    meld.append(f'status {p["status"]}, verwacht publish')
if raw.count(KOP) != 1:
    meld.append(f'"Het korte antwoord." {raw.count(KOP)} keer (verwacht 1)')
if raw.count(OUD) != 1:
    meld.append(f'oude alinea {raw.count(OUD)} keer gevonden (verwacht 1)')
# controle modelgegevens: aantal Stihl-modellen en draad
st = [m for m in api('rmk/v1/modellen')['data']['modellen'] if m['merk'] == 'Stihl']
draad = sum(1 for m in st if m['specs'].get('begrenzingsdraad', {}).get('waarde') == 'ja')
print(f'Stihl in modelgegevens: {len(st)} modellen, met begrenzingsdraad: {draad}')
if len(st) != 9 or draad != 9:
    meld.append(f'"negen" en "allemaal met draad" kloppen niet: {len(st)} modellen, {draad} met draad')
print('Meldingen:' if meld else 'Geen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
nieuw = raw.replace(OUD, NIEUW, 1)
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde107-pagina{PID}-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(PID): {'status': p['status'], 'content': raw}}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api(f'wp/v2/pages/{PID}', {'content': nieuw})
q = api(f'wp/v2/pages/{PID}?context=edit')
print(f'#{PID} opgeslagen; status {q["status"]} (was {p["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == nieuw}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
