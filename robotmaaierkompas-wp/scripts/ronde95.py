#!/usr/bin/env python3
"""Ronde 95, MET DE HAND: gerichte vervangingen op de gepubliceerde pagina /husqvarna-of-gardena-robotmaaier/ (#461),
het app-rating-pluspunt van M055 (dataroute) en het sjabloonconcept #26 husqvarna-vs-gardena naar de prullenbak.
Niets wordt opnieuw uit de md gebouwd. Elke zoektekst moet precies één keer voorkomen; anders schrijft het niets.
Gebruik:  python3 scripts/ronde95.py            (proefdraai, schrijft niets)
          python3 scripts/ronde95.py --schrijf
"""
import base64, copy, json, os, re, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api, _auth
from ronde88_lib import pas_toe

SCHRIJF = '--schrijf' in sys.argv
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(D))  # backups/ naast scripts/

# ---- 1-5: pagina #461 (punt 8: de zin over de Husqvarna Group blijft staan)
R = '<th scope="row">'
STAPPEN = [
    (f'{R}Diefstalalarm</th><td>Ja, bij de modellen die we uitzochten</td><td>Niet genoemd</td>',
     f'{R}Diefstalalarm</th><td>Ja, bij de modellen die we uitzochten</td><td>Nee volgens de productpagina\'s van Gardena</td>',
     '1 tabel, Diefstalalarm (Gardena)'),
    ('<td>Gardena smart system, 4,49</td>',
     '<td>Gardena smart system 4,49 (sense en free); Bluetooth-app 4,37 (minimo, city en max)</td>', '1 tabel, App (Gardena)'),
    (f'{R}Garantie</th><td>2 jaar, accu 2 jaar</td>', f'{R}Garantie</th><td>2 jaar op de maaier en de accu, onder voorwaarden</td>',
     '1 tabel, Garantie (Husqvarna)'),
    ('<td>3 jaar na registratie, de accu valt buiten de gewone voorwaarden</td>',
     '<td>3 jaar na registratie (bevestigd bij de minimo\'s en de sense-modellen); de accuvoorwaarden verschillen per model</td>',
     '1 tabel, Garantie (Gardena)'),
    ('geeft 3 jaar garantie na registratie', 'geeft bij de modellen waar we dat bevestigden 3 jaar garantie na registratie',
     '2 korte antwoord'),
    (f'{R}Tot 1.500 m²</th><td>310E NERA (69,5), zonder camera</td>',
     f'{R}Tot 1.500 m²</th><td>310E NERA (69,5), zonder camera, of de uitlopende 410VE NERA (87,3, met camera)</td>',
     '3 keuzetabel, Tot 1.500 m² (Husqvarna)'),
    ('bij de Husqvarna-modellen die we uitzochten zit een alarm, bij geen van de Gardena-modellen noemt Gardena er een.',
     'bij de Husqvarna-modellen die we uitzochten zit een alarm; volgens de productpagina\'s van Gardena hebben de Gardena-modellen er geen.',
     '4 bullet Alarm'),
    ('<strong>Garantie:</strong> 3 jaar na registratie, tegenover 2 jaar bij Husqvarna.',
     '<strong>Garantie:</strong> 3 jaar na registratie bij de minimo\'s en de sense-modellen, tegenover 2 jaar bij Husqvarna.',
     '4 bullet Garantie'),
    ('de kleinere Husqvarna-modellen alleen met een losse Connect Kit',
     'de uitlopende 410VE ook; de 308V, 312V en Aspire R6V alleen met een losse Connect Kit (209 euro) en de 305 met een andere Connect Kit (329 euro)',
     '5 FAQ GPS'),
    ('Bij de Gardena-modellen die we uitzochten noemt Gardena geen diefstalalarm',
     'Volgens de productpagina\'s van Gardena hebben de Gardena-modellen die we uitzochten geen alarm', '5 FAQ diefstalalarm'),
    ('Gardena geeft 3 jaar na registratie; Husqvarna 2 jaar, ook op de accu.',
     'Gardena geeft bij de minimo\'s en de sense-modellen 3 jaar na registratie; Husqvarna 2 jaar, ook op de accu, onder voorwaarden.',
     '5 FAQ garantie'),
]
print('== Pagina #461')
p = api('wp/v2/pages/461?context=edit')
assert p['status'] == 'publish' and p['slug'] == 'husqvarna-of-gardena-robotmaaier'
assert p['content']['raw'].count('Gardena is een merk van de Husqvarna Group') == 1
_, meld = pas_toe(461, STAPPEN, False, 'r95')

