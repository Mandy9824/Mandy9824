#!/usr/bin/env python3
"""Ronde 71: conceptpagina robotmaaier-kleine-tuin uit pagina-robotmaaier-kleine-tuin.md bouwen (afgeleid van ronde67_bouw.py).

Gebruik:  python3 scripts/ronde71_bouw.py pagina-robotmaaier-kleine-tuin.md robotmaaierkompas_modeldata_v1.xlsx modellen.json
Schrijft scripts/ronde71/kleine-tuin.json (titel, slug, inhoud, meta). Schrijft niets naar de site.
modellen.json: de live modelgegevens (na de upload van ronde 71), voor slug, naam en scores van de kaarten.

- Opmaak zoals de merkpagina's (patroon pagina-merk, ronde 63/67), met bovenschrift "Kopersgids". Het patroon
  pagina-kopersgids (smalle kolom met vaste inhoudsopgave) past niet bij een tabel met zeven kolommen en productkaarten.
- Productkaarten voor M016, M002, M056, M064, M046, M063 en M053, in die volgorde (kop "modellen:" in de md); het thema
  vult specificatiekaart, Beste voor, analyse, plus- en minpunten en het prijsblok (Bol, Coolblue, Amazon volgens de
  prijstaken en schakelaars, of "Bekijk de actuele prijs") uit de modelgegevens. In de inhoud staan geen winkellinks of prijzen.
- M052, M027, M021, M026 en M050 staan alleen in de tabel (geen kaart); in de eerste tabel linken de zeven modelnamen
  met een kaart naar hun kaart.
- Bronnen per model (alle twaalf) uit het blad Bronnen: alleen handleidingen, fabrikantpagina's en appwinkels; geen
  winkels, winkelclaims, "niet gevonden", "niet geopend" of Bol. Indeling per domein zoals in ronde 28, 43, 52, 60, 63 en 67.
- Metabeschrijving: de metabeschrijving uit de md. Kruimelpad "Robotmaaier kleine tuin".
- "Meer lezen": beste, zonder draad, zonder grensdraad, kosten. De links naar de merkpagina's zet scripts/ronde71_links.py
  na publicatie (opdracht Mandy).
"""
import datetime as dt, html, json, os, re, sys
from urllib.parse import urlparse

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excel_naar_json import app_store  # itunes-adressen -> leesbare App Store-pagina (ronde 29)

MD, XLSX, MODELLEN = sys.argv[1:4]
UIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde71', 'kleine-tuin.json')
MAANDEN = 'januari februari maart april mei juni juli augustus september oktober november december'.split()
BASIS = set()
# Modelnaam in de tabellen van de md -> model-ID
KORT = {'Navimow i205 AWD': 'M016', 'Navimow i206 AWD': 'M002', 'Roborock RockNeo Q105': 'M056', 'Mova ViAX 500': 'M064',
        'Worx Landroid WR303E': 'M046', 'Mova ViAX 250': 'M063', 'Eufy C15 Solo': 'M053'}  # alleen modellen met een kaart
TABEL_MODELLEN = ['M052', 'M027', 'M021', 'M026', 'M050']  # alleen in de tabel, wel bronnen
# Tekst in de md -> interne link (één keer per zin, alleen deze plekken)
LINKS = [
    ('Hoe we scoren: zie Hoe we beoordelen.', 'Hoe we scoren: zie <a href="/hoe-we-beoordelen/#scoremodel">Hoe we beoordelen</a>.'),
    ('Zie robotmaaier mesjes.', 'Zie <a href="/robotmaaier-mesjes/">robotmaaier mesjes</a>.'),
    ('lees je op robotmaaier kosten.', 'lees je op <a href="/robotmaaier-kosten/">robotmaaier kosten</a>.'),
    ('kijk dan naar robotmaaier zonder draad.', 'kijk dan naar <a href="/robotmaaier-zonder-draad/">robotmaaier zonder draad</a>.'),
    ('kijk dan op robotmaaier zonder draad.', 'kijk dan op <a href="/robotmaaier-zonder-draad/">robotmaaier zonder draad</a>.'),
    ('lees je op robotmaaier zonder grensdraad.', 'lees je op <a href="/robotmaaier-zonder-grensdraad/">robotmaaier zonder grensdraad</a>.'),
    ('Mail contact@robotmaaierkompas.nl.', 'Mail <a href="mailto:contact@robotmaaierkompas.nl">contact@robotmaaierkompas.nl</a>.'),
]
MEER_LEZEN = ('<h2 id="meer-lezen">Meer lezen</h2>\n<ul>'
              '<li><a href="/beste-robotmaaier/">Beste robotmaaier</a>: onze selectie per situatie.</li>'
              '<li><a href="/robotmaaier-zonder-draad/">Robotmaaier zonder draad</a>: tien modellen vergeleken.</li>'
              '<li><a href="/robotmaaier-zonder-grensdraad/">Robotmaaier zonder grensdraad</a>: hoe het werkt en wanneer je het kiest.</li>'
              '<li><a href="/robotmaaier-kosten/">Robotmaaier kosten</a>: wat het echt kost, met verborgen kosten.</li></ul>')

