#!/usr/bin/env python3
"""Ronde 21: tekstwijzigingen na de eerste controle (tekstwijzigingen-controle1.md, secties A tot en met C).

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde21_upload.py          (proefdraai, schrijft niets)
          python3 scripts/ronde21_upload.py --schrijf
Publiceert niets: elke pagina moet een concept zijn en blijft dat. Elke "Was"-tekst moet precies
één keer voorkomen; anders stopt het script vóór er iets geschreven is.
"""
import base64, json, os, sys, urllib.request, urllib.error

SITE = 'https://robotmaaierkompas.nl/wp-json/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
SCHRIJF = '--schrijf' in sys.argv
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()
AFF = '<a href="/affiliate-melding/">affiliate-melding</a>'

# (pagina-id, was, wordt): exacte HTML in de ruwe inhoud
PAGINAS = [
    # A1 affiliate-melding
    (81, 'robotmaaierkompas.nl verdient geld met affiliatelinks. Als je via een winkelknop iets koopt, krijgen wij soms een commissie van de winkel. Jij betaalt niets extra.',
         'robotmaaierkompas.nl is gratis te gebruiken. Op dit moment verdienen we niets aan de links naar winkels op deze site. Dat kan later veranderen: zodra we samenwerken met winkels via affiliatelinks, melden we dat hier en bij de links zelf.'),
    # A2 over ons (de link naar de affiliate-melding zit in de nieuwe zin)
    (77, 'We verdienen geld met affiliatelinks: koop je via een knop, dan krijgen wij soms een commissie van de winkel. Dat verandert de score of de volgorde niet. Lees hoe in <a href="/hoe-we-beoordelen/#verdienmodel">Zo verdienen we geld</a> op de pagina <a href="/hoe-we-beoordelen/">Hoe we beoordelen</a>.',
         f'Fabrikanten en winkels kunnen geen plek in onze lijsten kopen en beïnvloeden onze score niet. Op dit moment verdienen we niets aan de links naar winkels; verandert dat, dan melden we het in de {AFF}.'),
    # A3 colofon
    (80, f'We verdienen een commissie als je via onze knoppen koopt. Lees meer in de {AFF}.',
         f'Op dit moment verdienen we niets aan de links op deze site. Zie de {AFF}.'),
    # A4 hoe we beoordelen, Zo verdienen we geld
    (76, f'Koop je iets via een winkelknop, dan kan de winkel ons een commissie betalen. Jij betaalt niets extra. De volgorde in onze lijsten volgt de score, niet de commissie. Zie ook de {AFF}.',
         f'Op dit moment verdienen we niets aan de links naar winkels. Verandert dat, dan melden we het in de {AFF} en bij de links. De volgorde in onze lijsten volgt de score en kan niet worden gekocht.'),
    # A6 homepage: het patroon met de regel "Advertentie: ..." eruit (terugzetten: zie bouwlogboek ronde 21)
    (9, '<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n<div class="wp-block-group rmk-container rmk-block rmk-column">\n<!-- wp:pattern {"slug":"robotmaaierkompas/affiliate-melding"} /-->\n</div>\n<!-- /wp:group -->\n',
         ''),
    # B7 hub, zin "Waarom deze" bij Husqvarna
    (10, 'en de prijs ligt ruim 3.000 euro.', 'en de prijs ligt boven de 3.000 euro.'),
    # B8 mesjespagina, eerlijkheidsblok (opmaak zoals op de hub)
    (236, '<strong>Gebaseerd op handleidingen en fabrikantpagina\'s, bijgewerkt op 7 oktober 2026.</strong> We testen de maaiers niet zelf. Zo werken we: zie <a href="/hoe-we-beoordelen/">Hoe we beoordelen</a>.',
          '<strong>Vergeleken op basis van handleidingen, fabrikantpagina\'s en winkelinformatie. Bijgewerkt op 7 oktober 2026.</strong> Zo vergelijken we: zie <a href="/hoe-we-beoordelen/">Hoe we beoordelen</a>.'),
    # B9 mesjespagina, zin onder de tabel
    (236, 'Dat ligt in dezelfde orde van grootte als wat wij zien voor een verpakking van 12, maar het hangt af van het aantal messen per verpakking.',
          'Dat ligt in dezelfde orde van grootte als de verpakkingen die wij zagen, maar het hangt af van het aantal messen per verpakking.'),
]
# A5 footer (template part, aangepaste versie in de site-editor)
FOOTER = (f'Wij kunnen een commissie ontvangen bij aankopen via links op deze site. Zie de {AFF}.',
          f'Op dit moment verdienen we niets aan de links op deze site. Zie de {AFF}.')
