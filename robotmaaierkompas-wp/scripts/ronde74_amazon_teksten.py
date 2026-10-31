#!/usr/bin/env python3
"""Teksten voor het moment dat de Amazon-knoppen live gaan (tekstwijzigingen-amazon-affiliate.md, punten 1-8).

KLAARGEZET, NIET GEDRAAID. Pas met --schrijf als Mandy meldt dat "Amazon aan" mag, op hetzelfde moment als
RMK_AMAZON_ACTIVE in wp-config.php. Tot dan blijven de huidige teksten (bol.com en Coolblue) staan.

1. #81 affiliate-melding: eerste zin aangepast; alinea "Als Amazon-partner …" aan het einde. 2. #77 over-ons.
3. #80 colofon. 4. #76 hoe-we-beoordelen, "Zo verdienen we geld". 5. footer (template part, alle pagina's).
6. #82 privacy, punt "Winkels en affiliatenetwerken". 7. #83 cookies: rij onder "Cookies van Coolblue en Awin na een klik".
8. instelling rmk_advertentie_tekst (regel boven de eerste knop).
Komt een "Was"-tekst niet precies één keer voor, dan schrijft het script niets en meldt het waar. Het script weigert
ook als het thema ouder is dan 1.3.13 of als het statusoverzicht niet "Amazon-knop zichtbaar" meldt.
Met --schrijf eerst een volledige kopie van de zes pagina's, de footer en de instelling in backups/ (niet in git).
Terugdraaien: scripts/ronde74_amazon_terug.py.

Gebruik:  python3 scripts/ronde74_amazon_teksten.py            (proefdraai, schrijft niets)
          python3 scripts/ronde74_amazon_teksten.py --schrijf  (alleen na "Amazon aan" van Mandy)
          python3 scripts/ronde74_amazon_teksten.py --stand <stand.json>  (proefdraai op een opgeslagen stand, voor tests)
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api, lees, toepassen, schrijf
from amazon_teksten_lib import AAN, ADVERTENTIE

if '--stand' in sys.argv:
    stand = json.load(open(sys.argv[sys.argv.index('--stand') + 1], encoding='utf-8'))
    stand['inhoud'] = {(int(k) if k.isdigit() else k): v for k, v in stand['inhoud'].items()}
else:
    stand = lees()
print(f'Actief thema {stand["thema"]}; advertentie-tekst nu {stand["advertentie"]!r}')
nieuw, meld, log = toepassen(stand['inhoud'], AAN)
print('\n'.join(log))
print(f'  instelling rmk_advertentie_tekst:\n    was:   {stand["advertentie"]!r}\n    wordt: {ADVERTENTIE!r}')
klaar = []  # voorwaarden voor --schrijf (geen tekstmeldingen)
if tuple(int(x) for x in re.findall(r'\d+', stand['thema'] or '')[:3]) < (1, 3, 13):
    klaar.append(f'thema {stand["thema"]} is ouder dan 1.3.13 (geen Amazon-knop).')
if '--stand' not in sys.argv:
    status = api('rmk/v1/status')
    regels = status if isinstance(status, list) else status.get('controles', status.get('checks', []))
    am = [r for r in regels if isinstance(r, dict) and str(r.get('label', '')).startswith('Amazon-knop')]
    if not am or 'Amazon-knop zichtbaar' not in str(am[0].get('info', am[0].get('detail', ''))):
        klaar.append('statusoverzicht meldt geen "Amazon-knop zichtbaar" (RMK_AMAZON_TAG of RMK_AMAZON_ACTIVE ontbreekt).')
print('\nMeldingen over de teksten:' if meld else '\nGeen meldingen over de teksten: alle "Was"-teksten precies één keer gevonden (of al toegepast).')
for m in meld:
    print('  - ' + m)
for m in klaar:
    print('  (nog niet klaar voor --schrijf) ' + m)
if '--schrijf' not in sys.argv:
    sys.exit(1 if meld else 0)
if meld or klaar or '--stand' in sys.argv:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/amazon-teksten-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
with open(pad, 'w', encoding='utf-8') as f:
    json.dump(stand, f, ensure_ascii=False, indent=1, default=str)
print(f'Kopie van de oude teksten: {pad}')
schrijf(stand, nieuw, ADVERTENTIE)