modellen = {m['id']: m for m in json.load(open(MODELLEN, encoding='utf-8'))['modellen']}
md = open(MD, encoding='utf-8').read()
fm, body = re.match(r'^---\n(.*?)\n---\n(.*)$', md, re.S).groups()
fm = dict(re.findall(r'^(\w+): (.*)$', fm, re.M))
META = fm['metabeschrijving']
body = re.sub(r'^INSTRUCTIE VOOR DE BOUWER.*?\n', '', body, flags=re.M)
# Kaarten in de volgorde van "modellen:" in de kop, zoals de instructie vraagt
assert re.findall(r'\{\{productbox model=(M\d+)\}\}', body) == [x.strip() for x in fm['modellen'].split(',')], 'volgorde kaarten'
d = dt.date.fromisoformat(fm['bijgewerkt'])
datum_nl = f'{d.day} {MAANDEN[d.month - 1]} {d.year}'


def esc(t):
    return html.escape(t, quote=False)


def inline(t):
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    for a, b in LINKS:
        t = t.replace(esc(a), b)
    return t


def slugid(t):
    t = re.sub(r'[^a-z0-9]+', '-', t.lower().replace('é', 'e')).strip('-')
    return t


def anker(mid):
    return 'p-' + modellen[mid]['slug']


def modellink(cel):
    for kort, mid in sorted(KORT.items(), key=lambda kv: -len(kv[0])):
        if cel.startswith(kort):
            return f'<a href="#{anker(mid)}">{esc(kort)}</a>' + esc(cel[len(kort):])
    return inline(cel)


def tabel(regels):
    rijen = [[c.strip() for c in r.strip().strip('|').split('|')] for r in regels if not re.match(r'^\|\s*-', r)]
    kop, rest = rijen[0], rijen[1:]
    h = '<div class="rmk-tablewrap"><table class="rmk-table"><thead><tr>' + ''.join(f'<th scope="col">{esc(c)}</th>' for c in kop) + '</tr></thead><tbody>'
    for r in rest:
        cellen = [modellink(c) if i == 0 and kop[0] == 'Model' else inline(c) for i, c in enumerate(r)]
        h += '<tr><th scope="row">' + cellen[0] + '</th>' + ''.join(f'<td>{c}</td>' for c in cellen[1:]) + '</tr>'
    return h + '</tbody></table></div>'


def proza(tekst):
    """Markdown-fragment (alinea's, ##/###, tabellen, lijsten) -> HTML."""
    uit, blok = [], []
    for deel in re.split(r'\n\s*\n', tekst.strip()):
        regels = deel.strip().split('\n')
        if not deel.strip():
            continue
        if regels[0].startswith('## '):
            t = regels[0][3:].strip()
            uit.append(f'<h2 id="{slugid(t)}">{esc(t)}</h2>')
        elif regels[0].startswith('### '):
            uit.append(f'<h3>{esc(regels[0][4:].strip())}</h3>')
        elif regels[0].startswith('|'):
            uit.append(tabel(regels))
        elif regels[0].startswith('- '):
            uit.append('<ul>' + ''.join(f'<li>{inline(r[2:].strip())}</li>' for r in regels) + '</ul>')
        else:
            uit.append('<p>' + inline(' '.join(r.strip() for r in regels)) + '</p>')
    return '\n'.join(uit)


def sectie(inner):
    return f'<!-- wp:html -->\n<section class="rmk-container rmk-section--tight rmk-column"><div class="rmk-prose">\n{inner}\n</div></section>\n<!-- /wp:html -->'


def groep(inner, extra=''):
    return ('<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}' + extra + '} -->\n'
            '<div class="wp-block-group rmk-container rmk-block rmk-column"><!-- wp:html -->\n' + inner + '\n<!-- /wp:html --></div>\n<!-- /wp:group -->')


def kaart(mid, titel):
    m = modellen[mid]
    a = anker(mid)
    if mid in BASIS:
        cel = (f'<div class="rmk-scorecell" data-model="{mid}"><div class="rmk-minis rmk-minis--none"><b aria-hidden="true">–</b>'
               '<small>Niet beoordeeld</small></div></div>')
    else:
        s = m['scores']
        f = lambda v: '' if v is None else str(v)
        ds = '; '.join(f'{k}={f(s.get(k))}' for k in ('betrouwbaarheid', 'navigatie', 'prijskwaliteit', 'hellingen', 'app', 'veiligheid', 'geluid')) + '; reviews='
        cel = (f'<div class="rmk-scorecell" data-rmk-score data-scores="{ds}" data-model="{mid}"><div class="rmk-minis"><b data-out="total">–</b>'
               '<small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div>')
    return groep(f'''<article class="rmk-product" aria-labelledby="{a}">
  <div class="rmk-product__head rmk-product__head--nomedia" style="grid-template-columns: 1fr">
    <div class="rmk-product__title">
      <h3 id="{a}">{esc(titel)}</h3>
      {cel}
    </div>
  </div>
  <div class="rmk-product__aside rmk-offers">
    <div class="rmk-offer"></div>
  </div>
</article>''')


