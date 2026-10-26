#!/usr/bin/env python3
"""Ronde 67: conceptpagina eufy-robotmaaier uit pagina-eufy-robotmaaier.md bouwen (afgeleid van ronde63_bouw.py).

Gebruik:  python3 scripts/ronde67_bouw.py pagina-eufy-robotmaaier.md robotmaaierkompas_modeldata_v1.xlsx modellen.json
Schrijft scripts/ronde67/eufy.json (titel, slug, inhoud, meta). Schrijft niets naar de site.
modellen.json: de live modelgegevens (na de upload van ronde 67), voor slug en naam van de kaarten.

- Opmaak zoals de hub (ronde 16): kop met kruimelpad, eerlijkheidsblok, tekst, productkaarten, FAQ, bronnen, auteursblok.
- Productkaarten in de volgorde van de tekst; het thema vult specificatiekaart, Beste voor, analyse, plus- en minpunten
  en het prijsblok (prijs met winkel of "Bekijk de actuele prijs" naar fabrikant_url) uit de modelgegevens.
- Bronnen per model uit het blad Bronnen: alleen handleidingen, fabrikantpagina's en appwinkels; geen winkels,
  winkelclaims, "niet gevonden", "niet geopend" of Bol. Daarna het scoremodel als eigen methode.
- Ronde 67: www.eufy.com en service.eufy.com tellen als fabrikant; de handleidingen (pdf op
  salesforce-knowledge-download.s3.us-west-2.amazonaws.com en de User Guide-pagina's op service.eufy.com) als
  handleiding; de conformiteitsverklaring (pdf 000038406, zonder geluidswaarde) niet. Kaarten voor M006, M007, M052 en M053, in die volgorde;
  de teksten staan in de modelgegevens (M007, M052, M053 sinds ronde 67). Het thema vult de Bol- en Coolblue-regels
  uit de prijstaken; in de inhoud staan geen winkellinks of prijzen. Geen modellen die alleen in de tabel staan.
- Metabeschrijving: de metabeschrijving uit de md.
- "Meer lezen" met Worx (al gepubliceerd); de links naar Navimow en Mova/Dreame zet scripts/ronde67_links.py na
  publicatie (opdracht Mandy).
"""
import datetime as dt, html, json, os, re, sys
from urllib.parse import urlparse

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excel_naar_json import app_store  # itunes-adressen -> leesbare App Store-pagina (ronde 29)

MD, XLSX, MODELLEN = sys.argv[1:4]
UIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde67', 'eufy.json')
MAANDEN = 'januari februari maart april mei juni juli augustus september oktober november december'.split()
BASIS = set()
# Modelnaam in de tabellen van de md -> model-ID
KORT = {'E15 Solo': 'M006', 'E18': 'M007', 'C15 met garage': 'M052', 'C15 Solo': 'M053'}  # alleen modellen met een kaart
TABEL_MODELLEN = []
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
              '<li><a href="/robotmaaier-test-vergelijking/">Robotmaaiers vergelijken</a>: alle specificaties en scores in één tabel.</li>'
              '<li><a href="/robotmaaier-kosten/">Robotmaaier kosten</a>: wat het echt kost, met verborgen kosten.</li>'
              '<li><a href="/robotmaaier-mesjes/">Robotmaaier mesjes</a>: prijzen en vervangtermijnen.</li>'
              '<li><a href="/worx-robotmaaier/">Worx robotmaaier</a>: de Landroid-modellen vergeleken.</li></ul>')

modellen = {m['id']: m for m in json.load(open(MODELLEN, encoding='utf-8'))['modellen']}
md = open(MD, encoding='utf-8').read()
fm, body = re.match(r'^---\n(.*?)\n---\n(.*)$', md, re.S).groups()
fm = dict(re.findall(r'^(\w+): (.*)$', fm, re.M))
META = fm['metabeschrijving']
body = re.sub(r'^INSTRUCTIE VOOR DE BOUWER.*?\n', '', body, flags=re.M)
# Kaarten in de volgorde van "modellen:" in de kop (M006, M007, M052, M053), zoals de instructie vraagt
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
        cellen = [modellink(c) if i == (0 if kop[0] == 'Model' else 1) else inline(c) for i, c in enumerate(r)]
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


