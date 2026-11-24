#!/usr/bin/env python3
"""Ronde 109: conceptpagina robotmaaier-gps uit pagina-robotmaaier-gps.md bouwen (afgeleid van ronde106_bouw.py).

Gebruik:  python3 scripts/ronde109_bouw.py pagina-robotmaaier-gps.md modellen.json [robotmaaierkompas_modeldata_v1.xlsx]
                 [--extra=pagina470.json,pagina20.json]
Schrijft scripts/ronde109/gps.json (titel, slug, inhoud, meta, kaarten). Schrijft niets naar de site.
modellen.json: de live modelgegevens (rmk/v1/modellen), voor slug, naam, scores en (zonder Excel) de bronnen.

- Opmaak als de RTK-pagina (/robotmaaier-rtk-lidar-camera/): patroon pagina-merk met het bovenschrift "Uitleg";
  kruimelpad en Yoast-kruimeltitel "Robotmaaier met GPS".
- Productkaarten M015, M069, M059, M071, M047, M056 in die volgorde (instructie, kop "modellen:" en hoofdtekst van de
  md moeten gelijk zijn; anders stopt het script). De ### kop wordt de titel van de kaart. Het thema vult
  specificatiekaart, teksten en het prijsblok (Bol, Coolblue, Amazon volgens prijstaken en schakelaars, anders
  "Bekijk de actuele prijs"). Geen winkellinks, winkelnamen of prijzen van winkels in de inhoud.
- Tekst letterlijk uit de md; afwijkingen tegen de modelgegevens worden gemeld (BOUWLOGBOEK), niet aangepast.
- Bronnen per model: met het Excel-bestand uit het blad Bronnen (velden navigatie, GPS-tracking, verbinding/4G,
  modules en extra kosten, oppervlak, geluid, kernvelden); zonder Excel uit de live modelgegevens (dezelfde soort
  velden). Filterregels als ronde 97/102/106: alleen fabrikant, handleiding, appwinkel; geen winkels, winkelclaims,
  "niet gevonden", "niet geopend", "tegenstrijdig" of Bol.
  Zonder Excel kunnen met --extra bronregels worden overgenomen uit de bronnenlijst van gepubliceerde pagina's die
  uit het blad Bronnen zijn gebouwd (ronde 109: RTK-pagina #470 en Husqvarna-pagina #20, opgeslagen als JSON van
  wp/v2/pages/<id>?context=edit): per modelkop alleen regels waarvan de tekst bij VELDPAT past en waarvan het adres
  nog niet in de lijst staat (zo komen de Connect Kit-pagina's van Husqvarna mee, die niet in de live gegevens staan).
- "Meer lezen": de pagina's uit de lijst interne links van de md die niet al in de tekst gelinkt zijn.
- Metabeschrijving uit de md.
"""
import datetime as dt, html, json, os, re, sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
MD, MODELLEN = ARGS[:2]
XLSX = ARGS[2] if len(ARGS) > 2 else None
EXTRA = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--extra=')), [])
UIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde109', 'gps.json')
MAANDEN = 'januari februari maart april mei juni juli augustus september oktober november december'.split()
KRUIMEL = 'Robotmaaier met GPS'
KAARTEN = ['M015', 'M069', 'M059', 'M071', 'M047', 'M056']
# Verder in de tabellen en tekst bij typenaam genoemd (bronnen, geen kaart)
TABEL_MODELLEN = ['M016', 'M002', 'M070', 'M010', 'M072', 'M060', 'M006', 'M007', 'M066', 'M067', 'M068', 'M046',
                  'M057', 'M004', 'M005', 'M008', 'M058', 'M053', 'M052', 'M020', 'M022', 'M011', 'M055', 'M027']
VELDPAT = (r'^navigatie|gps|tracking|verbinding|abonnement|\b4g\b|module|connect kit|find my|antidiefstal|'
           r'referentiestation|gateway|tuingrootte|geluid|kernvelden|network rtk')  # geen messen, garage of draad