# ---------------------------------------------------------------- bronnen
S3 = 'salesforce-knowledge-download.s3.us-west-2.amazonaws.com'
FABRIKANT = ('navimow.com', 'husqvarna.com', 'stihl.nl', 'support.stihl.com', 'eu.worx.com', 'mova.tech', 'eufy.com',
             'garden.roborock.com', 'garden-support.roborock.com')
PDF_HOSTS = ('cdn.shopify.com', 'storage.onpage.it', 'ssc.stihl.com', S3)  # handleidingen (pdf) van de fabrikanten zelf


def soort(u):
    """(label, korte plek of None) voor een adres, of None (winkels, API-adressen en alles daarbuiten)."""
    p = urlparse(u)
    host = p.netloc.lower().removeprefix('www.')
    pad = p.path.lower()
    if host.endswith('adobeioruntime.net'):
        return None  # API-adres van Stihl (ronde 52)
    if 'mansier' in host:
        return 'Handleiding (kopie op mansier.com)', None
    if host.endswith('manualslib.com'):
        return 'Handleiding (kopie op manualslib.com)', None
    if host == S3:
        # 000038406 is de EU-conformiteitsverklaring van de C15, zonder geluidswaarde (ronde 67)
        return None if '000038406' in pad else ('Handleiding', 'handleiding (pdf)')
    if host in PDF_HOSTS and pad.endswith('.pdf'):
        return 'Handleiding', None
    if 'zendesk' in host or '/tdrdownload/' in pad:
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


def bronnen(mid, rijen):
    groepen = {}
    for r in rijen:
        veld, bron, datum, status = str(r[1] or '').strip(), app_store(r[3]), r[4], str(r[5] or '').strip().lower()
        if 'bol' in (bron + veld).lower() or status.startswith(('winkelclaim', 'niet gevonden', 'niet geopend')):
            continue
        urls = re.findall(r'https?://[^\s;()]+', bron)
        for u in urls:
            s = soort(u)
            if not s:
                continue  # winkels (Coolblue, Amazon, Hornbach, x-kom, ...), API-adressen en Bol
            host = urlparse(u).netloc.lower().removeprefix('www.')
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
        # Twee adressen op hetzelfde domein in één regel: korte aanduiding in plaats van het lange pad (past op 360 px)
        kort = 'handleiding' if '/tdrdownload/' in p.path else 'pdf-bijlage' if 'attachments' in p.path else 'supportartikel' if '/articles/' in p.path else p.path.rstrip('/').split('/')[-1][:40]
        plek = g['plek'] or (g['host'] + (', ' + kort if g['pad'] else ''))
        dd = dt.date.fromisoformat(g['datum'])
        li.append(f'  <li><div><a href="{html.escape(u)}">{esc(tekst)} ({esc(plek)})</a><div class="rmk-sources__meta">'
                  f'<span class="rmk-chip">{g["label"]}</span><span>geraadpleegd op {dd.day} {MAANDEN[dd.month - 1]} {dd.year}</span></div></div></li>')
    return li


wb = openpyxl.load_workbook(XLSX, data_only=True)
bronrijen = [r for r in wb['Bronnen'].iter_rows(min_row=2, values_only=True) if r[0]]

# ---------------------------------------------------------------- pagina
titel = fm['titel']
delen = []
delen.append(f'''<!-- wp:group {{"tagName":"main","className":"rmk","layout":{{"type":"default"}},"anchor":"inhoud"}} -->
<main id="inhoud" class="wp-block-group rmk"><!-- wp:html -->
<div class="rmk-container rmk-column">
  <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li aria-current="page">Robotmaaier kleine tuin</li></ol></nav>
  <header class="rmk-pagehead">
    <p class="rmk-eyebrow">Kopersgids</p>
    <h1>{esc(titel)}</h1>
    <p class="rmk-meta">Door <a href="/over-ons/mandy-van-den-broek/">{esc(fm['auteur'])}</a> · bijgewerkt op {datum_nl}</p>
  </header>
</div>
<!-- /wp:html -->''')
delen.append(groep(f'''<aside class="rmk-honesty" aria-label="Hoe deze pagina tot stand kwam">
  <span class="rmk-honesty__icon"><svg class="rmk-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M16.2 7.8 13.3 13.3 10.7 10.7Z"/><path d="M7.8 16.2 10.7 10.7 13.3 13.3Z"/></svg></span>
  <div class="rmk-honesty__text">
    <p><strong>Vergeleken op basis van handleidingen, fabrikantpagina's en winkelinformatie. Bijgewerkt op {datum_nl}.</strong> Zo vergelijken we: zie <a href="/hoe-we-beoordelen/">Hoe we beoordelen</a>.</p>
    <div class="rmk-honesty__links"><a href="/hoe-we-beoordelen/#scoremodel">Zo werkt ons scoremodel</a><a href="/hoe-we-beoordelen/#verdienmodel">Zo verdienen we geld</a></div>
  </div>
</aside>'''))

