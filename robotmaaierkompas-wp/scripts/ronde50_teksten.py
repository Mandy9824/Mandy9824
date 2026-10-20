#!/usr/bin/env python3
"""Ronde 50 (zonder thema-zip): tekstwijzigingen-mesjes-testpagina.md, secties A tot en met D.
A. Testpagina (#13): zin toevoegen aan de alinea onder "Wat is de beste robotmaaier volgens de Consumentenbond?",
   de oude sectie "Wat vonden we bij de Consumentenbond?" (kop en alinea) weg. Gevolg: in de inhoudsopgave
   "In deze gids" gaat de link naar die kop weg en komt de nieuwe kop achteraan (zoals op de pagina).
B. Hub (#10), "Meer lezen": "wat de Consumentenbond, Test-Aankoop en Stiftung Warentest publiek hebben."
C. Mesjespagina (#236): tabelcel 305E/310E NERA; nieuwe sectie "Automower messen: Endurance of Classic?" vóór
   "Zo houd je de kosten laag" (ook in de inhoudsopgave); bronnen uit Bronnen rijen 546-554 (per adres één regel,
   achter de bestaande 305E NERA-regels); zin onder "Wat we nog niet weten".
D. Husqvarna-pagina (#20), FAQ "Wat kosten Automower-mesjes?": zin met link naar de nieuwe kop.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Gebruik:  python3 scripts/ronde50_teksten.py <xlsx> [--schrijf]
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
"""
import html, json, os, re, sys, time
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
XLSX = next(a for a in sys.argv[1:] if not a.startswith('--'))
MES = '/robotmaaier-mesjes/#automower-messen-endurance-of-classic'

# ---------------------------------------------------------------- bronnen (blad Bronnen, rijen 546-554)
LABEL = {
    'endurance-blades': 'Husqvarna Endurance-messen: kenmerken, verpakkingen, prijzen en passende modellen',
    'classic-blades': 'Husqvarna Classic-messen: kenmerken, verpakkingen, prijzen en passende modellen',
    'endurance-hss-blades': 'Husqvarna Endurance HSS-messen: passende modellen',
    'automower-enhance-hss-blades': 'Husqvarna Enhance HSS- en HSS+-messen: passende modellen en toepassing (automower-enhance-hss-blades)',
    'enhance-hss-mes': 'Husqvarna Enhance HSS- en HSS+-messen: passende modellen en toepassing (enhance-hss-mes)',
}
ws = openpyxl.load_workbook(XLSX, data_only=True)['Bronnen']
urls, datums = [], set()
for i in range(546, 555):
    r = [c.value for c in ws[i]]
    assert 'husqvarna.com/nl/robotmaaiermessen/' in str(r[3]), (i, r[3])
    datums.add(str(r[4])[:10])
    for u in re.findall(r'https?://[^\s;()]+', str(r[3])):
        if u not in urls:
            urls.append(u)
assert datums == {'2026-10-19'}, datums
BRONNEN = ''.join(
    f'\n<li><div><a href="{html.escape(u)}">{html.escape(LABEL[u.rstrip("/").split("/")[-1]], quote=False)}</a><div class="rmk-sources__meta">'
    '<span class="rmk-chip">Fabrikant</span><span>geraadpleegd op 19 oktober 2026</span></div></div></li>' for u in urls)

# ---------------------------------------------------------------- A. testpagina
A_ZIN = 'Een beste robotmaaier volgens de Consumentenbond kunnen we dus niet noemen.'
A_OUD = ('<h2 id="wat-vonden-we-bij-de-consumentenbond">Wat vonden we bij de Consumentenbond?</h2>\n'
         '<p>Bij onze controle op 5 oktober 2026 zagen we op consumentenbond.nl alleen testen van gewone grasmaaiers (accu, snoer en hand). '
         'Websites en nieuwsberichten verwijzen soms naar een robotmaaiertest van de Consumentenbond; wat daar precies in staat en hoe actueel '
         'het is, kunnen we niet nagaan. We nemen daarom geen uitspraken over wat de Consumentenbond over robotmaaiers zegt. Zoek je een '
         'Nederlandse test, kijk dan zelf op hun website of vraag het hen.</p>\n')
A_TOC_OUD = '<li><a href="#wat-vonden-we-bij-de-consumentenbond">Wat vonden we bij de Consumentenbond?</a></li>'
A_TOC_LAATSTE = '<li><a href="#zo-gebruik-je-een-test-samen-met-onze-ve">Zo gebruik je een test samen met onze vergelijking</a></li></ol></nav>'

# ---------------------------------------------------------------- C. mesjespagina
C1_WAS = 'Endurance 26,99 euro of Classic 22,99 euro (het aantal messen per verpakking is niet bevestigd)'
C1_WORDT = 'Endurance 26,99 euro voor 6 of Classic 22,99 euro voor 9'
RIJEN = [('Endurance', '6 messen', '26,99 euro', 'ongeveer 4,50 euro'), ('Endurance', '45 messen', '144,99 euro', 'ongeveer 3,22 euro'),
         ('Endurance', '300 messen', '849 euro', 'ongeveer 2,83 euro'), ('Classic', '9 messen', '22,99 euro', 'ongeveer 2,55 euro'),
         ('Classic', '45 messen', '94,99 euro', 'ongeveer 2,11 euro'), ('Classic', '300 messen', '579 euro', 'ongeveer 1,93 euro')]
