#!/usr/bin/env python3
"""Ronde 55, KLAARGEZET: het blok "coolblue" (blad Coolblue: merchant_product_id en productpagina) in de live
modelgegevens (dataroute /rmk/v1/modellen). Pas draaien NA de upload van thema 1.3.10 (dat controleert het blok);
zonder RMK_COOLBLUE_ACTIVE verandert er op de site niets.

- Alleen bij live modellen die in het blad Coolblue staan; verder verandert er niets (het script weigert anders).
- Modellen uit het blad die nog niet live staan (M052-M058) worden overgeslagen en gemeld.
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde55_coolblue_data.py <omzetting.json>            (proefdraai)
          python3 scripts/ronde55_coolblue_data.py <omzetting.json> --schrijf
          python3 scripts/ronde55_coolblue_data.py <omzetting.json> --uit <bestand>  (alleen samenvoegen, voor tests)
"""
import copy, json, os, sys

SCHRIJF = '--schrijf' in sys.argv
BRON = next(a for a in sys.argv[1:] if not a.startswith('--') and a != (sys.argv[sys.argv.index('--uit') + 1] if '--uit' in sys.argv else None))


def samenvoegen(live, omz):
    """Live gegevens met alleen het blok coolblue erbij. Geeft (nieuw, toegevoegd, overgeslagen)."""
    nieuw, toegevoegd = copy.deepcopy(live), []
    for m in nieuw['modellen']:
        cb = omz.get(m['id'], {}).get('coolblue')
        if cb:
            m['coolblue'] = cb
            toegevoegd.append(m['id'])
    overgeslagen = sorted(i for i, m in omz.items() if m.get('coolblue') and i not in {x['id'] for x in live['modellen']})
    return nieuw, toegevoegd, overgeslagen


if __name__ == '__main__':
    omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
    if '--uit' in sys.argv:
        live = json.load(open(sys.argv[sys.argv.index('--live') + 1], encoding='utf-8'))
        nieuw, toegevoegd, overgeslagen = samenvoegen(live, omz)
        json.dump(nieuw, open(sys.argv[sys.argv.index('--uit') + 1], 'w', encoding='utf-8'), ensure_ascii=False)
        print('toegevoegd', toegevoegd, 'overgeslagen (niet live)', overgeslagen)
        sys.exit(0)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from affiliate_teksten_lib import api
    thema = api('wp/v2/themes?status=active')[0].get('version') or ''
    if tuple(int(x) for x in thema.split('.')[:3] if x.isdigit()) < (1, 3, 10):
        sys.exit(f'Actief thema {thema}: eerst 1.3.10 uploaden. Niets gewijzigd.')
    live = api('rmk/v1/modellen')['data']
    nieuw, toegevoegd, overgeslagen = samenvoegen(live, omz)
    zonder = lambda d: [{k: v for k, v in m.items() if k != 'coolblue'} for m in d['modellen']]
    gelijk = zonder(live) == zonder(nieuw) and {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
    for i in toegevoegd:
        print(f'  {i}: coolblue {next(m for m in nieuw["modellen"] if m["id"] == i)["coolblue"]}')
    print(f'Overgeslagen (staan niet live): {overgeslagen}')
    print(f'Verder alles ongewijzigd: {gelijk}; {len(toegevoegd)} modellen met coolblue')
    if not gelijk:
        sys.exit('Er zou meer veranderen dan het blok coolblue. Niets gewijzigd.')
    if not SCHRIJF:
        sys.exit(0)
    os.makedirs('backups', exist_ok=True)
    json.dump(live, open('backups/modellen-voor-ronde55.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
    print('Live na upload gelijk aan bedoeld:', api('rmk/v1/modellen')['data'] == nieuw)
