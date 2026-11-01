#!/usr/bin/env python3
"""Vergelijkt de uitvoer van tests/thema-paginas.php (ronde 80): thema 1.3.13 tegen 1.3.14, per modus (zonder, live).
Gebruik: python3 -I tests/thema-paginas-vergelijk.py <map met r-oud-zonder.json, r-nieuw-zonder.json, r-oud-live.json, r-nieuw-live.json>
         <modellen.json> <paginas-raw.json>
Controleert:
- geen HTTP-verzoeken;
- alle pagina's zonder scoretabel byte voor byte gelijk;
- pagina's met [rmk_scoretabel]: de nieuwe HTML is precies de oude met alleen (1) het bijschrift "scoremodel v1.0" zonder
  "(concept tot bevriezing)" en (2) per rij de cel "Details": met kaart op de pagina "Details" naar de kaart, anders
  "Merkpagina" naar de merkpagina, zonder merkpagina een lege cel. Daarmee zijn ook scores, volgorde en winkelregels gelijk.
"""
import html, json, re, sys

D, MOD, PAG = sys.argv[1:4]
mod = {m['slug']: m for m in json.load(open(MOD, encoding='utf-8'))['modellen']}
raw = {p['slug']: p['raw'] for p in json.load(open(PAG, encoding='utf-8'))}
MERK = {'Segway Navimow': '/segway-navimow-robotmaaier/', 'Husqvarna': '/husqvarna-robotmaaier/', 'Gardena': '/gardena-robotmaaier/',
        'Stihl': '/stihl-robotmaaier/', 'Worx': '/worx-robotmaaier/', 'Mova': '/mova-dreame-robotmaaier/',
        'Dreame': '/mova-dreame-robotmaaier/', 'Eufy': '/eufy-robotmaaier/'}
OUD_CAP = 'Scores volgens scoremodel v1.0 (concept tot bevriezing). Volgorde'
NIEUW_CAP = 'Scores volgens scoremodel v1.0. Volgorde'
fout = 0


def t(naam, ok, info=''):
    global fout
    print(('OK   ' if ok else 'FOUT ') + naam + (f'\n       {info}' if info and not ok else ''))
    fout += 0 if ok else 1


for modus in ('zonder', 'live'):
    o = json.load(open(f'{D}/r-oud-{modus}.json', encoding='utf-8'))
    n = json.load(open(f'{D}/r-nieuw-{modus}.json', encoding='utf-8'))
    t(f'{modus}: geen HTTP-verzoeken (oud en nieuw)', o['verzoeken'] == [] == n['verzoeken'])
    t(f'{modus}: zelfde pagina\'s', set(o['paginas']) == set(n['paginas']))
    for slug in sorted(o['paginas']):
        a, b = o['paginas'][slug], n['paginas'][slug]
        if '[rmk_scoretabel' not in raw[slug]:
            t(f'{modus}: /{slug}/ byte voor byte gelijk', a == b)
            continue
        t(f'{modus}: /{slug}/ oude versie heeft een gerenderde scoretabel', 'rmk-table--cards' in a and '[rmk_scoretabel' not in a)
        t(f'{modus}: /{slug}/ bijschrift oud 1x', a.count(OUD_CAP) == 1)
        verwacht = a.replace(OUD_CAP, NIEUW_CAP)
        telling = {'kaart': 0, 'merk': 0, 'geen': 0}
        details = {}

        def cel(m):
            s = html.unescape(m.group(1))
            md = mod[s]
            if re.search(r'\sid="p-' + re.escape(s) + '"', raw[slug]):
                telling['kaart'] += 1
                details[s] = 'Details'
                return m.group(0)
            if md['merk'] in MERK:
                telling['merk'] += 1
                details[s] = 'Merkpagina ' + MERK[md['merk']]
                return f'<td class="c-go"><a href="{MERK[md["merk"]]}">Merkpagina</a></td></tr>'
            telling['geen'] += 1
            details[s] = 'geen link'
            return '<td class="c-go"></td></tr>'
        verwacht = re.sub(r'<td class="c-go"><a href="#p-([^"]+)">Details</a></td></tr>', cel, verwacht)
        t(f'{modus}: /{slug}/ precies de oude pagina met alleen bijschrift en Details-cellen anders '
          f'(kaart {telling["kaart"]}, merkpagina {telling["merk"]}, geen link {telling["geen"]})', verwacht == b,
          next((f'eerste verschil bij teken {i}: …{a[i-80:i+80]!r}… / …{b[i-80:i+80]!r}…' for i in range(min(len(verwacht), len(b))) if verwacht[i] != b[i]), 'lengte'))
        if modus == 'live':
            for s, d in details.items():
                if d != 'Details':
                    print(f'       {mod[s]["id"]} {mod[s]["naam"]} ({mod[s]["merk"]}): {d}')
        t(f'{modus}: /{slug}/ geen "concept tot bevriezing" meer', 'concept tot bevriezing' not in b)
print(f'\n{fout} fout(en)')
sys.exit(1 if fout else 0)