def soort_eufy(u):
    """(label, korte plek) voor een Eufy-adres, of None (winkels en alles daarbuiten)."""
    p = urlparse(u)
    host = p.netloc.lower().removeprefix('www.')
    if host == S3 and p.path.lower().endswith('.pdf'):
        # 000038406 is de EU-conformiteitsverklaring van de C15; die noemt geen geluidswaarde (Opmerking in het blad
        # Modellen), dus geen bron voor het geluid op de pagina
        return None if '000038406' in p.path else ('Handleiding', 'handleiding (pdf)')
    if host == 'service.eufy.com':
        if 'User-Guide' in p.path:
            return 'Handleiding', 'service.eufy.com, handleiding'
        if 'Cellular-Data-FAQ' in p.path:
            return 'Fabrikant', 'service.eufy.com, 4G-data'
        return 'Fabrikant', 'service.eufy.com, ' + ('welkom C15' if 'C15' in p.path else p.path.rstrip('/').split('/')[-1][:30])
    if host == 'eufy.com':
        return 'Fabrikant', 'eufy.com, ' + p.path.rstrip('/').split('/')[-1]
    if host in ('apps.apple.com', 'itunes.apple.com', 'play.google.com'):
        return 'Appwinkel', host
    return None


def bronnen(mid, rijen):
    groepen = {}
    for r in rijen:
        veld, bron, datum, status = str(r[1] or '').strip(), app_store(r[3]), r[4], str(r[5] or '').strip().lower()
        if 'bol' in (bron + veld).lower() or status.startswith(('winkelclaim', 'niet gevonden', 'niet geopend')):
            continue
        urls = re.findall(r'https?://[^\s;()]+', bron)
        for u in urls:
            s = soort_eufy(u)
            if not s:
                continue  # winkels (Coolblue, Amazon, x-kom) en Bol
            g = groepen.setdefault(u, {'label': s[0], 'velden': [], 'datum': None, 'plek': s[1]})
            if veld not in g['velden']:
                g['velden'].append(veld)
            ds = datum.strftime('%Y-%m-%d') if hasattr(datum, 'strftime') else str(datum or '')[:10]
            g['datum'] = min(filter(None, [g['datum'], ds]))
    li = []
    for u, g in groepen.items():
        v = g['velden'][:6]
        tekst = ', '.join(v) + (' en meer' if len(g['velden']) > 6 else '')
        plek = g['plek']  # korte aanduiding in plaats van het lange pad (past op 360 px)
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
  <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li aria-current="page">Eufy robotmaaier</li></ol></nav>
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
delen.append(groep('<ol class="rmk-sources">\n  <li><div><a href="/hoe-we-beoordelen/#scoremodel">Scoremodel v1.0 (concept tot bevriezing)</a><div class="rmk-sources__meta"><span class="rmk-chip rmk-chip--brand">Eigen methode</span></div></div></li>\n</ol>'))
delen.append('<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n'
             '<div class="wp-block-group rmk-container rmk-block rmk-column">\n<!-- wp:pattern {"slug":"robotmaaierkompas/auteursblok"} /-->\n</div>\n<!-- /wp:group -->\n'
             '</main>\n<!-- /wp:group -->')

inhoud = '\n\n'.join(x for x in delen if x)
os.makedirs(os.path.dirname(UIT), exist_ok=True)
json.dump({'slug': fm['slug'], 'title': titel, 'status': 'draft', 'content': inhoud,
           'meta': {'_yoast_wpseo_metadesc': META, '_yoast_wpseo_bctitle': 'Eufy robotmaaier'}},
          open(UIT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({'geschreven': UIT, 'kaarten': volgorde, 'bronregels': telling, 'faq': len(vragen), 'tekens': len(inhoud)}, ensure_ascii=False))
