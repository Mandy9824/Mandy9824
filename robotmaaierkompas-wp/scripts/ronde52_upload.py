#!/usr/bin/env python3
"""Ronde 52: modelgegevens M025 tot en met M045 en de verbinding van M023/M024 (dataroute /rmk/v1/modellen).

- M001-M022 en de algemene velden blijven ONGEWIJZIGD.
- M023 en M024: alleen "verbinding" (Bluetooth, scripts/verbinding_toewijzing.json); verder ongewijzigd.
- M025: alleen het geluid (specs.geluid_dba: 58 dB(A), gegarandeerd); verder ongewijzigd. Geen verbinding (geen chip).
- M026-M045 (Stihl iMOW, Cramer) nieuw uit de omzetting (excel_naar_json.py --uit <json>), met fabrikantpagina;
  M026 en M027 met de teksten uit modellen-teksten-stihl.json. M035: extra installatiekosten leeg. Geen EAN, Bol of prijs.
Het script weigert als er meer verandert dan dit. Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde52_upload.py <omzetting.json>            (proefdraai)
          python3 scripts/ronde52_upload.py <omzetting.json> --schrijf
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--'))
NIEUW = [f'M{n:03d}' for n in range(26, 46)]
D = os.path.dirname(os.path.abspath(__file__))
TEKSTEN = json.load(open(os.path.join(D, 'modellen_teksten.json'), encoding='utf-8'))
ANALYSE = json.load(open(os.path.join(D, 'modellen_analyse.json'), encoding='utf-8'))

live = api('rmk/v1/modellen')['data']
omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
L = {m['id']: m for m in live['modellen']}
if any(i in L for i in NIEUW):
    sys.exit(f'Er staan al nieuwe modellen live: {[i for i in NIEUW if i in L]}. Niets gewijzigd.')


def zonder(m, *paden):
    m = copy.deepcopy(m)
    for p in paden:
        d = m
        *kop, laatste = p.split('.')
        for k in kop:
            d = d.get(k, {})
        d.pop(laatste, None)
    return m


# Alleen de bedoelde velden mogen verschillen
for i in ('M023', 'M024'):
    assert zonder(L[i], 'verbinding') == zonder(omz[i], 'verbinding'), f'{i}: meer dan de verbinding verandert'
    assert omz[i]['verbinding']['tekst'] == 'Bluetooth' and omz[i]['verbinding']['extra'] == 'bluetooth', i
assert zonder(L['M025'], 'specs.geluid_dba') == zonder(omz['M025'], 'specs.geluid_dba'), 'M025: meer dan het geluid verandert'
assert omz['M025']['specs']['geluid_dba']['waarde'] == 58 and not omz['M025'].get('verbinding'), 'M025'
for i in NIEUW:
    m = omz[i]
    assert m.get('fabrikant_url', '').startswith(('https://www.stihl.nl/nl/', 'https://cramertools.com/nl-nl/')), i
    assert not m.get('ean') and not m.get('bol') and not m.get('prijs'), f'{i}: onverwacht Bol- of prijsgegeven'
for i in ('M026', 'M027'):
    m = omz[i]
    assert (m.get('beste_voor'), m.get('pluspunten'), m.get('minpunten'), m.get('analyse')) == (
        TEKSTEN[i]['beste_voor'], TEKSTEN[i]['pluspunten'], TEKSTEN[i]['minpunten'], ANALYSE[i]['analyse']), f'{i}: teksten wijken af'
assert omz['M035']['kosten'].get('extra_installatiekosten', {}).get('waarde') is None if 'extra_installatiekosten' in omz['M035'].get('kosten', {}) else True
assert omz['M035']['specs'].get('extra_installatiekosten', {}).get('waarde') is None if isinstance(omz['M035']['specs'].get('extra_installatiekosten'), dict) else True

nieuw = copy.deepcopy(live)
nieuw['modellen'] = [omz[m['id']] if m['id'] in ('M023', 'M024', 'M025') else m for m in live['modellen']] + [omz[i] for i in NIEUW]
ongewijzigd = [m['id'] for m in live['modellen'] if m['id'] not in ('M023', 'M024', 'M025')]
gelijk = all(L[i] == next(x for x in nieuw['modellen'] if x['id'] == i) for i in ongewijzigd) and \
    {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
for i in NIEUW:
    m = omz[i]
    print(f'{i} {m["naam"]}: beschikbaarheid {m.get("beschikbaarheid")}, fabrikant {m["fabrikant_url"]}')
print(f'{len(ongewijzigd)} live modellen en algemene velden ongewijzigd: {gelijk}; M023/M024 verbinding Bluetooth, M025 geluid 58; '
      f'totaal {len(nieuw["modellen"])} modellen')
if not gelijk:
    sys.exit('Bestaande gegevens zouden veranderen. Niets gewijzigd.')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
json.dump(live, open('backups/modellen-voor-ronde52.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
