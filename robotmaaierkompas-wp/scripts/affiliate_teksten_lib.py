"""Gedeeld door scripts/ronde30_affiliate_teksten.py (aanzetten) en scripts/ronde30_affiliate_terug.py (terugdraaien).

Nieuwe teksten: letterlijk uit tekstwijzigingen-affiliate-live.md (Mandy, 13 oktober 2026; dat bestand staat niet in de
repository). Oude teksten: zoals ze op 13 oktober 2026 live stonden (gelijk aan scripts/ronde21_upload.py).
Elke stap zoekt zijn tekst; komt die niet precies één keer voor, dan meldt het script dat en schrijft het niets.
Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD.
"""
import base64, json, os, re, sys, urllib.request, urllib.error

ROOT = 'https://robotmaaierkompas.nl/wp-json/'
DOELEN = (76, 77, 80, 81, 82, 83, 'footer')

# ---- teksten (oud, nieuw) ----------------------------------------------------------------------------------------
TEKST = [  # (doel, oud, nieuw): lopende tekst; tags ertussen mogen, een link "affiliate-melding" blijft staan
    (77, 'Fabrikanten en winkels kunnen geen plek in onze lijsten kopen en beïnvloeden onze score niet. Op dit moment verdienen we niets aan de links naar winkels; verandert dat, dan melden we het in de affiliate-melding.',
         'Fabrikanten en winkels kunnen geen plek in onze lijsten kopen en beïnvloeden onze score niet. We verdienen geld met affiliatelinks naar bol.com: koop je via een knop, dan kunnen wij een commissie ontvangen. Zie de affiliate-melding.'),
    (80, 'Op dit moment verdienen we niets aan de links op deze site. Zie de affiliate-melding.',
         'We kunnen een commissie ontvangen als je via onze links naar bol.com iets koopt. Zie de affiliate-melding.'),
    (76, 'Op dit moment verdienen we niets aan de links naar winkels. Verandert dat, dan melden we het in de affiliate-melding en bij de links. De volgorde in onze lijsten volgt de score en kan niet worden gekocht.',
         'Koop je via een knop naar bol.com iets, dan kan bol.com ons een commissie betalen. Jij betaalt niets extra. De volgorde in onze lijsten volgt de score, niet de commissie. Zie ook de affiliate-melding.'),
    ('footer', 'Op dit moment verdienen we niets aan de links op deze site. Zie de affiliate-melding.',
         'Wij kunnen een commissie ontvangen bij aankopen via links naar bol.com. Zie de affiliate-melding.'),
]
A81_OUD = ('<p>robotmaaierkompas.nl is gratis te gebruiken. Op dit moment verdienen we niets aan de links naar winkels op deze site. '
           'Dat kan later veranderen: zodra we samenwerken met winkels via affiliatelinks, melden we dat hier en bij de links zelf.</p>')
A81_NIEUW = ('<p>robotmaaierkompas.nl verdient geld met affiliatelinks. Als je via een knop naar bol.com gaat en daar iets koopt, kunnen wij een commissie ontvangen van bol.com. '
             'Jij betaalt niets extra. Knoppen naar andere winkels zijn gewone links waar we op dit moment niets aan verdienen; verandert dat, dan melden we het hier.</p>')
A81_SLOT = ('<p>Prijzen, beoordelingen en afbeeldingen van bol.com tonen we met bronvermelding. De beoordelingen zijn eigendom van bol.com. '
            'Wij zijn niet bol.com: bestellingen, betalingen en vragen over een bestelling lopen altijd via bol.com zelf.</p>')
P82_OUD = ('<li>Winkels en affiliatenetwerken: als je op een winkelknop klikt, ga je naar de website van de winkel. Die kan eigen cookies plaatsen '
           'om te zien dat je via ons kwam. Wij hebben daar geen toegang toe. Lees het privacy- en cookiebeleid van de winkel.</li>')
P82_NIEUW = P82_OUD[:-5] + ' Als je op een knop naar bol.com klikt, kan bol.com een cookie plaatsen om te zien dat je via ons kwam. Lees het cookiebeleid van bol.com.</li>'
C83_OUD = ('<tr><th scope="row">Cookies van winkels en netwerken na een klik</th><td>De winkel ziet dat je via ons kwam</td>'
           '<td>Verschilt per winkel</td><td>Wordt door de winkel geplaatst</td></tr>')
C83_NIEUW = ('<tr><th scope="row">Cookies van bol.com na een klik</th><td>bol.com ziet dat je via ons kwam</td>'
             '<td>Verschilt, zie het cookiebeleid van bol.com</td><td>Wordt door bol.com geplaatst</td></tr>')
ADVERTENTIE = 'Advertentie: via deze knoppen naar bol.com krijgen wij mogelijk een commissie. Dat verandert de score niet.'

# Stappen per richting: (doel, soort, zoek, vervang). soort 'exact' = letterlijke HTML, 'tekst' = lopende tekst.
AAN = [(81, 'exact', A81_OUD, A81_NIEUW), (81, 'exact', '</p></article>', '</p>' + A81_SLOT + '</article>')] \
    + [(d, 'tekst', o, n) for d, o, n in TEKST] \
    + [(82, 'exact', P82_OUD, P82_NIEUW), (83, 'exact', C83_OUD, C83_NIEUW)]
