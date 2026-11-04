#!/usr/bin/env python3
"""Ronde 100: conceptpagina's robotmaaier-diefstal-verzekering en robotmaaier-egels uit de md bouwen
(afgeleid van ronde97_bouw.py).

Gebruik:  python3 scripts/ronde100_bouw.py <diefstal|egels> <pagina.md> robotmaaierkompas_modeldata_v1.xlsx modellen.json
Schrijft scripts/ronde100/<diefstal-verzekering|egels>.json (titel, slug, inhoud, meta). Schrijft niets naar de site.
modellen.json: de live modelgegevens, voor slug en scores van de kaarten.

- Opmaak als de kopersgidsen (/robotmaaier-kleine-tuin/): patroon pagina-merk met het bovenschrift "Uitleg".
- Productkaarten in de volgorde van "modellen:" in de kop van de md; het thema vult specificatiekaart, teksten en het
  prijsblok (Bol, Coolblue, Amazon volgens prijstaken en schakelaars, anders "Bekijk de actuele prijs").
  In de inhoud staan geen winkellinks of prijzen. Geen modellinks in de tabellen (de cellen noemen groepen en merken).
- Bronnen: de rijen van het blad Bronnen waarvan het veld begint met "Onderzoek diefstal" resp. "Onderzoek egels":
  per adres één regel (titel, adres, datum), zonder dubbele adressen. Niet opgenomen: rijen zonder adres
  ("Zoekmachine"), rijen met status "niet geopend" (gemeente Groningen, niet zelf gelezen) en het OData-adres van het
  gegevensmagazijn (API-adres zonder leesbare pagina). Daarna het scoremodel als eigen methode.
- "Meer lezen": beste, zonder draad (en kosten bij diefstal). De links naar elkaar, de RTK-pagina en de merkpagina's
  zet scripts/ronde100_links.py na publicatie (opdracht Mandy). De kopen-pagina bestaat niet (zie bouwlogboek).
- Metabeschrijving uit de md; Yoast-kruimeltitel per pagina.
"""
import datetime as dt, html, json, os, re, sys
from urllib.parse import urlparse

import openpyxl

SOORT, MD, XLSX, MODELLEN = sys.argv[1:5]
CFG = {
    'diefstal': dict(uit='diefstal-verzekering.json', kruimel='Diefstal, GPS en verzekering', veld='Onderzoek diefstal',
                     intro='Uit ons onderzoek van 4 november 2026: verzekeraars, politie en fabrikant.',
                     links=[('lees je op robotmaaier kosten.', 'lees je op <a href="/robotmaaier-kosten/">robotmaaier kosten</a>.')],
                     meer=[('/beste-robotmaaier/', 'Beste robotmaaier', ': onze selectie per situatie.'),
                           ('/robotmaaier-zonder-draad/', 'Robotmaaier zonder draad', ': tien modellen vergeleken.'),
                           ('/robotmaaier-kosten/', 'Robotmaaier kosten', ': wat het echt kost, met verborgen kosten.')]),
    'egels': dict(uit='egels.json', kruimel='Robotmaaier en egels', veld='Onderzoek egels',
                  intro='Uit ons onderzoek van 4 november 2026: organisaties, overheid, nieuws en fabrikant.',
                  links=[],
                  meer=[('/beste-robotmaaier/', 'Beste robotmaaier', ': onze selectie per situatie.'),
                        ('/robotmaaier-zonder-draad/', 'Robotmaaier zonder draad', ': tien modellen vergeleken.')]),
}[SOORT]
UIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ronde100', CFG['uit'])
MAANDEN = 'januari februari maart april mei juni juli augustus september oktober november december'.split()
BASIS = set()
KORT = {}  # geen modellinks in de tabellen
LINKS = CFG['links'] + [
    ('Mail contact@robotmaaierkompas.nl.', 'Mail <a href="mailto:contact@robotmaaierkompas.nl">contact@robotmaaierkompas.nl</a>.'),
]
MEER_LEZEN = '<h2 id="meer-lezen">Meer lezen</h2>\n<ul>' + ''.join(
    f'<li><a href="{u}">{t}</a>{r}</li>' for u, t, r in CFG['meer']) + '</ul>'

modellen = {m['id']: m for m in json.load(open(MODELLEN, encoding='utf-8'))['modellen']}
md = open(MD, encoding='utf-8').read()
fm, body = re.match(r'^---\n(.*?)\n---\n(.*)$', md, re.S).groups()
fm = dict(re.findall(r'^(\w+): (.*)$', fm, re.M))
META = fm['metabeschrijving']
body = re.sub(r'^INSTRUCTIE VOOR DE BOUWER.*?\n', '', body, flags=re.M)
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
        if esc(a) in t:
            GELINKT.add(a)
        t = t.replace(esc(a), b)
    return t


