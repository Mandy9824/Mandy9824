#!/usr/bin/env python3
"""Ronde 53: conceptpagina stihl-robotmaaier (#22), tabel "De Stihl iMOW-modellen naast elkaar": laatste kolom "Meer info"
met per model "Bekijk bij Stihl" naar fabrikant_url uit de live modelgegevens (gewone externe link, rel="noopener").
Bouwt op de live inhoud (niet op scripts/ronde52/stihl.json). Alleen deze tabel verandert; de pagina blijft concept.
Weigert als een model geen fabrikant_url heeft, als de tabel niet precies één keer voorkomt of als #22 geen concept is.
Gebruik:  python3 scripts/ronde53_meer_info.py [--schrijf]
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
"""
import html, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
KOP = ('<thead><tr><th scope="col">Model</th><th scope="col">Oppervlak</th><th scope="col">Helling</th><th scope="col">Geluid (LWA)</th>'
       '<th scope="col">Max. draadlengte</th><th scope="col">Mobiele verbinding</th><th scope="col">Functiescore</th></tr></thead>')

p = api('wp/v2/pages/22?context=edit')
if p['status'] != 'draft' or p['slug'] != 'stihl-robotmaaier':
    sys.exit(f'#22 is {p["slug"]} met status {p["status"]}, geen concept stihl-robotmaaier. Niets gewijzigd.')
raw = p['content']['raw']
modellen = {m['naam']: m for m in api('rmk/v1/modellen')['data']['modellen'] if m.get('merk') == 'Stihl'}

tabellen = re.findall(r'<div class="rmk-tablewrap"><table class="rmk-table">' + re.escape(KOP) + r'<tbody>.*?</tbody></table></div>', raw, re.S)
if len(tabellen) != 1:
    sys.exit(f'Tabel "De Stihl iMOW-modellen naast elkaar" {len(tabellen)} keer gevonden (verwacht 1). Niets gewijzigd.')
oud = tabellen[0]
nieuw = oud.replace(KOP, KOP.replace('</tr></thead>', '<th scope="col">Meer info</th></tr></thead>'), 1)
rijen = re.findall(r'<tr><th scope="row">(.*?)</th>.*?</tr>', oud.split('<tbody>', 1)[1], re.S)
zonder, gebruikt = [], []
for cel in rijen:
    naam = 'Stihl ' + re.sub(r'<[^>]+>', '', cel).strip()
    m = modellen.get(naam)
    url = (m or {}).get('fabrikant_url')
    if not url:
        zonder.append(naam)
        continue
    gebruikt.append((m['id'], naam, url))
if zonder or len(rijen) != 9:
    sys.exit(f'Rijen: {len(rijen)} (verwacht 9); zonder fabrikant_url: {zonder}. Niets gewijzigd.')
body = nieuw.split('<tbody>', 1)[1]
for (mid, naam, url), cel in zip(gebruikt, rijen):
    rij = re.search(r'<tr><th scope="row">' + re.escape(cel) + r'</th>.*?</tr>', body, re.S).group(0)
    body = body.replace(rij, rij[:-5] + f'<td><a href="{html.escape(url)}" rel="noopener">Bekijk bij Stihl</a></td></tr>', 1)
nieuw = nieuw.split('<tbody>', 1)[0] + '<tbody>' + body
assert raw.count(oud) == 1
inhoud = raw.replace(oud, nieuw, 1)
for mid, naam, url in gebruikt:
    print(f'  {mid} {naam}: {url}')
print(f'{len(gebruikt)} rijen met "Bekijk bij Stihl"; verder ongewijzigd: {inhoud.replace(nieuw, oud) == raw}')
if not SCHRIJF:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde53-pagina22-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({'22': {'status': p['status'], 'content': raw}}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api('wp/v2/pages/22', {'content': inhoud})
q = api('wp/v2/pages/22?context=edit')
print(f'#22 opgeslagen; status {q["status"]} (was {p["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == inhoud}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
