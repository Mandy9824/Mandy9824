#!/usr/bin/env python3
"""Ronde 104, MET DE HAND (zonder thema-zip): gerichte vervangingen (via scripts/ronde88_lib.py: kopie vooraf, elke
zoektekst precies 1x, anders schrijft hij niets; status blijft gelijk).
A. Kopen-pagina #508: punten 1-8 uit de opdracht van Mandy (7 november 2026).
B. Egelpagina #490: korte antwoord en de regel over de motie-Kostic.
C. Diefstalpagina #489: FAQ "Welke robotmaaier heeft GPS?".
D. Modelgegevens M008 (analyse en minpunten; ook scripts/modellen_teksten.json en modellen_analyse.json).
Gebruik:  python3 scripts/ronde104.py            (proefdraai)
          python3 scripts/ronde104.py --schrijf
"""
import copy, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
from ronde88_lib import pas_toe

SCHRIJF = '--schrijf' in sys.argv
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(D))
A = lambda u, t: f'<a href="{u}">{t}</a>'
NIEUWE_SECTIES = (
    '<h2 id="drie-voorbeelden">Drie voorbeelden</h2>\n<ul>'
    '<li><strong>400 m², vlak, wifi alleen bij het huis:</strong> kijk naar modellen die voor de navigatie geen wifi of satelliet '
    'nodig hebben, zoals de Mova ViAX 500 (LiDAR en camera\'s, 500 m², 75,9). Voor de app heb je wel wifi of Bluetooth nodig. '
    f'Zie {A("/robotmaaier-kleine-tuin/", "robotmaaier voor een kleine tuin")}.</li>'
    '<li><strong>1.200 m² met stukken tot 45% helling:</strong> de Mova LiDAX Ultra 1200 (80,5) of 1600 (87,3), beide 45% helling '
    'volgens Mova. Voor nog steiler zijn er 4WD-modellen, zoals de Mova AWD (80%). '
    f'Zie {A("/robotmaaier-zonder-draad/", "robotmaaier zonder draad")}.</li>'
    '<li><strong>4.000 m² buiten de stad:</strong> de Husqvarna Automower 430V NERA (tot 4.800 m², 96,4) of, met draad, de Stihl '
    f'iMOW 7 (5.000 m²). Zie {A("/robotmaaier-grote-tuin/", "robotmaaier voor een grote tuin")}.</li></ul>\n'
    '<h2 id="waar-koop-je-een-robotmaaier">Waar koop je een robotmaaier?</h2>\n'
    '<p>Dat verschilt per merk. Husqvarna verkoopt de Automower via onafhankelijke dealers en soms via de webshop van Husqvarna NL '
    '(de 430V NERA alleen via een dealer). Stihl toont op zijn site geen voorraad en verwijst naar de dealer, en Cramer verkoopt via '
    'dealers. Voor de andere merken vind je op onze pagina\'s bij elk model de winkels waar we een aanbod van tonen. Bij een dealer '
    'kun je ook vragen naar de installatie van de draad, een Connect Kit of een referentiestation; wat dat kost, verschilt en hebben '
    'we niet gevonden. Prijzen en voorraad wisselen, dus controleer de beschikbaarheid, zeker bij modellen die uitlopen.</p>\n')
