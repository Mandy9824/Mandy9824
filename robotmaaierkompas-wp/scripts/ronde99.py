#!/usr/bin/env python3
"""Ronde 99, MET DE HAND (zonder thema-zip): gerichte vervangingen (via scripts/ronde88_lib.py: kopie vooraf, elke
zoektekst precies 1x, anders schrijft hij niets; status blijft gelijk).
A. /robotmaaier-rtk-lidar-camera/ (#470): punten 1-7 uit de opdracht van Mandy (4 november 2026).
B. (1) "grootste draadloze maaier" bij de Ecovacs: hub #10 en grote tuin #15 (tekst, kaart, FAQ) en de analyse van M058
   (modelgegevens en scripts/modellen_analyse.json). (2) "stopt als hij het satellietsignaal kwijtraakt": Husqvarna #20.
C. Lege sjablonen #35, #36, #37, #38 naar de prullenbak, alleen als geen gepubliceerde pagina (inhoud en openbare HTML)
   ernaar linkt.
Gebruik:  python3 scripts/ronde99.py            (proefdraai)
          python3 scripts/ronde99.py --schrijf
"""
import copy, json, os, re, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
from ronde88_lib import pas_toe

SCHRIJF = '--schrijf' in sys.argv
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(D))
R = '<th scope="row">'
NIEUW = 'een van de grootste draadloze maaiers met een score in onze selectie (3.000 m²)'