# ---- 6: M055, pluspunt app-rating 4,48 -> 4,49 (alleen dat tekstveld)
print('\n== Modelgegevens M055')
live = api('rmk/v1/modellen')['data']
TEKSTVELDEN = ('beste_voor', 'pluspunten', 'minpunten', 'analyse')
waar = [(m['id'], k) for m in live['modellen'] for k, v in m.items() if '4,48' in json.dumps(v, ensure_ascii=False)]
print('4,48 in de modelgegevens:', waar)
OUD, NIEUW = 'App-rating 4,48, koppeling met slimme thuissystemen', 'App-rating 4,49, koppeling met slimme thuissystemen'
nieuw = copy.deepcopy(live)
m55 = next(m for m in nieuw['modellen'] if m['id'] == 'M055')
if m55['pluspunten'].count(OUD) != 1 or waar != [('M055', 'pluspunten')]:
    meld.append(f'M055: pluspunt "{OUD}" {m55["pluspunten"].count(OUD)} keer; 4,48 op {waar}.')
else:
    m55['pluspunten'] = [NIEUW if x == OUD else x for x in m55['pluspunten']]
    print('  M055 pluspunten: ok')
anders = [a['id'] for a, b in zip(live['modellen'], nieuw['modellen']) if a != b]
assert anders in ([], ['M055']) and {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
# ook in scripts/modellen_teksten.json (bron voor latere omzettingen)
TPAD = os.path.join(D, 'modellen_teksten.json')
tekst = open(TPAD, encoding='utf-8').read()
if tekst.count('4,48') != 1 or tekst.count(OUD) != 1:
    meld.append(f'modellen_teksten.json: 4,48 {tekst.count("4,48")} keer.')
if '4,48' in open(os.path.join(D, 'modellen_analyse.json'), encoding='utf-8').read():
    meld.append('modellen_analyse.json bevat 4,48.')

# ---- 7: #26 naar de prullenbak, als geen gepubliceerde pagina ernaar linkt
print('\n== Concept #26')
c = api('wp/v2/pages/26?context=edit&_fields=id,status,slug,link,title')
print(' ', c)
if c['status'] != 'draft' or c['slug'] != 'husqvarna-vs-gardena':
    meld.append(f'#26: status {c["status"]}, slug {c["slug"]} (verwacht draft, husqvarna-vs-gardena).')
pub = api('wp/v2/pages?per_page=100&status=publish&context=edit&_fields=id,slug,link,content')
patroon = re.compile(r'husqvarna-vs-gardena|page_id=26\b|[?&]p=26\b')
in_inhoud = [x['slug'] for x in pub if patroon.search(x['content']['raw'])]
in_html = []
for x in pub:  # openbare HTML (ook menu, footer, kruimelpad)
    h = urllib.request.urlopen(urllib.request.Request(x['link'] + '?nocache=' + str(time.time()), headers={'User-Agent': 'Mozilla/5.0 rmk-controle'}), timeout=60).read().decode()
    if patroon.search(h):
        in_html.append(x['slug'])
print(f'  links naar #26: in de inhoud {in_inhoud or "geen"}, in de openbare HTML van {len(pub)} pagina\'s {in_html or "geen"}')
if in_inhoud or in_html:
    meld.append(f'#26 wordt gelinkt vanaf {in_inhoud + in_html}.')

print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')

pas_toe(461, STAPPEN, True, 'r95')
pad = f'backups/modellen-voor-ronde95-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie modelgegevens:', pad, '| opgeslagen:', api('rmk/v1/modellen', nieuw))  # leegt ook LiteSpeed
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
open(TPAD, 'w', encoding='utf-8').write(tekst.replace(OUD, NIEUW))
# #26: kopie, dan naar de prullenbak (DELETE zonder force = prullenbak, terug te zetten)
oud26 = api('wp/v2/pages/26?context=edit')
json.dump({k: oud26[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta', 'modified')},
          open(f'backups/r95-pagina26-voor-{time.strftime("%Y%m%d-%H%M%S")}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
req = urllib.request.Request('https://robotmaaierkompas.nl/wp-json/wp/v2/pages/26', method='DELETE', headers={'Authorization': _auth()})
with urllib.request.urlopen(req, timeout=60) as r:
    print('#26 status na verwijderen:', json.load(r).get('status'))
