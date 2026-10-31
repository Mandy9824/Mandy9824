#!/usr/bin/env python3
"""Ronde 77 (met de hand gewijzigde teksten, zonder thema-zip).

1. #76 /hoe-we-beoordelen/: oude sectie "Versies" samengevoegd in "Versie en wijzigingen" (nieuwe kop en tekst blijven,
   de inhoud van de oude sectie als datumregels in een lijst eronder, oude kop en sectie weg); inhoudsopgave: alleen nog
   "Versie en wijzigingen".
2. In de paginatekst "Scoremodel v1.0 (concept tot bevriezing)" -> "Scoremodel v1.0" (bronnenlijst-regel, eyebrow #76) en
   in het tabelbijschrift van robotmaaier-test-vergelijking "scoremodel v1.0 (concept tot bevriezing)" -> "scoremodel v1.0".
   Wat het thema zelf rendert (scoreblok, bijschriften uit inc/score.php, patronen) blijft staan: thema 1.3.14.
Elke zoektekst moet precies het verwachte aantal keer voorkomen, anders schrijft het script niets. Met --schrijf eerst een
kopie van alle te wijzigen pagina's in backups/. Pagina's houden hun status.
Gebruik:  python3 scripts/ronde77_versies_scoremodel.py            (proefdraai)
          python3 scripts/ronde77_versies_scoremodel.py --schrijf
          python3 scripts/ronde77_versies_scoremodel.py --terug <kopie> --schrijf
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

BRON_OUD = '<a href="/hoe-we-beoordelen/#scoremodel">Scoremodel v1.0 (concept tot bevriezing)</a>'
BRON_NIEUW = '<a href="/hoe-we-beoordelen/#scoremodel">Scoremodel v1.0</a>'
CAP_OUD = '<caption>Voorlopige functiescores volgens scoremodel v1.0 (concept tot bevriezing). '
CAP_NIEUW = '<caption>Voorlopige functiescores volgens scoremodel v1.0. '
EYE_OUD = '<p class="rmk-eyebrow">Scoremodel v1.0 (concept tot bevriezing)</p>'
EYE_NIEUW = '<p class="rmk-eyebrow">Scoremodel v1.0</p>'
TOC_OUD = '<li><a href="#versies">Versies</a></li><li><a href="#versie-en-wijzigingen">Versie en wijzigingen</a></li>'
TOC_NIEUW = '<li><a href="#versie-en-wijzigingen">Versie en wijzigingen</a></li>'
OUD_VERSIES = ('\n      <section id="versies" class="rmk-prose" aria-labelledby="versies-t">\n'
    '        <h2 id="versies-t" style="margin-top: 0">Versies</h2>\n'
    '        <ul><li><strong>v1.0 (concept), 5 oktober 2026:</strong> zeven onderdelen met vaste gewichten. Voor het bevriezen aangepast: '
    'mes-stop telt niet mee in veiligheid (veiligheid is berekend over vijf onderdelen); de rating van de app wordt niet afgerond; '
    'bij tegenstrijdige opgaven van een fabrikant rekenen we met de laagste waarde; een functiescore heet voortaan zo en wordt niet als '
    'eindscore getoond.</li><li>Voor het bevriezen vervangen we de trappen in de schalen voor helling, geluid, betrouwbaarheid en '
    'app-rating door vloeiende schalen. Dat noteren we hier.</li></ul>\n      </section>')
NIEUW_P_EIND = 'Wijzigingen aan het scoremodel melden we hier met de datum.</p>\n'
LIJST = ('        <ul><li><strong>5 oktober 2026:</strong> eerste concept, zeven onderdelen met vaste gewichten. Voor het bevriezen aangepast: '
    'mes-stop telt niet mee in veiligheid (veiligheid is berekend over vijf onderdelen); de rating van de app wordt niet afgerond; '
    'bij tegenstrijdige opgaven van een fabrikant rekenen we met de laagste waarde; een functiescore heet voortaan zo en wordt niet als '
    'eindscore getoond. Voor het bevriezen vervangen we de trappen in de schalen voor helling, geluid, betrouwbaarheid en app-rating '
    'door vloeiende schalen. Dat noteren we hier.</li><li><strong>oktober 2026:</strong> v1.0.</li></ul>\n')

# (paginaslug, zoek, vervang, verwacht aantal)
STAPPEN = [(s, BRON_OUD, BRON_NIEUW, 1) for s in (
    'beste-robotmaaier', 'robotmaaier-zonder-draad', 'robotmaaier-test-vergelijking', 'robotmaaier-zonder-grensdraad',
    'robotmaaier-kosten', 'robotmaaier-kleine-tuin', 'husqvarna-robotmaaier', 'gardena-robotmaaier', 'stihl-robotmaaier',
    'worx-robotmaaier', 'segway-navimow-robotmaaier', 'mova-dreame-robotmaaier', 'eufy-robotmaaier')] + [
    ('robotmaaier-test-vergelijking', CAP_OUD, CAP_NIEUW, 1),
    ('hoe-we-beoordelen', EYE_OUD, EYE_NIEUW, 1),
    ('hoe-we-beoordelen', OUD_VERSIES, '', 1),
    ('hoe-we-beoordelen', NIEUW_P_EIND, NIEUW_P_EIND + LIJST, 1),
    ('hoe-we-beoordelen', TOC_OUD, TOC_NIEUW, 1),
]

pag = {p['slug']: p for p in api('wp/v2/pages?status=publish&per_page=100&context=edit&_fields=id,slug,status,content')}
oud = {s: pag[s]['content']['raw'] for s in {x[0] for x in STAPPEN}}
if '--terug' in sys.argv:
    nieuw, meld = json.load(open(sys.argv[sys.argv.index('--terug') + 1], encoding='utf-8'))['inhoud'], []
else:
    nieuw, meld = dict(oud), []
    for s, z, v, n in STAPPEN:
        k = nieuw[s].count(z)
        if k != n:
            meld.append(f'{s}: "{re.sub("<[^>]+>", " ", z).strip()[:60]}…" {k} keer gevonden (verwacht {n})')
            continue
        nieuw[s] = nieuw[s].replace(z, v)
        print(f'  {s}: {re.sub("<[^>]+>", " ", z).strip()[:70]!r} -> {re.sub("<[^>]+>", " ", v).strip()[:70]!r}')
    rest = {s: nieuw[s].count('concept tot bevriezing') for s in nieuw if 'concept tot bevriezing' in nieuw[s]}
    if rest:
        meld.append(f'daarna nog "concept tot bevriezing" in {rest}')
    for p in pag.values():
        if p['slug'] not in nieuw and 'concept tot bevriezing' in p['content']['raw']:
            meld.append(f'{p["slug"]}: "concept tot bevriezing" op een niet voorziene pagina')
print('Meldingen:\n  - ' + '\n  - '.join(meld) if meld else 'Geen meldingen: elke zoektekst precies zo vaak als verwacht.')
if '--schrijf' not in sys.argv or meld:
    sys.exit(1 if meld else 0)
os.makedirs('backups', exist_ok=True)
pad = f'backups/versies-scoremodel-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({'inhoud': oud, 'status': {s: pag[s]['status'] for s in oud}, 'id': {s: pag[s]['id'] for s in oud}}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for s in oud:
    if nieuw[s] == oud[s]:
        continue
    api(f'wp/v2/pages/{pag[s]["id"]}', {'content': nieuw[s]})
    q = api(f'wp/v2/pages/{pag[s]["id"]}?context=edit')
    print(f'{s} (#{pag[s]["id"]}) opgeslagen; status {q["status"]} (was {pag[s]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == nieuw[s]}')
