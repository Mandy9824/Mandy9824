#!/usr/bin/env python3
"""NIET OPNIEUW GEBRUIKEN NA RONDE 87 zonder overleg: /husqvarna-robotmaaier/ (#20) is in ronde 87 met de hand vervangen
en mag niet opnieuw uit de md gebouwd worden (zie BOUWLOGBOEK, ronde 87). Latere wijzigingen alleen via de API, met
gerichte vervangingen en een kopie vooraf.

Ronde 87: nieuwe inhoud voor de gepubliceerde pagina /husqvarna-robotmaaier/ (#20) uit pagina-husqvarna-robotmaaier-v2.md
(afgeleid van ronde82_bouw.py en ronde68_bouw.py).

Gebruik:  python3 scripts/ronde87_bouw.py pagina-husqvarna-robotmaaier-v2.md robotmaaierkompas_modeldata_v1.xlsx modellen.json live20.html
Schrijft scripts/ronde87/husqvarna.json (titel, slug, inhoud, meta). Schrijft niets naar de site.
modellen.json: de live modelgegevens (na de upload van ronde 87). live20.html: de huidige ruwe inhoud van #20.

- Opmaak zoals de bestaande merkpagina (patroon pagina-merk, bovenschrift "Merk", kruimelpad "Husqvarna robotmaaier").
- Productkaarten M069, M070, M010, M068, M066, M067, M022, M020, M021 in die volgorde (kop "modellen:" in de md); het
  thema vult specificatiekaart, Beste voor, analyse, plus- en minpunten en het prijsblok (hier alleen "Bekijk de actuele
  prijs" naar de fabrikantpagina: Husqvarna staat niet bij Bol, Coolblue of Amazon) uit de modelgegevens.
- In beide tabellen linken de modelnamen (exacte celtekst) naar hun kaart.
- Bronnen per model uit het blad Bronnen (regels als ronde 82): handleidingen, fabrikantpagina's, appwinkels; geen
  winkels, winkelclaims, "niet gevonden", "niet geopend" of Bol.
- Behouden van de live pagina: "Meer lezen" (met de links die de linkscripts zetten), aangevuld met "Robotmaaier zonder
  grensdraad" (staat in de lijst interne links van de md), en het uitgeschreven auteursblok.
- Metabeschrijving: de metabeschrijving uit de md; Yoast-kruimeltitel "Husqvarna robotmaaier" (zoals live).
"""
import datetime as dt, html, json, os, re, sys
from urllib.parse import urlparse

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excel_naar_json import app_store  # itunes-adressen -> leesbare App Store-pagina (ronde 29)

MD, XLSX, MODELLEN, LIVE = sys.argv[1:5]
live = open(LIVE, encoding='utf-8').read()
UIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde87', 'husqvarna.json')
MAANDEN = 'januari februari maart april mei juni juli augustus september oktober november december'.split()
BASIS = set()
# Modelnaam in de tabellen van de md (exacte celtekst) -> model-ID
KORT = {'430V NERA': 'M069', '450V NERA': 'M070', '410VE NERA (loopt uit)': 'M010', 'Aspire R6V': 'M068', '308V': 'M066',
        '312V': 'M067', '310E NERA': 'M022', '305E NERA': 'M020', '305 (met draad)': 'M021', 'Automower 305': 'M021'}