A = lambda u, t: f'<a href="{u}">{t}</a>'
RTK, DIEF = '/robotmaaier-rtk-lidar-camera/', '/robotmaaier-diefstal-verzekering/'
LINKS = [  # (tekst in de md, met link) — elke tekst precies 1x
    ('Zie RTK, LiDAR of camera.', f'Zie {A(RTK, "RTK, LiDAR of camera")}.'),
    ('Zie diefstal en verzekering.', f'Zie {A(DIEF, "diefstal en verzekering")}.'),
    ('Zie RTK, LiDAR of camera voor het verschil', f'Zie {A(RTK, "RTK, LiDAR of camera")} voor het verschil'),
    ('staat op onze pagina over diefstal en verzekering.', f'staat op onze {A(DIEF, "pagina over diefstal en verzekering")}.'),
    ('hangt van de polis af; zie diefstal en verzekering.', f'hangt van de polis af; zie {A(DIEF, "diefstal en verzekering")}.'),
    ('zie de diefstalpagina.', f'zie {A(DIEF, "de diefstalpagina")}.'),
    ('Mail contact@robotmaaierkompas.nl.', 'Mail <a href="mailto:contact@robotmaaierkompas.nl">contact@robotmaaierkompas.nl</a>.'),
]
MEER_LEZEN = ('<h2 id="meer-lezen">Meer lezen</h2>\n<ul>'
              '<li><a href="/beste-robotmaaier/">Beste robotmaaier</a>: onze selectie per situatie.</li>'
              '<li><a href="/robotmaaier-zonder-draad/">Robotmaaier zonder draad</a>: tien modellen vergeleken.</li>'
              '<li><a href="/robotmaaier-zonder-grensdraad/">Robotmaaier zonder grensdraad</a>: hoe het werkt en wanneer je het kiest.</li>'
              '<li><a href="/robotmaaier-kleine-tuin/">Robotmaaier voor een kleine tuin</a>: tot 600 m².</li>'
              '<li><a href="/robotmaaier-grote-tuin/">Robotmaaier voor een grote tuin</a>: 1.000 tot 3.000 m².</li>'
              '<li><a href="/robotmaaier-helling/">Robotmaaier voor hellingen</a>: welke kan hoe steil?</li>'
              '<li><a href="/robotmaaier-kopen-waar-op-letten/">Robotmaaier kopen: waar let je op?</a></li>'
              '<li>Per merk: <a href="/segway-navimow-robotmaaier/">Segway Navimow</a>, <a href="/husqvarna-robotmaaier/">Husqvarna</a>, '
              '<a href="/gardena-robotmaaier/">Gardena</a>, <a href="/stihl-robotmaaier/">Stihl</a>, <a href="/worx-robotmaaier/">Worx</a>, '
              '<a href="/mova-dreame-robotmaaier/">Mova en Dreame</a> en <a href="/eufy-robotmaaier/">Eufy</a>.</li></ul>')

_m = json.load(open(MODELLEN, encoding='utf-8'))
modellen = {m['id']: m for m in _m.get('data', _m)['modellen']}  # antwoord van rmk/v1/modellen of alleen 'data'
md = open(MD, encoding='utf-8').read()
fm, body = re.match(r'^---\n(.*?)\n---\n(.*)$', md, re.S).groups()
fm = dict(re.findall(r'^(\w+): ?(.*)$', fm, re.M))
assert [x.strip() for x in fm['modellen'].split(',')] == KAARTEN, 'kop modellen: wijkt af van de instructie'
assert fm['status'] == 'concept' and fm['slug'] == 'robotmaaier-gps'
META = fm['metabeschrijving']
instructie = re.search(r'^INSTRUCTIE VOOR DE BOUWER.*$', body, re.M).group(0)
assert ', '.join(KAARTEN[:-1]) + ' en ' + KAARTEN[-1] in instructie, 'kaartvolgorde in de instructie wijkt af'
body = body.replace(instructie + '\n', '')
for a, _ in LINKS:
    assert body.count(a) == 1, f'linkplek {body.count(a)}x in de md: {a}'
d = dt.date.fromisoformat(fm['bijgewerkt'])
datum_nl = f'{d.day} {MAANDEN[d.month - 1]} {d.year}'
GELINKT = set()

assert re.findall(r'\{\{productbox model=(M\d+)\}\}', body) == KAARTEN, 'kaartvolgorde in de tekst wijkt af'


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
        assert len(r) == len(kop), r
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


# ---------------------------------------------------------------- bronnen (indeling als ronde 97/106)
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
    if host == 'garden-support.roborock.com' and (pad.endswith('.pdf') or 'manual' in pad):
        return 'Handleiding', None
    if host.endswith(FABRIKANT):
        return 'Fabrikant', None
    if host in ('apps.apple.com', 'itunes.apple.com', 'play.google.com'):
        return 'Appwinkel', None
    return None


def live_rijen(mid):
    """Rijen (model, veld, -, bron, datum, status) uit de live modelgegevens, zoals het blad Bronnen."""
    m = modellen[mid]
    velden = [('navigatie', 'Navigatie'), ('begrenzingsdraad', 'Begrenzingsdraad'), ('gps_tracking', 'GPS-tracking'),
              ('max_tuingrootte_m2', 'Max. tuingrootte'), ('geluid_dba', 'Geluid')]
    rijen = []
    for k, naam in velden:
        v = m['specs'].get(k)
        if isinstance(v, dict) and v.get('waarde') is not None and v.get('bron'):
            rijen.append((mid, naam, None, v['bron'], v.get('datum'), v.get('status')))
    v = m.get('verbinding')
    if isinstance(v, dict) and v.get('bron'):
        rijen.append((mid, 'Verbinding / 4G', None, v['bron'], v.get('datum'), v.get('status')))
    for k, naam in (('antidiefstal', 'Extra kosten: GPS-module'), ('antenne_gateway', 'Extra kosten: antenne of gateway'),
                    ('verbinding_per_jaar', 'Verbinding per jaar'), ('gratis_periode_jaren', 'Verbinding: gratis periode')):
        v = m['kosten'].get(k)
        if isinstance(v, dict) and v.get('waarde') is not None and v.get('bron'):
            rijen.append((mid, naam, None, v['bron'], v.get('datum'), v.get('status')))
    return rijen


