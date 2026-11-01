#!/usr/bin/env python3
"""Ronde 89: gerichte vervangingen op gepubliceerde pagina's (MET DE HAND; niets bouwen), met kopie vooraf per pagina
(scripts/ronde88_lib.py). Elke zoektekst moet precies één keer voorkomen, anders schrijft het script niets voor die pagina.
Niet uitgevoerd (gemeld): de scoretabel op pagina 1 staat al op score (de shortcode sorteert zelf; alleen de kaarten staan
anders); "elf modellen met score" staat niet in het korte antwoord van #15 (alleen de metabeschrijving is aangepast).
Gebruik:  python3 scripts/ronde89_paginas.py [--schrijf]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ronde88_lib import pas_toe
from affiliate_teksten_lib import api
SCHRIJF = '--schrijf' in sys.argv
KT_OUD = '<li><a href="/robotmaaier-kleine-tuin/">Robotmaaier voor een kleine tuin</a>: twaalf modellen tot 600 m².</li>'
KT_NIEUW = KT_OUD.replace('twaalf', 'vijftien')
KT = (KT_OUD, KT_NIEUW, '6 Meer lezen: kleine tuin vijftien modellen')
SIT_OUD, SIT_NIEUW = 'Grote tuin tot ongeveer 1.500 m², systematisch maaien', 'Grote tot zeer grote tuin (tot 4.800 m²)'
STAPPEN = {
    21: [('Het geluid is het gemeten geluidsvermogen (LWA); winkels noemen vaak de waargenomen waarde.',
          'Het geluid is het geluidsvermogen (LWA) uit de handleiding: bij de city 250 de gegarandeerde waarde, bij de andere modellen '
          'de gemeten waarde; winkels noemen vaak de waargenomen waarde.', '1a voetnoot geluid'),
         ('<td>Display met toetsen</td>', '<td>Display met toetsen en Bluetooth-app</td>', '1b city 250 verbinding'),
         ('bij de max 1200 werken kaart, zones en volgen alleen met een losse smart Gateway',
          'bij de max 1200 werken kaart en zones alleen met een losse smart Gateway; GPS-tracking heeft hij ook met die gateway niet', '1c Smart Gateway'),
         ('Gardena verkoopt ze zelf niet meer of heeft ze niet op voorraad', 'Gardena heeft ze niet op voorraad of noemt ze een voorgaand model', '1d korte antwoord'),
         ('Gardena verkoopt hem zelf niet meer en een aantal winkels noemt hem niet meer leverbaar.',
          'Gardena heeft hem niet op voorraad en een aantal winkels noemt hem niet meer leverbaar.', '1d FAQ minimo'),
         KT],
    11: [('<td>Twaalf modellen tot 600 m² vergeleken,', '<td>Vijftien modellen tot 600 m² vergeleken,', '2 keuzetabel (met hoofdletter)')],
    10: [(f'<th scope="row">{SIT_OUD}</th>', f'<th scope="row">{SIT_NIEUW}</th>', '3 tabelrij'),
         ('<h3>Grote tuin, systematisch maaien: Husqvarna Automower 430V NERA</h3>', f'<h3>{SIT_NIEUW}: Husqvarna Automower 430V NERA</h3>', '3 kop onderdeel')],
    16: [('Voor zeven van de twaalf modellen hebben we geen reviews gevonden, waaronder de Roborock Q105 en de Stihl iMOW 3 EVO.',
          'Voor de meeste modellen hebben we geen reviews gevonden, waaronder de Roborock Q105 en de Stihl iMOW 3 EVO.', '4 betrouwbaarheid')],
    15: [KT],
    20: [('Voor de V-modellen hebben we de prijs niet gevonden.',
          'Voor de 308V, 312V en Aspire R6V is de Connect Kit één kit van 209 euro (adviesprijs) en het EPOS RS1-referentiestation 309 euro; '
          'beide koop je alleen in de winkel en installeert een dealer. Wat die rekent, hebben we niet gevonden. De NL-pagina van het '
          "referentiestation noemt deze drie modellen niet in de lijst 'geschikt voor', terwijl hun productpagina's het wel als optie noemen.", '7a kosten'),
         ('en wat de Connect Kit voor de V-modellen kost', 'en wat een dealer rekent voor het inbouwen van de Connect Kit of het referentiestation', '7b Wat we nog niet weten'),
         KT],
}
for pid in (264, 22, 24, 351, 366):
    STAPPEN[pid] = [KT]
META15 = {'_yoast_wpseo_metadesc': (
    'Welke robotmaaier past in een grote tuin van 1.000 tot 3.000 m²? Elf modellen met score en zeven zonder score vergeleken op oppervlak, helling, geluid en 4G.',
    'Welke robotmaaier past in een grote tuin van 1.000 tot 3.000 m²? Veertien modellen met score en zeven zonder score vergeleken op oppervlak, helling, geluid en 4G.')}
for pid, st in STAPPEN.items():
    print(f'\n=== #{pid}')
    pas_toe(pid, st, SCHRIJF, 'r89', meta=META15 if pid == 15 else None)
