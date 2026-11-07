#!/usr/bin/env python3
"""Ronde 105, MET DE HAND (zonder thema-zip): gerichte vervangingen (via scripts/ronde88_lib.py: kopie vooraf, elke
zoektekst precies 1x, anders schrijft hij niets; status blijft gelijk).
1. Hub #10, "Waarom deze" Dreame A1 Pro: "het grootste opgegeven oppervlak (2.000 m²)" en "3,91" (de enige plek op de
   gepubliceerde pagina's buiten de kaarten; gezocht op 7 november 2026).
2. Kopen-pagina #508, FAQ abonnement: "… proefdata van 7 dagen volgens de FAQ van Eufy".
Gebruik:  python3 scripts/ronde105.py [--schrijf]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
from ronde88_lib import pas_toe

SCHRIJF = '--schrijf' in sys.argv
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGINAS = {
    10: [('<strong>Waarom deze:</strong> het grootste opgegeven oppervlak (2.000 m²) en de goedkoopste link-module',
          '<strong>Waarom deze:</strong> een opgegeven oppervlak tot 2.000 m² en de goedkoopste link-module', '1 hub, oppervlak'),
         ('de app staat op 3,91 in Google Play', 'de app staat op 3,87 in Google Play', '1 hub, app-rating')],
    508: [('bij de Eufy E15 en E18 alleen proefdata van 7 dagen', 'bij de Eufy E15 en E18 alleen proefdata van 7 dagen volgens de FAQ van Eufy',
           '2 FAQ abonnement')],
}
meld = []
for pid, st in PAGINAS.items():
    if api(f'wp/v2/pages/{pid}?context=edit&_fields=status')['status'] != 'publish':
        meld.append(f'#{pid}: geen publish')
    meld += pas_toe(pid, st, False, 'r105')[1]
if meld or not SCHRIJF:
    sys.exit('Meldingen: ' + str(meld) if meld else 0)
for pid, st in PAGINAS.items():
    pas_toe(pid, st, True, 'r105')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
