#!/usr/bin/env python3
"""Ronde 79 (opdracht van Mandy, 1 november 2026): M058 op pagina 1 (#11) en de hub (#10), en bronnen, MET DE HAND.

Gerichte vervangingen en toevoegingen via de WordPress-API; de pagina's worden NIET opnieuw gebouwd. Elk anker moet
precies één keer voorkomen; anders schrijft het script niets. Pagina's houden status, slug en titel.

Vooraf (scripts/ronde79_modellen.py): M058 heeft functiescore 79,5 (alarm 0, gecontroleerd); het script weigert anders.

Pagina 1: M058 in de scoretabel na M004 (vóór M008); kaart M058 vóór M008; rij "Grote tuin tot 3.000 m²" na de rij
  "Tuin tot 1.600 m²"; "vierentwintig" -> "vijfentwintig" (korte antwoord, kop); de zin met de zeven merklinks onder
  de tabel weg, op die plek "De Navimow i105E loopt uit: controleer de beschikbaarheid voor je kiest."; bronnen van
  15 modellen vóór de regel "Scoremodel v1.0" (platte lijst, "Modelnaam: " ervoor, zoals de bestaande regels).
Hub: "Zeven keuzes" -> "Acht keuzes" (meta), "zeven modellen" -> "acht modellen"; "Alle vierentwintig modellen naast
  elkaar" en "Meer lezen" "de vierentwintig modellen vergeleken" -> vijfentwintig; tabel "In een oogopslag" met rij
  M058 en op functiescore (hoogste eerst; bij gelijke score blijft de volgorde); onderdeel M058 (H3, kaart, "Waarom
  deze") op volgorde van score, dus na Mova 1200 (80,5) en vóór Dreame (78,6); bronblokken M060 (na Husqvarna) en
  M058 (na Mova 1200), zoals de bestaande blokken (kop + lijst).

Bronregels uit het blad Bronnen van het Excel-bestand, met dezelfde regels als de merkpagina's (scripts/ronde71_bouw.py
soort()/bronnen(); Gardena zoals ronde48_bouw.py), aangevuld voor Ecovacs: ecovacs.com en help.ecovacs.com = Fabrikant,
de pdf op site-static.ecovacs.com = Handleiding. Overgeslagen: winkels (Coolblue, Amazon, Hornbach, x-kom,
testfreaks), Bol, en rijen met status winkelclaim, niet gevonden of niet geopend. Geen dubbele regels.

Gebruik:  python3 scripts/ronde79_p1_hub.py <modeldata.xlsx>            (proefdraai)
          python3 scripts/ronde79_p1_hub.py <modeldata.xlsx> --schrijf  (kopie in backups/, opslaan, LiteSpeed legen)
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
"""
import datetime as dt, html, json, os, re, sys, time
from urllib.parse import urlparse
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
from excel_naar_json import app_store

SCHRIJF = '--schrijf' in sys.argv
XLSX = next(a for a in sys.argv[1:] if a.endswith('.xlsx'))
MAANDEN = 'januari februari maart april mei juni juli augustus september oktober november december'.split()
P1_BRONNEN = ['M059', 'M060', 'M056', 'M057', 'M058', 'M064', 'M046', 'M047', 'M020', 'M022', 'M063', 'M007', 'M052', 'M053', 'M055']

pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in (10, 11)}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
data = api('rmk/v1/modellen')['data']
live = {m['id']: m for m in data['modellen']}
meld, log = [], []


def esc(t):
    return html.escape(t, quote=False)


def kort(s, n=150):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', s))).strip()[:n]


def vervang(pid, was, wordt, wat):
    n = raw[pid].count(was)
    if n != 1:
        meld.append(f'#{pid} {wat}: "Was" {n} keer gevonden (verwacht 1); niet gewijzigd.')
        return
    raw[pid] = raw[pid].replace(was, wordt, 1)
    log.append(f'  #{pid} {wat}:\n    was:   {kort(was)}\n    wordt: {kort(wordt, 300)}')


def blok(h, slug):
    if h.count(f'aria-labelledby="p-{slug}"') != 1:
        return None
    i = h.find(f'aria-labelledby="p-{slug}"')
    s = h.rfind('<!-- wp:group', 0, i)
    e = h.find('<!-- /wp:group -->', i) + len('<!-- /wp:group -->')
    return h[s:e]


def kaart_als(sjabloon, art):
    return re.sub(r'<article class="rmk-product".*?</article>', lambda _: art, sjabloon, count=1, flags=re.S)