def slugid(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower().replace('é', 'e')).strip('-')


def anker(mid):
    return 'p-' + modellen[mid]['slug']


def tabel(regels):
    rijen = [[c.strip() for c in r.strip().strip('|').split('|')] for r in regels if not re.match(r'^\|\s*-', r)]
    kop, rest = rijen[0], rijen[1:]
    h = '<div class="rmk-tablewrap"><table class="rmk-table"><thead><tr>' + ''.join(f'<th scope="col">{esc(c)}</th>' for c in kop) + '</tr></thead><tbody>'
    for r in rest:
        cellen = [inline(c) for c in r]
        h += '<tr><th scope="row">' + cellen[0] + '</th>' + ''.join(f'<td>{c}</td>' for c in cellen[1:]) + '</tr>'
    return h + '</tbody></table></div>'


def proza(tekst):
    """Markdown-fragment (alinea's, ##/###, tabellen, lijsten, genummerde lijsten) -> HTML."""
    uit = []
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
        elif re.match(r'^\d+\. ', regels[0]):
            assert all(re.match(r'^\d+\. ', r) for r in regels), regels
            uit.append('<ol>' + ''.join(f'<li>{inline(re.sub(r"^\d+\. ", "", r).strip())}</li>' for r in regels) + '</ol>')
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


# ---------------------------------------------------------------- bronnen (blad Bronnen, veld "Onderzoek ...")
SOORTEN = [  # host -> label van de chip
    (('interpolis.nl', 'centraalbeheer.nl', 'anwb.nl', 'nn.nl', 'unive.nl'), 'Verzekeraar'),
    (('verzekeraars.nl',), 'Brancheorganisatie'),
    (('politie.nl', 'officielebekendmakingen.nl', 'wetten.overheid.nl', 'rijksoverheid.nl'), 'Officieel'),
    (('nos.nl',), 'Nieuws'),
    (('husqvarna.com',), 'Fabrikant'),
    (('egelbescherming.nl', 'zodion.nl', 'egelwerkgroep.nl', 'dierenbescherming.nl', 'vogelbescherming.nl'), 'Organisatie'),
]
WEGGELATEN = []


def label(host):
    for hosts, l in SOORTEN:
        if host.endswith(hosts):
            return l
    raise SystemExit(f'onbekende bron: {host}')


def datum(t):
    t = str(t or '').strip()
    if hasattr(t, 'strftime'):
        t = t.strftime('%Y-%m-%d')
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', t)
    if m:
        y, mo, dd = map(int, m.groups())
        t = t.replace(m.group(0), f'{dd} {MAANDEN[mo - 1]} {y}')
        return t.replace('versie ', 'versie van ').replace('(paginametadata)', '(volgens de gegevens van de pagina)')
    return t[:1].lower() + t[1:] if t[:1].isupper() and t.split()[0].lower() in MAANDEN else t


def onderzoeksbronnen(rijen):
    gezien, li = set(), []
    for r in rijen:
        veld, bron, dat, status = str(r[1]).strip(), str(r[3] or '').strip(), r[4], str(r[5] or '').strip().lower()
        dat = dat.strftime('%Y-%m-%d') if hasattr(dat, 'strftime') else str(dat or '')
        if status == 'niet geopend':
            WEGGELATEN.append(f'{veld}: status niet geopend')
            continue
        if not re.search(r'https?://', bron):
            WEGGELATEN.append(f'{veld}: geen adres ({bron})')
            continue
        delen = [x.strip() for x in bron.split(' ; ')]
        org = None
        for i, deel in enumerate(delen):
            m = re.search(r'https?://[^\s;()]+', deel)
            u = m.group(0)
            host = urlparse(u).netloc.lower().removeprefix('www.')
            if host.startswith('gegevensmagazijn.'):
                WEGGELATEN.append(f'{veld}: {u} (API-adres)')
                continue
            voor = deel[:m.start()].strip().removesuffix('-').strip()
            if i == 0:
                org = voor.split(', ')[0] if ', ' in voor else voor
                titel = voor
            else:
                titel = f'{org}, {voor}' if voor else org
            if u in gezien:
                continue
            gezien.add(u)
            if i == 0 or 'geen datum' in dat:
                if status == 'niet gevonden' and re.match(r'\d{4}-\d{2}-\d{2}$', dat):
                    meta = f'gezocht op {datum(dat)}'
                elif 'geen datum' in dat:
                    meta = 'geen datum op de pagina, geraadpleegd op 4 november 2026'
                else:
                    ing = ' (ingediend)' if 'motie' in veld.lower() else ''  # blad Egels (c): 16-06-2026 (ingediend)
                    meta = f'datum: {datum(dat)}{ing}, geraadpleegd op 4 november 2026'
            else:
                meta = 'geraadpleegd op 4 november 2026'
            li.append(f'  <li><div><a href="{html.escape(u)}">{esc(titel)} ({esc(host)})</a><div class="rmk-sources__meta">'
                      f'<span class="rmk-chip">{label(host)}</span><span>{esc(meta)}</span></div></div></li>')
    return li


