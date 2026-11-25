#!/usr/bin/env python3
"""Ronde 114: de 43 lege conceptsjablonen (eerste opzet, 6 oktober 2026) naar de PRULLENBAK (niet definitief verwijderen).
Opdracht Mandy (25-11-2026). Publiceert niets en wijzigt geen gepubliceerde pagina.

Proefdraai (standaard, alleen lezen): CSV-overzicht en alle controles. Met --schrijf daarna:
  1. kopie van de 43 concepten (volledig, context=edit) in backups/ (niet in git);
  2. momentopname van de gepubliceerde pagina's (REST: status, slug, ouder, wijzigingsdatum, inhoud; live HTML van <main>);
  3. per concept DELETE zonder force (= prullenbak), met controle dat de status "trash" is;
  4. dezelfde momentopname opnieuw en vergelijken.
Weigert als: de concepten niet precies deze 43 zijn, er één na 2026-10-06 is gewijzigd, een gepubliceerde pagina een van de 43
als ouder heeft, of er ergens (inhoud of live HTML van een gepubliceerde pagina, navigatie, sjabloondelen, sjablonen,
herbruikbare blokken, klassieke menu's) naar een van de 43 wordt gelinkt.
Gebruik:  python3 scripts/ronde114.py <uit.csv>            (proef)
          python3 scripts/ronde114.py <uit.csv> --schrijf
"""
import base64, csv, hashlib, html, json, os, re, subprocess, sys, time, urllib.error, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api, _auth

SCHRIJF = '--schrijf' in sys.argv
CSV = [a for a in sys.argv[1:] if not a.startswith('--')][0]
IDS = [14, 19, 23, 25, 27, 28, 29, 30, 31, 32, 33, 34, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
       56, 60, 62, 63, 64, 65, 67, 68, 69, 70, 71, 72, 73, 74, 75]
assert len(IDS) == 43
SJABLOON = {14: 'toplijst', 64: 'toplijst', 23: 'merk', 19: 'sectie-overzicht', 25: 'sectie-overzicht',
            27: 'sectie-overzicht', 65: 'sectie-overzicht'}
SJABLOON.update({i: 'hulp' for i in range(67, 76)})
GROEP_C = {19, 25, 27, 65, 28}


def alle(pad):
    uit, pg = [], 1
    while True:
        r = api(f'{pad}&per_page=100&page={pg}')
        uit += r
        if len(r) < 100:
            return uit
        pg += 1


def woorden(raw):
    t = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    return len(re.findall(r'\w+', t)), t


def live(url):
    r = subprocess.run(['curl', '-s', '-m', '60', '-w', '\n%{http_code}', url + ('&' if '?' in url else '?') + f'nc={int(time.time())}'],
                       capture_output=True, text=True).stdout
    return r[-3:], r[:-4]


def main_html(h):
    m = re.search(r'<main\b.*?</main>', h, re.S)
    return m.group(0) if m else ''


def momentopname(pubs):
    s = {}
    for p in pubs:
        q = api(f'wp/v2/pages/{p["id"]}?context=edit&_fields=id,status,slug,parent,modified,content,link')
        code, h = live(q['link'])
        s[q['id']] = {'status': q['status'], 'slug': q['slug'], 'parent': q['parent'], 'modified': q['modified'],
                      'inhoud': hashlib.sha256(q['content']['raw'].encode()).hexdigest(), 'http': code,
                      'main': hashlib.sha256(main_html(h).encode()).hexdigest(), 'link': q['link'], '_html': h}
    return s


concepten = alle('wp/v2/pages?status=draft&context=edit')
pubs = alle('wp/v2/pages?status=publish&context=edit&_fields=id,slug,parent,link,content,status')
meld = []
if sorted(p['id'] for p in concepten) != IDS:
    meld.append(f'concepten zijn niet precies de 43 verwachte: {sorted(p["id"] for p in concepten)}')
dr = {p['id']: p for p in concepten if p['id'] in IDS}
for i, p in dr.items():
    if not p['modified'].startswith('2026-10-06'):
        meld.append(f'#{i}: gewijzigd op {p["modified"]} (verwacht 2026-10-06).')

# Ouders
for q in pubs:
    if q['parent'] in IDS:
        meld.append(f'gepubliceerde #{q["id"]} {q["slug"]} heeft concept #{q["parent"]} als ouder.')


def linkt(tekst, p):
    s = p['slug']
    return bool((s and re.search(r'(href|url)=?\\?"(https?:\\?/\\?/(www\.)?robotmaaierkompas\.nl)?\\?/(?:[^"]*\\?/)?' + re.escape(s) + r'\\?/?(#[^"]*)?\\?"', tekst))
                or re.search(r'[?&](page_id|p)=' + str(p['id']) + r'\b', tekst)
                or re.search(r'"id":\s*' + str(p['id']) + r'\b[^}]*"(kind|type)":\s*"post-type"', tekst)
                or re.search(r'"(kind|type)":\s*"post-type"[^}]*"id":\s*' + str(p['id']) + r'\b', tekst))


bronnen = [('gepubliceerd #%d %s (inhoud)' % (q['id'], q['slug']), q['content']['raw']) for q in pubs]
for ep in ('wp/v2/navigation?status=publish,draft&context=edit', 'wp/v2/template-parts?context=edit',
           'wp/v2/templates?context=edit', 'wp/v2/blocks?status=publish,draft&context=edit'):
    for x in alle(ep):
        c = x.get('content')
        bronnen.append((f'{ep.split("?")[0]}:{x.get("id")}', c.get('raw', '') if isinstance(c, dict) else str(c or '')))
