#!/usr/bin/env python3
"""Ronde 41 (17 oktober 2026, opdracht van Mandy), zonder thema-zip:
1. Bronnen van M015 (i210 LiDAR Pro) en M016 (i205 AWD) overnemen van de Navimow-pagina (#264):
   - hub (#10): per model een blok (kop + lijst) zoals op #264, M015 direct na het i206-blok;
   - pagina 1 (#11): die lijst is één platte lijst met de modelnaam vóór elke regel; de regels van M015 en daarna
     M016 komen direct na de laatste i206-regel, met "Modelnaam: " ervoor. Geen dubbele regels.
2. Mesjespagina (#236): tabelrij Husqvarna Automower 305E NERA (na de 410VE NERA) en een alinea onder
   "Husqvarna robotmaaier mesjes" (na de bestaande alinea).
Elke ankertekst moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: eerst een kopie in backups/, daarna opslaan en LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde41_bronnen_mesjes.py [--schrijf]
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in (10, 11, 236, 264)}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld, log = [], []
MODELLEN = ('Segway Navimow i210 LiDAR Pro', 'Segway Navimow i205 AWD')


def bron_blok(h, naam):
    """Kop-blok + lijst-blok van een model in een gegroepeerde bronnenlijst (zoals #264 en de hub)."""
    i = h.find('>Bronnen<')
    kop = f'<div class="rmk-container rmk-column"><h3 style="font-size: var(--rmk-fs-lg); margin-top: 16px">{naam}</h3></div>'
    if h.count(kop, i) != 1:
        return None
    s = h.rfind('<!-- wp:html -->', 0, h.find(kop, i))
    e = h.find('<!-- /wp:group -->', s) + len('<!-- /wp:group -->')
    return h[s:e]


def vervang(pid, was, wordt, wat):
    n = raw[pid].count(was)
    if n != 1:
        meld.append(f'#{pid} {wat}: ankertekst {n} keer gevonden (verwacht 1); niet gewijzigd.')
        return
    raw[pid] = raw[pid].replace(was, wordt, 1)
    log.append(f'  #{pid} {wat}')


blokken = {n: bron_blok(raw[264], n) for n in MODELLEN}
if not all(blokken.values()):
    sys.exit('Bronnenblokken van M015/M016 niet precies één keer op #264 gevonden. Niets gewijzigd.')
items = {n: re.findall(r'<li><div><a href="[^"]+">[^<]+</a><div class="rmk-sources__meta">.*?</li>', b, re.S) for n, b in blokken.items()}
for n, it in items.items():
    if len(it) != len(set(it)):
        meld.append(f'#264 {n}: dubbele regels in de bron.')
    log.append(f'  {n}: {len(it)} bronnen op #264')

# ---- hub: blok M015 na het i206-blok
for n in MODELLEN:
    if f'margin-top: 16px">{n}</h3>' in raw[10]:
        meld.append(f'#10: bronnenblok {n} staat er al.')
i206 = bron_blok(raw[10], 'Segway Navimow i206 AWD')
if i206:
    vervang(10, i206, i206 + '\n\n' + blokken['Segway Navimow i210 LiDAR Pro'], 'bronnen M015 (blok met kop) na i206')
else:
    meld.append('#10: bronnenblok i206 niet precies één keer gevonden.')

# ---- pagina 1: regels met modelnaam na de laatste i206-regel
b11 = raw[11].find('>Bronnen<')
i206_regels = [m for m in re.finditer(r'<li><div><a href="[^"]+">Segway Navimow i206 AWD: [^<]+</a>.*?</li>', raw[11][b11:], re.S)]
bestaand = set(re.findall(r'<li><div><a href="([^"]+)">([^<]+)</a>', raw[11][b11:]))
nieuw = []
for n in MODELLEN:
    if f'>{n}: ' in raw[11][b11:]:
        meld.append(f'#11: bronnen van {n} staan er al.')
    for it in items[n]:
        it2 = re.sub(r'(<a href="[^"]+">)', lambda m: m.group(1) + n + ': ', it, count=1)
        sleutel = re.search(r'<a href="([^"]+)">([^<]+)</a>', it2).groups()
        if sleutel in bestaand or it2 in nieuw:
            continue  # geen dubbele regels
        nieuw.append(it2)
if i206_regels:
    laatste = i206_regels[-1].group(0)
    vervang(11, laatste, laatste + ''.join('\n  ' + x for x in nieuw), f'bronnen M015 en M016 ({len(nieuw)} regels) na de laatste i206-regel')
else:
    meld.append('#11: geen i206-regels in de bronnenlijst gevonden.')

# ---- mesjespagina
rij_410 = ('<tr><th scope="row">Husqvarna Automower 410VE NERA</th><td>26,99 euro voor 6</td><td>hoofdschijf elke 3 tot 6 weken, '
           'EdgeCut-schijf elke 9 tot 12 weken</td><td>niet berekend: het aantal per schijf is onbekend</td></tr>')
rij_305 = ('<tr><th scope="row">Husqvarna Automower 305E NERA</th><td>Endurance 26,99 euro of Classic 22,99 euro (het aantal messen per '
           'verpakking is niet bevestigd)</td><td>hoofdschijf elke 3 tot 6 weken</td><td>niet berekend: het aantal per schijf is onbekend</td></tr>')
if '305E NERA' in raw[236]:
    meld.append('#236: 305E NERA staat er al.')
vervang(236, rij_410, rij_410 + rij_305, 'tabelrij Husqvarna Automower 305E NERA na de 410VE NERA')
alinea = re.findall(r'<h2 id="husqvarna-robotmaaier-mesjes">Husqvarna robotmaaier mesjes</h2>\n<p>.*?</p>', raw[236], re.S)
if len(alinea) == 1:
    vervang(236, alinea[0], alinea[0] + '\n<p>Voor de Automower 305E NERA noemt Husqvarna Endurance-messen (26,99 euro) en Classic-messen '
            '(22,99 euro); de messen van de hoofdschijf gaan volgens Husqvarna 3 tot 6 weken mee.</p>', 'alinea 305E NERA onder "Husqvarna robotmaaier mesjes"')
else:
    meld.append(f'#236: kop "Husqvarna robotmaaier mesjes" met alinea {len(alinea)} keer gevonden.')

print('\n'.join(log))
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde41-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': pag[pid]['status'], 'content': pag[pid]['content']['raw']} for pid in (10, 11, 236)},
          open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in (10, 11, 236):
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
