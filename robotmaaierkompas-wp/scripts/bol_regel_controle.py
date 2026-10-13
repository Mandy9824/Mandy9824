#!/usr/bin/env python3
"""Controle per model: staat de Bol-regel op de site (of zou hij er staan met de schakelaar aan), en hoe ziet de link eruit.

Alleen lezen. Volgt GEEN enkele link naar bol.com of partner.bol.com; de links worden alleen uit de HTML gehaald en
ontleed. De site-ID wordt nooit getoond (alleen of hij overal gelijk is en uit cijfers bestaat).

Per model met EAN en bol-product-URL:
- uitkomst van de laatste ronde (bol-status, ingelogd), prijs en verkoper;
- verwacht: Bol-regel zichtbaar met de schakelaar aan (zelfde regel als rmk_bol_knop_zichtbaar in inc/bol.php)?
- publieke prijsroute /rmk/v1/bol-prijs (zonder inloggen): wat een bezoeker krijgt;
- op welke openbare pagina's de kaart staat, en op welke daarvan nu een Bol-regel in de HTML staat;
- de vorm van elke gevonden link: https://partner.bol.com/click/click?p=2&t=url&s=<SITE_ID>&f=api&url=<www.bol.com/...>
  &name=<modelnaam>&subid=<paginaslug>, met rel="sponsored nofollow" (Logboek 144-145, besluiten 13 oktober 2026).
Met de schakelaar uit hoort er nergens een Bol-regel te staan; het script meldt elke afwijking als FOUT.

Gebruik:  python3 scripts/bol_regel_controle.py
Het wachtwoord komt alleen uit RMK_WP_APP_PASSWORD (voor bol-status en de modelgegevens).
"""
import html as htmlmod, json, os, re, sys, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SITE = 'https://robotmaaierkompas.nl'