# A6 overal: de regel verbergen zolang er geen affiliatelinks zijn (aanvullende CSS)
CSS_AFF = '/* Ronde 21: geen affiliatelinks bij de lancering; weghalen zodra de programma\'s zijn goedgekeurd */\n.rmk-affnote { display: none !important; }'
# B7 modelgegevens M010
M010 = {'analyse': ('Daar staat tegenover dat de prijs rond 3.000 euro ligt', 'Daar staat tegenover dat de prijs boven de 3.000 euro ligt'),
        'minpunt': ('Prijs rond 3.000 euro', 'Prijs boven 3.000 euro')}
# C metabeschrijvingen (Yoast)
META = {
    82: "Hoe robotmaaierkompas.nl met je gegevens omgaat: wat we bewaren, waarom en hoe lang, en welke rechten je hebt.",
    83: "Welke cookies robotmaaierkompas.nl gebruikt en hoe je je keuze op elk moment kunt wijzigen.",
    81: "Hoe robotmaaierkompas.nl geld verdient en wat dat betekent voor onze scores en de volgorde in onze lijsten.",
    84: "Hoe we robotmaaiers vergelijken, onze pagina's bijwerken en fouten corrigeren.",
    80: "Wie achter robotmaaierkompas.nl zit en hoe je contact opneemt.",
    79: "Een vraag, tip of fout gevonden? Mail robotmaaierkompas.nl via contact@robotmaaierkompas.nl.",
    77: "Een onafhankelijk project van Mandy van den Broek: robotmaaiers vergeleken op specificaties, kosten en reviews.",
    78: "Mandy van den Broek vergelijkt producten voor kopers in Nederland en beheert keukenapparaatgids.nl en compareaitools.org.",
    76: "Hoe we robotmaaiers beoordelen: zeven onderdelen met vaste gewichten, bronnen met status en een openbaar scoremodel.",
    18: "De prijs van de maaier is maar een deel. Wat kosten verbinding, antidiefstal en messen? Acht modellen, met bron en datum.",
    236: "Hoe vaak vervang je robotmaaier mesjes en wat kosten ze per jaar? Prijzen en termijnen van vijf merken, met bron.",
    17: "Robotmaaier zonder grensdraad: hoe werkt het met RTK, camera of LiDAR en wanneer kies je het? Voor- en nadelen.",
    13: "Welke robotmaaier tests zijn er? Overzicht van Test-Aankoop, Stiftung Warentest en de Consumentenbond, zonder testcijfers over te nemen.",
    11: "Acht robotmaaiers zonder draad vergeleken op navigatie, helling, app, veiligheid en kosten. Functiescores met bron en datum.",
    12: "Robotmaaiers naast elkaar op tuingrootte, navigatie, helling en verbinding. Filterbare tabel met functiescores, bron en datum.",
    10: "De beste robotmaaier hangt af van je tuin. Vijf keuzes per situatie met specificaties, kosten en functiescore, met bron en datum.",
    9: "Kies een robotmaaier met een open scoremodel. Elke waarde met bron en datum, ook de kosten die niet op de winkelpagina staan.",
}


def api(path, data=None):
    req = urllib.request.Request(SITE + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data, ensure_ascii=False).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:300]!r}')


def vervang(naam, raw, was, wordt):
    """Geeft de nieuwe tekst terug; stopt als 'was' niet precies één keer voorkomt (tenzij al aangepast)."""
    if was not in raw and (wordt in raw if wordt else 'robotmaaierkompas/affiliate-melding' not in raw):
        print(f'  {naam}: al aangepast')
        return raw
    n = raw.count(was)
    if n != 1:
        sys.exit(f'{naam}: "Was"-tekst {n} keer gevonden, verwacht 1. Niets geschreven.')
    print(f'  {naam}: vervangen')
    return raw.replace(was, wordt)


