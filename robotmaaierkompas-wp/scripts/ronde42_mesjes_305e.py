#!/usr/bin/env python3
"""Ronde 42 (17 oktober 2026, opdracht van Mandy): mesjespagina (#236).
1. Zin "Voor andere Husqvarna-modellen hebben we de mesjes nog niet uitgezocht." vervangen.
2. Bronnen voor de Automower 305E NERA toevoegen, direct na de twee 410VE NERA-regels. Bron: blad Bronnen van
   robotmaaierkompas_modeldata_v1.xlsx (17 oktober), M020, veld "Extra kosten: messen" (drie URL's: Endurance-messen,
   Classic-messen, handleiding 305E/310E NERA par. 7.1 voor de vervangtermijn), datum 17 oktober 2026. Het Excel-bestand
   staat niet in de repository; de URL's staan hieronder. Geen dubbele regels.
Elke "Was"-tekst moet precies één keer voorkomen; anders schrijft het script niets. De pagina houdt haar status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde42_mesjes_305e.py [--schrijf]
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
p = api('wp/v2/pages/236?context=edit')
raw = p['content']['raw']
nieuw = raw
meld = []


def regel(url, tekst, chip):
    return (f'<li><div><a href="{url}">{tekst}</a><div class="rmk-sources__meta"><span class="rmk-chip">{chip}</span>'
            f'<span>geraadpleegd op 17 oktober 2026</span></div></div></li>')


BRONNEN = [
    regel('https://www.husqvarna.com/nl/robotmaaiermessen/endurance-blades/?fits-to=970819612', 'Husqvarna Automower 305E NERA: Endurance-messen, prijs', 'Fabrikant'),
    regel('https://www.husqvarna.com/nl/robotmaaiermessen/classic-blades/?fits-to=970819612', 'Husqvarna Automower 305E NERA: Classic-messen, prijs', 'Fabrikant'),
    regel('https://www.husqvarna.com/hbd/tdrdownload/v2/pub000105498/doc000264944/OM/KO5PMFpHS7mEYGp-jHJrxxg0ETw',
          'Husqvarna Automower 305E NERA: vervangtermijn messen', 'Handleiding'),
]

was = 'Voor andere Husqvarna-modellen hebben we de mesjes nog niet uitgezocht.'
wordt = 'Voor andere Husqvarna-modellen dan de 410VE NERA en de 305E NERA hebben we de mesjes nog niet uitgezocht.'
if nieuw.count(was) == 1:
    nieuw = nieuw.replace(was, wordt)
    print(f'  zin:\n    was:   {was}\n    wordt: {wordt}')
else:
    meld.append(f'Zin {nieuw.count(was)} keer gevonden (verwacht 1).')

b = nieuw.find('>Bronnen<')
bestaande_urls = set(re.findall(r'<li><div><a href="([^"]+)"', nieuw[b:]))
toe = [r for r in BRONNEN if re.search(r'href="([^"]+)"', r).group(1) not in bestaande_urls]
anker = re.findall(r'<li><div><a href="[^"]+">Husqvarna Automower 410VE NERA: vervangtermijn messen</a>.*?</li>', nieuw[b:], re.S)
if len(anker) == 1 and toe:
    nieuw = nieuw[:b] + nieuw[b:].replace(anker[0], anker[0] + ''.join('\n' + r for r in toe), 1)
    print(f'  bronnen: {len(toe)} regels na "410VE NERA: vervangtermijn messen"')
elif not toe:
    print('  bronnen: staan er al')
else:
    meld.append(f'Ankerregel 410VE NERA vervangtermijn {len(anker)} keer gevonden.')

print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde42-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({'236': {'status': p['status'], 'content': raw}}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api('wp/v2/pages/236', {'content': nieuw})
q = api('wp/v2/pages/236?context=edit')
print(f'#236 opgeslagen; status {q["status"]} (was {p["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == nieuw}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
