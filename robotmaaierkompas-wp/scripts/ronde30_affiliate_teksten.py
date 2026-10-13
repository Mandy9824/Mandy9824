#!/usr/bin/env python3
"""Teksten voor het moment dat de Bol-links live gaan (tekstwijzigingen-affiliate-live.md, Mandy, 13 oktober 2026).

KLAARGEZET, NIET GEDRAAID. Pas toepassen als Mandy zegt dat RMK_AFFILIATE_ACTIVE aan mag. Tot dan blijven de huidige
teksten ("Op dit moment verdienen we niets aan de links…") staan. Het md-bestand zelf staat niet in de repository;
de teksten hieronder zijn er letterlijk uit overgenomen.

1. #81 affiliate-melding: eerste alinea vervangen; slotalinea toevoegen. 2. #77 over-ons. 3. #80 colofon.
4. #76 hoe-we-beoordelen, "Zo verdienen we geld". 5. footer (template part). 6. #82 privacy, punt
"Winkels en affiliatenetwerken": zin erachter. 7. #83 cookies: tabelrij vervangen. 8. tekst van de advertentie-regel
boven de eerste Bol-knop (instelling rmk_advertentie_tekst, thema 1.3.6); de Bol-regel zelf staat al in het thema.

Elke "Was"-tekst moet precies één keer voorkomen (tags zoals <a> ertussen mogen); anders meldt het script dat en
verandert het die plek niet. Een link naar de affiliate-melding in de oude tekst blijft in de nieuwe tekst staan.
Pagina's houden hun status. Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde30_affiliate_teksten.py            (proefdraai, schrijft niets)
          python3 scripts/ronde30_affiliate_teksten.py --schrijf  (alleen na akkoord van Mandy)
"""
import base64, json, os, re, sys, urllib.request, urllib.error

ROOT = 'https://robotmaaierkompas.nl/wp-json/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
SCHRIJF = '--schrijf' in sys.argv
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()

VERVANG = [  # (pagina-id of 'footer', was, wordt)
    (77, 'Fabrikanten en winkels kunnen geen plek in onze lijsten kopen en beïnvloeden onze score niet. Op dit moment verdienen we niets aan de links naar winkels; verandert dat, dan melden we het in de affiliate-melding.',
         'Fabrikanten en winkels kunnen geen plek in onze lijsten kopen en beïnvloeden onze score niet. We verdienen geld met affiliatelinks naar bol.com: koop je via een knop, dan kunnen wij een commissie ontvangen. Zie de affiliate-melding.'),
    (80, 'Op dit moment verdienen we niets aan de links op deze site. Zie de affiliate-melding.',
         'We kunnen een commissie ontvangen als je via onze links naar bol.com iets koopt. Zie de affiliate-melding.'),
    (76, 'Op dit moment verdienen we niets aan de links naar winkels. Verandert dat, dan melden we het in de affiliate-melding en bij de links. De volgorde in onze lijsten volgt de score en kan niet worden gekocht.',
         'Koop je via een knop naar bol.com iets, dan kan bol.com ons een commissie betalen. Jij betaalt niets extra. De volgorde in onze lijsten volgt de score, niet de commissie. Zie ook de affiliate-melding.'),
    ('footer', 'Op dit moment verdienen we niets aan de links op deze site. Zie de affiliate-melding.',
         'Wij kunnen een commissie ontvangen bij aankopen via links naar bol.com. Zie de affiliate-melding.'),
]
A81_NIEUW = ('robotmaaierkompas.nl verdient geld met affiliatelinks. Als je via een knop naar bol.com gaat en daar iets koopt, kunnen wij een commissie ontvangen van bol.com. Jij betaalt niets extra. Knoppen naar andere winkels zijn gewone links waar we op dit moment niets aan verdienen; verandert dat, dan melden we het hier.')
A81_SLOT = ('Prijzen, beoordelingen en afbeeldingen van bol.com tonen we met bronvermelding. De beoordelingen zijn eigendom van bol.com. Wij zijn niet bol.com: bestellingen, betalingen en vragen over een bestelling lopen altijd via bol.com zelf.')
P82_ZIN = ' Als je op een knop naar bol.com klikt, kan bol.com een cookie plaatsen om te zien dat je via ons kwam. Lees het cookiebeleid van bol.com.'
C83_RIJ = ('<tr><th scope="row">Cookies van bol.com na een klik</th><td>bol.com ziet dat je via ons kwam</td>'
           '<td>Verschilt, zie het cookiebeleid van bol.com</td><td>Wordt door bol.com geplaatst</td></tr>')
ADVERTENTIE = 'Advertentie: via deze knoppen naar bol.com krijgen wij mogelijk een commissie. Dat verandert de score niet.'


def api(path, data=None):
    req = urllib.request.Request(ROOT + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data, ensure_ascii=False).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:300]!r}')


def tekst_regex(t):
    """Regex voor tekst t in HTML: tussen woorden en leestekens mogen spaties en tags staan."""
    delen = re.findall(r'\w[\w-]*|[^\w\s]', t)
    return re.compile(r'(?:\s|<[^>]+>)*'.join(re.escape(d) for d in delen))


