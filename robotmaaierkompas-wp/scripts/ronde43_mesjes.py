#!/usr/bin/env python3
"""Ronde 43, stap 4: mesjespagina (#236).
- "Wat we nog niet weten": zin over Gardena en andere Husqvarna-modellen vervangen.
- Tabelrij "Husqvarna Automower 305E NERA" -> "Husqvarna Automower 305E en 310E NERA" (alleen de modelnaam).
Elke "Was"-tekst moet precies één keer voorkomen; anders schrijft het script niets. De pagina houdt haar status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde43_mesjes.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
p = api('wp/v2/pages/236?context=edit')
raw = p['content']['raw']
nieuw, meld = raw, []
for was, wordt in (
        ('De mesjes van Gardena en andere Husqvarna-modellen: die hebben we nog niet uitgezocht.',
         'De mesjes van Gardena en van andere Husqvarna-modellen dan de 410VE NERA, 305E NERA en 310E NERA: die hebben we nog niet uitgezocht.'),
        ('<th scope="row">Husqvarna Automower 305E NERA</th>', '<th scope="row">Husqvarna Automower 305E en 310E NERA</th>')):
    if nieuw.count(was) != 1:
        meld.append(f'"{was[:60]}…" {nieuw.count(was)} keer gevonden (verwacht 1).')
        continue
    nieuw = nieuw.replace(was, wordt)
    print(f'  was:   {was}\n  wordt: {wordt}')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde43-mesjes-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({'236': {'status': p['status'], 'content': raw}}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api('wp/v2/pages/236', {'content': nieuw})
q = api('wp/v2/pages/236?context=edit')
print(f'#236 opgeslagen; status {q["status"]} (was {p["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == nieuw}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