TABEL_MODELLEN = []
# Tekst in de md -> interne link (alleen deze plekken)
LINKS = [
    ('Hoe we scoren: zie Hoe we beoordelen.', 'Hoe we scoren: zie <a href="/hoe-we-beoordelen/#scoremodel">Hoe we beoordelen</a>.'),
    ('Zie robotmaaier mesjes.', 'Zie <a href="/robotmaaier-mesjes/">robotmaaier mesjes</a>.'),
    ('lees je op robotmaaier kosten.', 'lees je op <a href="/robotmaaier-kosten/">robotmaaier kosten</a>.'),
    ('lees je bij Automower messen op robotmaaier mesjes.',
     'lees je bij <a href="/robotmaaier-mesjes/#automower-messen-endurance-of-classic">Automower messen</a> op robotmaaier mesjes.'),
    ('Mail contact@robotmaaierkompas.nl.', 'Mail <a href="mailto:contact@robotmaaierkompas.nl">contact@robotmaaierkompas.nl</a>.'),
]
# "Meer lezen" van de live pagina (met de links van de linkscripts), plus de regel "zonder grensdraad" (als op #16)
ml = re.search(r'<h2 id="meer-lezen">Meer lezen</h2>\n<ul>.*?</ul>', live, re.S)
assert ml and live.count('id="meer-lezen"') == 1, 'Meer lezen niet precies één keer gevonden'
ZD = '<li><a href="/robotmaaier-zonder-draad/">Robotmaaier zonder draad</a>: tien modellen vergeleken.</li>'
ZG = '<li><a href="/robotmaaier-zonder-grensdraad/">Robotmaaier zonder grensdraad</a>: hoe het werkt en wanneer je het kiest.</li>'
assert ml.group(0).count(ZD) == 1 and '/robotmaaier-zonder-grensdraad/' not in ml.group(0)
MEER_LEZEN = ml.group(0).replace(ZD, ZD + ZG)

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


GELINKT = set()


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
    mid = KORT.get(cel)
    GELINKT.add(cel) if mid else None
    return f'<a href="#{anker(mid)}">{esc(cel)}</a>' if mid else inline(cel)


def tabel(regels):
    rijen = [[c.strip() for c in r.strip().strip('|').split('|')] for r in regels if not re.match(r'^\|\s*-', r)]
    kop, rest = rijen[0], rijen[1:]
    h = '<div class="rmk-tablewrap"><table class="rmk-table"><thead><tr>' + ''.join(f'<th scope="col">{esc(c)}</th>' for c in kop) + '</tr></thead><tbody>'
    for r in rest:
        cellen = [modellink(c) if (i == 0 and kop[0] == 'Model') or (i == 1 and kop[1] == 'Kijk naar') else inline(c) for i, c in enumerate(r)]
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
             'garden.roborock.com', 'garden-support.roborock.com', 'gardena.com', 'ecovacs.com', 'dreametech.com')
PDF_HOSTS = ('cdn.shopify.com', 'storage.onpage.it', 'ssc.stihl.com', S3, 'site-static.ecovacs.com')  # handleidingen (pdf) van de fabrikanten zelf


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
  <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li aria-current="page">Husqvarna robotmaaier</li></ol></nav>
  <header class="rmk-pagehead">
    <p class="rmk-eyebrow">Merk</p>
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
delen.append(groep('<ol class="rmk-sources">\n  <li><div><a href="/hoe-we-beoordelen/#scoremodel">Scoremodel v1.0</a><div class="rmk-sources__meta"><span class="rmk-chip rmk-chip--brand">Eigen methode</span></div></div></li>\n</ol>'))
# auteursblok: het uitgeschreven blok van de live pagina, tot en met het einde
k = live.rindex('<div class="wp-block-group rmk-container rmk-block rmk-column"><!-- wp:html {"metadata":{"categories":["robotmaaierkompas"],"patternName":"robotmaaierkompas/auteursblok"')
AUTEUR = live[k + len('<div class="wp-block-group rmk-container rmk-block rmk-column">'):live.rindex('</main>')]
assert 'rmk-author' in AUTEUR and live.count('robotmaaierkompas/auteursblok') == 1
delen.append('<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n'
             '<div class="wp-block-group rmk-container rmk-block rmk-column">' + AUTEUR + '</main>\n<!-- /wp:group -->')

inhoud = '\n\n'.join(x for x in delen if x)
os.makedirs(os.path.dirname(UIT), exist_ok=True)
json.dump({'slug': fm['slug'], 'title': titel, 'status': 'draft', 'content': inhoud,
           'meta': {'_yoast_wpseo_metadesc': META, '_yoast_wpseo_bctitle': 'Husqvarna robotmaaier'}},
          open(UIT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
assert GELINKT == set(KORT), f'niet gelinkt: {set(KORT) - GELINKT}'
print(json.dumps({'geschreven': UIT, 'kaarten': volgorde, 'bronregels': telling, 'faq': len(vragen), 'tekens': len(inhoud)}, ensure_ascii=False))
