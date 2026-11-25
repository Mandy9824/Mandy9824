#!/usr/bin/env python3
"""Ronde 115: conceptpagina stilste-robotmaaier uit pagina-robotmaaier-stil.md bouwen (afgeleid van ronde106_bouw.py).

Gebruik:  python3 scripts/ronde115_bouw.py pagina-robotmaaier-stil.md robotmaaierkompas_modeldata_v1.xlsx modellen.json
Schrijft scripts/ronde115/stilste.json (titel, slug, inhoud, meta, kaarten). Schrijft niets naar de site.
modellen.json: de live modelgegevens (rmk/v1/modellen), voor slug, naam en scores.

- Opmaak als de grote-tuinpagina: patroon pagina-merk met het bovenschrift "Kopersgids"; kruimelpad en
  Yoast-kruimeltitel "Stilste robotmaaier".
- Productkaarten M069, M071, M059, M004, M047, M015 in die volgorde (instructie, kop "modellen:" en hoofdtekst van
  de md moeten gelijk zijn; anders stopt het script). De ### kop wordt de titel van de kaart. Het thema vult
  specificatiekaart, teksten en het prijsblok (Bol, Coolblue, Amazon volgens prijstaken en schakelaars, anders
  "Bekijk de actuele prijs"). Geen winkellinks of winkelnamen in de inhoud.
- Tekst letterlijk uit de md; afwijkingen tegen de modelgegevens worden gemeld (BOUWLOGBOEK), niet aangepast.
- Bronnen per model uit het blad Bronnen, alleen de velden die de pagina gebruikt (VELDPAT: geluid, oppervlak,
  navigatie, helling, verbinding/4G, kernvelden). Filterregels als ronde 97/102/106: alleen fabrikant, handleiding,
  appwinkel; geen winkels, winkelclaims, "niet gevonden", "niet geopend", "tegenstrijdig" of Bol.
- "Meer lezen": de pagina's uit de lijst interne links van de md die niet al in de tekst gelinkt zijn.
- Metabeschrijving uit de md.
"""
import datetime as dt, html, json, os, re, sys
from urllib.parse import urlparse

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excel_naar_json import app_store  # itunes-adressen -> leesbare App Store-pagina (ronde 29)

MD, XLSX, MODELLEN = sys.argv[1:4]
UIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde115', 'stilste.json')
MAANDEN = 'januari februari maart april mei juni juli augustus september oktober november december'.split()
KRUIMEL = 'Stilste robotmaaier'
KAARTEN = ['M069', 'M071', 'M059', 'M004', 'M047', 'M015']
# Verder in de tabellen en tekst bij typenaam genoemd (bronnen, geen kaart): de tabel "zonder draad met een score",
# de Navimow X420, de Mova AWD-modellen, de met-draadmodellen (Cramer RM1000-RM2700, Gardena Sileno max 1200,
# Stihl iMOW 3 EVO) en de Worx Landroid S en L.
TABEL_MODELLEN = ['M072', 'M005', 'M064', 'M046', 'M063', 'M011', 'M055', 'M070', 'M052', 'M053', 'M016', 'M002',
                  'M056', 'M057', 'M020', 'M022', 'M066', 'M067', 'M068', 'M058', 'M008', 'M060', 'M006', 'M007',
                  'M018', 'M061', 'M062', 'M042', 'M043', 'M044', 'M045', 'M054', 'M027', 'M050', 'M051']
VELDPAT = r'geluid|tuingrootte|^navigatie|helling|kernvelden|verbinding|^4g'
A = lambda u, t: f'<a href="{u}">{t}</a>'
LINKS = [  # (tekst in de md, met link) — elke tekst precies 1x
    ('Hoe we scoren: zie Hoe we beoordelen.', f'Hoe we scoren: zie {A("/hoe-we-beoordelen/", "Hoe we beoordelen")}.'),
    ('zie robotmaaier voor hellingen.', f'zie {A("/robotmaaier-helling/", "robotmaaier voor hellingen")}.'),
    ('Zie robotmaaier kopen: waar op letten.', f'Zie {A("/robotmaaier-kopen-waar-op-letten/", "robotmaaier kopen: waar op letten")}.'),
    ('Mail contact@robotmaaierkompas.nl.', 'Mail <a href="mailto:contact@robotmaaierkompas.nl">contact@robotmaaierkompas.nl</a>.'),
]
MEER_LEZEN = ('<h2 id="meer-lezen">Meer lezen</h2>\n<ul>'  # niet al in de tekst gelinkt (helling en kopen staan in de tekst)
              '<li><a href="/beste-robotmaaier/">Beste robotmaaier</a>: onze selectie per situatie.</li>'
              '<li><a href="/robotmaaier-zonder-draad/">Robotmaaier zonder draad</a>: tien modellen vergeleken.</li>'
              '<li><a href="/robotmaaier-kleine-tuin/">Robotmaaier voor een kleine tuin</a>: tot 600 m².</li>'
              '<li><a href="/robotmaaier-grote-tuin/">Robotmaaier voor een grote tuin</a>: 1.000 tot 3.000 m².</li>'
              '<li><a href="/robotmaaier-gps/">Robotmaaier met GPS</a>: welke modellen hebben het echt?</li>'
              '<li><a href="/robotmaaier-rtk-lidar-camera/">RTK, LiDAR of camera</a>: hoe navigeert een robotmaaier zonder draad?</li>'
              '<li><a href="/robotmaaier-kosten/">Robotmaaier kosten</a>: wat het echt kost, met verborgen kosten.</li>'
              '<li>Per merk: <a href="/segway-navimow-robotmaaier/">Segway Navimow</a>, <a href="/husqvarna-robotmaaier/">Husqvarna</a>, '
              '<a href="/gardena-robotmaaier/">Gardena</a>, <a href="/stihl-robotmaaier/">Stihl</a>, <a href="/worx-robotmaaier/">Worx</a>, '
              '<a href="/mova-dreame-robotmaaier/">Mova en Dreame</a> en <a href="/eufy-robotmaaier/">Eufy</a>.</li></ul>')

