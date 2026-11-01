#!/usr/bin/env python3
"""Ronde 88, stap 5: pagina 1 (#11), hub (#10), kleine tuin (#16) en grote tuin (#15) volgens
tekstwijzigingen-nieuwe-modellen-overig.md (secties A-D), MET DE HAND: gerichte vervangingen en toevoegingen via de API,
niets uit een md gebouwd. Per pagina een kopie vooraf (scripts/ronde88_lib.py); elke zoektekst moet precies één keer
voorkomen, anders schrijft het script niets voor die pagina.
Niet uitgevoerd (gemeld in het bouwlogboek): aantekening "uitlopend" bij M010 in de scoretabel van pagina 1 (de shortcode
toont de modelnaam uit de modelgegevens; kan alleen met een themawijziging) en D4 tweede deel (de cel "Tuin van 1.500
tot 1.600 m²" noemt de 310E NERA al; de vervanging zou hem dubbel noemen).
Gebruik:  python3 scripts/ronde88_paginas.py <modellen.json> [--schrijf] [--alleen 11,10,16,15]
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ronde88_lib import pas_toe

SCHRIJF = '--schrijf' in sys.argv
MOD = {m['id']: m for m in json.load(open(next(a for a in sys.argv[1:] if a.endswith('.json')), encoding='utf-8'))['modellen']}
ALLEEN = next((a.split('=')[1] for a in sys.argv if a.startswith('--alleen=')), '11,10,16,15').split(',')
D = os.path.dirname(os.path.abspath(__file__))


def scores(mid):
    s = MOD[mid]['scores']
    f = lambda v: '' if v is None else str(v)
    return '; '.join(f'{k}={f(s.get(k))}' for k in ('betrouwbaarheid', 'navigatie', 'prijskwaliteit', 'hellingen', 'app', 'veiligheid', 'geluid')) + '; reviews='


def artikel(mid, titel):
    a = 'p-' + MOD[mid]['slug']
    return (f'<article class="rmk-product" aria-labelledby="{a}">\n'
            '  <div class="rmk-product__head rmk-product__head--nomedia" style="grid-template-columns: 1fr">\n'
            '    <div class="rmk-product__title">\n'
            f'      <h3 id="{a}">{titel}</h3>\n'
            f'      <div class="rmk-scorecell" data-rmk-score data-scores="{scores(mid)}" data-model="{mid}"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div>\n'
            '    </div>\n  </div>\n  <div class="rmk-product__aside rmk-offers">\n    <div class="rmk-offer"></div>\n  </div>\n</article>')


GROEP = '<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n<div class="wp-block-group rmk-container rmk-block rmk-column"><!-- wp:html -->\n'


def kaart_p1(mid, titel):  # zoals de kaarten op pagina 1 (dubbele wp:html, sinds ronde 78)
    return GROEP + '<!-- wp:html -->\n' + artikel(mid, titel) + '\n<!-- /wp:html -->\n<!-- /wp:html --></div>\n<!-- /wp:group -->'


def kaart(mid, titel):  # zoals op de grote-tuinpagina (ronde82_bouw.py)
    return GROEP + artikel(mid, titel) + '\n<!-- /wp:html --></div>\n<!-- /wp:group -->'


def kaartblok(raw_slug, p1=False):
    """Het volledige blok van een bestaande kaart (vanaf <article> tot en met de afsluitende wp:group), als zoektekst."""
    return re.compile(r'<article class="rmk-product" aria-labelledby="p-' + re.escape(raw_slug) + r'">.*?<!-- /wp:group -->', re.S)


def blok(raw, slug):
    m = list(kaartblok(slug).finditer(raw))
    assert len(m) == 1, f'kaart {slug}: {len(m)} keer'
    return m[0].group(0)


def rij(*cellen):
    return '<tr><th scope="row">' + cellen[0] + '</th>' + ''.join(f'<td>{c}</td>' for c in cellen[1:]) + '</tr>'


from affiliate_teksten_lib import api
live = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in (11, 10, 16, 15)}
R = {pid: p['content']['raw'] for pid, p in live.items()}
STAPPEN = {}

# ---------------------------------------------------------------- A. pagina 1 (#11)
OUD_LIJST = 'M015,M002,M016,M010,M059,M060,M056,M057,M005,M004,M058,M008,M001,M064,M046,M047,M020,M022,M063,M006,M007,M052,M053,M011,M055'
NIEUW_LIJST = 'M015,M069,M070,M002,M016,M010,M059,M060,M066,M067,M068,M056,M057,M005,M004,M058,M008,M071,M072,M001,M064,M046,M047,M020,M022,M063,M006,M007,M052,M053,M011,M055'
assert sorted(OUD_LIJST.split(',') + 'M066 M067 M068 M069 M070 M071 M072'.split()) == sorted(NIEUW_LIJST.split(','))
b15, b16 = blok(R[11], 'segway-navimow-i210-lidar-pro'), blok(R[11], 'segway-navimow-i205-awd')
KZ_P1 = '<td>Twaalf modellen tot 600 m² vergeleken, van de Mova ViAX 250 tot de Navimow i206 AWD</td></tr></tbody></table></div>'
STAPPEN[11] = [
    ('We vergeleken vijfentwintig modellen', 'We vergeleken tweeëndertig modellen', 'A2 korte antwoord'),
    ('<h2>Vergelijking van de vijfentwintig modellen</h2>', '<h2>Vergelijking van de tweeëndertig modellen</h2>', 'A2 kop'),
    (f'[rmk_scoretabel modellen="{OUD_LIJST}"]', f'[rmk_scoretabel modellen="{NIEUW_LIJST}"]', 'A3 scoretabel (+7 modellen)'),
    (KZ_P1, KZ_P1.replace('</tbody>', rij('Zeer grote tuin (tot 7.500 m²), met 4G en GPS ingebouwd', 'Husqvarna Automower 430V of 450V NERA',
                                         'Tot 4.800 en 7.500 m² en 50% helling volgens Husqvarna, met AI-camera en 4G') + '</tbody>'), 'A4 rij keuzetabel'),
    (b15, b15 + '\n\n' + kaart_p1('M069', 'Husqvarna Automower 430V NERA'), 'A5 kaart M069 na M015'),
    (b16, b16 + '\n\n' + kaart_p1('M070', 'Husqvarna Automower 450V NERA'), 'A5 kaart M070 na M016'),
]

# ---------------------------------------------------------------- B. hub (#10)
H3_OUD = '<h3>Grote tuin, systematisch maaien: Husqvarna Automower 410VE NERA</h3>'
art410 = re.search(r'<article class="rmk-product" aria-labelledby="p-husqvarna-automower-410ve-nera">.*?</article>', R[10], re.S).group(0)
WAAROM_OUD = ('<p><strong>Waarom deze:</strong> de enige in onze selectie die 1.500 m² systematisch opgeeft, met 4G ingebouwd en gratis '
              'correctiedata. Je hebt wel mobiele of wifidekking over het hele gazon nodig, en de prijs ligt boven de 3.000 euro. '
              'Hij loopt uit: controleer de beschikbaarheid.</p>')
WAAROM_NIEUW = ('<p><strong>Waarom deze:</strong> de hoogste functiescore van alle Husqvarna-modellen: tuinen tot 4.800 m² en 50% helling '
                'volgens Husqvarna, stil (55 dB(A)) en met 4G en GPS ingebouwd. Husqvarna verkoopt hem via dealers.</p>')
RIJ_SIT = 'Grote tuin tot ongeveer 1.500 m², systematisch maaien'
RIJ_410 = rij(RIJ_SIT, '<a href="#p-husqvarna-automower-410ve-nera">Husqvarna Automower 410VE NERA</a>', '87,3')
RIJ_I210 = rij('Tuin tot ongeveer 1.000 m² met veel obstakels, zonder antenne', '<a href="#p-segway-navimow-i210-lidar-pro">Segway Navimow i210 LiDAR Pro</a>', '96,4')
RIJ_430 = rij(RIJ_SIT, '<a href="#p-husqvarna-automower-430v-nera">Husqvarna Automower 430V NERA</a>', '96,4')
# bronnen: het blok van de 410VE vervangen door dat van de 430V (zelfde regels als op de Husqvarna-pagina, scripts/ronde87/husqvarna.json)
h87 = json.load(open(os.path.join(D, 'ronde87', 'husqvarna.json'), encoding='utf-8'))['content']
def bronblok(raw, titel):
    m = list(re.finditer(r'<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var\(--rmk-fs-lg\); margin-top: 16px">'
                         + re.escape(titel) + r'</h3></div>\n<!-- /wp:html -->\n\n<!-- wp:group .*?<!-- /wp:group -->', raw, re.S))
    assert len(m) == 1, f'bronblok {titel}: {len(m)}'
    return m[0].group(0)
BRON_410, BRON_430 = bronblok(R[10], 'Husqvarna Automower 410VE NERA'), bronblok(h87, 'Husqvarna Automower 430V NERA')
assert 'automower-430v-nera' in BRON_430 and BRON_430.count('<li>') >= 5
STAPPEN[10] = [
    (H3_OUD, H3_OUD.replace('410VE NERA', '430V NERA'), 'B1 kop'),
    (art410, artikel('M069', 'Husqvarna Automower 430V NERA'), 'B1 kaart M010 -> M069'),
    (WAAROM_OUD, WAAROM_NIEUW, 'B1 Waarom deze (zonder "Hij loopt uit")'),
    (RIJ_410, '', 'B1 rij 410VE uit de tabel'),
    (RIJ_I210, RIJ_I210 + RIJ_430, 'B1 rij 430V (96,4) na de i210 LiDAR Pro'),
    ('<p>Alle vijfentwintig modellen naast elkaar', '<p>Alle tweeëndertig modellen naast elkaar', 'B3 Alle ... modellen'),
    ('Robotmaaier zonder draad</a>: de vijfentwintig modellen vergeleken.', 'Robotmaaier zonder draad</a>: de tweeëndertig modellen vergeleken.', 'B3 Meer lezen'),
    (BRON_410, BRON_430, 'bronnen 410VE -> 430V'),
]

# ---------------------------------------------------------------- C. kleine tuin (#16)
I206 = '<td>4G ingebouwd (service heeft een einddatum)</td><td>92,7</td></tr>'
Q105 = '<td>Losse 4G-module</td><td>84,1</td></tr>'
KZ16 = '<td>Husqvarna Automower 305, Stihl iMOW 3 of Worx WR165E</td></tr></tbody></table></div>'
STILSTE = '<summary>Welke is de stilste?</summary><div><p>De Mova ViAX 250 en 500 en de Worx WR303E hebben een geluidsvermogen van 57 dB(A).</p>'
STAPPEN[16] = [
    ('<h1>Robotmaaier voor een kleine tuin: 12 modellen tot 600 m² vergeleken (2026)</h1>',
     '<h1>Robotmaaier voor een kleine tuin: 15 modellen tot 600 m² vergeleken (2026)</h1>', 'C1 H1'),
    ('kun je kiezen uit twaalf robotmaaiers die nu nieuw te koop zijn: acht zonder draad en vier met begrenzingsdraad.',
     'kun je kiezen uit vijftien robotmaaiers die nu nieuw te koop zijn: elf zonder draad en vier met begrenzingsdraad.', 'C1/C4 korte antwoord'),
    ('>De twaalf modellen naast elkaar</h2>', '>De vijftien modellen naast elkaar</h2>', 'C2 kop (id blijft)'),
    (I206, I206 + rij('Husqvarna Automower Aspire R6V', '600 m²', '40%', 'RTK met AI-camera via wifi', '62 dB(A)', 'Wifi', '84,5'), 'C2 rij Aspire R6V'),
    (Q105, Q105 + rij('Gardena Sileno sense 600', '600 m²', '25%', 'RTK met AI-camera', '55 dB(A)', 'Gratis ingebouwde simkaart', '78,6')
     + rij('Gardena Sileno sense 400', '400 m²', '25%', 'RTK met AI-camera', '55 dB(A)', 'Gratis ingebouwde simkaart', '78,6'), 'C2 rijen sense 600 en 400'),
    (KZ16, KZ16.replace('</tbody>', rij('Tuin tot 600 m², zonder draad, met AI-camera', 'Husqvarna Automower Aspire R6V')
                        + rij('Tuin tot 400 m², zonder draad, met GPS', 'Gardena Sileno sense 400') + '</tbody>'), 'C3 twee rijen keuzetabel'),
    ('Nee: acht van de twaalf modellen werken zonder begrenzingsdraad.', 'Nee: elf van de vijftien modellen werken zonder begrenzingsdraad.', 'C1 FAQ draad'),
    (STILSTE, STILSTE.replace('<p>De Mova', '<p>De Gardena Sileno sense 400 en 600 (55 dB(A)). De Mova'), 'C5 FAQ stilste'),
]
META16 = {'_yoast_wpseo_metadesc': (
    'Welke robotmaaier past in een kleine tuin tot 600 m²? Twaalf modellen met en zonder draad vergeleken op oppervlak, helling, geluid, 4G en kosten.',
    'Welke robotmaaier past in een kleine tuin tot 600 m²? Vijftien modellen met en zonder draad vergeleken op oppervlak, helling, geluid, 4G en kosten.')}
TITEL16 = ('Robotmaaier voor een kleine tuin: 12 modellen tot 600 m² vergeleken (2026)', 'Robotmaaier voor een kleine tuin: 15 modellen tot 600 m² vergeleken (2026)')

# ---------------------------------------------------------------- D. grote tuin (#15)
I210_15 = '<td>LiDAR met camera en netwerk-RTK (volgens Navimow)</td><td>59 dB(A)</td><td>4G ingebouwd</td><td>96,4</td></tr>'
R410_15 = ('<tr><th scope="row"><a href="#p-husqvarna-automower-410ve-nera">Husqvarna Automower 410VE NERA</a></th><td>1.500 m²</td><td>30%</td>'
           '<td>RTK met camera</td><td>60 dB(A)</td><td>4G ingebouwd</td><td>87,3</td></tr>')
KORT_OUD = ('De hoogste functiescore voor ongeveer 1.000 m² is voor de Navimow i210 LiDAR Pro (96,4), gevolgd door de Mova LiDAX Ultra 1600 '
            'en 1000 AWD en de Husqvarna Automower 410VE NERA (alle drie 87,3).')
KORT_NIEUW = ('De hoogste functiescore hebben de Husqvarna Automower 430V NERA en de Navimow i210 LiDAR Pro (beide 96,4), gevolgd door de '
              'Husqvarna 450V NERA (94,5) en de Mova LiDAX Ultra 1600 en 1000 AWD (beide 87,3).')
H2_DRAAD = '<h2 id="draadloos-bij-een-grote-tuin-waar-je-op-moet-letten">Draadloos bij een grote tuin: waar je op moet letten</h2>'
SECTIE_5000 = ('<h2 id="robotmaaier-voor-5-000-m-en-meer">Robotmaaier voor 5.000 m² en meer</h2>\n'
               '<p>Voor tuinen boven de 3.000 m² zijn er in ons overzicht twee Husqvarna-modellen: de Automower 430V NERA (tot 4.800 m², '
               '3.200 m² bij onregelmatig maaien) en de 450V NERA (tot 7.500 m²). Beide hebben een AI-camera, 50% helling volgens Husqvarna, '
               'en 4G en GPS ingebouwd, volgens Husqvarna NL 10 jaar gratis. Met draad is er de Stihl iMOW 7 en 7 EVO (5.000 m²).</p>\n')
WAAROM_I210 = '<p><strong>Waarom deze:</strong> de hoogste functiescore voor een tuin van 1.000 m², met 4G ingebouwd en 55% helling.</p>\n</div></section>\n<!-- /wp:html -->'
RIJ_4G = '<td>Navimow i210 en i220 Pro, Navimow X420, Mova LiDAX Ultra 1600 en AWD, Husqvarna 410VE NERA of Eufy E18</td>'
STAPPEN[15] = [
    (I210_15, I210_15 + rij('<a href="#p-husqvarna-automower-430v-nera">Husqvarna Automower 430V NERA</a>', '4.800 m²', '50%', 'RTK met AI-camera', '55 dB(A)', '4G ingebouwd', '96,4')
     + rij('Husqvarna Automower 450V NERA', '7.500 m²', '50%', 'RTK met AI-camera', '58 dB(A)', '4G ingebouwd', '94,5'), 'D1 rijen 430V en 450V na de i210 LiDAR Pro'),
    (R410_15, R410_15.replace('410VE NERA</a></th>', '410VE NERA</a> (loopt uit)</th>')
     + rij('Husqvarna Automower 312V', '1.200 m²', '40%', 'RTK met AI-camera via wifi', '62 dB(A)', 'Wifi', '84,5'), 'D1 rij 312V, D4 410VE "(loopt uit)"'),
    (H2_DRAAD, SECTIE_5000 + H2_DRAAD, 'D2 sectie 5.000 m² en meer'),
    (KORT_OUD, KORT_NIEUW, 'D3 korte antwoord'),
    (WAAROM_I210, WAAROM_I210 + '\n\n' + kaart('M069', 'Husqvarna Automower 430V NERA'), 'D5 kaart M069 na M015'),
    (RIJ_4G, RIJ_4G.replace('Husqvarna 410VE NERA of Eufy E18', 'Husqvarna 430V NERA, Husqvarna 410VE NERA of Eufy E18'), 'D5 rij 4G en GPS ingebouwd'),
]

for pid in map(int, ALLEEN):
    naam = {11: 'pagina1', 10: 'hub', 16: 'kleine-tuin', 15: 'grote-tuin'}[pid]
    print(f'\n=== #{pid} {naam}')
    pas_toe(pid, STAPPEN[pid], SCHRIJF, naam, meta=META16 if pid == 16 else None, titel=TITEL16 if pid == 16 else None)