def vervang_tekst(html, was, wordt, wat, meldingen):
    hits = list(tekst_regex(was).finditer(html))
    if len(hits) != 1:
        meldingen.append(f'{wat}: "Was" {len(hits)} keer gevonden (verwacht 1); niet gewijzigd.')
        return html
    oud = hits[0].group(0)
    link = re.search(r'<a\b[^>]*>affiliate-melding</a>', oud)
    nieuw = wordt
    if link and 'affiliate-melding' in nieuw:  # link behouden
        i = nieuw.rfind('affiliate-melding')
        nieuw = nieuw[:i] + link.group(0) + nieuw[i + len('affiliate-melding'):]
    # Openingstags vóór de tekst en sluitingstags erna laten staan (de match begint en eindigt op tekst).
    print(f'  {wat}:\n    was:   {re.sub("<[^>]+>", "", oud)[:150]}\n    wordt: {re.sub("<[^>]+>", "", nieuw)[:150]}')
    return html[:hits[0].start()] + nieuw + html[hits[0].end():]


meldingen, nieuw_inhoud = [], {}
thema = api('wp/v2/themes?status=active')[0]
versie = tuple(int(x) for x in re.findall(r'\d+', thema.get('version', ''))[:3])
print(f'Actief thema {thema.get("version")}')
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in (76, 77, 80, 81, 82, 83)}
footer = [t for t in api('wp/v2/template-parts?context=edit&per_page=100') if t['slug'] == 'footer' and t['source'] == 'custom']
if len(footer) != 1:
    meldingen.append(f'footer: {len(footer)} aangepaste template parts "footer" gevonden (verwacht 1).')
inh = {pid: p['content']['raw'] for pid, p in pag.items()}
if footer:
    inh['footer'] = footer[0]['content']['raw']
# 1. #81
h = inh[81]
eerste = re.findall(r'<p>robotmaaierkompas\.nl is gratis te gebruiken\..*?</p>', h, re.S)
if len(eerste) == 1:
    print(f'  #81 eerste alinea:\n    was:   {re.sub("<[^>]+>", "", eerste[0])[:150]}\n    wordt: {A81_NIEUW[:150]}')
    h = h.replace(eerste[0], f'<p>{A81_NIEUW}</p>')
else:
    meldingen.append(f'#81: eerste alinea {len(eerste)} keer gevonden; niet gewijzigd.')
if len(tekst_regex('Dat verandert de score of de volgorde niet').findall(h)) != 1:
    meldingen.append('#81: alinea "Dat verandert de score of de volgorde niet…" niet precies één keer gevonden.')
slot = h.count('</p></article>')
if slot == 1 and A81_SLOT not in h:
    h = h.replace('</p></article>', f'</p><p>{A81_SLOT}</p></article>')
    print(f'  #81 slotalinea toegevoegd: {A81_SLOT[:80]}…')
elif A81_SLOT not in h:
    meldingen.append(f'#81: einde van de tekst ("</p></article>") {slot} keer gevonden; slotalinea niet toegevoegd.')
inh[81] = h
# 2-5
for doel, was, wordt in VERVANG:
    if doel in inh:
        inh[doel] = vervang_tekst(inh[doel], was, wordt, f'#{doel}' if doel != 'footer' else 'footer', meldingen)
# 6. #82
li = re.findall(r'<li>Winkels en affiliatenetwerken:.*?</li>', inh[82], re.S)
if len(li) == 1:
    inh[82] = inh[82].replace(li[0], li[0][:-5] + P82_ZIN + '</li>')
    print(f'  #82 zin toegevoegd achter "Winkels en affiliatenetwerken: …"')
else:
    meldingen.append(f'#82: punt "Winkels en affiliatenetwerken" {len(li)} keer gevonden; niet gewijzigd.')
# 7. #83
rij = re.findall(r'<tr><th scope="row">Cookies van winkels en netwerken na een klik</th>.*?</tr>', inh[83], re.S)
if len(rij) == 1:
    inh[83] = inh[83].replace(rij[0], C83_RIJ)
    print('  #83 tabelrij vervangen')
else:
    meldingen.append(f'#83: rij "Cookies van winkels en netwerken na een klik" {len(rij)} keer gevonden; niet gewijzigd.')
# 8. advertentie-regel
if versie < (1, 3, 6):
    meldingen.append('8: thema 1.3.6 is nog niet actief; de advertentie-tekst (instelling rmk_advertentie_tekst) kan nog niet worden gezet.')
print('\nMeldingen:' if meldingen else '\nGeen meldingen: alle "Was"-teksten precies één keer gevonden.')
for m in meldingen:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
for pid in (76, 77, 80, 81, 82, 83):
    if inh[pid] != pag[pid]['content']['raw']:
        api(f'wp/v2/pages/{pid}', {'content': inh[pid]})
        print(f'#{pid} opgeslagen (status {api(f"wp/v2/pages/{pid}?_fields=status")["status"]})')
if footer and inh['footer'] != footer[0]['content']['raw']:
    api(f'wp/v2/template-parts/{footer[0]["id"]}', {'content': inh['footer']})
    print('footer opgeslagen')
if versie >= (1, 3, 6):
    print('advertentie-tekst:', api('wp/v2/settings', {'rmk_advertentie_tekst': ADVERTENTIE}).get('rmk_advertentie_tekst'))