H_MINDER = '<h2 id="waar-je-minder-op-moet-vertrouwen">Waar je minder op moet vertrouwen</h2>'
PAGINAS = {
    508: [
        ('Modellen in ons overzicht van 250 tot 7.500 m².', 'Modellen met een score in ons overzicht: van 250 tot 7.500 m².', 'A1 rij 1'),
        ('RTK vraagt vaak wifi, een gateway of mobiele dekking, LiDAR en camera volgens de fabrikanten niet.',
         'RTK vraagt vaak wifi, een gateway of mobiele dekking; LiDAR en camera hebben volgens de fabrikanten geen satellietsignaal '
         'nodig (sommige, zoals de Eufy C15, vragen wel wifi bij het gazon voor de app).', 'A2 rij 4'),
        ('Navimow 1 jaar (daarna 29,99 euro per jaar), Mova 1600 1 jaar, Mova AWD 3 jaar, Husqvarna 430V en 450V 10 jaar.',
         'Navimow i205 en i210 LiDAR Pro 1 jaar (daarna 29,99 euro per jaar; bij de i206 heeft de 4G-service een einddatum), '
         'Mova 1600 1 jaar, Mova 1000 AWD 3 jaar, Husqvarna 430V en 450V 10 jaar.', 'A3 rij 5, gratis periode'),
        ('Worx (149 euro)', 'Worx (149 euro), Navimow i105E (Access+, 99,99 euro en daarna 29,90 euro per jaar), '
         'Husqvarna Connect Kit (209 euro, bij de 305 329 euro)', 'A3 rij 5, losse modules'),
        ('Gardena en Roborock 4,49', 'Gardena sense en free en Roborock 4,49, Gardena minimo, city en max (Bluetooth-app) 4,37', 'A4 rij 8'),
        ('Garantie 2 tot 3 jaar, vaak met een kortere termijn voor de accu.',
         'Garantie meestal 2 tot 3 jaar, vaak met een kortere termijn voor de accu (Dreame noemt in de handleiding geen fabrieksgarantie).',
         'A5 rij 9'),
        ('Voor boven 3.000 m² zijn er de Husqvarna 430V en 450V NERA.',
         'Voor boven 3.000 m² zijn er de Husqvarna 430V en 450V NERA en, met draad, de Stihl iMOW 7 en 7 EVO (5.000 m²); de Cramer '
         'AiConic 5, 8 en 12 konden we niet als beschikbaar bevestigen.', 'A6 stap 1'),
        ('(1 tot 10 jaar)', '(1 tot 10 jaar; bij de Eufy E15 en E18 alleen proefdata van 7 dagen)', 'A7 FAQ abonnement'),
        (H_MINDER, NIEUWE_SECTIES + H_MINDER, 'A8 twee nieuwe secties'),
    ],
    490: [
        ('de Tweede Kamer nam in juni 2026 wel een motie aan die om overleg met de provincies vraagt',
         'een motie van de Tweede Kamer, ingediend op 16 juni 2026 en volgens het gegevensmagazijn aangenomen, vraagt om overleg met de provincies',
         'B1 korte antwoord'),
        ('(tussen 18:00 en 9:00). Volgens het gegevensmagazijn van de Tweede Kamer is hij aangenomen; het is een verzoek en geen regel.',
         '(tussen 18:00 en 9:00). Hij is ingediend op 16 juni 2026 en volgens het gegevensmagazijn van de Tweede Kamer aangenomen; '
         'het is een verzoek en geen regel.', 'B2 motie-Kostic'),
    ],
    489: [
        ('de Mova LiDAX Ultra 1600 en AWD-modellen', 'de Mova LiDAX Ultra 1600 en 1000 AWD', 'C FAQ GPS'),
    ],
}
ANA = [(': het grootste in onze selectie.', '.'), ('staat op 3,91 in Google Play', 'staat op 3,87 in Google Play')]
MIN = ('App-rating 3,91 (de app dient ook voor andere Dreame-apparaten)', 'App-rating 3,87 (de app dient ook voor andere Dreame-apparaten)')

meld = []
for pid, st in PAGINAS.items():
    if api(f'wp/v2/pages/{pid}?context=edit&_fields=status')['status'] != 'publish':
        meld.append(f'#{pid}: geen publish')
    _, m = pas_toe(pid, st, False, 'r104')
    meld += [f'#{pid} {x}' for x in m]

print('\n== Modelgegevens M008 (analyse, minpunten)')
live = api('rmk/v1/modellen')['data']
nieuw = copy.deepcopy(live)
m8 = next(m for m in nieuw['modellen'] if m['id'] == 'M008')
pad_t, pad_a = os.path.join(D, 'modellen_teksten.json'), os.path.join(D, 'modellen_analyse.json')
tek, ana = json.load(open(pad_t, encoding='utf-8')), json.load(open(pad_a, encoding='utf-8'))
for doel, wie in ((m8, 'live'), (ana['M008'], 'modellen_analyse.json')):
    for oud, wordt in ANA:
        if doel['analyse'].count(oud) != 1:
            meld.append(f'M008 analyse ({wie}): "{oud}" {doel["analyse"].count(oud)}x')
        else:
            doel['analyse'] = doel['analyse'].replace(oud, wordt)
for doel, wie in ((m8, 'live'), (tek['M008'], 'modellen_teksten.json')):
    if doel['minpunten'].count(MIN[0]) != 1:
        meld.append(f'M008 minpunt ({wie}) niet precies 1x')
    else:
        doel['minpunten'][doel['minpunten'].index(MIN[0])] = MIN[1]
if ana['M008']['analyse'] != m8['analyse'] or tek['M008']['minpunten'] != m8['minpunten']:
    meld.append('repository-teksten M008 wijken af van de bedoelde live teksten')
if '3,91' in json.dumps(m8, ensure_ascii=False):
    meld.append('M008: 3,91 komt nog voor: ' + json.dumps(m8, ensure_ascii=False)[:200])
for a, b in zip(live['modellen'], nieuw['modellen']):
    for k in set(a) | set(b):
        if a.get(k) != b.get(k):
            assert (a['id'], k) in {('M008', 'analyse'), ('M008', 'minpunten')}, (a['id'], k)
assert {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
print('  analyse:', m8['analyse'][:160], '…\n  minpunt:', MIN[1])
pub = api('wp/v2/pages?status=publish&per_page=100&context=edit&_fields=id,slug,content')
print('  kaart M008 op:', [p['slug'] for p in pub if 'data-model="M008"' in p['content']['raw']])

print('\nMeldingen:' if meld else '\nGeen meldingen.')
for x in meld:
    print('  - ' + x)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
for pid in PAGINAS:
    pas_toe(pid, PAGINAS[pid], True, 'r104')
os.makedirs('backups', exist_ok=True)
pad = f'backups/modellen-voor-ronde104-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie modelgegevens:', pad, '| opgeslagen:', api('rmk/v1/modellen', nieuw))  # leegt ook LiteSpeed
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
open(pad_t, 'w', encoding='utf-8').write(json.dumps(tek, ensure_ascii=False, indent=2))
open(pad_a, 'w', encoding='utf-8').write(json.dumps(ana, ensure_ascii=False, indent=2))