def bronnen(mid, rijen):
    groepen = {}
    for r in rijen:
        veld, bron, datum, status = str(r[1] or '').strip(), app_store(r[3]), r[4], str(r[5] or '').strip().lower()
        if r[0] != mid or not re.search(VELDPAT, veld, re.I):
            continue
        if 'bol' in (bron + veld).lower() or status.startswith(('winkelclaim', 'niet gevonden', 'niet geopend', 'tegenstrijdig')):
            continue
        for u in re.findall(r'https?://[^\s;()]+', bron):
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
        meta = f'<span class="rmk-chip">{g["label"]}</span>'
        if g['datum']:
            dd = dt.date.fromisoformat(g['datum'])
            meta += f'<span>geraadpleegd op {dd.day} {MAANDEN[dd.month - 1]} {dd.year}</span>'
        li.append(f'  <li><div><a href="{html.escape(u)}">{esc(tekst)} ({esc(plek)})</a><div class="rmk-sources__meta">{meta}</div></div></li>')
    return li


def extra_li(mid, al):
    """Bronregels (<li>) van gepubliceerde pagina's voor dit model; alleen nieuwe adressen."""
    naam = modellen[mid]['naam']
    uit = []
    for pad in EXTRA:
        c = json.load(open(pad, encoding='utf-8'))['content']['raw']
        c = c[c.index('>Bronnen</h2>'):]
        delen = re.split(r'<h3 style="font-size: var\(--rmk-fs-lg\); margin-top: 16px">(.*?)</h3>', c)
        for k in range(1, len(delen), 2):
            if html.unescape(delen[k]) != naam:
                continue
            for li in re.findall(r'  <li>.*?</li>', delen[k + 1]):
                u, t = re.search(r'<a href="([^"]+)">([^<]*)</a>', li).groups()
                u = html.unescape(u)
                if u in al or not re.search(VELDPAT, re.sub(r'\([^)]*\)$', '', html.unescape(t)), re.I):
                    continue
                if 'bol' in (u + t).lower():
                    continue
                al.add(u)
                uit.append(li)
    return uit


if XLSX:
    import openpyxl
    from excel_naar_json import app_store  # itunes-adressen -> leesbare App Store-pagina (ronde 29)
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    bronrijen = [r for r in wb['Bronnen'].iter_rows(min_row=2, values_only=True) if r[0]]
    BRONSOORT = 'Excel, blad Bronnen'
else:
    app_store = lambda t: str(t or '')
    bronrijen = [r for mid in KAARTEN + TABEL_MODELLEN for r in live_rijen(mid)]
    BRONSOORT = 'live modelgegevens'


# ---------------------------------------------------------------- pagina
titel = fm['titel']
delen = [f'''<!-- wp:group {{"tagName":"main","className":"rmk","layout":{{"type":"default"}},"anchor":"inhoud"}} -->
<main id="inhoud" class="wp-block-group rmk"><!-- wp:html -->
<div class="rmk-container rmk-column">
  <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li aria-current="page">{esc(KRUIMEL)}</li></ol></nav>
  <header class="rmk-pagehead">
    <p class="rmk-eyebrow">Uitleg</p>
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
    if EXTRA and not XLSX:
        al = {html.unescape(x) for x in re.findall(r'<a href="([^"]+)"', '\n'.join(li))}
        li += extra_li(mid, al)
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
assert not re.search(r'\{\{|INSTRUCTIE|bol\.com|coolblue|amazon\.(nl|com|de)', inhoud, re.I)
assert not re.search(r'\b(Bol|Coolblue|Amazon|MediaMarkt|Hornbach|Gamma|Praxis)\b', re.sub(r'<[^>]+>', ' ', inhoud)), 'winkelnaam in de tekst'
os.makedirs(os.path.dirname(UIT), exist_ok=True)
json.dump({'slug': fm['slug'], 'title': titel, 'status': 'draft', 'content': inhoud, 'kaarten': KAARTEN,
           'meta': {'_yoast_wpseo_metadesc': META, '_yoast_wpseo_bctitle': KRUIMEL}},
          open(UIT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({'geschreven': UIT, 'bronnen_uit': BRONSOORT, 'kaarten': KAARTEN, 'bronregels': telling, 'faq': len(vragen),
                  'tekens': len(inhoud)}, ensure_ascii=False))