modellen = {m['id']: m for m in json.load(open(MODELLEN, encoding='utf-8'))['modellen']}
md = open(MD, encoding='utf-8').read()
fm, body = re.match(r'^---\n(.*?)\n---\n(.*)$', md, re.S).groups()
fm = dict(re.findall(r'^(\w+): ?(.*)$', fm, re.M))
assert [x.strip() for x in fm['modellen'].split(',')] == KAARTEN, 'kop modellen: wijkt af van de instructie'
assert fm['status'] == 'concept' and fm['slug'] == 'stilste-robotmaaier'
META = fm['metabeschrijving']
body = re.sub(r'^INSTRUCTIE VOOR DE BOUWER.*?\n', '', body, flags=re.M)
for a, _ in LINKS:
    assert body.count(a) == 1, f'linkplek {body.count(a)}x in de md: {a}'
d = dt.date.fromisoformat(fm['bijgewerkt'])
datum_nl = f'{d.day} {MAANDEN[d.month - 1]} {d.year}'
GELINKT = set()

assert re.findall(r'\{\{productbox model=(M\d+)\}\}', body) == KAARTEN


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


def anker(mid):
    return 'p-' + modellen[mid]['slug']


def kaart(mid, titel):
    s = modellen[mid]['scores']
    f = lambda v: '' if v is None else str(v)
    ds = '; '.join(f'{k}={f(s.get(k))}' for k in ('betrouwbaarheid', 'navigatie', 'prijskwaliteit', 'hellingen', 'app', 'veiligheid', 'geluid')) + '; reviews='
    a = anker(mid)
    return groep(f'''<article class="rmk-product" aria-labelledby="{a}">
  <div class="rmk-product__head rmk-product__head--nomedia" style="grid-template-columns: 1fr">
    <div class="rmk-product__title">
      <h3 id="{a}">{esc(titel)}</h3>
      <div class="rmk-scorecell" data-rmk-score data-scores="{ds}" data-model="{mid}"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div>
    </div>
  </div>
  <div class="rmk-product__aside rmk-offers">
    <div class="rmk-offer"></div>
  </div>
</article>''')


# ---------------------------------------------------------------- bronnen (indeling als ronde 97)
S3 = 'salesforce-knowledge-download.s3.us-west-2.amazonaws.com'
FABRIKANT = ('navimow.com', 'husqvarna.com', 'stihl.nl', 'support.stihl.com', 'eu.worx.com', 'mova.tech', 'eufy.com',
             'garden.roborock.com', 'garden-support.roborock.com', 'gardena.com', 'ecovacs.com', 'dreametech.com',
             'cramertools.com')  # ronde 115: Cramer RM-modellen
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
    if host == 'garden-support.roborock.com' and (pad.endswith('.pdf') or 'manual' in pad):
        return 'Handleiding', None
    if host.endswith(FABRIKANT):
        return 'Fabrikant', None
    if host in ('apps.apple.com', 'itunes.apple.com', 'play.google.com'):
        return 'Appwinkel', None
    return None