UIT = [(81, 'exact', A81_NIEUW, A81_OUD), (81, 'exact', A81_SLOT, '')] \
    + [(d, 'tekst', n, o) for d, o, n in TEKST] \
    + [(82, 'exact', P82_NIEUW, P82_OUD), (83, 'exact', C83_NIEUW, C83_OUD)]


# ---- API --------------------------------------------------------------------------------------------------------------
def _auth():
    pw = os.environ.get('RMK_WP_APP_PASSWORD')
    if not pw:
        sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
    user = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
    return 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()


def api(path, data=None):
    req = urllib.request.Request(ROOT + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data, ensure_ascii=False).encode() if data is not None else None,
                                 headers={'Authorization': _auth(), 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:300]!r}')


def lees():
    """Ruwe inhoud van de zes pagina's en de footer, plus de footer-id, de status per pagina en de advertentie-tekst."""
    pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in DOELEN if pid != 'footer'}
    inh = {pid: p['content']['raw'] for pid, p in pag.items()}
    status = {pid: p['status'] for pid, p in pag.items()}
    footer = [t for t in api('wp/v2/template-parts?context=edit&per_page=100') if t['slug'] == 'footer' and t['source'] == 'custom']
    if len(footer) != 1:
        sys.exit(f'footer: {len(footer)} aangepaste template parts "footer" gevonden (verwacht 1). Niets gewijzigd.')
    inh['footer'] = footer[0]['content']['raw']
    return {'inhoud': inh, 'status': status, 'footer_id': footer[0]['id'],
            'advertentie': api('wp/v2/settings').get('rmk_advertentie_tekst'), 'thema': api('wp/v2/themes?status=active')[0].get('version')}


# ---- tekst zoeken en vervangen ----------------------------------------------------------------------------------------
def tekst_regex(t):
    """Regex voor tekst t in HTML: tussen woorden en leestekens mogen spaties en tags staan."""
    delen = re.findall(r'\w[\w-]*|[^\w\s]', t)
    return re.compile(r'(?:\s|<[^>]+>)*'.join(re.escape(d) for d in delen))


def _tel(html, soort, t):
    return len(tekst_regex(t).findall(html)) if soort == 'tekst' else html.count(t)


def _kort(s):
    return re.sub(r'<[^>]+>', ' ', s).strip()[:110]


def toepassen(inh, stappen):
    """Past de stappen toe op een kopie van inh. Geeft (nieuwe inhoud, meldingen, regels voor het overzicht)."""
    inh, meld, log = dict(inh), [], []
    for doel, soort, zoek, vervang in stappen:
        wat = f'#{doel}' if doel != 'footer' else 'footer'
        h = inh[doel]
        if vervang and _tel(h, soort, vervang) == 1 and (vervang.find(zoek) >= 0 or _tel(h, soort, zoek) == 0):
            log.append(f'  {wat}: al gedaan ({_kort(vervang)[:60]}…)')
            continue
        n = _tel(h, soort, zoek)
        if n == 0 and not vervang:
            log.append(f'  {wat}: al gedaan (weggehaald: {_kort(zoek)[:60]}…)')
            continue
        if n != 1:
            meld.append(f'{wat}: "{_kort(zoek)[:70]}…" {n} keer gevonden (verwacht 1).')
            continue
        if soort == 'tekst':
            m = tekst_regex(zoek).search(h)
            nieuw = vervang
            link = re.search(r'<a\b[^>]*>affiliate-melding</a>', m.group(0))
            if link and 'affiliate-melding' in nieuw:  # link naar de affiliate-melding blijft staan
                i = nieuw.rfind('affiliate-melding')
                nieuw = nieuw[:i] + link.group(0) + nieuw[i + len('affiliate-melding'):]
            inh[doel] = h[:m.start()] + nieuw + h[m.end():]
        else:
            inh[doel] = h.replace(zoek, vervang, 1)
        log.append(f'  {wat}:\n    was:   {_kort(zoek) or "(niets)"}\n    wordt: {_kort(vervang) or "(weggehaald)"}')
    return inh, meld, log


def schrijf(stand, nieuw, advertentie):
    """Schrijft alleen wat verandert. Pagina's houden hun status (alleen 'content' wordt gestuurd)."""
    for pid in DOELEN:
        if pid == 'footer' or nieuw[pid] == stand['inhoud'][pid]:
            continue
        api(f'wp/v2/pages/{pid}', {'content': nieuw[pid]})
        q = api(f'wp/v2/pages/{pid}?context=edit')
        print(f'#{pid} opgeslagen; status {q["status"]} (was {stand["status"][pid]}); inhoud zoals bedoeld: {q["content"]["raw"] == nieuw[pid]}')
    if nieuw['footer'] != stand['inhoud']['footer']:
        api(f'wp/v2/template-parts/{stand["footer_id"]}', {'content': nieuw['footer']})
        print('footer opgeslagen')
    if advertentie is not None and advertentie != (stand['advertentie'] or ''):
        print('advertentie-tekst:', repr(api('wp/v2/settings', {'rmk_advertentie_tekst': advertentie}).get('rmk_advertentie_tekst')))
    print('Leeg daarna de LiteSpeed-cache en de CDN (de footer staat op elke pagina).')
