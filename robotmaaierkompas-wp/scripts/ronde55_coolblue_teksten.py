#!/usr/bin/env python3
"""Teksten voor het moment dat de Coolblue-knoppen live gaan (tekstwijzigingen-coolblue-affiliate.md, punten 1-8).

KLAARGEZET, NIET GEDRAAID. Pas met --schrijf als Mandy meldt dat "Coolblue aan" mag, op hetzelfde moment als
RMK_COOLBLUE_ACTIVE in wp-config.php. Tot dan blijven de huidige teksten (alleen bol.com) staan.

1. #81 affiliate-melding: eerste alinea vervangen; slotalinea over Coolblue en Awin toevoegen (aan het einde).
2. #77 over-ons. 3. #80 colofon. 4. #76 hoe-we-beoordelen, "Zo verdienen we geld". 5. footer (template part).
6. #82 privacy, punt "Winkels en affiliatenetwerken". 7. #83 cookies: rij onder "Cookies van bol.com na een klik".
8. instelling rmk_advertentie_tekst (regel boven de eerste knop).
Komt een "Was"-tekst niet precies één keer voor, dan schrijft het script niets en meldt het waar. Het script weigert
ook als het thema ouder is dan 1.3.10 of als het statusoverzicht niet "Coolblue-regel zichtbaar" meldt.
Met --schrijf eerst een volledige kopie van de zeven teksten en de instelling in backups/ (niet in git).
Terugdraaien: scripts/ronde55_coolblue_terug.py.

Gebruik:  python3 scripts/ronde55_coolblue_teksten.py            (proefdraai, schrijft niets)
          python3 scripts/ronde55_coolblue_teksten.py --schrijf  (alleen na "Coolblue aan" van Mandy)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api, lees, toepassen, schrijf
from coolblue_teksten_lib import AAN, ADVERTENTIE

stand = lees()
print(f'Actief thema {stand["thema"]}; advertentie-tekst nu {stand["advertentie"]!r}')
nieuw, meld, log = toepassen(stand['inhoud'], AAN)
print('\n'.join(log))
print(f'  instelling rmk_advertentie_tekst:\n    was:   {stand["advertentie"]!r}\n    wordt: {ADVERTENTIE!r}')
if tuple(int(x) for x in re.findall(r'\d+', stand['thema'] or '')[:3]) < (1, 3, 10):
    meld.append(f'thema {stand["thema"]} is ouder dan 1.3.10 (geen Coolblue-regel).')
status = api('rmk/v1/status')
regels = status if isinstance(status, list) else status.get('controles', status.get('checks', []))
cb = [r for r in regels if isinstance(r, dict) and str(r.get('label', '')).startswith('Coolblue-koppeling')]
if not cb or 'Coolblue-regel zichtbaar' not in str(cb[0].get('info', cb[0].get('detail', ''))):
    meld.append('statusoverzicht meldt geen "Coolblue-regel zichtbaar" (RMK_COOLBLUE_ACTIVE of de constanten ontbreken).')
print('\nMeldingen:' if meld else '\nGeen meldingen: alle "Was"-teksten precies één keer gevonden (of al toegepast).')
for m in meld:
    print('  - ' + m)
if '--schrijf' not in sys.argv:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/coolblue-teksten-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
with open(pad, 'w', encoding='utf-8') as f:
    json.dump({k: v for k, v in stand.items()}, f, ensure_ascii=False, indent=1, default=str)
print(f'Kopie van de oude teksten: {pad}')
schrijf(stand, nieuw, ADVERTENTIE)
