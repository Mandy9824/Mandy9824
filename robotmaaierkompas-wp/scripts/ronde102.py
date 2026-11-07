#!/usr/bin/env python3
"""Ronde 102, MET DE HAND (zonder thema-zip): gerichte vervangingen (via scripts/ronde88_lib.py: kopie vooraf, elke
zoektekst precies 1x, anders schrijft hij niets; status blijft gelijk).
A. Diefstalpagina /robotmaaier-diefstal-verzekering/ (#489): punten 1-7 uit de opdracht van Mandy (7 november 2026).
B. Egelpagina /robotmaaier-egels/ (#490): punten 2 en 3 (punt 1 zie VOORSTELLEN).
C. Lege sjablonen #57, #61, #58, #59, #43 naar de prullenbak, alleen als geen gepubliceerde pagina (inhoud en openbare
   HTML) ernaar linkt.
D1. Modelgegevens (dataroute): minpunt M022 (en hetzelfde in scripts/modellen_teksten.json).
D2. RTK-pagina /robotmaaier-rtk-lidar-camera/ (#470): "…310E: Zonder wifi" -> "…310E: zonder wifi".
Niet uitgevoerd (letterlijk gaf het een kapotte zin), alleen met --met-voorstellen (na akkoord van Mandy):
  B1 egelpagina "Hij is ingediend op 16 juni 2026 en volgens het gegevensmagazijn van de Tweede Kamer aangenomen";
  D1 analyse M008 ": het grootste in onze selectie" weg (letterlijk zou er "tot 2.000 m²: tot 2.000 m²" staan).
Gebruik:  python3 scripts/ronde102.py            (proefdraai)
          python3 scripts/ronde102.py --schrijf
"""
import base64, copy, json, os, re, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
from ronde88_lib import pas_toe

SCHRIJF = '--schrijf' in sys.argv
VOORSTELLEN = '--met-voorstellen' in sys.argv
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(D))

TABEL_EIND = '<td>Nee</td></tr></tbody></table></div>\n'
PAGINAS = {
    489: [
        ('de hoogste functiescore (96,4)', 'de hoogste functiescore (96,4, gedeeld met de Husqvarna Automower 430V NERA)',
         'A1 Waarom deze i210'),
        (TABEL_EIND,
         '<td>Nee</td></tr><tr><th scope="row">Navimow i105E (loopt uit)</th><td>Ja</td><td>Nee</td><td>Nee</td><td>Nee</td></tr>'
         '</tbody></table></div>\n<p>Bij de Husqvarna 305E en 310E NERA past ook de Connect Kit (209 euro); of die GPS-tracking '
         'toevoegt, hebben we niet vastgesteld.</p>\n', 'A2 tabel, rij i105E en zin onder de tabel'),
        ('Navimow 1 jaar, daarna volgens Navimow 29,99 euro per jaar',
         'Navimow i205 en i210 LiDAR Pro 1 jaar, daarna volgens Navimow 29,99 euro per jaar (bij de i206 heeft de 4G-service '
         'een einddatum en is de verlenging niet bevestigd)', 'A3 Wat kost GPS volgen?, Navimow'),
        ('Mova 1600 1 jaar en de AWD-modellen 3 jaar',
         'Mova 1600 1 jaar en de Mova LiDAX Ultra 1000 AWD 3 jaar (de 1600 en 2000 AWD hebben we alleen op basisniveau uitgezocht)',
         'A3/A7 Wat kost GPS volgen?, Mova'),
        ('Bij een schade vragen verzekeraars meestal bewijs van eigendom, de waarde en de leeftijd, en aangifte bij de politie.',
         'Interpolis en Centraal Beheer vragen op verzoek bewijs van eigendom, de waarde en de leeftijd, en aangifte bij de politie.',
         'A4 bewijs bij schade'),
        ('Het Verbond van Verzekeraars heeft geen standpunt over robotmaaiers.',
         'Het Verbond van Verzekeraars heeft op de pagina\'s die we vonden geen standpunt over robotmaaiers.', 'A5 Verbond'),
        ('braaksporen worden alleen gevraagd bij diefstal uit bijgebouwen en bergingen',
         'braaksporen worden gevraagd bij diefstal uit bijgebouwen, bergingen, opslag elders, een garage op een ander adres, '
         'een kelder of een garagebox', 'A6 braaksporen'),
    ],
    490: [
        ('een goede beveiliging en liefst intrekbare messen.</td><td>17 januari 2020</td>',
         'een goede beveiliging en liefst intrekbare messen. Voor de biodiversiteit is het volgens de Zoogdiervereniging het '
         'beste geen robotmaaier te gebruiken.</td><td>17 januari 2020</td>', 'B2 Zoogdiervereniging, advies'),
        ('Modus "Diervriendelijk": blijft uit de buurt van huisdieren en kleine dieren</td>',
         'Modus "Diervriendelijk": blijft uit de buurt van huisdieren en kleine dieren; de handleidingen noemen ook '
         'BioLife-zones (no-go) voor onder andere egels</td>', 'B3 Navimow-rij'),
    ],
    470: [
        ('Bij de 308V, 312V, Aspire R6V, 305E en 310E: Zonder wifi', 'Bij de 308V, 312V, Aspire R6V, 305E en 310E: zonder wifi',
         'D2 Husqvarna-bullet, kleine letter'),
    ],
}
if VOORSTELLEN:
    PAGINAS[490].append(('Volgens het gegevensmagazijn van de Tweede Kamer is hij aangenomen;',
                         'Hij is ingediend op 16 juni 2026 en volgens het gegevensmagazijn van de Tweede Kamer aangenomen;', 'B1 motie'))
