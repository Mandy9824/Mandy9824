#!/usr/bin/env python3
"""Ronde 110: gerichte vervangingen MET DE HAND (via ronde88_lib.pas_toe; kopie vooraf, elke zoektekst precies 1x,
status blijft gelijk). Publiceert niets.
1. /robotmaaier-gps/ (#559, concept): bron bij de Husqvarna 305 (Connect Kit-pagina i.p.v. handleiding) en de
   tegenstrijdigheid bij de Stihl iMOW 3 EVO (eSIM).
2. /robotmaaier-grote-tuin/ (#15, gepubliceerd): de zin over de 310E NERA die "stopt" vervangen door de
   formulering uit het blad Reviews. Vooraf: de pagina moet nog dezelfde wijzigingsdatum hebben als bij de
   controle van ronde 109 (2026-11-23T13:15:12) en de status publish.
Daarna LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde110.py            (proefdraai, schrijft niets)
          python3 scripts/ronde110.py --schrijf
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
from ronde88_lib import pas_toe

SCHRIJF = '--schrijf' in sys.argv

GPS = [
    ('komen met de Connect Kit van 329 euro volgens de handleiding GPS-positie en alarm in de app erbij',
     'komen met de Connect Kit van 329 euro volgens de Connect Kit-pagina van Husqvarna GPS-positie en alarm in de app erbij',
     'Husqvarna 305: bron Connect Kit-pagina'),
    ('De Stihl iMOW 3 EVO heeft volgens de handleiding een mobiele verbinding (eSIM), maar werkt met begrenzingsdraad',
     'De Stihl iMOW 3 EVO heeft volgens de handleiding een mobiele verbinding (eSIM); de vergelijkingstabel van Stihl zegt dat niet. Hij werkt met begrenzingsdraad',
     'Stihl iMOW 3 EVO: eSIM tegenstrijdig'),
]
GROTE_TUIN = [
    ('bij de Husqvarna 310E NERA werd in reviews (vertaald, niet in onze score) genoemd dat de maaier stopt als het satellietsignaal wegvalt',
     'bij de Husqvarna 310E NERA werd in vier gelezen reviews (vertaald, niet in onze score) satelliet- of verbindingsverlies of slechte GPS-dekking onder bomen genoemd',
     '310E NERA: reviews zoals blad Reviews'),
]

p15 = api('wp/v2/pages/15?context=edit&_fields=id,status,modified')
p559 = api('wp/v2/pages/559?context=edit&_fields=id,status,modified')
vooraf = []
if p15['status'] != 'publish' or p15['modified'] != '2026-11-23T13:15:12':
    vooraf.append(f'#15: status {p15["status"]}, gewijzigd {p15["modified"]} (verwacht publish, 2026-11-23T13:15:12): pagina is aangepast.')
if p559['status'] != 'draft':
    vooraf.append(f'#559: status {p559["status"]}, verwacht draft.')
if vooraf:
    sys.exit('Niets gedaan:\n  ' + '\n  '.join(vooraf))
print(f'#15 ongewijzigd sinds {p15["modified"]}; #559 concept (gewijzigd {p559["modified"]}).')

# Eerst beide als proef, zodat er niets geschreven wordt als één van de twee een melding heeft
meld = pas_toe(559, GPS, False, 'r110')[1] + pas_toe(15, GROTE_TUIN, False, 'r110')[1]
if not SCHRIJF or meld:
    sys.exit('Niets geschreven vanwege de meldingen.' if meld else 0)
pas_toe(559, GPS, True, 'r110')
pas_toe(15, GROTE_TUIN, True, 'r110')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
