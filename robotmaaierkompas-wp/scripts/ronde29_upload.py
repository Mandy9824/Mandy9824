#!/usr/bin/env python3
"""Ronde 29: analyse M002, "Waarom deze" op de hub, App Store-links in de bronnenlijsten.

1. Modelgegevens (rmk/v1/modellen): in de analyse van M002 "In onze functiescore staat dit model bovenaan."
   -> "In onze functiescore scoort dit model hoog (92,7)." Verder niets.
2. Hub (#10): "de hoogste functiescore in onze selectie, helling tot 45%"
   -> "een van de hoogste functiescores in onze selectie, helling tot 45%".
3. Bronnenlijsten op de hub (#10) en pagina 1 (#11): itunes.apple.com-links -> leesbare App Store-pagina
   (app_store() uit excel_naar_json.py), op de hub ook de domeinnaam in de linktekst. Twee regels met hetzelfde
   adres in één lijst van de hub worden één regel ("App iOS én Android, App-rating (apps.apple.com)").
   Labels blijven staan. De Navimow-pagina (#264, concept) gaat via ronde28_bouw.py en ronde28_upload.py.

Elke tekstvervanging alleen als de oude tekst precies één keer voorkomt. Status van pagina's blijft zoals hij is.
Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde29_upload.py           (proefdraai, schrijft niets)
          python3 scripts/ronde29_upload.py --schrijf
"""
import base64, json, os, re, sys, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excel_naar_json import app_store

ROOT = 'https://robotmaaierkompas.nl/wp-json/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
SCHRIJF = '--schrijf' in sys.argv
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()
ANALYSE = ('In onze functiescore staat dit model bovenaan.', 'In onze functiescore scoort dit model hoog (92,7).')
WAAROM = ('de hoogste functiescore in onze selectie, helling tot 45%', 'een van de hoogste functiescores in onze selectie, helling tot 45%')


def api(path, data=None):
    req = urllib.request.Request(ROOT + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data, ensure_ascii=False).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:300]!r}')


def een_keer(tekst, oud, nieuw, wat):
    n = tekst.count(oud)
    if n != 1:
        sys.exit(f'{wat}: oude tekst {n} keer gevonden. Niets gewijzigd.')
    return tekst.replace(oud, nieuw)


def app_links(raw, samenvoegen):
    """itunes-links in de bronnenlijsten vervangen; op de hub ook de domeinnaam en dubbele regels samenvoegen."""
    def lijst(m):
        ol = m.group(0)
        ol = re.sub(r'(<a href=")([^"]*itunes\.apple\.com[^"]*)(">)(.*?)(</a>)',
                    lambda a: a.group(1) + app_store(a.group(2)) + a.group(3) + a.group(4).replace('(itunes.apple.com)', '(apps.apple.com)') + a.group(5), ol)
        if not samenvoegen:
            return ol
        gezien, uit = {}, []
        for li in re.findall(r'<li>.*?</li>|[^<]+|<[^>]*>', ol, re.S):
            a = re.match(r'<li><div><a href="([^"]+)">(.*?) \(([^()]+)\)</a>', li)
            if a and a.group(1) in gezien:
                i = gezien[a.group(1)]
                eerste = re.match(r'<li><div><a href="[^"]+">(.*?) \(([^()]+)\)</a>', uit[i])
                uit[i] = uit[i].replace(f'>{eerste.group(1)} ({eerste.group(2)})</a>', f'>{eerste.group(1)}, {a.group(2)} ({eerste.group(2)})</a>', 1)
                if uit and uit[-1].strip() == '':
                    uit.pop()  # inspringing en regeleinde van de weggevallen regel
                continue
            if a:
                gezien[a.group(1)] = len(uit)
            uit.append(li)
        return ''.join(uit)
    return re.sub(r'<ol class="rmk-sources">.*?</ol>', lijst, raw, flags=re.S)


# 1. Modelgegevens
m = api('rmk/v1/modellen')
data = m['data']
m002 = [x for x in data['modellen'] if x['id'] == 'M002'][0]
m002_nieuw = een_keer(m002['analyse'], *ANALYSE, 'analyse M002')
print('M002 analyse:', 'al aangepast' if ANALYSE[1] in m002['analyse'] else 'wordt aangepast')
print('M002 fabrikant_url:', m002['fabrikant_url'])
# 2 en 3. Pagina's
nieuw = {}
for pid in (10, 11):
    p = api(f'wp/v2/pages/{pid}?context=edit')
    raw = p['content']['raw']
    uit = een_keer(raw, *WAAROM, f'#{pid} Waarom deze') if pid == 10 else raw
    uit = app_links(uit, samenvoegen=(pid == 10))
    print(f'#{pid} {p["slug"]} ({p["status"]}): itunes {raw.count("itunes.apple.com")} -> {uit.count("itunes.apple.com")}, '
          f'regels in bronnenlijsten {raw.count("<li><div>")} -> {uit.count("<li><div>")}')
    nieuw[pid] = (p, uit)
if not SCHRIJF:
    sys.exit(0)
m002['analyse'] = m002_nieuw
print('modelgegevens:', api('rmk/v1/modellen', data))
for pid, (p, uit) in nieuw.items():
    if uit != p['content']['raw']:
        api(f'wp/v2/pages/{pid}', {'content': uit})
        q = api(f'wp/v2/pages/{pid}?context=edit')
        print(f'#{pid} opgeslagen, status {q["status"]}, inhoud zoals bedoeld: {q["content"]["raw"] == uit}')
