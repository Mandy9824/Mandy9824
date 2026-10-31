#!/usr/bin/env python3
"""Ronde 78: de nieuwe topmodellen op pagina 1 (#11) en de hub (#10), met de hand
(tekstwijzigingen-pagina1-hub-nieuwe-modellen.md, Mandy, 1 november 2026; dat bestand staat niet in de repository),
ZONDER M058 (Ecovacs GOAT A3000 LiDAR Pro), op Mandy's besluit van 31 oktober 2026: M058 heeft op de site geen
functiescore (alarm "niet gevonden"), dus komt hij later. Daarom "zeven" (hub) en "vierentwintig" (pagina 1).

Gerichte vervangingen via de WordPress-API; de pagina's worden NIET opnieuw gebouwd. Elk anker moet precies één keer
voorkomen; anders schrijft het script niets. Pagina's houden hun status, slug en titel.

A. Pagina 1: metabeschrijving "Tien …" -> "Meer dan twintig …"; "tien modellen" -> "vierentwintig modellen" (korte
   antwoord en kop); scoretabel met 24 modellen; drie rijen onder "Welke past bij jouw tuin?" (derde cel: tekst van
   Mandy); kaarten M059, M060 en M056 na M010; zin met de merklinks onder de tabel.
B. Hub: metabeschrijving "Zes keuzes" -> "Zeven keuzes"; korte antwoord "zes modellen" -> "zeven modellen"; rij M060
   in "In een oogopslag" na Husqvarna (beide 87,3); onderdeel M060 (H3, kaart, "Waarom deze") na Husqvarna;
   "Alle tien modellen naast elkaar" -> "Alle vierentwintig …"; "Meer lezen": "de tien modellen vergeleken" ->
   "de vierentwintig modellen vergeleken" (zelfde verwijzing naar pagina 1).

Kaarten: hetzelfde skelet als op de andere pagina's (het thema vult ze uit de modelgegevens): M059/M060 van de
Mova-pagina (#351), M056 van de kleine-tuinpagina (#16), in de omhulling van de doelpagina.

M058 later toevoegen (nieuwe ronde, zodra de alarmbron van M058 vastligt en de score zichtbaar is): hub "zeven" ->
"acht", rij "Grote tuin tot 3.000 m²", onderdeel M058 na Mova 1200; pagina 1 "vierentwintig" -> "vijfentwintig",
M058 tussen M004 en M008 in de scoretabel, rij "Grote tuin tot 3.000 m²", kaart vóór M008 (zie BOUWLOGBOEK ronde 78).

Gebruik:  python3 scripts/ronde78_p1_hub.py            (proefdraai)
          python3 scripts/ronde78_p1_hub.py --schrijf  (kopie in backups/, opslaan, LiteSpeed legen via de dataroute)
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
"""
import html, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
MOVA, KLEIN = 351, 16
OUD_VOLGORDE = 'M015,M002,M016,M010,M005,M004,M008,M001,M006,M011'
# Op functiescore, bij gelijke score op ID (de bestaande tien houden hun volgorde). Zonder M058.
NIEUW_VOLGORDE = ('M015,M002,M016,M010,M059,M060,M056,M057,M005,M004,M008,M001,M064,'
                  'M046,M047,M020,M022,M063,M006,M007,M052,M053,M011,M055')
assert len(NIEUW_VOLGORDE.split(',')) == 24 and 'M058' not in NIEUW_VOLGORDE

pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in (10, 11, MOVA, KLEIN)}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
live = {m['id']: m for m in api('rmk/v1/modellen')['data']['modellen']}
meld, log = [], []


def kort(s, n=150):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', s))).strip()[:n]


def vervang(pid, was, wordt, wat):
    n = raw[pid].count(was)
    if n != 1:
        meld.append(f'#{pid} {wat}: "Was" {n} keer gevonden (verwacht 1); niet gewijzigd.')
        return
    raw[pid] = raw[pid].replace(was, wordt, 1)
    log.append(f'  #{pid} {wat}:\n    was:   {kort(was)}\n    wordt: {kort(wordt, 400)}')


def blok(h, slug):
    """Het volledige wp:group-blok (omhulling + kaartskelet) van een model, of None als het er niet precies één keer is."""
    if h.count(f'aria-labelledby="p-{slug}"') != 1:
        return None
    i = h.find(f'aria-labelledby="p-{slug}"')
    s = h.rfind('<!-- wp:group', 0, i)
    e = h.find('<!-- /wp:group -->', i) + len('<!-- /wp:group -->')
    return h[s:e]


def kaart_als(sjabloon, art):
    """Kaartskelet in de omhulling van de doelpagina (die verschilt per pagina)."""
    return re.sub(r'<article class="rmk-product".*?</article>', lambda _: art, sjabloon, count=1, flags=re.S)


