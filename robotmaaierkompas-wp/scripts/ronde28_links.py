#!/usr/bin/env python3
"""Ronde 28, stap 3: link naar /segway-navimow-robotmaaier/ op de hub (#10) en pagina 1 (#11).

Klaargezet, nog niet gedraaid (besluit Mandy 12 oktober 2026): de hub en pagina 1 zijn gepubliceerd, en een link
naar een concept geeft bezoekers een 404. Draai dit pas als de Navimow-pagina gepubliceerd is; het script weigert anders.

- /beste-robotmaaier/ (#10): onder "Meer lezen" één extra regel in de lijst.
- /robotmaaier-zonder-draad/ (#11): onder het kopje "De modellen een voor een" één alinea.
Tekst: "Alle Segway Navimow-modellen die nu nieuw te koop zijn, met kosten: zie Segway Navimow robotmaaier."
Elke wijziging alleen als het ankerpunt precies één keer voorkomt en de regel er nog niet staat. Status blijft zoals hij is.

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde28_links.py           (proefdraai, schrijft niets)
          python3 scripts/ronde28_links.py --schrijf
          python3 scripts/ronde28_links.py --test HUB.html PAGINA1.html   (alleen lokaal: toont het resultaat op kopieën)
"""
import base64, json, os, re, sys, urllib.request, urllib.error

SLUG = 'segway-navimow-robotmaaier'
LINK = f'<a href="/{SLUG}/">Segway Navimow robotmaaier</a>'
ZIN = f'Alle Segway Navimow-modellen die nu nieuw te koop zijn, met kosten: zie {LINK}.'
WIJZIGINGEN = {
    10: ('<h2 id="meer-lezen">Meer lezen</h2>\n<ul>', f'<h2 id="meer-lezen">Meer lezen</h2>\n<ul><li>{ZIN}</li>'),
    11: ('<h2>De modellen een voor een</h2>', f'<h2>De modellen een voor een</h2>\n<p>{ZIN}</p>'),
}


def pas_toe(pid, raw):
    oud, nieuw = WIJZIGINGEN[pid]
    if f'href="/{SLUG}/"' in raw:
        return raw, 'staat er al'
    n = raw.count(oud)
    if n != 1:
        return None, f'ankerpunt {n} keer gevonden'
    return raw.replace(oud, nieuw), 'toegevoegd'


if '--test' in sys.argv:
    for pid, pad in zip((10, 11), sys.argv[sys.argv.index('--test') + 1:]):
        raw = open(pad, encoding='utf-8').read()
        uit, st = pas_toe(pid, raw)
        print(pid, st)
        if uit:
            i = uit.find(ZIN)
            print('   ', re.sub(r'\s+', ' ', uit[max(0, i - 160):i + len(ZIN) + 40]))
            print('    alleen deze regel erbij:', uit.replace(WIJZIGINGEN[pid][1], WIJZIGINGEN[pid][0]) == raw)
    sys.exit(0)

SITE = 'https://robotmaaierkompas.nl/wp-json/wp/v2/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
SCHRIJF = '--schrijf' in sys.argv
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()


def api(path, data=None):
    req = urllib.request.Request(SITE + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:300]!r}')


doel = api(f'pages?slug={SLUG}&status=publish,draft,pending,private,future&context=edit&_fields=id,status')
if len(doel) != 1 or doel[0]['status'] != 'publish':
    sys.exit(f'/{SLUG}/ is niet gepubliceerd ({[d["status"] for d in doel] or "niet gevonden"}). Niets gewijzigd: een link zou een 404 geven.')
for pid in WIJZIGINGEN:
    p = api(f'pages/{pid}?context=edit')
    uit, st = pas_toe(pid, p['content']['raw'])
    print(f'#{pid} {p["slug"]} ({p["status"]}): {st}')
    if uit and st == 'toegevoegd' and SCHRIJF:
        api(f'pages/{pid}', {'content': uit})
        q = api(f'pages/{pid}?context=edit')
        print(f'   opgeslagen; status {q["status"]}; link aanwezig: {f"href=\"/{SLUG}/\"" in q["content"]["raw"]}')