wb = openpyxl.load_workbook(XLSX, data_only=True)
onderzoek = [r for r in wb['Bronnen'].iter_rows(min_row=2, values_only=True) if str(r[1] or '').startswith(CFG['veld'])]

# ---------------------------------------------------------------- pagina
titel = fm['titel']
delen = []
delen.append(f'''<!-- wp:group {{"tagName":"main","className":"rmk","layout":{{"type":"default"}},"anchor":"inhoud"}} -->
<main id="inhoud" class="wp-block-group rmk"><!-- wp:html -->
<div class="rmk-container rmk-column">
  <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li aria-current="page">{esc(CFG['kruimel'])}</li></ol></nav>
  <header class="rmk-pagehead">
    <p class="rmk-eyebrow">Uitleg</p>
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
stukken = re.split(r'\{\{productbox model=(M\d+)\}\}', voor_faq)
tekst = stukken[0]
for i in range(1, len(stukken), 2):
    mid, na = stukken[i], stukken[i + 1]
    tekst, kop = re.match(r'^(.*)\n### (.+?)\s*$', tekst.rstrip(), re.S).groups()
    delen.append(sectie(proza(tekst)) if tekst.strip() else '')
    delen.append(kaart(mid, kop))
    tekst = na
delen.append(sectie(proza(tekst) + '\n' + MEER_LEZEN))
faq, rest = re.split(r'\n## ', na_faq.strip(), maxsplit=1)
vragen = re.findall(r'\*\*(.+?)\*\*\s*(.+?)(?=\n\s*\n\*\*|\Z)', faq.strip(), re.S)
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h2 style="font-size: var(--rmk-fs-xl)">Veelgestelde vragen</h2></div>\n<!-- /wp:html -->')
delen.append(groep('<div class="rmk-faq">\n' + '\n'.join(f'  <details><summary>{esc(v)}</summary><div><p>{inline(" ".join(a.split()))}</p></div></details>' for v, a in vragen) + '\n</div>'))
delen.append(sectie(proza('## ' + rest)))
li = onderzoeksbronnen(onderzoek)
delen.append(f'<!-- wp:html -->\n<div class="rmk-container rmk-column" style="padding-top: 24px"><h2 style="font-size: var(--rmk-fs-xl)">Bronnen</h2><p class="rmk-small">{esc(CFG["intro"])}</p></div>\n<!-- /wp:html -->')
delen.append(groep('<ol class="rmk-sources">\n' + '\n'.join(li) + '\n</ol>'))
delen.append('<!-- wp:html -->\n<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">Scoremodel</h3></div>\n<!-- /wp:html -->')
delen.append(groep('<ol class="rmk-sources">\n  <li><div><a href="/hoe-we-beoordelen/#scoremodel">Scoremodel v1.0</a><div class="rmk-sources__meta"><span class="rmk-chip rmk-chip--brand">Eigen methode</span></div></div></li>\n</ol>'))
delen.append('<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->\n'
             '<div class="wp-block-group rmk-container rmk-block rmk-column">\n<!-- wp:pattern {"slug":"robotmaaierkompas/auteursblok"} /-->\n</div>\n<!-- /wp:group -->\n'
             '</main>\n<!-- /wp:group -->')

inhoud = '\n\n'.join(x for x in delen if x)
os.makedirs(os.path.dirname(UIT), exist_ok=True)
json.dump({'slug': fm['slug'], 'title': titel, 'status': 'draft', 'content': inhoud, 'kaarten': [x.strip() for x in fm['modellen'].split(',')],
           'meta': {'_yoast_wpseo_metadesc': META, '_yoast_wpseo_bctitle': CFG['kruimel']}},
          open(UIT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
assert GELINKT == {a for a, _ in LINKS}, f'niet gelinkt: {set(a for a, _ in LINKS) - GELINKT}'
print(json.dumps({'geschreven': UIT, 'kaarten': re.findall(r'\{\{productbox model=(M\d+)\}\}', voor_faq), 'bronregels': len(li),
                  'weggelaten': WEGGELATEN, 'faq': len(vragen), 'tekens': len(inhoud)}, ensure_ascii=False, indent=1))