def publiek(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 rmk-bolcontrole', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


def link_vorm(href, naam, slug, fouten, wat):
    """Ontleedt een affiliatelink; geeft de vorm terug met <SITE_ID> in plaats van de site-ID."""
    u = urllib.parse.urlsplit(href)
    q = urllib.parse.parse_qsl(u.query, keep_blank_values=True)
    sleutels = [k for k, _ in q]
    d = dict(q)
    if (u.scheme, u.netloc, u.path) != ('https', 'partner.bol.com', '/click/click'):
        fouten.append(f'{wat}: link gaat naar {u.scheme}://{u.netloc}{u.path}')
    if sleutels != ['p', 't', 's', 'f', 'url', 'name', 'subid']:
        fouten.append(f'{wat}: parameters {sleutels}')
    for k, v in (('p', '2'), ('t', 'url'), ('f', 'api'), ('name', naam), ('subid', slug)):
        if d.get(k) != v:
            fouten.append(f'{wat}: {k}={d.get(k)!r}, verwacht {v!r}')
    if not re.fullmatch(r'\d+', d.get('s', '')):
        fouten.append(f'{wat}: site-ID is geen getal')
    doel = urllib.parse.urlsplit(d.get('url', ''))
    if (doel.scheme, doel.netloc) != ('https', 'www.bol.com') or not doel.path.startswith('/nl/nl/p/'):
        fouten.append(f'{wat}: url= wijst naar {doel.scheme}://{doel.netloc}{doel.path[:20]}')
    vorm = f'https://partner.bol.com/click/click?p={d.get("p")}&t={d.get("t")}&s=<SITE_ID>&f={d.get("f")}' \
           f'&url={doel.scheme}://{doel.netloc}{doel.path[:28]}…&name={d.get("name")}&subid={d.get("subid")}'
    return vorm, d.get('s')


status = api('rmk/v1/bol-status')
data = api('rmk/v1/modellen')['data']
modellen = {m['id']: m for m in data['modellen'] if m.get('ean') and (m.get('bol') or {}).get('product_url')}
schakelaar = bool(status.get('affiliate_actief'))
prijs = json.loads(publiek(f'{SITE}/wp-json/rmk/v1/bol-prijs?modellen={",".join(modellen)}')).get('modellen') or {}
paginas = [p['link'] for p in api('wp/v2/pages?per_page=100&status=publish&_fields=link')] + [SITE + '/']
fouten, site_ids, kaarten, regels = [], set(), {}, {}
for url in sorted(set(paginas)):
    h = publiek(url)
    slug = urllib.parse.urlsplit(url).path.strip('/').split('/')[-1] or 'home'
    for m in modellen.values():
        if f'aria-labelledby="p-{m["slug"]}"' in h:
            kaarten.setdefault(m['id'], []).append(slug)
    for blok in re.finditer(r'<div class="rmk-offer[^"]*rmk-offer--bol"[^>]*data-rmk-bol-model="(M\d+)"[^>]*>(.*?)</div>', h, re.S):
        mid, binnen = blok.group(1), blok.group(2)
        a = re.search(r'<a\b([^>]*)data-rmk-bol-link[^>]*>', binnen)
        href = htmlmod.unescape(re.search(r'href="([^"]*)"', a.group(1)).group(1)) if a else ''
        rel = (re.search(r'rel="([^"]*)"', a.group(0)) or [None, ''])[1] if a else ''
        wat = f'{mid} op /{slug}/'
        if rel != 'sponsored nofollow':
            fouten.append(f'{wat}: rel="{rel}"')
        if 'Je gaat naar bol.com. Bron: bol.com.' not in binnen:
            fouten.append(f'{wat}: bronregel ontbreekt')
        vorm, s = link_vorm(href, modellen[mid]['naam'] if mid in modellen else '?', slug, fouten, wat)
        site_ids.add(s)
        regels.setdefault(mid, []).append((slug, vorm))
    if 'data-rmk-bol' in h and not schakelaar:
        fouten.append(f'/{slug}/: Bol-regel in de HTML terwijl de schakelaar uit staat')

print(f'Schakelaar RMK_AFFILIATE_ACTIVE: {"aan" if schakelaar else "uit"}; constanten aanwezig: {status.get("constanten_aanwezig")}')
lr = status.get('laatste_ronde') or {}
print(f'Laatste ronde: ok {lr.get("ok")}, geen aanbod {lr.get("geen_aanbod")}, fout {lr.get("fout")}, gestopt {lr.get("gestopt")}; volgende {status.get("volgende_ronde")}\n')
for mid, m in modellen.items():
    s = status['modellen'].get(mid, {})
    verwacht = s.get('uitkomst') not in ('geen_aanbod', 'ongeldig')
    p = prijs.get(mid) or {}
    pub = p.get('prijs_tekst') or p.get('status') or '(niets)'
    print(f'{mid} {m["naam"]}')
    print(f'   ronde: {s.get("uitkomst")}, {s.get("prijs")} bij {s.get("verkoper")}{" (partner)" if s.get("partner") else ""}, opgehaald {s.get("opgehaald")}, geldig tot {s.get("geldig_tot")}')
    print(f'   met schakelaar aan: {"Bol-regel (knop" + (", prijs)" if s.get("uitkomst") == "ok" else ", geen prijs)") if verwacht else "geen Bol-regel"}; publieke prijsroute nu: {pub}')
    print(f'   kaart op: {", ".join(kaarten.get(mid, [])) or "(geen openbare pagina)"}')
    for slug, vorm in regels.get(mid, []):
        print(f'   Bol-regel op /{slug}/: {vorm}')
    if schakelaar and verwacht and set(kaarten.get(mid, [])) != {sl for sl, _ in regels.get(mid, [])}:
        fouten.append(f'{mid}: kaart op {kaarten.get(mid)} maar Bol-regel op {[sl for sl, _ in regels.get(mid, [])]}')
    if not schakelaar and (regels.get(mid) or p):
        fouten.append(f'{mid}: zichtbaar of in de prijsroute terwijl de schakelaar uit staat')
    if regels.get(mid) and not verwacht:
        fouten.append(f'{mid}: Bol-regel terwijl de laatste ronde "{s.get("uitkomst")}" gaf')
if len(site_ids) > 1:
    fouten.append('verschillende site-ID\'s in de links')
print(f'\n{sum(len(v) for v in regels.values())} Bol-regels op {len(set(paginas))} openbare adressen; links niet gevolgd.')
print('\n'.join(['FOUTEN:'] + ['  - ' + f for f in fouten]) if fouten else 'Geen fouten.')
sys.exit(1 if fouten else 0)
