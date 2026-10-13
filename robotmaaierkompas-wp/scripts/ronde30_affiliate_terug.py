#!/usr/bin/env python3
"""Terugdraaien van scripts/ronde30_affiliate_teksten.py: de oude teksten ("Op dit moment verdienen we niets aan de
links…") weer zetten op #76, #77, #80, #81, #82, #83 en in de footer, en de advertentie-tekst leegmaken.

Gebruik dit samen met het weghalen van RMK_AFFILIATE_ACTIVE uit wp-config.php (zonder schakelaar geen Bol-regel).
Werkt per tekststuk: alleen de nieuwe teksten worden vervangen; andere wijzigingen op die pagina's blijven staan.
Komt een nieuwe tekst niet precies één keer voor, dan schrijft het script niets en meldt het waar.

Gebruik:  python3 scripts/ronde30_affiliate_terug.py            (proefdraai, schrijft niets)
          python3 scripts/ronde30_affiliate_terug.py --schrijf
          python3 scripts/ronde30_affiliate_terug.py --schrijf --backup backups/affiliate-voor-<tijd>.json
              (noodgeval: zet de VOLLEDIGE inhoud van de zeven teksten en de advertentie-tekst terug zoals in die kopie;
               latere wijzigingen op die pagina's gaan dan verloren)
Pagina's houden hun status. Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import UIT, lees, toepassen, schrijf

stand = lees()
print(f'Actief thema {stand["thema"]}; advertentie-tekst nu {stand["advertentie"]!r}')
backup = sys.argv[sys.argv.index('--backup') + 1] if '--backup' in sys.argv else None
if backup:
    with open(backup, encoding='utf-8') as f:
        kopie = json.load(f)
    nieuw = {(int(k) if k.isdigit() else k): v for k, v in kopie['inhoud'].items()}
    meld, advertentie = [], kopie.get('advertentie') or ''
    for d in nieuw:
        if nieuw[d] != stand['inhoud'][d]:
            print(f'  #{d}: volledige inhoud uit {backup}')
else:
    nieuw, meld, log = toepassen(stand['inhoud'], UIT)
    print('\n'.join(log))
    advertentie = ''
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if '--schrijf' not in sys.argv:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen. Eventueel: --backup <kopie> (zie boven).')
schrijf(stand, nieuw, advertentie)
