#!/usr/bin/env python3
"""Ronde 102: conceptpagina robotmaaier-kopen-waar-op-letten uit de md bouwen (afgeleid van ronde100_bouw.py en
ronde97_bouw.py).

Gebruik:  python3 scripts/ronde102_bouw.py <pagina.md> robotmaaierkompas_modeldata_v1.xlsx
Schrijft scripts/ronde102/kopen-waar-op-letten.json (titel, slug, inhoud, meta). Schrijft niets naar de site.

- Opmaak als de kopersgidsen (/robotmaaier-kleine-tuin/): patroon pagina-merk met het bovenschrift "Kopersgids".
  Geen productkaarten (md: "modellen:" leeg). Kruimelpad en Yoast-kruimeltitel "Robotmaaier kopen".
- Tekstlinks alleen op de plekken in LINKS (elke plek precies 1x in de md, anders stopt het script); allemaal naar
  pagina's die al gepubliceerd zijn. "Meer lezen": beste en zonder draad; de andere pagina's uit de lijst interne links
  van de md zet scripts/ronde102_links.py na publicatie (opdracht Mandy).
- Bronnen per onderwerp van de checklist uit het blad Bronnen: voor de modellen en velden in ONDERWERPEN, alleen
  fabrikant, handleiding en appwinkel (geen winkels, winkelclaims, "niet gevonden", "niet geopend" of Bol), per adres
  één regel. Daarna het scoremodel als eigen methode.
- Metabeschrijving uit de md.
"""
import datetime as dt, html, json, os, re, sys
from urllib.parse import urlparse

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excel_naar_json import app_store  # itunes-adressen -> leesbare App Store-pagina (ronde 29)

MD, XLSX = sys.argv[1:3]
UIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde102', 'kopen-waar-op-letten.json')
MAANDEN = 'januari februari maart april mei juni juli augustus september oktober november december'.split()
KRUIMEL = 'Robotmaaier kopen'
A = lambda u, t: f'<a href="{u}">{t}</a>'
LINKS = [  # (tekst in de md, met link) — elke tekst precies 1x
    ('wat het echt kost, lees je op robotmaaier kosten.', f'wat het echt kost, lees je op {A("/robotmaaier-kosten/", "robotmaaier kosten")}.'),
    ('Zie kleine tuin en grote tuin.', f'Zie {A("/robotmaaier-kleine-tuin/", "kleine tuin")} en {A("/robotmaaier-grote-tuin/", "grote tuin")}.'),
    ('Zie RTK, LiDAR of camera voor 4WD.', f'Zie {A("/robotmaaier-rtk-lidar-camera/", "RTK, LiDAR of camera")} voor 4WD.'),
    ('Zie zonder draad.', f'Zie {A("/robotmaaier-zonder-draad/", "zonder draad")}.'),
    ('Zie RTK, LiDAR of camera.', f'Zie {A("/robotmaaier-rtk-lidar-camera/", "RTK, LiDAR of camera")}.'),
    ('Zie robotmaaier mesjes.', f'Zie {A("/robotmaaier-mesjes/", "robotmaaier mesjes")}.'),
    ('kleine tuin (tot 600 m²) of grote tuin (1.000 tot 3.000 m²)',
     f'{A("/robotmaaier-kleine-tuin/", "kleine tuin")} (tot 600 m²) of {A("/robotmaaier-grote-tuin/", "grote tuin")} (1.000 tot 3.000 m²)'),
    ('Op robotmaaier kosten zetten we', f'Op {A("/robotmaaier-kosten/", "robotmaaier kosten")} zetten we'),
    ('vergelijken we op Husqvarna of Gardena; de andere merken hebben elk een eigen pagina: Segway Navimow, Stihl, Worx, Mova en Dreame en Eufy.',
     f'vergelijken we op {A("/husqvarna-of-gardena-robotmaaier/", "Husqvarna of Gardena")}; de andere merken hebben elk een eigen pagina: '
     f'{A("/segway-navimow-robotmaaier/", "Segway Navimow")}, {A("/stihl-robotmaaier/", "Stihl")}, {A("/worx-robotmaaier/", "Worx")}, '
     f'{A("/mova-dreame-robotmaaier/", "Mova en Dreame")} en {A("/eufy-robotmaaier/", "Eufy")}.'),
    ('Zie robotmaaier voor een kleine tuin en voor een grote tuin.',
     f'Zie {A("/robotmaaier-kleine-tuin/", "robotmaaier voor een kleine tuin")} en {A("/robotmaaier-grote-tuin/", "voor een grote tuin")}.'),
    ('Onze keuzes per situatie vind je op beste robotmaaier;', f'Onze keuzes per situatie vind je op {A("/beste-robotmaaier/", "beste robotmaaier")};'),
    ('Zie robotmaaier zonder draad.', f'Zie {A("/robotmaaier-zonder-draad/", "robotmaaier zonder draad")}.'),
    ('Mail contact@robotmaaierkompas.nl.', 'Mail <a href="mailto:contact@robotmaaierkompas.nl">contact@robotmaaierkompas.nl</a>.'),
]
MEER_LEZEN = ('<h2 id="meer-lezen">Meer lezen</h2>\n<ul>'
              '<li><a href="/beste-robotmaaier/">Beste robotmaaier</a>: onze selectie per situatie.</li>'
              '<li><a href="/robotmaaier-zonder-draad/">Robotmaaier zonder draad</a>: tien modellen vergeleken.</li></ul>')