PAGINAS = {
    470: [
        ('de Mova- en Ecovacs-modellen en de Dreame A1 Pro met LiDAR',
         'de Mova LiDAX Ultra-modellen, de Mova ViAX 500, de Ecovacs-modellen en de Dreame A1 Pro met LiDAR', 'A1 korte antwoord'),
        ('bij RTK via wifi of een gateway (Husqvarna V- en NERA-modellen, Gardena free) moet je het hele gazon kunnen bereiken',
         'bij RTK via wifi, een gateway of mobiele dekking (Husqvarna V- en NERA-modellen, Gardena free en sense) moet je het hele gazon kunnen bereiken',
         'A2 praktijk, dekking'),
        ('noemen vier van de twintig gelezen reviews bij de 310E NERA dat de maaier stopt als hij het satellietsignaal kwijtraakt. '
         'LiDAR en camera hebben dat bezwaar volgens de fabrikanten niet.',
         'noemen vier van de twintig gelezen reviews bij de 310E NERA problemen door satelliet- of verbindingsverlies. '
         'LiDAR en camera hebben volgens de fabrikanten geen satellietsignaal nodig; sommige modellen (zoals de Eufy C15) vragen '
         'wel wifi bij het gazon voor de app.', 'A2 praktijk, reviews'),
        ('De 4WD-modellen zijn wel luider: 66 dB(A) bij de Mova AWD en 68 dB(A) bij de Navimow X420, tegenover 55 tot 62 dB(A) bij de meeste andere.',
         'De Mova AWD (66 dB(A)) en de Navimow X420 (68 dB(A)) zijn luider dan de meeste andere modellen (55 tot 62 dB(A)); '
         'van de Worx 4WD WR342E kennen we het geluid niet.', 'A3 4WD of 2WD'),
        ('Ze zijn luider (66 tot 68 dB(A)).', 'De Mova AWD en de Navimow X420 zijn luider (66 en 68 dB(A)).', 'A3 FAQ 4WD/AWD'),
        (f'{R}Een stille maaier</th><td>De niet-4WD-modellen van Mova (57 dB(A)) en de Husqvarna 430V (55 dB(A))</td>',
         f'{R}Een stille maaier</th><td>De Husqvarna 430V en de Gardena sense 400 en 600 (55 dB(A)) en de niet-4WD-modellen van Mova (57 dB(A))</td>',
         'A4 keuzetabel, Een stille maaier'),
        ('de hoogste functiescore (96,4)', 'de hoogste functiescore (96,4, gedeeld met de Husqvarna Automower 430V NERA)', 'A5 Waarom deze i210'),
        ('anders gebruik je de antenne uit de doos.',
         'anders gebruik je de antenne uit de doos (bij de i205, i206 en X420; de LiDAR Pro-modellen hebben geen antenne nodig).',
         'A6 Navimow-bullet'),
        ('de Navimow gebruikt netwerk-RTK of een antenne uit de doos',
         'de Navimow i205, i206 en X420 gebruiken netwerk-RTK of een antenne uit de doos; de LiDAR Pro-modellen niet', 'A6 FAQ antenne'),
        ('de grootste draadloze maaier met een score (3.000 m²)',
         'een van de grootste draadloze maaiers met een score (3.000 m²; alleen de Husqvarna 430V en 450V zijn groter)', 'A7 Waarom deze Ecovacs'),
        ('Zonder wifi heb je een Connect Kit (209 euro) of een referentiestation (309 euro) nodig.',
         'Bij de 308V, 312V, Aspire R6V, 305E en 310E: Zonder wifi heb je een Connect Kit (209 euro) of een referentiestation (309 euro) nodig.',
         'A7 Husqvarna-bullet'),
    ],
    10: [
        ('de grootste draadloze maaier met een score in onze selectie: tot 3.000 m² en 50% helling volgens Ecovacs, met LiDAR zonder draad.',
         f'{NIEUW}: 50% helling volgens Ecovacs, met LiDAR zonder draad.', 'B1 hub, Waarom deze Ecovacs'),
    ],
    15: [
        ('De grootste draadloze maaier met een score is de Ecovacs GOAT A3000 LiDAR Pro (3.000 m², 79,5).',
         f'De Ecovacs GOAT A3000 LiDAR Pro (79,5) is {NIEUW}.', 'B1 grote tuin, Robotmaaier voor 3.000 m²'),
        ('<strong>Waarom deze:</strong> de grootste draadloze maaier met een score, tot 3.000 m².',
         f'<strong>Waarom deze:</strong> {NIEUW}.', 'B1 grote tuin, Waarom deze Ecovacs'),
        ('<summary>Wat is de grootste robotmaaier zonder draad?</summary><div><p>Met een score de Ecovacs GOAT A3000 LiDAR Pro (3.000 m²). '
         'Zonder draad zijn er grotere, zoals de Cramer AiConic 5 tot en met 12; die konden we niet als beschikbaar bevestigen.</p>',
         '<summary>Wat is de grootste robotmaaier zonder draad?</summary><div><p>Met een score de Husqvarna Automower 450V NERA (7.500 m², 94,5), '
         'gevolgd door de 430V NERA (4.800 m²) en de Ecovacs GOAT A3000 LiDAR Pro (3.000 m²). Zonder draad zijn er grotere, zoals de Cramer '
         'AiConic 5 tot en met 12; die konden we niet als beschikbaar bevestigen.</p>', 'B1 grote tuin, FAQ grootste zonder draad'),
    ],
    20: [
        ('noemen vier van de twintig gelezen reviews bij de 310E NERA dat de maaier stopt als hij het satellietsignaal kwijtraakt.',
         'noemen vier van de twintig gelezen reviews bij de 310E NERA problemen door satelliet- of verbindingsverlies.', 'B2 Husqvarna, Waar op te letten'),
    ],
}
A_OUD = 'is de grootste draadloze maaier in onze selectie, voor tuinen tot 3.000 m² en een helling tot 50% volgens Ecovacs.'
A_NIEUW = f'is {NIEUW}, met een helling tot 50% volgens Ecovacs.'
SJABLONEN = {35: 'rtk-of-begrenzingsdraad', 36: 'gps-vision-lidar-robotmaaier', 37: 'rtk-antenne-robotmaaier', 38: 'robotmaaier-4wd-of-2wd'}

