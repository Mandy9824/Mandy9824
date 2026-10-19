#!/usr/bin/env python3
"""Ronde 49 (zonder thema-zip): twee tekstwijzigingen rond de testpagina.
1. Testpagina (#13): direct vóór de veelgestelde vragen (aan het einde van de tekst, na de lijst onder
   "Zo gebruik je een test samen met onze vergelijking") de H2 "Wat is de beste robotmaaier volgens de Consumentenbond?"
   met een alinea; "beste robotmaaier" linkt naar /beste-robotmaaier/.
2. Pagina 1 (#11), onder "De nadelen van een robotmaaier zonder draad", na de opsomming: één zin met
   "robotmaaier test" als link naar /robotmaaier-test-consumentenbond/.
Elk anker moet precies één keer voorkomen; anders schrijft het script niets. Pagina's houden hun status.
Met --schrijf: kopie in backups/, opslaan, LiteSpeed legen via de dataroute (modelgegevens ongewijzigd).
Gebruik:  python3 scripts/ronde49_teksten.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
TEST_EIND = '<li><strong>Let op de modellen:</strong> fabrikanten brengen vaak varianten uit. Een test van een model zegt niet altijd iets over een opvolger.</li></ol>'
TEST_NIEUW = ('<h2 id="wat-is-de-beste-robotmaaier-volgens-de-c">Wat is de beste robotmaaier volgens de Consumentenbond?</h2>\n'
              '<p>Op 5 oktober 2026 konden we op consumentenbond.nl geen robotmaaiertest vinden, alleen tests van gewone grasmaaiers. '
              'Een beste robotmaaier volgens de Consumentenbond kunnen we dus niet noemen. Wat wel openbaar is: Test-Aankoop publiceerde '
              'in 2026 een test van een dertigtal robotmaaiers, met aparte rangschikkingen voor draadloos en met draad, en de Stiftung '
              'Warentest test 14 modellen. Wil je onze eigen keuze per tuinsituatie, met specificaties en kosten, kijk dan op '
              '<a href="/beste-robotmaaier/">beste robotmaaier</a>.</p>')
NADEEL_EIND = ('<li><strong>Willekeurig of systematisch:</strong> niet elke maaier maait in rijen. Dat is niet altijd zichtbaar in de '
               'specificaties.</li></ul>')
NADEEL_NIEUW = ('<p>Wil je ook weten wat laboratoria meten? Lees dan wat de Consumentenbond, Test-Aankoop en de Stiftung Warentest '
                'publiceren op <a href="/robotmaaier-test-consumentenbond/">robotmaaier test</a>.</p>')
STAPPEN = [
    (13, TEST_EIND, TEST_EIND + '\n' + TEST_NIEUW, 'testpagina, vóór de FAQ', 'Wat is de beste robotmaaier volgens de Consumentenbond?'),
    (11, '<h2>De nadelen van een robotmaaier zonder draad</h2>\n<ul>', None, 'pagina 1, kopje nadelen', None),
    (11, NADEEL_EIND, NADEEL_EIND + '\n' + NADEEL_NIEUW, 'pagina 1, na de opsomming nadelen', 'Wil je ook weten wat laboratoria meten?'),
]

ids = sorted({s[0] for s in STAPPEN})
pag = {pid: api(f'wp/v2/pages/{pid}?context=edit') for pid in ids}
raw = {pid: p['content']['raw'] for pid, p in pag.items()}
meld = []
for pid, was, wordt, wat, kenmerk in STAPPEN:
    if kenmerk and kenmerk in raw[pid]:
        meld.append(f'#{pid} {wat}: tekst staat er al.')
    elif raw[pid].count(was) != 1:
        meld.append(f'#{pid} {wat}: anker {raw[pid].count(was)} keer gevonden (verwacht 1).')
    elif wordt is None:
        print(f'  #{pid} {wat}: gevonden (precies deze kop, direct gevolgd door de opsomming)')
    else:
        raw[pid] = raw[pid].replace(was, wordt, 1)
        print(f'  #{pid} {wat}: toegevoegd')
print('\nMeldingen:' if meld else '\nGeen meldingen.')
for m in meld:
    print('  - ' + m)
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde49-teksten-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({str(pid): {'status': p['status'], 'content': p['content']['raw']} for pid, p in pag.items()}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
for pid in ids:
    api(f'wp/v2/pages/{pid}', {'content': raw[pid]})
    q = api(f'wp/v2/pages/{pid}?context=edit')
    print(f'#{pid} opgeslagen; status {q["status"]} (was {pag[pid]["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == raw[pid]}')
print('LiteSpeed legen via de dataroute (modelgegevens ongewijzigd):', api('rmk/v1/modellen', api('rmk/v1/modellen')['data']))
print('Leeg daarna ook de CDN-cache (hPanel > Prestaties > CDN).')