# Bronnen per onderwerp: (kop, modellen, velden als regex op het veld in het blad Bronnen)
ONDERWERPEN = [
    ('Oppervlak en helling', ['M023', 'M025', 'M070', 'M071', 'M072', 'M018', 'M049', 'M060'],
     r'tuingrootte|helling|kernvelden'),
    ('Draad en installatie', ['M021', 'M026', 'M027', 'M023', 'M024', 'M025'], r'installatie|draad'),
    ('4G, GPS en modules', ['M016', 'M015', 'M002', 'M059', 'M060', 'M069', 'M070', 'M004', 'M005', 'M008', 'M052', 'M046'],
     r'4g|link|verbinding|abonnement|find my|verborgen'),
    ('Beveiliging', ['M006', 'M007', 'M052', 'M053', 'M071', 'M072', 'M055', 'M054', 'M069', 'M070', 'M066', 'M067', 'M068', 'M020', 'M022', 'M021'],
     r'pincode|alarm|beveilig|veiligheid'),
    ('Geluid', ['M069', 'M071', 'M072', 'M018', 'M060'], r'geluid|kernvelden'),
    ('App-ratings', ['M026', 'M046', 'M004', 'M008', 'M006', 'M069', 'M071', 'M056', 'M015'], r'app-rating'),
    ('Garantie en beschikbaarheid', ['M015', 'M069', 'M071', 'M026', 'M046', 'M004', 'M006', 'M056', 'M058', 'M001', 'M010', 'M023', 'M024', 'M025'],
     r'^garantie$|^beschikbaarheid( fabrikant.*)?$'),
    ('Messen', ['M015', 'M016', 'M020', 'M021', 'M022', 'M023', 'M024', 'M025'], r'messen'),
]

md = open(MD, encoding='utf-8').read()
fm, body = re.match(r'^---\n(.*?)\n---\n(.*)$', md, re.S).groups()
fm = dict(re.findall(r'^(\w+): ?(.*)$', fm, re.M))
assert not fm.get('modellen', '').strip() and '{{productbox' not in body, 'deze pagina heeft geen productkaarten'
META = fm['metabeschrijving']
body = re.sub(r'^INSTRUCTIE VOOR DE BOUWER.*?\n', '', body, flags=re.M)
for a, _ in LINKS:
    assert body.count(a) == 1, f'linkplek {body.count(a)}x in de md: {a}'