def skelet(mid):
    """Zelfde skelet als scripts/ronde71_bouw.py kaart() voor een model met scores."""
    m = live[mid]
    a = 'p-' + m['slug']
    f = lambda v: '' if v is None else str(v)
    ds = '; '.join(f'{k}={f(m["scores"].get(k))}' for k in
                   ('betrouwbaarheid', 'navigatie', 'prijskwaliteit', 'hellingen', 'app', 'veiligheid', 'geluid')) + '; reviews='
    return f'''<article class="rmk-product" aria-labelledby="{a}">
  <div class="rmk-product__head rmk-product__head--nomedia" style="grid-template-columns: 1fr">
    <div class="rmk-product__title">
      <h3 id="{a}">{esc(m['naam'])}</h3>
      <div class="rmk-scorecell" data-rmk-score data-scores="{ds}" data-model="{mid}"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div>
    </div>
  </div>
  <div class="rmk-product__aside rmk-offers">
    <div class="rmk-offer"></div>
  </div>
</article>'''


# ---------------------------------------------------------------- bronnen (regels als scripts/ronde71_bouw.py)
S3 = 'salesforce-knowledge-download.s3.us-west-2.amazonaws.com'
FABRIKANT = ('navimow.com', 'husqvarna.com', 'stihl.nl', 'support.stihl.com', 'eu.worx.com', 'mova.tech', 'eufy.com',
             'garden.roborock.com', 'garden-support.roborock.com', 'gardena.com', 'ecovacs.com')
PDF_HOSTS = ('cdn.shopify.com', 'storage.onpage.it', 'ssc.stihl.com', S3, 'site-static.ecovacs.com')


def soort(u, veld):
    p = urlparse(u)
    host = p.netloc.lower().removeprefix('www.')
    pad = p.path.lower()
    if host.endswith('adobeioruntime.net'):
        return None
    if 'mansier' in host:
        return 'Handleiding (kopie op mansier.com)', None
    if host.endswith('manualslib.com'):
        return 'Handleiding (kopie op manualslib.com)', None
    if host == S3:
        return None if '000038406' in pad else ('Handleiding', 'handleiding (pdf)')
    if host in PDF_HOSTS and pad.endswith('.pdf'):
        return 'Handleiding', None
    if 'zendesk' in host or '/tdrdownload/' in pad:
        return 'Handleiding', None
    if host == 'content.tdr.dss.husqvarnagroup.net':  # Gardena-handleiding (ronde 48: label Handleiding)
        return 'Handleiding', None
    if host == 'service.eufy.com':
        if 'user-guide' in pad:
            return 'Handleiding', 'service.eufy.com, handleiding'
        if 'cellular-data-faq' in pad:
            return 'Fabrikant', 'service.eufy.com, 4G-data'
        return 'Fabrikant', 'service.eufy.com, ' + ('welkom C15' if 'c15' in pad else p.path.rstrip('/').split('/')[-1][:30])
    if host == 'garden-support.roborock.com' and (pad.endswith('.pdf') or 'manual' in pad):
        return 'Handleiding', None
    if host.endswith(FABRIKANT):
        return 'Fabrikant', None
    if host in ('apps.apple.com', 'itunes.apple.com', 'play.google.com'):
        return 'Appwinkel', None
    return None


def bronnen(rijen, prefix=''):
    groepen, overgeslagen = {}, set()
    for r in rijen:
        veld, bron, datum, status = str(r[1] or '').strip(), app_store(r[3]), r[4], str(r[5] or '').strip().lower()
        if 'bol' in (bron + veld).lower() or status.startswith(('winkelclaim', 'niet gevonden', 'niet geopend')):
            continue
        urls = re.findall(r'https?://[^\s;()]+', bron)
        for u in urls:
            s = soort(u, veld)
            host = urlparse(u).netloc.lower().removeprefix('www.')
            if not s:
                overgeslagen.add(host)
                continue
            zelfde_host = sum(urlparse(x).netloc.lower().removeprefix('www.') == host for x in urls) > 1
            g = groepen.setdefault(u, {'label': s[0], 'velden': [], 'datum': None, 'pad': False, 'host': host, 'plek': s[1]})
            g['pad'] = g['pad'] or zelfde_host
            if veld not in g['velden']:
                g['velden'].append(veld)
            ds = datum.strftime('%Y-%m-%d') if hasattr(datum, 'strftime') else str(datum or '')[:10]
            g['datum'] = min(filter(None, [g['datum'], ds]))
    li = []
    for u, g in groepen.items():
        v = g['velden'][:6]
        tekst = ', '.join(v) + (' en meer' if len(g['velden']) > 6 else '')
        p = urlparse(u)
        k = 'handleiding' if '/tdrdownload/' in p.path else 'pdf-bijlage' if 'attachments' in p.path else 'supportartikel' if '/articles/' in p.path else p.path.rstrip('/').split('/')[-1][:40]
        plek = g['plek'] or (g['host'] + (', ' + k if g['pad'] else ''))
        dd = dt.date.fromisoformat(g['datum'])
        li.append((u, f'  <li><div><a href="{html.escape(u)}">{esc(prefix)}{esc(tekst)} ({esc(plek)})</a><div class="rmk-sources__meta">'
                      f'<span class="rmk-chip">{g["label"]}</span><span>geraadpleegd op {dd.day} {MAANDEN[dd.month - 1]} {dd.year}</span></div></div></li>'))
    return li, overgeslagen