try:
    items = alle('wp/v2/menu-items?context=edit')
except SystemExit:
    items = []
for it in items:
    if it.get('object_id') in IDS or any(linkt(it.get('url') or '', dr[i]) for i in dr):
        meld.append(f'klassiek menu-item #{it["id"]} verwijst naar {it.get("object_id")} / {it.get("url")}')
print(f'Bronnen doorzocht: {len(bronnen)} (inhoud {len(pubs)} gepubliceerde pagina\'s, navigatie, sjabloondelen, sjablonen, blokken), '
      f'{len(items)} klassieke menu-items.')
inkomend = {i: [] for i in IDS}
for naam, tekst in bronnen:
    for i, p in dr.items():
        if linkt(tekst, p):
            inkomend[i].append(naam)
# live HTML (menu, voettekst, kruimelpad) van alle gepubliceerde pagina's
for q in pubs:
    code, h = live(q['link'])
    if code != '200':
        meld.append(f'gepubliceerde #{q["id"]} {q["slug"]}: HTTP {code}')
    for i, p in dr.items():
        if linkt(h, p):
            inkomend[i].append(f'live HTML {q["slug"]}')
for i, v in inkomend.items():
    if v:
        meld.append(f'#{i} {dr[i]["slug"]}: gelinkt vanaf {v}')
# links tussen concepten onderling (alleen ter info; die gaan samen naar de prullenbak)
onderling = {i: [j for j in dr if j != i and linkt(dr[j]['content']['raw'], dr[i])] for i in dr}

# CSV
with open(CSV, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['ID', 'Titel', 'Slug', 'Ouder (ID)', 'Type/sjabloon', 'Groep', 'Woorden', 'Productkaarten', 'Scoreblok/-tabel (shortcode)',
                'Inhoud', 'Plaatshouders [..]', 'Aangemaakt', 'Laatst gewijzigd', 'Gelinkt vanaf gepubliceerd/menu', 'Gelinkt vanaf andere concepten'])
    for i in IDS:
        p = dr[i]
        raw = p['content']['raw']
        n, t = woorden(raw)
        typ = SJABLOON.get(i, 'kopersgids')
        groep = 'c (overig/onduidelijk)' if i in GROEP_C else 'a (leeg/bijna leeg sjabloon)'
        inh = {'kopersgids': 'voorbeeldtekst "Een robotmaaier kiezen in 5 stappen" (gelijk voor 27 pagina\'s)',
               'hulp': 'hulpsjabloon met [Probleem]/[Stap]', 'toplijst': 'toplijstsjabloon, lege patronen scoretabel/productbox',
               'merk': 'merksjabloon met [Merknaam]', 'sectie-overzicht': 'alleen "[Overzichtspagina: ...]"'}[typ]
        w.writerow([i, html.unescape(p['title']['raw']), p['slug'], p['parent'] or '', typ, groep, n,
                    len(re.findall(r'<article class="rmk-product"', raw)), len(re.findall(r'\[rmk_(scoreblok|scoretabel)', raw)), inh,
                    len(re.findall(r'\[[^\]]{2,60}\]', t)), p['date'][:10], p['modified'].replace('T', ' ')[:16],
                    ', '.join(inkomend[i]) or 'nee', ', '.join(f'#{j}' for j in onderling[i]) or 'nee'])
print('CSV:', CSV)
print('Meldingen:' if meld else 'Geen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(1 if meld else 0)
if meld:
    sys.exit('Niets verplaatst vanwege de meldingen.')

# 1. kopie
os.makedirs('backups', exist_ok=True)
tijd = time.strftime('%Y%m%d-%H%M%S')
kopie = f'backups/ronde114-concepten-voor-{tijd}.json'
json.dump([api(f'wp/v2/pages/{i}?context=edit') for i in IDS], open(kopie, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie van de 43 concepten:', kopie)
# 2. momentopname vooraf
voor = momentopname(pubs)
json.dump({k: {kk: vv for kk, vv in v.items() if kk != '_html'} for k, v in voor.items()},
          open(f'backups/ronde114-gepubliceerd-voor-{tijd}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# 3. naar de prullenbak (DELETE zonder force)
verplaatst = []
for i in IDS:
    req = urllib.request.Request(f'https://robotmaaierkompas.nl/wp-json/wp/v2/pages/{i}', method='DELETE',
                                 headers={'Authorization': _auth(), 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            st = json.load(r).get('status')
    except urllib.error.HTTPError as e:
        sys.exit(f'#{i}: HTTP {e.code} {e.read()[:200]!r}. Gestopt; al verplaatst: {verplaatst}')
    q = api(f'wp/v2/pages/{i}?context=edit&_fields=id,status')
    if st != 'trash' or q['status'] != 'trash':
        sys.exit(f'#{i}: status {st}/{q["status"]}, verwacht trash. Gestopt; al verplaatst: {verplaatst}')
    verplaatst.append(i)
print(f'Naar de prullenbak ({len(verplaatst)}):', verplaatst)
# 4. momentopname na en vergelijken
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
na = momentopname(pubs)
afw = []
for k, v in voor.items():
    for veld in ('status', 'slug', 'parent', 'modified', 'inhoud', 'http', 'main'):
        if v[veld] != na[k][veld]:
            afw.append(f'#{k} {v["slug"]}: {veld} {v[veld]} -> {na[k][veld]}')
over = alle('wp/v2/pages?status=draft&context=edit&_fields=id')
print(f'Gepubliceerd: {len(na)} pagina\'s; afwijkingen: {afw or "geen"}; concepten over: {len(over)}')
sys.exit(1 if afw else 0)