d = dt.date.fromisoformat(fm['bijgewerkt'])
datum_nl = f'{d.day} {MAANDEN[d.month - 1]} {d.year}'
GELINKT = set()


def esc(t):
    return html.escape(t, quote=False)


def inline(t):
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    for a, b in LINKS:
        if esc(a) in t:
            GELINKT.add(a)
        t = t.replace(esc(a), b)
    return t


def slugid(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower().replace('é', 'e')).strip('-')


def tabel(regels):
    rijen = [[c.strip() for c in r.strip().strip('|').split('|')] for r in regels if not re.match(r'^\|\s*-', r)]
    kop, rest = rijen[0], rijen[1:]
    h = '<div class="rmk-tablewrap"><table class="rmk-table"><thead><tr>' + ''.join(f'<th scope="col">{esc(c)}</th>' for c in kop) + '</tr></thead><tbody>'
    for r in rest:
        cellen = [inline(c) for c in r]
        h += '<tr><th scope="row">' + cellen[0] + '</th>' + ''.join(f'<td>{c}</td>' for c in cellen[1:]) + '</tr>'
    return h + '</tbody></table></div>'


def proza(tekst):
    uit = []
    for deel in re.split(r'\n\s*\n', tekst.strip()):
        regels = deel.strip().split('\n')
        if not deel.strip():
            continue
        if regels[0].startswith('## '):
            t = regels[0][3:].strip()
            uit.append(f'<h2 id="{slugid(t)}">{esc(t)}</h2>')
        elif regels[0].startswith('|'):
            uit.append(tabel(regels))
        elif regels[0].startswith('- '):
            uit.append('<ul>' + ''.join(f'<li>{inline(r[2:].strip())}</li>' for r in regels) + '</ul>')
        elif re.match(r'^\d+\. ', regels[0]):
            assert all(re.match(r'^\d+\. ', r) for r in regels), regels
            uit.append('<ol>' + ''.join(f'<li>{inline(re.sub(r"^\d+\. ", "", r).strip())}</li>' for r in regels) + '</ol>')
        else:
            assert not regels[0].startswith('#'), regels[0]
            uit.append('<p>' + inline(' '.join(r.strip() for r in regels)) + '</p>')
    return '\n'.join(uit)


def sectie(inner):
    return f'<!-- wp:html -->\n<section class="rmk-container rmk-section--tight rmk-column"><div class="rmk-prose">\n{inner}\n</div></section>\n<!-- /wp:html -->'


def groep(inner):
    return ('<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n'
            '<div class="wp-block-group rmk-container rmk-block rmk-column"><!-- wp:html -->\n' + inner + '\n<!-- /wp:html --></div>\n<!-- /wp:group -->')


# ---------------------------------------------------------------- bronnen (zelfde indeling als ronde 97)
S3 = 'salesforce-knowledge-download.s3.us-west-2.amazonaws.com'
FABRIKANT = ('navimow.com', 'husqvarna.com', 'stihl.nl', 'support.stihl.com', 'eu.worx.com', 'mova.tech', 'eufy.com',
             'garden.roborock.com', 'garden-support.roborock.com', 'gardena.com', 'ecovacs.com', 'dreametech.com')
PDF_HOSTS = ('cdn.shopify.com', 'storage.onpage.it', 'ssc.stihl.com', S3, 'site-static.ecovacs.com')


def soort(u):
    p = urlparse(u)
    host, pad = p.netloc.lower().removeprefix('www.'), p.path.lower()
    if host == 'web.archive.org' and 'gardena.com' in u:
        return 'Fabrikant (archief)', 'gardena.com, gearchiveerd'
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
    if 'zendesk' in host or '/tdrdownload/' in pad or host == 'content.tdr.dss.husqvarnagroup.net':
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