body = re.sub(r'^# .*\n', '', body, flags=re.M).replace('{{eerlijkheidsblok}}', '')
voor_faq, na_faq = body.split('{{faq}}')
na_faq, _ = na_faq.split('{{bronnenlijst}}')
# Tekst en kaarten tot de FAQ
stukken = re.split(r'\{\{productbox model=(M\d+)\}\}', voor_faq)
tekst = stukken[0]
for i in range(1, len(stukken), 2):
    mid, na = stukken[i], stukken[i + 1]
    # de ### vlak voor de kaart wordt de titel van de kaart (geen dubbele kop)
    tekst, kop = re.match(r'^(.*)\n### (.+?)\s*$', tekst.rstrip(), re.S).groups()
    delen.append(sectie(proza(tekst)) if tekst.strip() else '')
    delen.append(kaart(mid, kop))
    tekst = na
# Wat na de laatste kaart staat (zonder ###), plus Meer lezen
delen.append(sectie(proza(tekst) + '\n' + MEER_LEZEN))
# FAQ
faq, rest = re.split(r'\n## ', na_faq.strip(), maxsplit=1)
vragen = re.findall(r'\*\*(.+?)\*\*\s*(.+?)(?=\n\s*\n\*\*|\Z)', faq.strip(), re.S)
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h2 style="font-size: var(--rmk-fs-xl)">Veelgestelde vragen</h2></div>\n<!-- /wp:html -->')
delen.append(groep('<div class="rmk-faq">\n' + '\n'.join(f'  <details><summary>{esc(v)}</summary><div><p>{inline(" ".join(a.split()))}</p></div></details>' for v, a in vragen) + '\n</div>'))
delen.append(sectie(proza('## ' + rest)))
# Bronnen
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column" style="padding-top: 24px"><h2 style="font-size: var(--rmk-fs-xl)">Bronnen</h2><p class="rmk-small">Per model, uit handleidingen, fabrikantpagina\'s en appwinkels.</p></div>\n<!-- /wp:html -->')
volgorde = [m for m in re.findall(r'\{\{productbox model=(M\d+)\}\}', voor_faq)]
kaarttitel = dict((mid, kop) for kop, mid in re.findall(r'### (.+?)\s*\n\s*\{\{productbox model=(M\d+)\}\}', voor_faq))
telling = {}
for mid in volgorde + TABEL_MODELLEN:
    li = bronnen(mid, [r for r in bronrijen if r[0] == mid])
    telling[mid] = len(li)
    delen.append(f'<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">{esc(kaarttitel.get(mid) or modellen[mid]["naam"])}</h3></div>\n<!-- /wp:html -->')
    delen.append(groep('<ol class="rmk-sources">\n' + '\n'.join(li) + '\n</ol>'))
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">Scoremodel</h3></div>\n<!-- /wp:html -->')
delen.append(groep('<ol class="rmk-sources">\n  <li><div><a href="/hoe-we-beoordelen/#scoremodel">Scoremodel v1.0 (concept tot bevriezing)</a><div class="rmk-sources__meta"><span class="rmk-chip rmk-chip--brand">Eigen methode</span></div></div></li>\n</ol>'))
delen.append('<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n'
             '<div class="wp-block-group rmk-container rmk-block rmk-column">\n<!-- wp:pattern {"slug":"robotmaaierkompas/auteursblok"} /-->\n</div>\n<!-- /wp:group -->\n'
             '</main>\n<!-- /wp:group -->')

inhoud = '\n\n'.join(x for x in delen if x)
os.makedirs(os.path.dirname(UIT), exist_ok=True)
json.dump({'slug': fm['slug'], 'title': titel, 'status': 'draft', 'content': inhoud,
           'meta': {'_yoast_wpseo_metadesc': META, '_yoast_wpseo_bctitle': 'Robotmaaier kleine tuin'}},
          open(UIT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({'geschreven': UIT, 'kaarten': volgorde, 'bronregels': telling, 'faq': len(vragen), 'tekens': len(inhoud)}, ensure_ascii=False))