meld = []
for pid, st in PAGINAS.items():
    p = api(f'wp/v2/pages/{pid}?context=edit&_fields=status')
    if p['status'] != 'publish':
        meld.append(f'#{pid}: status {p["status"]}')
    _, m = pas_toe(pid, st, False, 'r99')
    meld += [f'#{pid} {x}' for x in m]

print('\n== Modelgegevens M058 (analyse)')
live = api('rmk/v1/modellen')['data']
nieuw = copy.deepcopy(live)
m58 = next(m for m in nieuw['modellen'] if m['id'] == 'M058')
if m58['analyse'].count(A_OUD) != 1:
    meld.append(f'M058 analyse: zoektekst {m58["analyse"].count(A_OUD)} keer.')
else:
    m58['analyse'] = m58['analyse'].replace(A_OUD, A_NIEUW)
    print('  M058 analyse: ok')
for a, b in zip(live['modellen'], nieuw['modellen']):
    if a != b:
        assert a['id'] == 'M058' and {k for k in set(a) | set(b) if a.get(k) != b.get(k)} == {'analyse'}
assert {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
pad_a = os.path.join(D, 'modellen_analyse.json')
ana = json.load(open(pad_a, encoding='utf-8'))
if ana['M058']['analyse'].count(A_OUD) != 1:
    meld.append('modellen_analyse.json M058: zoektekst niet precies 1x.')
else:
    ana['M058']['analyse'] = ana['M058']['analyse'].replace(A_OUD, A_NIEUW)
    if ana['M058']['analyse'] != m58['analyse']:
        meld.append('modellen_analyse.json M058 wijkt af van de bedoelde live analyse.')

print('\n== Sjablonen #35-#38: links vanaf gepubliceerde pagina\'s?')
pub = api('wp/v2/pages?status=publish&per_page=100&context=edit&_fields=id,slug,link,content')
for pid, slug in SJABLONEN.items():
    s = api(f'wp/v2/pages/{pid}?context=edit&_fields=id,slug,status,parent,link')
    if s['slug'] != slug or s['status'] != 'draft':
        meld.append(f'#{pid}: slug {s["slug"]}, status {s["status"]} (verwacht {slug}, draft).')
    pat = re.compile(rf'{re.escape(slug)}|[?&](page_id|p)={pid}\b')
    treffers = [p['slug'] for p in pub if pat.search(p['content']['raw'])]
    for p in pub:  # openbare HTML (menu, footer)
        html = urllib.request.urlopen(urllib.request.Request(p['link'] + '?nocache=' + str(time.time()), headers={'Cache-Control': 'no-cache'}), timeout=60).read().decode()
        if pat.search(html):
            treffers.append(p['slug'] + ' (HTML)')
    print(f'  #{pid} {slug}: {treffers or "geen links"}')
    if treffers:
        meld.append(f'#{pid} {slug}: gelinkt vanaf {treffers}.')

print('\nMeldingen:' if meld else '\nGeen meldingen.')
for x in meld:
    print('  - ' + x)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
for pid in PAGINAS:
    pas_toe(pid, PAGINAS[pid], True, 'r99')
pad = f'backups/modellen-voor-ronde99-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie modelgegevens:', pad, '| opgeslagen:', api('rmk/v1/modellen', nieuw))  # leegt ook LiteSpeed
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
open(pad_a, 'w', encoding='utf-8').write(json.dumps(ana, ensure_ascii=False, indent=2))
for pid in SJABLONEN:
    oud = api(f'wp/v2/pages/{pid}?context=edit')
    json.dump({k: oud[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta')},
              open(f'backups/r99-pagina{pid}-voor-{time.strftime("%Y%m%d-%H%M%S")}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    req = urllib.request.Request  # DELETE zonder force = prullenbak
    import base64
    pw = os.environ['RMK_WP_APP_PASSWORD']; user = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
    r = urllib.request.urlopen(req(f'https://robotmaaierkompas.nl/wp-json/wp/v2/pages/{pid}', method='DELETE',
                                   headers={'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()}), timeout=60)
    print(f'#{pid} naar de prullenbak: status {json.load(r)["status"]}')