def bronnen(mids, veldpat, rijen, namen):
    groepen = {}
    for r in rijen:
        if r[0] not in mids or not re.search(veldpat, str(r[1] or '').strip(), re.I):
            continue
        veld, bron, datum, status = str(r[1] or '').strip(), app_store(r[3]), r[4], str(r[5] or '').strip().lower()
        if 'bol' in (bron + veld).lower() or status.startswith(('winkelclaim', 'niet gevonden', 'niet geopend', 'tegenstrijdig')):
            continue
        urls = re.findall(r'https?://[^\s;()]+', bron)
        for u in urls:
            s = soort(u)
            if not s:
                continue
            host = urlparse(u).netloc.lower().removeprefix('www.')
            g = groepen.setdefault(u, {'label': s[0], 'modellen': [], 'velden': [], 'datum': None, 'host': host, 'plek': s[1]})
            if namen[r[0]] not in g['modellen']:
                g['modellen'].append(namen[r[0]])
            if veld.lower().startswith(('extra kosten', 'verborgen kosten')):
                v = (veld.split(':', 1)[1].strip() if ':' in veld else '') or 'kosten'
            elif veld.lower().startswith('kernvelden'):
                v = 'kernvelden (navigatie, oppervlak, helling, geluid, verbinding)'
            else:
                v = veld
            if v not in g['velden']:
                g['velden'].append(v)
            ds = datum.strftime('%Y-%m-%d') if hasattr(datum, 'strftime') else str(datum or '')[:10]
            if re.match(r'\d{4}-\d{2}-\d{2}$', ds):
                g['datum'] = min(filter(None, [g['datum'], ds]))
    li = []
    hosts = [g['host'] for g in groepen.values()]
    for u, g in groepen.items():
        m = g['modellen']
        wie = ', '.join(m[:-1]) + ' en ' + m[-1] if len(m) > 1 else m[0]
        p = urlparse(u)
        kort = 'handleiding' if '/tdrdownload/' in p.path else (
            re.sub(r'[^a-z0-9-]', '', p.path.rstrip('/').split('/')[-1].lower())[:40] if hosts.count(g['host']) > 1 else '')
        plek = g['plek'] or (g['host'] + (', ' + kort if kort else ''))
        dd = dt.date.fromisoformat(g['datum'])
        li.append(f'  <li><div><a href="{html.escape(u)}">{esc(wie)}: {esc(", ".join(g["velden"][:4]).lower())} ({esc(plek)})</a>'
                  f'<div class="rmk-sources__meta"><span class="rmk-chip">{g["label"]}</span><span>geraadpleegd op '
                  f'{dd.day} {MAANDEN[dd.month - 1]} {dd.year}</span></div></div></li>')
    return li


wb = openpyxl.load_workbook(XLSX, data_only=True)
bronrijen = [r for r in wb['Bronnen'].iter_rows(min_row=2, values_only=True) if r[0]]
namen = {r[0]: f'{r[1]} {r[2]}'.replace('Segway Navimow', 'Navimow') for r in wb['Modellen'].iter_rows(min_row=2, values_only=True) if r[0]}

# ---------------------------------------------------------------- pagina
titel = fm['titel']
delen = [f'''<!-- wp:group {{"tagName":"main","className":"rmk","layout":{{"type":"default"}},"anchor":"inhoud"}} -->
<main id="inhoud" class="wp-block-group rmk"><!-- wp:html -->
<div class="rmk-container rmk-column">
  <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li aria-current="page">{esc(KRUIMEL)}</li></ol></nav>
  <header class="rmk-pagehead">
    <p class="rmk-eyebrow">Kopersgids</p>
    <h1>{esc(titel)}</h1>
    <p class="rmk-meta">Door <a href="/over-ons/mandy-van-den-broek/">{esc(fm['auteur'])}</a> · bijgewerkt op {datum_nl}</p>
  </header>
</div>
<!-- /wp:html -->''']
delen.append(groep(f'''<aside class="rmk-honesty" aria-label="Hoe deze pagina tot stand kwam">
  <span class="rmk-honesty__icon"><svg class="rmk-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M16.2 7.8 13.3 13.3 10.7 10.7Z"/><path d="M7.8 16.2 10.7 10.7 13.3 13.3Z"/></svg></span>
  <div class="rmk-honesty__text">
    <p><strong>Vergeleken op basis van handleidingen, fabrikantpagina's en winkelinformatie. Bijgewerkt op {datum_nl}.</strong> Zo vergelijken we: zie <a href="/hoe-we-beoordelen/">Hoe we beoordelen</a>.</p>
    <div class="rmk-honesty__links"><a href="/hoe-we-beoordelen/#scoremodel">Zo werkt ons scoremodel</a><a href="/hoe-we-beoordelen/#verdienmodel">Zo verdienen we geld</a></div>
  </div>
</aside>'''))