def bronnen(mid, rijen):
    groepen = {}
    for r in rijen:
        veld, bron, datum, status = str(r[1] or '').strip(), app_store(r[3]), r[4], str(r[5] or '').strip().lower()
        if r[0] != mid or not re.search(VELDPAT, veld, re.I):
            continue
        if 'bol' in (bron + veld).lower() or status.startswith(('winkelclaim', 'niet gevonden', 'niet geopend', 'tegenstrijdig')):
            continue
        urls = re.findall(r'https?://[^\s;()]+', bron)
        for u in urls:
            s = soort(u)
            if not s:
                continue
            host = urlparse(u).netloc.lower().removeprefix('www.')
            g = groepen.setdefault(u, {'label': s[0], 'velden': [], 'datum': None, 'host': host, 'plek': s[1]})
            v = 'kernvelden (navigatie, oppervlak, helling, geluid, verbinding)' if veld.lower().startswith('kernvelden') else veld
            if v not in g['velden']:
                g['velden'].append(v)
            ds = datum.strftime('%Y-%m-%d') if hasattr(datum, 'strftime') else str(datum or '')[:10]
            if re.match(r'\d{4}-\d{2}-\d{2}$', ds):
                g['datum'] = min(filter(None, [g['datum'], ds]))
    li = []
    hosts = [g['host'] for g in groepen.values()]
    for u, g in groepen.items():
        v = g['velden'][:6]
        tekst = ', '.join(v) + (' en meer' if len(g['velden']) > 6 else '')
        p = urlparse(u)
        kort = 'handleiding' if '/tdrdownload/' in p.path else 'pdf-bijlage' if 'attachments' in p.path else \
            'supportartikel' if '/articles/' in p.path else p.path.rstrip('/').split('/')[-1][:40]
        plek = g['plek'] or (g['host'] + (', ' + kort if hosts.count(g['host']) > 1 else ''))
        dd = dt.date.fromisoformat(g['datum'])
        li.append(f'  <li><div><a href="{html.escape(u)}">{esc(tekst)} ({esc(plek)})</a><div class="rmk-sources__meta">'
                  f'<span class="rmk-chip">{g["label"]}</span><span>geraadpleegd op {dd.day} {MAANDEN[dd.month - 1]} {dd.year}</span></div></div></li>')
    return li


wb = openpyxl.load_workbook(XLSX, data_only=True)
bronrijen = [r for r in wb['Bronnen'].iter_rows(min_row=2, values_only=True) if r[0]]


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
stukken = re.split(r'\{\{productbox model=(M\d+)\}\}', voor_faq)
tekst = stukken[0]
kaarttitel = {}
for i in range(1, len(stukken), 2):
    mid, na = stukken[i], stukken[i + 1]
    tekst, kop = re.match(r'^(.*)\n### (.+?)\s*$', tekst.rstrip(), re.S).groups()
    kaarttitel[mid] = kop
    delen.append(sectie(proza(tekst)) if tekst.strip() else '')
    delen.append(kaart(mid, kop))
    tekst = na
delen.append(sectie(proza(tekst) + '\n' + MEER_LEZEN))
faq, rest = re.split(r'\n## ', na_faq.strip(), maxsplit=1)
vragen = re.findall(r'\*\*(.+?)\*\*\s*(.+?)(?=\n\s*\n\*\*|\Z)', faq.strip(), re.S)
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h2 style="font-size: var(--rmk-fs-xl)">Veelgestelde vragen</h2></div>\n<!-- /wp:html -->')
delen.append(groep('<div class="rmk-faq">\n' + '\n'.join(f'  <details><summary>{esc(v)}</summary><div><p>{inline(" ".join(a.split()))}</p></div></details>' for v, a in vragen) + '\n</div>'))
delen.append(sectie(proza('## ' + rest)))
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column" style="padding-top: 24px"><h2 style="font-size: var(--rmk-fs-xl)">Bronnen</h2>'
             '<p class="rmk-small">Per model, uit handleidingen, fabrikantpagina\'s en appwinkels.</p></div>\n<!-- /wp:html -->')
telling = {}
for mid in KAARTEN + TABEL_MODELLEN:
    li = bronnen(mid, bronrijen)
    telling[mid] = len(li)
    assert li, f'geen bronnen voor {mid}'
    naam = kaarttitel.get(mid) or modellen[mid]['naam'].replace('Segway Navimow', 'Navimow')
    delen.append(f'<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">{esc(naam)}</h3></div>\n<!-- /wp:html -->')
    delen.append(groep('<ol class="rmk-sources">\n' + '\n'.join(li) + '\n</ol>'))
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">Scoremodel</h3></div>\n<!-- /wp:html -->')
delen.append(groep('<ol class="rmk-sources">\n  <li><div><a href="/hoe-we-beoordelen/#scoremodel">Scoremodel v1.0</a><div class="rmk-sources__meta"><span class="rmk-chip rmk-chip--brand">Eigen methode</span></div></div></li>\n</ol>'))
delen.append('<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n'
             '<div class="wp-block-group rmk-container rmk-block rmk-column">\n<!-- wp:pattern {"slug":"robotmaaierkompas/auteursblok"} /-->\n</div>\n<!-- /wp:group -->\n'
             '</main>\n<!-- /wp:group -->')

inhoud = '\n\n'.join(x for x in delen if x)
assert GELINKT == {a for a, _ in LINKS}, f'niet gelinkt: {set(a for a, _ in LINKS) - GELINKT}'
assert not re.search(r'\{\{|bol\.com|coolblue|amazon\.(nl|com|de)', inhoud, re.I)
os.makedirs(os.path.dirname(UIT), exist_ok=True)
json.dump({'slug': fm['slug'], 'title': titel, 'status': 'draft', 'content': inhoud, 'kaarten': KAARTEN,
           'meta': {'_yoast_wpseo_metadesc': META, '_yoast_wpseo_bctitle': KRUIMEL}},
          open(UIT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({'geschreven': UIT, 'kaarten': KAARTEN, 'bronregels': telling, 'faq': len(vragen), 'tekens': len(inhoud)}, ensure_ascii=False))