# ---- kaartskeletten van de andere pagina's
SLUG = {i: live[i]['slug'] for i in ('M056', 'M059', 'M060')}
ART = {}
for mid, pid in (('M059', MOVA), ('M060', MOVA), ('M056', KLEIN)):
    b = blok(raw[pid], SLUG[mid])
    if not b or f'data-model="{mid}"' not in b:
        sys.exit(f'Kaart van {mid} niet precies één keer op #{pid} gevonden. Niets gewijzigd.')
    ART[mid] = re.search(r'<article class="rmk-product".*?</article>', b, re.S).group(0)
    for doel in (10, 11):
        if f'aria-labelledby="p-{SLUG[mid]}"' in raw[doel]:
            meld.append(f'#{doel}: kaart {mid} staat er al.')

# ---- A. pagina 1
vervang(11, 'We vergeleken tien modellen op navigatie, helling, app, veiligheid en geluid.',
        'We vergeleken vierentwintig modellen op navigatie, helling, app, veiligheid en geluid.', 'A2 korte antwoord')
vervang(11, 'Vergelijking van de tien modellen', 'Vergelijking van de vierentwintig modellen', 'A2 kop scoretabel')
vervang(11, f'[rmk_scoretabel modellen="{OUD_VOLGORDE}"]', f'[rmk_scoretabel modellen="{NIEUW_VOLGORDE}"]', 'A3 scoretabel (24 modellen)')

laatste = ('<tr><th scope="row">Kleinere tuin tot 800 m²</th><td>Mova LiDAX Ultra 800 of Gardena Smart Sileno Free 800</td>'
           '<td>Opgegeven oppervlak 800 m²</td></tr>')
rijen = [('Steile tuin (80% helling volgens Mova)', 'Mova LiDAX Ultra 1000 AWD',
          '80% helling, vierwielaandrijving en 4G ingebouwd met 3 jaar gratis service volgens Mova'),
         ('Tuin tot 1.600 m² met 4G en GPS ingebouwd', 'Mova LiDAX Ultra 1600',
          'Tot 1.600 m² en 45% helling, 4G en GPS ingebouwd met 1 jaar gratis service volgens Mova'),
         ('Kleine tuin tot 600 m²', 'Zie <a href="/robotmaaier-kleine-tuin/">Robotmaaier kleine tuin</a>',
          'Twaalf modellen tot 600 m² vergeleken, van de Mova ViAX 250 tot de Navimow i206 AWD')]
vervang(11, laatste, laatste + ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rijen),
        'A4 drie rijen "Welke past bij jouw tuin?" (zonder Grote tuin tot 3.000 m²)')

b010 = blok(raw[11], 'husqvarna-automower-410ve-nera')
if b010:
    vervang(11, b010, b010 + ''.join('\n\n' + kaart_als(b010, ART[m]) for m in ('M059', 'M060', 'M056')),
            'A5 kaarten M059, M060, M056 na M010')
else:
    meld.append('#11 A5: kaart M010 niet precies één keer gevonden.')

TABELNOOT = ('<p>De volgorde volgt de functiescore. Alle scores komen uit het openbare scoremodel op de pagina '
             '<a href="/hoe-we-beoordelen/">Hoe we beoordelen</a>. Een functiescore laat zien wat een maaier kan. Zodra er '
             'genoeg reviews en prijzen zijn, voegen we betrouwbaarheid en prijs-kwaliteit toe en wordt het een eindscore.</p>')
if 'Per merk vergelijken we' in raw[11]:
    meld.append('#11 A6: de zin "Per merk vergelijken we …" staat er al.')
MERKZIN = ('<p>Per merk vergelijken we de modellen uitgebreider op <a href="/segway-navimow-robotmaaier/">Segway Navimow</a>, '
           '<a href="/husqvarna-robotmaaier/">Husqvarna</a>, <a href="/gardena-robotmaaier/">Gardena</a>, '
           '<a href="/stihl-robotmaaier/">Stihl</a>, <a href="/worx-robotmaaier/">Worx</a>, '
           '<a href="/mova-dreame-robotmaaier/">Mova en Dreame</a> en <a href="/eufy-robotmaaier/">Eufy</a>.</p>')
vervang(11, TABELNOOT, TABELNOOT + '\n' + MERKZIN, 'A6 zin met merklinks onder de tabel')
MERKLINKS_AL = [u for u in re.findall(r'href="(/[a-z-]+-robotmaaier/)"', MERKZIN) if f'href="{u}"' in pag[11]['content']['raw']]

# ---- B. hub
vervang(10, 'Daarom kiezen we niet één winnaar maar zes modellen, elk voor een andere situatie',
        'Daarom kiezen we niet één winnaar maar zeven modellen, elk voor een andere situatie', 'B2 korte antwoord')
r410 = ('<tr><th scope="row">Grote tuin tot ongeveer 1.500 m², systematisch maaien</th><td><a href="#p-husqvarna-automower-410ve-nera">'
        'Husqvarna Automower 410VE NERA</a></td><td>87,3</td></tr>')
vervang(10, r410, r410 + f'<tr><th scope="row">Steile tuin (80% helling volgens Mova)</th><td><a href="#p-{SLUG["M060"]}">'
        'Mova LiDAX Ultra 1000 AWD</a></td><td>87,3</td></tr>', 'B3 rij Mova LiDAX Ultra 1000 AWD (87,3) na Husqvarna (87,3)')