body = re.sub(r'^# .*\n', '', body, flags=re.M).replace('{{eerlijkheidsblok}}', '')
voor_faq, na_faq = body.split('{{faq}}')
na_faq, staart = na_faq.split('{{bronnenlijst}}')
assert not staart.strip()
delen.append(sectie(proza(voor_faq) + '\n' + MEER_LEZEN))
faq, rest = re.split(r'\n## ', na_faq.strip(), maxsplit=1)
vragen = re.findall(r'\*\*(.+?)\*\*\s*(.+?)(?=\n\s*\n\*\*|\Z)', faq.strip(), re.S)
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h2 style="font-size: var(--rmk-fs-xl)">Veelgestelde vragen</h2></div>\n<!-- /wp:html -->')
delen.append(groep('<div class="rmk-faq">\n' + '\n'.join(f'  <details><summary>{esc(v)}</summary><div><p>{inline(" ".join(a.split()))}</p></div></details>' for v, a in vragen) + '\n</div>'))
delen.append(sectie(proza('## ' + rest)))
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column" style="padding-top: 24px"><h2 style="font-size: var(--rmk-fs-xl)">Bronnen</h2>'
             '<p class="rmk-small">Per onderwerp van de checklist, uit handleidingen, fabrikantpagina\'s en appwinkels.</p></div>\n<!-- /wp:html -->')
telling = {}
for kop, mids, pat in ONDERWERPEN:
    li = bronnen(mids, pat, bronrijen, namen)
    telling[kop] = len(li)
    assert li, f'geen bronnen voor {kop}'
    delen.append(f'<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">{esc(kop)}</h3></div>\n<!-- /wp:html -->')
    delen.append(groep('<ol class="rmk-sources">\n' + '\n'.join(li) + '\n</ol>'))
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">Scoremodel</h3></div>\n<!-- /wp:html -->')
delen.append(groep('<ol class="rmk-sources">\n  <li><div><a href="/hoe-we-beoordelen/#scoremodel">Scoremodel v1.0</a><div class="rmk-sources__meta"><span class="rmk-chip rmk-chip--brand">Eigen methode</span></div></div></li>\n</ol>'))
delen.append('<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n'
             '<div class="wp-block-group rmk-container rmk-block rmk-column">\n<!-- wp:pattern {"slug":"robotmaaierkompas/auteursblok"} /-->\n</div>\n<!-- /wp:group -->\n'
             '</main>\n<!-- /wp:group -->')

inhoud = '\n\n'.join(x for x in delen if x)
assert GELINKT == {a for a, _ in LINKS}, f'niet gelinkt: {set(a for a, _ in LINKS) - GELINKT}'
os.makedirs(os.path.dirname(UIT), exist_ok=True)
json.dump({'slug': fm['slug'], 'title': titel, 'status': 'draft', 'content': inhoud, 'kaarten': [],
           'meta': {'_yoast_wpseo_metadesc': META, '_yoast_wpseo_bctitle': KRUIMEL}},
          open(UIT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({'geschreven': UIT, 'bronregels': telling, 'faq': len(vragen), 'tekens': len(inhoud)}, ensure_ascii=False))
