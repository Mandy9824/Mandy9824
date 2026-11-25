#!/usr/bin/env python3
"""Ronde 116: /stilste-robotmaaier/ (#574) vier gerichte vervangingen MET DE HAND (via ronde88_lib.pas_toe: kopie vooraf,
elke zoektekst precies 1x, status blijft gelijk). Publiceert niets (Mandy had de pagina al gepubliceerd).
Daarna: controle dat elke nieuwe zin precies 1x en elke oude zin 0x voorkomt, en LiteSpeed legen via de dataroute.
Gebruik:  python3 scripts/ronde116.py            (proefdraai, schrijft niets)
          python3 scripts/ronde116.py --schrijf
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
from ronde88_lib import pas_toe

SCHRIJF = '--schrijf' in sys.argv
STAPPEN = [
    ('de Cramer RM-modellen noemen 57 zonder te zeggen om welk soort geluidsniveau het gaat',
     'de Cramer RM1000 tot en met RM2700 noemen 57 zonder te zeggen om welk soort geluidsniveau het gaat',
     '1. Stil per tuingrootte, rij Met draad'),
    ('Bij de Cramer RM-modellen (57) en de Worx Landroid S en L (67, zonder score) noemt',
     'Bij de Cramer RM1000 tot en met RM2700 (57) en de Worx Landroid S en L (67, zonder score) noemt',
     '2. Waarom sommige modellen luider zijn, Met draad kan ook stil zijn'),
    ('Bij de Cramer RM-modellen (57) en de Worx Landroid S en L (67) is niet vermeld',
     'Bij de Cramer RM1000 tot en met RM2700 (57) en de Worx Landroid S en L (67) is niet vermeld',
     '3. FAQ Is een robotmaaier met draad stiller?'),
    ('Het geluid van de Worx Landroid 4WD WR342E en de Cramer AiConic-modellen: dat hebben we niet gevonden.',
     'Het geluid per type bij de Worx Landroid 4WD WR342E (57 of 58 dB(A), niet per type vermeld) en bij de Cramer AiConic-modellen (niet gevonden).',
     '4. Wat we nog niet weten, WR342E en AiConic'),
]

raw, meld = pas_toe(574, STAPPEN, SCHRIJF, 'r116')
if not SCHRIJF:
    sys.exit(1 if meld else 0)
q = api('wp/v2/pages/574?context=edit&_fields=status,content')
ok = True
for oud, nieuw, wat in STAPPEN:
    n_nieuw, n_oud = q['content']['raw'].count(nieuw), q['content']['raw'].count(oud)
    print(f'  {wat}: nieuwe zin {n_nieuw}x, oude zin {n_oud}x')
    ok &= n_nieuw == 1 and n_oud == 0
print('status', q['status'], '| alle vier precies 1x:', ok)
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
sys.exit(0 if ok else 1)
