#!/usr/bin/env python3
"""Ronde 74, KLAARGEZET: het blok "amazon" (blad Amazon: ASIN en knop) in de live modelgegevens (dataroute
/rmk/v1/modellen). Pas draaien NA de upload van thema 1.3.13 (dat controleert het blok); zonder RMK_AMAZON_ACTIVE
verandert er op de site niets. Kan dus vóór "Amazon aan" al gedraaid worden.

- Alleen bij live modellen met een ASIN in het blad Amazon; verder verandert er niets (het script weigert anders).
- knop is true alleen bij "Knop: ja"; M050 krijgt knop false (uitgesloten in excel_naar_json.py en in het thema).
- Modellen uit het blad die nog niet live staan worden overgeslagen en gemeld.
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/excel_naar_json.py <xlsx> --uit /tmp/omzetting.json
          python3 scripts/ronde74_amazon_data.py /tmp/omzetting.json            (proefdraai, alleen lezen)
          python3 scripts/ronde74_amazon_data.py /tmp/omzetting.json --schrijf  (kopie in backups/, dan opslaan)
          python3 scripts/ronde74_amazon_data.py <omzetting.json> --live <live.json> --uit <bestand>  (alleen samenvoegen, voor tests)
"""
import copy, json, os, re, sys

SCHRIJF = '--schrijf' in sys.argv
_vlag = {sys.argv[i + 1] for i, a in enumerate(sys.argv[:-1]) if a in ('--uit', '--live')}
BRON = next(a for a in sys.argv[1:] if not a.startswith('--') and a not in _vlag)


def samenvoegen(live, omz):
    """Live gegevens met alleen het blok amazon erbij (of bijgewerkt). Geeft (nieuw, toegevoegd, overgeslagen)."""
    nieuw, toegevoegd = copy.deepcopy(live), []
    for m in nieuw['modellen']:
        am = omz.get(m['id'], {}).get('amazon')
        if am:
            assert set(am) == {'asin', 'knop'} and re.fullmatch(r'[A-Z0-9]{10}', am['asin']) and isinstance(am['knop'], bool), m['id']
            if m['id'] == 'M050':
                am = dict(am, knop=False)  # uitgesloten (zie BOUWLOGBOEK ronde 74)
            m['amazon'] = am
            toegevoegd.append(m['id'])
    overgeslagen = sorted(i for i, m in omz.items() if m.get('amazon') and i not in {x['id'] for x in live['modellen']})
    return nieuw, toegevoegd, overgeslagen


def alleen_amazon_anders(live, nieuw):
    zonder = lambda d: [{k: v for k, v in m.items() if k != 'amazon'} for m in d['modellen']]
    return zonder(live) == zonder(nieuw) and {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}


if __name__ == '__main__':
    omz = {m['id']: m for m in json.load(open(BRON, encoding='utf-8'))['modellen']}
    if '--uit' in sys.argv:
        live = json.load(open(sys.argv[sys.argv.index('--live') + 1], encoding='utf-8'))
        nieuw, toegevoegd, overgeslagen = samenvoegen(live, omz)
        assert alleen_amazon_anders(live, nieuw)
        json.dump(nieuw, open(sys.argv[sys.argv.index('--uit') + 1], 'w', encoding='utf-8'), ensure_ascii=False)
        print('toegevoegd', toegevoegd, 'overgeslagen (niet live)', overgeslagen)
        sys.exit(0)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from affiliate_teksten_lib import api
    thema = api('wp/v2/themes?status=active')[0].get('version') or ''
    te_oud = tuple(int(x) for x in re.findall(r'\d+', thema)[:3]) < (1, 3, 13)
    live = api('rmk/v1/modellen')['data']
    nieuw, toegevoegd, overgeslagen = samenvoegen(live, omz)
    gelijk = alleen_amazon_anders(live, nieuw)
    for i in toegevoegd:
        print(f'  {i}: amazon {next(m for m in nieuw["modellen"] if m["id"] == i)["amazon"]}')
    knop = [i for i in toegevoegd if next(m for m in nieuw['modellen'] if m['id'] == i)['amazon']['knop']]
    print(f'Overgeslagen (staan niet live): {overgeslagen}')
    print(f'Met knop: {len(knop)} {knop}')
    print(f'Verder alles ongewijzigd: {gelijk}; {len(toegevoegd)} modellen met een blok amazon')
    if not gelijk:
        sys.exit('Er zou meer veranderen dan het blok amazon. Niets gewijzigd.')
    if te_oud:
        print(f'Actief thema {thema}: eerst 1.3.13 uploaden (de dataroute van {thema} kent het blok amazon niet).')
    if not SCHRIJF:
        sys.exit(0)
    if te_oud:
        sys.exit('Niets gewijzigd.')
    os.makedirs('backups', exist_ok=True)
    json.dump(live, open('backups/modellen-voor-ronde74.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Kopie: backups/modellen-voor-ronde74.json (terugzetten: POST die inhoud naar rmk/v1/modellen)')
    print('Opgeslagen:', api('rmk/v1/modellen', nieuw))
    print('Live na upload gelijk aan bedoeld:', api('rmk/v1/modellen')['data'] == nieuw)
