#!/usr/bin/env python3
"""Terugdraaien van scripts/ronde74_amazon_teksten.py: de teksten van na de Coolblue-ronde (bol.com en Coolblue) weer
zetten op #76, #77, #80, #81, #82, #83 en in de footer, en de advertentie-tekst terug naar de Coolblue-tekst.

Gebruik dit samen met het weghalen van RMK_AMAZON_ACTIVE uit wp-config.php (zonder schakelaar geen Amazon-knop).
Werkt per tekststuk: alleen de Amazon-teksten worden vervangen; andere wijzigingen op die pagina's blijven staan.
Komt een tekst niet precies één keer voor, dan schrijft het script niets en meldt het waar.

Gebruik:  python3 scripts/ronde74_amazon_terug.py            (proefdraai, schrijft niets)
          python3 scripts/ronde74_amazon_terug.py --schrijf
          python3 scripts/ronde74_amazon_terug.py --schrijf --backup backups/amazon-teksten-voor-<tijd>.json
              (noodgeval: zet de VOLLEDIGE inhoud van de zes pagina's, de footer en de advertentie-tekst terug zoals in
               die kopie; latere wijzigingen op die pagina's gaan dan verloren)
          python3 scripts/ronde74_amazon_terug.py --stand <stand.json>   (proefdraai op een opgeslagen stand, voor tests)
Pagina's houden hun status. Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import lees, toepassen, schrijf
from amazon_teksten_lib import UIT, ADVERTENTIE_CB


def _int(d):
    return {(int(k) if str(k).isdigit() else k): v for k, v in d.items()}


if '--stand' in sys.argv:
    stand = json.load(open(sys.argv[sys.argv.index('--stand') + 1], encoding='utf-8'))
    stand['inhoud'] = _int(stand['inhoud'])
else:
    stand = lees()
print(f'Actief thema {stand["thema"]}; advertentie-tekst nu {stand["advertentie"]!r}')
backup = sys.argv[sys.argv.index('--backup') + 1] if '--backup' in sys.argv else None
if backup:
    with open(backup, encoding='utf-8') as f:
        kopie = json.load(f)
    nieuw = _int(kopie['inhoud'])
    meld, advertentie = [], kopie.get('advertentie') or ''
    for d in nieuw:
        if nieuw[d] != stand['inhoud'][d]:
            print(f'  {"#" if d != "footer" else ""}{d}: volledige inhoud uit {backup}')
else:
    nieuw, meld, log = toepassen(stand['inhoud'], UIT)
    print('\n'.join(log))
    advertentie = ADVERTENTIE_CB
    print(f'  instelling rmk_advertentie_tekst wordt: {advertentie!r}')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if '--schrijf' not in sys.argv:
    sys.exit(1 if meld else 0)
if meld or '--stand' in sys.argv:
    sys.exit('Niets geschreven vanwege de meldingen. Eventueel: --backup <kopie> (zie boven).')
schrijf(stand, nieuw, advertentie)