wb = openpyxl.load_workbook(XLSX, data_only=True)
bronrijen = {}
for r in wb['Bronnen'].iter_rows(min_row=2, values_only=True):
    if r[0]:
        bronrijen.setdefault(r[0], []).append(r)

# ---- voorwaarde: M058 heeft functiescore 79,5 in de live gegevens
s = live['M058']['scores']
known = {'navigatie': 20, 'hellingen': 10, 'app': 10, 'veiligheid': 10, 'geluid': 5}
if any(s.get(k) is None for k in known):
    sys.exit('M058 heeft nog geen volledige functiescore in de live gegevens. Niets gewijzigd.')
waarde = sum(w * s[k] for k, w in known.items()) / sum(known.values()) * 10
if f'{waarde:.1f}' != '79.5':
    sys.exit(f'M058 functiescore {waarde:.2f}, niet 79,5. Niets gewijzigd.')
print(f'M058 functiescore in de live gegevens: {waarde:.3f} -> 79,5')
for pid in (10, 11):
    if 'aria-labelledby="p-ecovacs-goat-a3000-lidar-pro"' in raw[pid]:
        meld.append(f'#{pid}: kaart M058 staat er al.')

# ---------------------------------------------------------------- A. pagina 1
vervang(11, '[rmk_scoretabel modellen="M015,M002,M016,M010,M059,M060,M056,M057,M005,M004,M008,',
        '[rmk_scoretabel modellen="M015,M002,M016,M010,M059,M060,M056,M057,M005,M004,M058,M008,', 'scoretabel: M058 na M004, vóór M008')
b008 = blok(raw[11], 'dreame-a1-pro')
if b008:
    vervang(11, b008, kaart_als(b008, skelet('M058')) + '\n\n' + b008, 'kaart M058 vóór M008')
else:
    meld.append('#11: kaart M008 niet precies één keer gevonden.')
r1600 = ('<tr><th scope="row">Tuin tot 1.600 m² met 4G en GPS ingebouwd</th><td>Mova LiDAX Ultra 1600</td>'
         '<td>Tot 1.600 m² en 45% helling, 4G en GPS ingebouwd met 1 jaar gratis service volgens Mova</td></tr>')
vervang(11, r1600, r1600 + '<tr><th scope="row">Grote tuin tot 3.000 m²</th><td>Ecovacs GOAT A3000 LiDAR Pro</td>'
        '<td>Tot 3.000 m² en 50% helling volgens Ecovacs, met LiDAR zonder draad</td></tr>', 'rij "Grote tuin tot 3.000 m²"')
vervang(11, 'We vergeleken vierentwintig modellen op navigatie', 'We vergeleken vijfentwintig modellen op navigatie', 'korte antwoord')
vervang(11, 'Vergelijking van de vierentwintig modellen', 'Vergelijking van de vijfentwintig modellen', 'kop scoretabel')
MERKZIN = ('<p>Per merk vergelijken we de modellen uitgebreider op <a href="/segway-navimow-robotmaaier/">Segway Navimow</a>, '
           '<a href="/husqvarna-robotmaaier/">Husqvarna</a>, <a href="/gardena-robotmaaier/">Gardena</a>, '
           '<a href="/stihl-robotmaaier/">Stihl</a>, <a href="/worx-robotmaaier/">Worx</a>, '
           '<a href="/mova-dreame-robotmaaier/">Mova en Dreame</a> en <a href="/eufy-robotmaaier/">Eufy</a>.</p>')
