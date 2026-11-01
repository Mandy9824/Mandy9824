#!/usr/bin/env python3
"""Ronde 79: modelgegevens via de dataroute (/rmk/v1/modellen), alleen:
  --stap m058   M058: specs.alarm en scores uit de omzetting van het nieuwe Excel-bestand (alarm 0, status gecontroleerd,
                31-10-2026; daardoor veiligheid 3,75 en functiescore 79,5). Verder verandert er niets aan M058.
  --stap m055   M055: beste_voor = "Tuinen tot 1.500 m² zonder begrenzingsdraad, met RTK via een gateway op je router"
                (tekst van Mandy; ook in scripts/modellen_teksten.json). Verder verandert er niets.
Alle andere modellen en de algemene velden blijven ongewijzigd; het script weigert anders. Opslaan via de dataroute
leegt ook de LiteSpeed-cache. Wachtwoord alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde79_modellen.py --stap m058 <omzetting.json> [--schrijf]
          python3 scripts/ronde79_modellen.py --stap m055 [--schrijf]
"""
import copy, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
STAP = sys.argv[sys.argv.index('--stap') + 1]
M055_TEKST = 'Tuinen tot 1.500 m² zonder begrenzingsdraad, met RTK via een gateway op je router'
TOTAAL = {'M058': 79.5}

live = api('rmk/v1/modellen')['data']
nieuw = copy.deepcopy(live)
N = {m['id']: m for m in nieuw['modellen']}
L = {m['id']: m for m in live['modellen']}
if STAP == 'm058':
    bron = next(a for a in sys.argv[1:] if a.endswith('.json'))
    o = next(m for m in json.load(open(bron, encoding='utf-8'))['modellen'] if m['id'] == 'M058')
    anders = sorted(k for k in set(o) | set(L['M058']) if o.get(k) != L['M058'].get(k))
    specs = sorted(k for k in set(o['specs']) | set(L['M058']['specs']) if o['specs'].get(k) != L['M058']['specs'].get(k))
    assert anders == ['scores', 'specs'] and specs == ['alarm'], f'M058: meer verschillen in de omzetting: {anders} {specs}'
    assert o['specs']['alarm']['waarde'] == 0 and o['specs']['alarm']['status'] == 'gecontroleerd', 'alarm niet 0/gecontroleerd'
    sc = {k for k in o['scores'] if o['scores'][k] != L['M058']['scores'].get(k)}
    assert sc == {'veiligheid'}, f'scores: {sc}'
    N['M058']['specs']['alarm'] = copy.deepcopy(o['specs']['alarm'])
    N['M058']['scores'] = copy.deepcopy(o['scores'])
    ID = 'M058'
elif STAP == 'm055':
    assert not L['M055'].get('beste_voor'), 'M055 heeft al een beste_voor'
    N['M055']['beste_voor'] = M055_TEKST
    ID = 'M055'
else:
    sys.exit('Onbekende stap.')

gelijk = all(a == b for a, b in zip(live['modellen'], nieuw['modellen']) if a['id'] != ID) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
velden = sorted(k for k in N[ID] if N[ID][k] != L[ID].get(k))
print(f'{ID}: gewijzigde velden {velden}; andere modellen en algemene velden ongewijzigd: {gelijk}')
if ID == 'M058':
    print('  alarm', L[ID]['specs']['alarm']['waarde'], L[ID]['specs']['alarm']['status'], '->',
          N[ID]['specs']['alarm']['waarde'], N[ID]['specs']['alarm']['status'], '| veiligheid',
          L[ID]['scores']['veiligheid'], '->', N[ID]['scores']['veiligheid'])
if not gelijk:
    sys.exit('Andere gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
pad = f'backups/modellen-voor-ronde79-{STAP}-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
