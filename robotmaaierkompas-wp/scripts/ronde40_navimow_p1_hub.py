#!/usr/bin/env python3
"""Ronde 40: de nieuwe Navimow-modellen op pagina 1 (#11) en de hub (#10)
(tekstwijzigingen-navimow-op-pagina1-en-hub.md, Mandy, 17 oktober 2026; dat bestand staat niet in de repository).

A. Pagina 1: metabeschrijving (acht -> tien), korte antwoord en kop "Vergelijking van de acht modellen" (-> tien),
   rij i210 LiDAR Pro onder de eerste rij van "Welke past bij jouw tuin?", M015 en M016 in de scoretabel en als kaart
   (volgorde M015, M002, M016, M010, M005, M004, M008, M001, M006, M011).
B. Hub: metabeschrijving (Vijf -> Zes), korte antwoord (vijf -> zes), rij i210 LiDAR Pro onder de eerste rij van
   "In een oogopslag", nieuw onderdeel (H3, kaart M015, "Waarom deze") direct na de i206-kaart, "Alle acht modellen
   naast elkaar" en de linktekst "de acht modellen vergeleken" -> tien.

De kaarten zijn hetzelfde skelet als op de Navimow-pagina (#264); het thema vult ze uit modellen.json (analyse,
plus- en minpunten, knop naar de fabrikant; geen Bol-regel omdat de prijstaak "geen aanbod" geeft).
Elke "Was"-tekst moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: eerst een kopie in backups/, daarna opslaan en de LiteSpeed-cache legen via de dataroute (de
modelgegevens ongewijzigd terugzetten; rmk_save_modellen roept litespeed_purge_all aan).
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde40_navimow_p1_hub.py            (proefdraai)
          python3 scripts/ronde40_navimow_p1_hub.py --schrijf
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
NAV = 264
OUD_VOLGORDE = 'M002,M010,M005,M004,M008,M001,M006,M011'
NIEUW_VOLGORDE = 'M015,M002,M016,M010,M005,M004,M008,M001,M006,M011'

pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in (10, 11, NAV)}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld, log = [], []


def blok(h, slug):
    """Het volledige wp:group-blok (wrapper + kaartskelet) van een model."""
    i = h.find(f'aria-labelledby="p-{slug}"')
    if i < 0 or h.count(f'aria-labelledby="p-{slug}"') != 1:
        return None
    s = h.rfind('<!-- wp:group', 0, i)
    e = h.find('<!-- /wp:group -->', i) + len('<!-- /wp:group -->')
    return h[s:e]


def kaart_als(template_blok, nav_blok):
    """Kaart van de Navimow-pagina in de wrapper van de doelpagina (die verschilt per pagina)."""
    art = re.search(r'<article class="rmk-product".*?</article>', nav_blok, re.S).group(0)
    return re.sub(r'<article class="rmk-product".*?</article>', lambda _: art, template_blok, count=1, flags=re.S)


def vervang(pid, was, wordt, wat):
    n = raw[pid].count(was)
    if n != 1:
        meld.append(f'#{pid} {wat}: "Was" {n} keer gevonden (verwacht 1); niet gewijzigd.')
        return
    raw[pid] = raw[pid].replace(was, wordt, 1)
    log.append(f'  #{pid} {wat}:\n    was:   {re.sub("<[^>]+>", " ", was)[:140].strip()}\n    wordt: {re.sub("<[^>]+>", " ", wordt)[:140].strip()}')


for slug in ('segway-navimow-i210-lidar-pro', 'segway-navimow-i205-awd'):
    for pid in (10, 11):
        if f'aria-labelledby="p-{slug}"' in raw[pid]:
            meld.append(f'#{pid}: kaart {slug} staat er al.')
b015, b016 = blok(raw[NAV], 'segway-navimow-i210-lidar-pro'), blok(raw[NAV], 'segway-navimow-i205-awd')
if not b015 or 'data-model="M015"' not in b015 or not b016 or 'data-model="M016"' not in b016:
    sys.exit('Kaarten van M015/M016 niet precies één keer op de Navimow-pagina gevonden. Niets gewijzigd.')

# ---- A. pagina 1
p11_i206 = blok(raw[11], 'segway-navimow-i206-awd')
vervang(11, 'We vergeleken acht modellen op navigatie, helling, app, veiligheid en geluid.',
        'We vergeleken tien modellen op navigatie, helling, app, veiligheid en geluid.', 'A2 korte antwoord')
vervang(11, 'Vergelijking van de acht modellen', 'Vergelijking van de tien modellen', 'A2 kop scoretabel')
vervang(11, '<tr><th scope="row">Tuin tot ongeveer 600 m² met hellingen en obstakels</th><td>Segway Navimow i206 AWD</td><td>Helling tot 45%, camera plus RTK, 4G ingebouwd</td></tr>',
        '<tr><th scope="row">Tuin tot ongeveer 600 m² met hellingen en obstakels</th><td>Segway Navimow i206 AWD</td><td>Helling tot 45%, camera plus RTK, 4G ingebouwd</td></tr>'
        '<tr><th scope="row">Tuin tot ongeveer 1.000 m² met veel obstakels</th><td>Segway Navimow i210 LiDAR Pro</td><td>LiDAR met camera en netwerk-RTK, helling 55% volgens de handleiding</td></tr>',
        'A3 rij "Welke past bij jouw tuin?"')
vervang(11, f'[rmk_scoretabel modellen="{OUD_VOLGORDE}"]', f'[rmk_scoretabel modellen="{NIEUW_VOLGORDE}"]', 'A4 scoretabel')
if p11_i206:
    vervang(11, p11_i206, kaart_als(p11_i206, b015) + '\n\n' + p11_i206 + '\n\n' + kaart_als(p11_i206, b016), 'A4 kaarten M015 vóór en M016 na de i206')
else:
    meld.append('#11: i206-kaart niet precies één keer gevonden.')

# ---- B. hub
p10_i206 = blok(raw[10], 'segway-navimow-i206-awd')
vervang(10, 'Daarom kiezen we niet één winnaar maar vijf modellen, elk voor een andere situatie',
        'Daarom kiezen we niet één winnaar maar zes modellen, elk voor een andere situatie', 'B2 korte antwoord')
eerste = ('<tr><th scope="row">Hellingen, obstakels en diefstalbeveiliging, tot ongeveer 600 m²</th>'
          '<td><a href="#p-segway-navimow-i206-awd">Segway Navimow i206 AWD</a></td><td>92,7</td></tr>')
vervang(10, eerste, eerste + '<tr><th scope="row">Tuin tot ongeveer 1.000 m² met veel obstakels, zonder antenne</th>'
        '<td><a href="#p-segway-navimow-i210-lidar-pro">Segway Navimow i210 LiDAR Pro</a></td><td>96,4</td></tr>', 'B3 rij "In een oogopslag"')
waarom_i206 = re.findall(r'<p><strong>Waarom deze:</strong> een van de hoogste functiescores in onze selectie, helling tot 45%.*?</p>\n', raw[10])
if len(waarom_i206) == 1 and p10_i206:
    nieuw = (waarom_i206[0] + '<h3>Tuin tot 1.000 m² met veel obstakels: Segway Navimow i210 LiDAR Pro</h3>\n</div></section>\n<!-- /wp:html -->\n\n'
             + kaart_als(p10_i206, b015) + '\n\n<!-- wp:html -->\n<section class="rmk-container rmk-section--tight rmk-column"><div class="rmk-prose">\n'
             '<p><strong>Waarom deze:</strong> de hoogste functiescore in onze selectie: LiDAR met camera en netwerk-RTK voor tuinen tot 1.000 m², '
             'helling 55% volgens de handleiding en een optilsensor die het mes stopt. Let op de kosten van 4G na het eerste jaar.</p>\n')
    vervang(10, waarom_i206[0], nieuw, 'B4 onderdeel i210 LiDAR Pro na de i206-kaart')
else:
    meld.append(f'#10: "Waarom deze" van de i206 {len(waarom_i206)} keer gevonden of i206-kaart niet gevonden.')
vervang(10, 'Alle acht modellen naast elkaar', 'Alle tien modellen naast elkaar', 'B5 verwijzing pagina 1')
vervang(10, 'Robotmaaier zonder draad</a>: de acht modellen vergeleken.', 'Robotmaaier zonder draad</a>: de tien modellen vergeleken.', 'B5 linktekst "Meer lezen" (extra, zelfde verwijzing)')

# ---- metabeschrijvingen
meta = {}
for pid, was, wordt in ((11, 'Acht robotmaaiers zonder draad vergeleken op navigatie, helling, app, veiligheid en kosten. Functiescores met bron en datum.',
                         'Tien robotmaaiers zonder draad vergeleken op navigatie, helling, app, veiligheid en kosten. Functiescores met bron en datum.'),
                        (10, 'De beste robotmaaier hangt af van je tuin. Vijf keuzes per situatie met specificaties, kosten en functiescore, met bron en datum.',
                         'De beste robotmaaier hangt af van je tuin. Zes keuzes per situatie met specificaties, kosten en functiescore, met bron en datum.')):
    nu = (pag[pid].get('meta') or {}).get('_yoast_wpseo_metadesc')
    if nu == was:
        meta[pid] = wordt
        log.append(f'  #{pid} metabeschrijving:\n    was:   {was}\n    wordt: {wordt}')
    else:
        meld.append(f'#{pid} metabeschrijving is niet de "Was"-tekst (nu: {nu!r}); niet gewijzigd.')

print('\n'.join(log))
print('\nMeldingen:' if meld else '\nGeen meldingen: alle "Was"-teksten precies één keer gevonden.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde40-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': pag[pid]['status'], 'content': pag[pid]['content']['raw'], 'meta': pag[pid].get('meta')} for pid in (10, 11)},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in (11, 10):
    body = {'content': raw[pid]}
    if pid in meta:
        body['meta'] = {'_yoast_wpseo_metadesc': meta[pid]}
    api(f'wp/v2/pages/{pid}', body)
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}; '
          f'metabeschrijving: {q["meta"].get("_yoast_wpseo_metadesc")!r}')
data = api('rmk/v1/modellen')['data']
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', data))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
