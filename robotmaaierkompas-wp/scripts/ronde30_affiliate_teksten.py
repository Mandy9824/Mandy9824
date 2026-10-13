#!/usr/bin/env python3
"""Teksten voor het moment dat de Bol-links live gaan (tekstwijzigingen-affiliate-live.md, Mandy, 13 oktober 2026).

KLAARGEZET, NIET GEDRAAID. Pas met --schrijf als Mandy zegt dat RMK_AFFILIATE_ACTIVE aan mag, op hetzelfde moment.
Tot dan blijven de huidige teksten ("Op dit moment verdienen we niets aan de links…") staan.

1. #81 affiliate-melding: eerste alinea vervangen; slotalinea toevoegen (de alinea "Dat verandert de score of de
   volgorde niet…" blijft). 2. #77 over-ons. 3. #80 colofon. 4. #76 hoe-we-beoordelen, "Zo verdienen we geld".
5. footer (template part). 6. #82 privacy, punt "Winkels en affiliatenetwerken": zin erachter. 7. #83 cookies: tabelrij.
8. instelling rmk_advertentie_tekst (regel boven de eerste Bol-knop). De Bol-regel zelf (knop, rel="sponsored nofollow",
   "Je gaat naar bol.com. Bron: bol.com.") staat al in het thema.
De teksten staan in scripts/affiliate_teksten_lib.py. Komt een "Was"-tekst niet precies één keer voor, dan schrijft het
script niets. Met --schrijf eerst een volledige kopie van de zeven teksten en de instelling in backups/ (niet in git).
Terugdraaien: scripts/ronde30_affiliate_terug.py.

Gebruik:  python3 scripts/ronde30_affiliate_teksten.py            (proefdraai, schrijft niets)
          python3 scripts/ronde30_affiliate_teksten.py --schrijf  (alleen na akkoord van Mandy)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import AAN, ADVERTENTIE, lees, toepassen, schrijf

stand = lees()
print(f'Actief thema {stand["thema"]}; advertentie-tekst nu {stand["advertentie"]!r}')
nieuw, meld, log = toepassen(stand['inhoud'], AAN)
print('\n'.join(log))
if tuple(int(x) for x in re.findall(r'\d+', stand['thema'] or '')[:3]) < (1, 3, 7):
    meld.append(f'thema {stand["thema"]} is ouder dan 1.3.7.')
print('\nMeldingen:' if meld else '\nGeen meldingen: alle "Was"-teksten precies één keer gevonden (of al toegepast).')
for m in meld:
    print('  - ' + m)
if '--schrijf' not in sys.argv:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/affiliate-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
with open(pad, 'w', encoding='utf-8') as f:
    json.dump({k: v for k, v in stand.items()}, f, ensure_ascii=False, indent=1, default=str)
print(f'Kopie van de oude teksten: {pad}')
schrijf(stand, nieuw, ADVERTENTIE)