hub_sjabloon = blok(raw[10], 'husqvarna-automower-410ve-nera')
W410 = ('<p><strong>Waarom deze:</strong> de enige in onze selectie die 1.500 m² systematisch opgeeft, met 4G ingebouwd en gratis '
        'correctiedata. Je hebt wel mobiele of wifidekking over het hele gazon nodig, en de prijs ligt boven de 3.000 euro.</p>\n')
if hub_sjabloon:
    vervang(10, W410, W410 + '<h3>Steile tuin: Mova LiDAX Ultra 1000 AWD</h3>\n</div></section>\n<!-- /wp:html -->\n\n'
            + kaart_als(hub_sjabloon, ART['M060'])
            + '\n\n<!-- wp:html -->\n<section class="rmk-container rmk-section--tight rmk-column"><div class="rmk-prose">\n'
            '<p><strong>Waarom deze:</strong> de Mova voor steile tuinen: 80% helling volgens Mova, vierwielaandrijving en 4G met '
            '3 jaar gratis service. Hij is wel luider (66 dB(A)).</p>\n', 'B4 onderdeel Mova LiDAX Ultra 1000 AWD na Husqvarna')
else:
    meld.append('#10 B4: Husqvarna-kaart niet precies één keer gevonden.')
for w in ('zes keuzes', 'Zes keuzes'):
    if w in raw[10]:
        meld.append(f'#10 B5: "{w}" staat in de inhoud; niet voorzien.')
vervang(10, 'Alle tien modellen naast elkaar', 'Alle vierentwintig modellen naast elkaar', 'B5 "Alle … modellen naast elkaar"')
vervang(10, 'Robotmaaier zonder draad</a>: de tien modellen vergeleken.', 'Robotmaaier zonder draad</a>: de vierentwintig modellen vergeleken.',
        'B5 extra: "Meer lezen", zelfde verwijzing naar pagina 1')

# ---- metabeschrijvingen
meta = {}
for pid, was, wordt in ((11, 'Tien robotmaaiers zonder draad vergeleken op navigatie, helling, app, veiligheid en kosten. Functiescores met bron en datum.',
                         'Meer dan twintig robotmaaiers zonder draad vergeleken op navigatie, helling, app, veiligheid en kosten. Functiescores met bron en datum.'),
                        (10, 'De beste robotmaaier hangt af van je tuin. Zes keuzes per situatie met specificaties, kosten en functiescore, met bron en datum.',
                         'De beste robotmaaier hangt af van je tuin. Zeven keuzes per situatie met specificaties, kosten en functiescore, met bron en datum.')):
    nu = (pag[pid].get('meta') or {}).get('_yoast_wpseo_metadesc')
    if nu == was:
        meta[pid] = wordt
        log.append(f'  #{pid} metabeschrijving:\n    was:   {was}\n    wordt: {wordt}')
    else:
        meld.append(f'#{pid} metabeschrijving is niet de "Was"-tekst (nu: {nu!r}); niet gewijzigd.')

# ---- tellingen ter controle
print('\n'.join(log))
TEL = {w: re.compile(rf'(?i)\b{w}\b') for w in ('tien', 'zes', 'acht', 'vijfentwintig')}
KAART = re.compile(r'data-model="(M\d+)"')
for pid in (10, 11):
    print(f'#{pid}: ' + ', '.join(f'"{w}" {len(r.findall(raw[pid]))}x' for w, r in TEL.items())
          + f'; M058/Ecovacs: {raw[pid].count("M058") + raw[pid].count("Ecovacs")}x; kaarten {KAART.findall(raw[pid])}')
print('A6: merklinks die al op pagina 1 stonden:', ', '.join(MERKLINKS_AL) or 'geen')
print('\nMeldingen:' if meld else '\nGeen meldingen: alle ankers precies één keer gevonden.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')

# Vlak voor het schrijven opnieuw lezen: is er intussen iets veranderd (editortab, andere sessie)?
for pid in (10, 11):
    q = api(f'wp/v2/pages/{pid}?context=edit')
    if q['content']['raw'] != pag[pid]['content']['raw'] or q['modified'] != pag[pid]['modified']:
        sys.exit(f'#{pid} is intussen gewijzigd ({q["modified"]}). Niets geschreven.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde78-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': pag[pid]['status'], 'slug': pag[pid]['slug'], 'modified': pag[pid]['modified'],
                      'content': pag[pid]['content']['raw'], 'meta': pag[pid].get('meta')} for pid in (10, 11)},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in (11, 10):
    body = {'content': raw[pid]}
    if pid in meta:
        body['meta'] = {'_yoast_wpseo_metadesc': meta[pid]}
    api(f'wp/v2/pages/{pid}', body)
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}), slug {q["slug"]}; inhoud zoals bedoeld: '
          f'{q["content"]["raw"] == raw[pid]}; metabeschrijving: {q["meta"].get("_yoast_wpseo_metadesc")!r}')
data = api('rmk/v1/modellen')['data']
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', data))
print('Mandy: leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