# 1. Alles eerst controleren en voorbereiden (nog niets schrijven)
nieuw, statussen = {}, {}
for pid in sorted({p for p, _, _ in PAGINAS} | set(META)):
    p = api(f'wp/v2/pages/{pid}?context=edit')
    if p['status'] != 'draft':
        sys.exit(f'#{pid} {p["slug"]} heeft status {p["status"]}, geen concept. Niets geschreven.')
    statussen[pid] = p
    nieuw[pid] = p['content']['raw']
print('Pagina\'s:')
for i, (pid, was, wordt) in enumerate(PAGINAS):
    nieuw[pid] = vervang(f'#{pid} {statussen[pid]["slug"]} ({i + 1})', nieuw[pid], was, wordt)

delen = api('wp/v2/template-parts?context=edit&per_page=100')
footer = [t for t in delen if t['slug'] == 'footer' and t.get('source') == 'custom']
if len(footer) != 1:
    sys.exit(f'Footer: {len(footer)} aangepaste footers gevonden, verwacht 1. Niets geschreven.')
footer = footer[0]
print('Footer:')
footer_nieuw = vervang(f'footer ({footer["id"]})', footer['content']['raw'], *FOOTER)

gs_id = api('wp/v2/themes?status=active')[0]['_links']['wp:user-global-styles'][0]['href'].rstrip('/').split('/')[-1]
gs = api(f'wp/v2/global-styles/{gs_id}?context=edit')
css = (gs.get('styles') or {}).get('css') or ''
print('Aanvullende CSS:', 'regel staat er al' if '.rmk-affnote' in css else 'regel toevoegen')

mod = api('rmk/v1/modellen')['data']
m = [x for x in mod['modellen'] if x.get('id') == 'M010']
if len(m) != 1:
    sys.exit('M010 niet (of dubbel) gevonden. Niets geschreven.')
m = m[0]
print('Modelgegevens M010:')
m['analyse'] = vervang('analyse', m['analyse'], *M010['analyse'])
mp = '\n'.join(m['minpunten'])
mp = vervang('minpunten', mp, *M010['minpunt'])
if '\n'.join(m['minpunten']) != mp:
    m['minpunten'] = mp.split('\n')

print('Metabeschrijvingen:')
for pid, tekst in META.items():
    assert len(tekst) <= 155, (pid, len(tekst))
    oud = statussen[pid]['meta'].get('_yoast_wpseo_metadesc') or ''
    print(f'  #{pid} {statussen[pid]["slug"]}: {"al goed" if oud == tekst else "zetten"} ({len(tekst)} tekens)')

if not SCHRIJF:
    sys.exit(0)

# 2. Schrijven
for pid, raw in nieuw.items():
    body = {}
    if raw != statussen[pid]['content']['raw']:
        body['content'] = raw
    if pid in META and (statussen[pid]['meta'].get('_yoast_wpseo_metadesc') or '') != META[pid]:
        body['meta'] = {'_yoast_wpseo_metadesc': META[pid]}
    if body:
        body['status'] = 'draft'
        api(f'wp/v2/pages/{pid}', body)
if footer_nieuw != footer['content']['raw']:
    api(f'wp/v2/template-parts/{footer["id"]}', {'content': footer_nieuw})
if '.rmk-affnote' not in css:
    styles = dict(gs.get('styles') or {})
    styles['css'] = (css.rstrip() + '\n' if css else '') + CSS_AFF
    api(f'wp/v2/global-styles/{gs_id}', {'styles': styles})
print('Modelgegevens:', api('rmk/v1/modellen', mod))

# 3. Controle: status, nieuwe teksten en metabeschrijvingen
fout = False
for pid in nieuw:
    p = api(f'wp/v2/pages/{pid}?context=edit')
    raw = p['content']['raw']
    ok = p['status'] == 'draft' and all(raw.count(w) == 1 for q, _, w in PAGINAS if q == pid and w) \
        and 'robotmaaierkompas/affiliate-melding' not in raw and (pid not in META or p['meta'].get('_yoast_wpseo_metadesc') == META[pid])
    fout |= not ok
    print(f'#{pid} {p["slug"]}: status {p["status"]}, {"in orde" if ok else "FOUT"}')
sys.exit(1 if fout else 0)