vervang(11, MERKZIN, '<p>De Navimow i105E loopt uit: controleer de beschikbaarheid voor je kiest.</p>',
        'merkzin weg, zin over de i105E op die plek')

SCOREMODEL = '  <li><div><a href="/hoe-we-beoordelen/#scoremodel">Scoremodel v1.0</a>'
p1_bestaand = set(re.findall(r'<li><div><a href="([^"]+)">([^<:]+):', raw[11]))
nieuwe_regels, overgeslagen_hosts, aantal = [], set(), {}
for mid in P1_BRONNEN:
    li, ov = bronnen(bronrijen.get(mid, []), live[mid]['naam'] + ': ')
    overgeslagen_hosts |= ov
    li = [x for u, x in li if (html.escape(u), live[mid]['naam']) not in p1_bestaand]
    aantal[mid] = len(li)
    nieuwe_regels += li
if len(set(nieuwe_regels)) != len(nieuwe_regels):
    meld.append('#11 bronnen: dubbele regels in de nieuwe regels.')
vervang(11, SCOREMODEL, '\n'.join(nieuwe_regels) + '\n' + SCOREMODEL, f'bronnen van {len(P1_BRONNEN)} modellen ({len(nieuwe_regels)} regels)')

# ---------------------------------------------------------------- B. hub
vervang(10, 'Daarom kiezen we niet één winnaar maar zeven modellen, elk voor een andere situatie',
        'Daarom kiezen we niet één winnaar maar acht modellen, elk voor een andere situatie', 'korte antwoord')
vervang(10, 'Alle vierentwintig modellen naast elkaar', 'Alle vijfentwintig modellen naast elkaar', '"Alle … modellen naast elkaar"')
vervang(10, 'Robotmaaier zonder draad</a>: de vierentwintig modellen vergeleken.',
        'Robotmaaier zonder draad</a>: de vijfentwintig modellen vergeleken.', '"Meer lezen"')

# Tabel "In een oogopslag": rij M058 erbij, dan op functiescore (hoogste eerst), gelijke score: volgorde blijft
m = re.findall(r'(<h2 id="in-een-oogopslag">In een oogopslag</h2>\s*<div class="rmk-tablewrap"><table class="rmk-table">'
               r'<thead>.*?</thead><tbody>)(.*?)(</tbody>)', raw[10], re.S)
if len(m) == 1:
    kop, body, slot = m[0]
    rijen = re.findall(r'<tr>.*?</tr>', body, re.S)
    assert ''.join(rijen) == body
    rijen.append('<tr><th scope="row">Grote tuin tot 3.000 m²</th><td><a href="#p-ecovacs-goat-a3000-lidar-pro">'
                 'Ecovacs GOAT A3000 LiDAR Pro</a></td><td>79,5</td></tr>')
    score = lambda r: float(re.findall(r'<td>([\d,]+)</td></tr>$', r)[0].replace(',', '.'))
    gesorteerd = sorted(rijen, key=score, reverse=True)
    print('Oogopslag na:', ' · '.join(f'{kort(re.search(r"<td>(.*?)</td>", r).group(1))} {score(r)}' for r in gesorteerd))
    vervang(10, kop + body + slot, kop + ''.join(gesorteerd) + slot, 'tabel "In een oogopslag": rij M058, op functiescore')
else:
    meld.append(f'#10: tabel "In een oogopslag" {len(m)} keer gevonden.')

hub_sjabloon = blok(raw[10], 'husqvarna-automower-410ve-nera')
W1200 = ('<p><strong>Waarom deze:</strong> LiDAR met camera zonder antenne of RTK, helling tot 45% volgens de fabrikant. Voor '
         'GPS-tracking en een melding buiten de kaart heb je de losse link-module nodig. Zit je tuin onder de 800 m², bekijk dan '
         'ook de Mova LiDAX Ultra 800.</p>\n')
if hub_sjabloon:
    vervang(10, W1200, W1200 + '<h3>Grote tuin tot 3.000 m²: Ecovacs GOAT A3000 LiDAR Pro</h3>\n</div></section>\n<!-- /wp:html -->\n\n'
            + kaart_als(hub_sjabloon, skelet('M058'))
            + '\n\n<!-- wp:html -->\n<section class="rmk-container rmk-section--tight rmk-column"><div class="rmk-prose">\n'
            '<p><strong>Waarom deze:</strong> de grootste draadloze maaier met een score in onze selectie: tot 3.000 m² en 50% '
            'helling volgens Ecovacs, met LiDAR zonder draad. GPS en 4G vragen een losse module en hij is luider (62 dB(A)).</p>\n',
            'onderdeel M058 na Mova 1200 (80,5), vóór Dreame (78,6)')