# Ter controle (meldingen, niets vervangen): plekken uit de opdracht die niet letterlijk voorkomen.
CONTROLE = {
    489: [('de AWD-modellen', 'A7 "de AWD-modellen" (na A3)', 0)],
    490: [('In juni 2026 aangenomen', 'B1 "In juni 2026 aangenomen"', None), ('in juni 2026 aangenomen', 'B1 "in juni 2026 aangenomen"', None)],
}
MP_OUD = 'In vier van de twintig gelezen reviews (vertaald, niet in de score) stopt de maaier als het satellietsignaal wegvalt'
MP_NIEUW = 'In vier van de twintig gelezen reviews (vertaald, niet in de score) worden problemen door satelliet- of verbindingsverlies genoemd'
A8_OUD, A8_NIEUW = ': het grootste in onze selectie.', '.'
SJABLONEN = {57: 'robotmaaier-diefstal', 61: 'robotmaaier-verzekering', 58: 'robotmaaier-egels-huisdieren',
             59: 'robotmaaier-nacht', 43: 'robotmaaier-abonnement-4g'}

meld = []
for pid, st in PAGINAS.items():
    p = api(f'wp/v2/pages/{pid}?context=edit&_fields=status')
    if p['status'] != 'publish':
        meld.append(f'#{pid}: status {p["status"]}')
    raw, m = pas_toe(pid, st, False, 'r102')
    meld += [f'#{pid} {x}' for x in m]
    for zoek, wat, verwacht in CONTROLE.get(pid, []):
        print(f'  ter controle {wat}: {raw.count(zoek)} keer na de vervangingen')

print('\n== Modelgegevens (alleen minpunten M022' + (' en analyse M008' if VOORSTELLEN else '') + ')')
live = api('rmk/v1/modellen')['data']
nieuw = copy.deepcopy(live)
by = {m['id']: m for m in nieuw['modellen']}
mp = by['M022']['minpunten']
if mp.count(MP_OUD) != 1:
    meld.append(f'M022 minpunt: {mp.count(MP_OUD)} keer als heel minpunt.')
else:
    mp[mp.index(MP_OUD)] = MP_NIEUW
    print('  M022 minpunt: ok')
if VOORSTELLEN:
    if by['M008']['analyse'].count(A8_OUD) != 1:
        meld.append('M008 analyse: zoektekst niet precies 1x.')
    else:
        by['M008']['analyse'] = by['M008']['analyse'].replace(A8_OUD, A8_NIEUW)
        print('  M008 analyse: ok')
toegestaan = {('M022', 'minpunten')} | ({('M008', 'analyse')} if VOORSTELLEN else set())
for a, b in zip(live['modellen'], nieuw['modellen']):
    for k in set(a) | set(b):
        if a.get(k) != b.get(k):
            assert (a['id'], k) in toegestaan, (a['id'], k)