C2_SECTIE = (
    '<h2 id="automower-messen-endurance-of-classic">Automower messen: Endurance of Classic?</h2>\n'
    '<p>Husqvarna verkoopt voor de Automower-modellen die wij bekeken twee veelgebruikte soorten messen: Endurance en Classic. De Endurance-messen '
    'hebben volgens Husqvarna een hardere, scherpere rand (4 snijkanten, 61 HRC) en gaan meer dan twee keer zo lang mee als klassieke messen. '
    'De Classic-messen zijn van gehard koolstofstaal met 2 snijkanten (58 HRC). Voor welk gebruik ze bedoeld zijn, noemt Husqvarna niet.</p>\n'
    '<div class="rmk-tablewrap"><table class="rmk-table"><thead><tr><th scope="col">Soort</th><th scope="col">Verpakking</th>'
    '<th scope="col">Prijs</th><th scope="col">Per mes (eigen berekening)</th></tr></thead><tbody>'
    + ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in RIJEN)
    + '</tbody></table></div>\n'
    '<p>Een grotere verpakking is per mes goedkoper. Per mes zijn Classic-messen goedkoper dan Endurance-messen. Gaan de Endurance-messen echt '
    'meer dan twee keer zo lang mee, zoals Husqvarna zegt, dan is Endurance per gebruiksperiode goedkoper: bij een verpakking van 6 ongeveer '
    '2,25 euro per vergelijkbare levensduur tegenover 2,55 euro voor Classic. Dat laatste is een rekenvoorbeeld op basis van de opgave van '
    'Husqvarna; wij hebben de levensduur niet zelf gemeten.</p>\n'
    '<p>Welke messen passen? De Automower 410VE NERA, 305E NERA, 310E NERA en 305 passen volgens Husqvarna NL alle vier op Endurance, Classic, '
    'Endurance HSS en Enhance HSS. Enhance HSS+ past op de 410VE NERA, 305E NERA en 310E NERA, maar niet op de 305. Voor de Enhance HSS-messen '
    'noemt Husqvarna als toepassing systematisch maaien of maaien zonder glijplaat. Controleer altijd de handleiding van jouw model.</p>\n')
C2_VOOR = '<h2 id="zo-houd-je-de-kosten-laag">Zo houd je de kosten laag</h2>'
C2_TOC = '<li><a href="#husqvarna-robotmaaier-mesjes">Husqvarna robotmaaier mesjes</a></li>'
C_BRON = ('<li><div><a href="https://www.husqvarna.com/hbd/tdrdownload/v2/pub000105498/doc000264944/OM/KO5PMFpHS7mEYGp-jHJrxxg0ETw">'
          'Husqvarna Automower 305E NERA: vervangtermijn messen</a><div class="rmk-sources__meta"><span class="rmk-chip">Handleiding</span>'
          '<span>geraadpleegd op 17 oktober 2026</span></div></div></li>')
C3_WAS = 'De mesjes van Gardena en van andere Husqvarna-modellen dan de 410VE NERA, 305E NERA en 310E NERA: die hebben we nog niet uitgezocht.'
C3_WORDT = 'De mesjes van Gardena en van andere Husqvarna-modellen dan de 410VE NERA, 305E NERA, 310E NERA en 305: die hebben we nog niet uitgezocht.'

STAPPEN = [
    (13, A_ZIN, A_ZIN + ' Websites en nieuwsberichten verwijzen soms naar een robotmaaiertest van de Consumentenbond; wat daar precies in staat '
     'en hoe actueel het is, kunnen we niet nagaan.', 'A1 zin toegevoegd'),
    (13, A_OUD, '', 'A2 oude sectie weg (kop en alinea)'),
    (13, A_TOC_OUD, '', 'A2 inhoudsopgave: link naar de oude kop weg'),
    (13, A_TOC_LAATSTE, A_TOC_LAATSTE.replace('</ol></nav>', '<li><a href="#wat-is-de-beste-robotmaaier-volgens-de-c">Wat is de beste '
     'robotmaaier volgens de Consumentenbond?</a></li></ol></nav>'), 'A2 inhoudsopgave: nieuwe kop achteraan'),
    (10, 'Robotmaaier test</a>: wat Test-Aankoop en Stiftung Warentest publiek hebben.',
     'Robotmaaier test</a>: wat de Consumentenbond, Test-Aankoop en Stiftung Warentest publiek hebben.', 'B Meer lezen'),
    (236, C1_WAS, C1_WORDT, 'C1 tabelrij 305E/310E NERA'),
    (236, C2_VOOR, C2_SECTIE + C2_VOOR, 'C2 nieuwe sectie'),
    (236, C2_TOC, C2_TOC + '<li><a href="#automower-messen-endurance-of-classic">Automower messen: Endurance of Classic?</a></li>', 'C2 inhoudsopgave'),
    (236, C_BRON, C_BRON + BRONNEN, f'C2 bronnen ({len(urls)} regels)'),
    (236, C3_WAS, C3_WORDT, 'C3 Wat we nog niet weten'),
    (20, 'Meer lees je op <a href="/robotmaaier-mesjes/">robotmaaier mesjes</a>.',
     f'Het verschil tussen Endurance en Classic lees je bij <a href="{MES}">Automower messen</a> op robotmaaier mesjes.', 'D FAQ'),
]

ids = sorted({s[0] for s in STAPPEN})
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
if any(f'href="{html.escape(u)}"' in raw[236] for u in urls):  # exact adres (de 305E NERA-regels hebben ?fits-to=…)
    meld.append('#236: een van de nieuwe bronadressen staat al in de bronnenlijst.')
for pid, was, wordt, wat in STAPPEN:
    n = raw[pid].count(was)
    if n != 1:
        meld.append(f'#{pid} {wat}: "Was"-tekst {n} keer gevonden (verwacht 1).')
    else:
        raw[pid] = raw[pid].replace(was, wordt, 1)
        print(f'  #{pid} {wat}')
assert 'Heeft de Consumentenbond een robotmaaier test?' in raw[13]
assert 'wat-vonden-we-bij-de-consumentenbond' not in raw[13]
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde50-teksten-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