def bron_blok(h, naam):
    i = h.find('>Bronnen<')
    k = f'<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">{naam}</h3></div>'
    if i < 0 or h.count(k, i) != 1:
        return None
    s = h.rfind('<!-- wp:html -->', 0, h.find(k, i))
    e = h.find('<!-- /wp:group -->', s) + len('<!-- /wp:group -->')
    return h[s:e]


def nieuw_bron_blok(mid):
    li, ov = bronnen(bronrijen.get(mid, []))
    aantal['hub ' + mid] = len(li)
    return ('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">'
            f'{esc(live[mid]["naam"])}</h3></div>\n<!-- /wp:html -->\n\n'
            '<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n'
            '<div class="wp-block-group rmk-container rmk-block rmk-column"><!-- wp:html -->\n<ol class="rmk-sources">\n'
            + '\n'.join(x for _, x in li) + '\n</ol>\n<!-- /wp:html --></div>\n<!-- /wp:group -->')


for na, mid in (('Husqvarna Automower 410VE NERA', 'M060'), ('Mova LiDAX Ultra 1200', 'M058')):
    if bron_blok(raw[10], live[mid]['naam']):
        meld.append(f'#10: bronblok {mid} staat er al.')
    b = bron_blok(raw[10], na)
    if b:
        vervang(10, b, b + '\n\n' + nieuw_bron_blok(mid), f'bronblok {mid} na {na}')
    else:
        meld.append(f'#10: bronblok {na} niet precies één keer gevonden.')

# ---------------------------------------------------------------- metabeschrijving hub
was = 'De beste robotmaaier hangt af van je tuin. Zeven keuzes per situatie met specificaties, kosten en functiescore, met bron en datum.'
wordt = 'De beste robotmaaier hangt af van je tuin. Acht keuzes per situatie met specificaties, kosten en functiescore, met bron en datum.'
meta = None
if (pag[10].get('meta') or {}).get('_yoast_wpseo_metadesc') == was:
    meta = wordt
    log.append(f'  #10 metabeschrijving:\n    was:   {was}\n    wordt: {wordt}')
else:
    meld.append('#10 metabeschrijving is niet de "Was"-tekst; niet gewijzigd.')

print('\n'.join(log))
print('Bronregels per model:', aantal)
print('Overgeslagen hosts (winkels e.d.):', sorted(overgeslagen_hosts))
TEL = {w: re.compile(rf'(?i)\b{w}\b') for w in ('vierentwintig', 'vijfentwintig', 'zeven', 'acht')}
for pid in (10, 11):
    hrefs = re.findall(r'<li><div><a href="([^"]+)">([^<]*)</a>', raw[pid])
    dubbel = len(hrefs) - len(set(hrefs))
    print(f'#{pid}: ' + ', '.join(f'"{w}" {len(r.findall(raw[pid]))}x' for w, r in TEL.items())
          + f'; kaarten {re.findall(r"data-model=\"(M\d+)\"", raw[pid])}; dubbele bronregels {dubbel}')
print('\nMeldingen:' if meld else '\nGeen meldingen: alle ankers precies één keer gevonden.')
for x in meld:
    print('  - ' + x)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
for pid in (10, 11):
    q = api(f'wp/v2/pages/{pid}?context=edit')
    if q['content']['raw'] != pag[pid]['content']['raw'] or q['modified'] != pag[pid]['modified']:
        sys.exit(f'#{pid} is intussen gewijzigd ({q["modified"]}). Niets geschreven.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde79-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': pag[pid]['status'], 'slug': pag[pid]['slug'], 'modified': pag[pid]['modified'],
                      'content': pag[pid]['content']['raw'], 'meta': pag[pid].get('meta')} for pid in (10, 11)},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in (11, 10):
    body = {'content': raw[pid]}
    if pid == 10:
        body['meta'] = {'_yoast_wpseo_metadesc': meta}
    api(f'wp/v2/pages/{pid}', body)
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}), slug {q["slug"]}; inhoud zoals bedoeld: '
          f'{q["content"]["raw"] == raw[pid]}; metabeschrijving: {q["meta"].get("_yoast_wpseo_metadesc")!r}')
d2 = api('rmk/v1/modellen')['data']
assert d2 == data, 'modelgegevens veranderd tijdens het schrijven'
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', d2))
print('Mandy: leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