assert {k: v for k, v in live.items() if k != 'modellen'} == {k: v for k, v in nieuw.items() if k != 'modellen'}
# overal in de modelgegevens nog de oude tekst?
for m in nieuw['modellen']:
    s = json.dumps(m, ensure_ascii=False)
    if 'stopt de maaier als het satellietsignaal' in s:
        meld.append(f'{m["id"]}: oude reviewzin komt nog voor.')
pad_t, pad_a = os.path.join(D, 'modellen_teksten.json'), os.path.join(D, 'modellen_analyse.json')
tek, ana = json.load(open(pad_t, encoding='utf-8')), json.load(open(pad_a, encoding='utf-8'))
tmp = tek['M022']['minpunten']
if tmp.count(MP_OUD) != 1:
    meld.append('modellen_teksten.json M022: minpunt niet precies 1x.')
else:
    tmp[tmp.index(MP_OUD)] = MP_NIEUW
    if tmp != by['M022']['minpunten']:
        meld.append('modellen_teksten.json M022 wijkt af van de bedoelde live minpunten.')
print('  modellen_analyse.json: M022 heeft geen minpunten daar (alleen analyse);',
      'oude reviewzin in modellen_analyse.json:', 'stopt de maaier als het satellietsignaal' in json.dumps(ana, ensure_ascii=False))
if VOORSTELLEN:
    if ana['M008']['analyse'].count(A8_OUD) != 1:
        meld.append('modellen_analyse.json M008: zoektekst niet precies 1x.')
    else:
        ana['M008']['analyse'] = ana['M008']['analyse'].replace(A8_OUD, A8_NIEUW)

print('\n== Sjablonen: links vanaf gepubliceerde pagina\'s?')
pub = api('wp/v2/pages?status=publish&per_page=100&context=edit&_fields=id,slug,link,content')
htmls = {p['slug']: urllib.request.urlopen(urllib.request.Request(p['link'] + '?nocache=' + str(time.time()),
                                                                 headers={'Cache-Control': 'no-cache'}), timeout=60).read().decode()
         for p in pub}
print(f'  {len(pub)} gepubliceerde pagina\'s nagelopen (inhoud en openbare HTML)')
for pid, slug in SJABLONEN.items():
    s = api(f'wp/v2/pages/{pid}?context=edit&_fields=id,slug,status,parent,link')
    if s['slug'] != slug or s['status'] != 'draft':
        meld.append(f'#{pid}: slug {s["slug"]}, status {s["status"]} (verwacht {slug}, draft).')
    # slug als heel pad-deel (dus niet /robotmaaier-diefstal-verzekering/ of /robotmaaier-egels/ meetellen)
    pat = re.compile(rf'/{re.escape(slug)}(?:/|["\'?#])|[?&](page_id|p)={pid}\b')
    treffers = [p['slug'] for p in pub if pat.search(p['content']['raw'])]
    treffers += [f'{sl} (HTML)' for sl, h in htmls.items() if pat.search(h)]
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
for pid in PAGINAS:
    pas_toe(pid, PAGINAS[pid], True, 'r102')
os.makedirs('backups', exist_ok=True)
pad = f'backups/modellen-voor-ronde102-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump(live, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie modelgegevens:', pad, '| opgeslagen:', api('rmk/v1/modellen', nieuw))  # leegt ook LiteSpeed
na = api('rmk/v1/modellen')['data']
print('Live na upload gelijk aan bedoeld:', na == nieuw, '| modellen:', len(na['modellen']))
open(pad_t, 'w', encoding='utf-8').write(json.dumps(tek, ensure_ascii=False, indent=2))
if VOORSTELLEN:
    open(pad_a, 'w', encoding='utf-8').write(json.dumps(ana, ensure_ascii=False, indent=2))
pw, user = os.environ['RMK_WP_APP_PASSWORD'], os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
for pid in SJABLONEN:
    oud = api(f'wp/v2/pages/{pid}?context=edit')
    json.dump({k: oud[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta')},
              open(f'backups/r102-pagina{pid}-voor-{time.strftime("%Y%m%d-%H%M%S")}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    r = urllib.request.urlopen(urllib.request.Request(  # DELETE zonder force = prullenbak
        f'https://robotmaaierkompas.nl/wp-json/wp/v2/pages/{pid}', method='DELETE',
        headers={'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()}), timeout=60)
    print(f'#{pid} naar de prullenbak: status {json.load(r)["status"]}')
