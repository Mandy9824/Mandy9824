#!/usr/bin/env python3
"""Ronde 76: voettekst (aangepast template-onderdeel "footer") en het kopje "Versie en wijzigingen" op /hoe-we-beoordelen/ (#76).

1. Footer: "© robotmaaierkompas.nl · Scoremodel v1.0 (concept tot bevriezing)" wordt
   "© robotmaaierkompas.nl · Scoremodel v1.0 · <a href="/hoe-we-beoordelen/">Hoe we scoren</a>".
2. #76: na de sectie "Versies" een sectie "Versie en wijzigingen" met de tekst van Mandy (31-10-2026), en een regel in
   "Op deze pagina".
Elke zoektekst moet precies één keer voorkomen, anders schrijft het script niets. Met --schrijf eerst een volledige kopie
van #76 en de footer in backups/ (niet in git). Pagina's houden hun status.
Gebruik:  python3 scripts/ronde76_footer_methode.py                         (proefdraai)
          python3 scripts/ronde76_footer_methode.py --schrijf
          python3 scripts/ronde76_footer_methode.py --terug <kopie> --schrijf  (zet #76 en de footer terug uit de kopie)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

F_OUD = '<span>© robotmaaierkompas.nl · Scoremodel v1.0 (concept tot bevriezing)</span>'
F_NIEUW = '<span>© robotmaaierkompas.nl · Scoremodel v1.0 · <a href="/hoe-we-beoordelen/">Hoe we scoren</a></span>'
TOC_OUD = '<li><a href="#versies">Versies</a></li>'
TOC_NIEUW = TOC_OUD + '<li><a href="#versie-en-wijzigingen">Versie en wijzigingen</a></li>'
SECTIE = ('\n      <section id="versie-en-wijzigingen" class="rmk-prose" aria-labelledby="versie-en-wijzigingen-t">\n'
          '        <h2 id="versie-en-wijzigingen-t" style="margin-top: 0">Versie en wijzigingen</h2>\n'
          '        <p>Scoremodel v1.0 (oktober 2026): de eerste versie, met zeven onderdelen. Betrouwbaarheid en prijs-kwaliteit '
          'tellen mee zodra er genoeg reviews of prijzen zijn; tot dan noemen we de score een functiescore. Wijzigingen aan het '
          'scoremodel melden we hier met de datum.</p>\n      </section>')


def versies_einde(r):
    i = r.find('<section id="versies"')
    return -1 if i < 0 or r.count('<section id="versies"') != 1 else r.find('</section>', i) + len('</section>')


pag = api('wp/v2/pages/76?context=edit')
footer = [t for t in api('wp/v2/template-parts?context=edit&per_page=100') if t['slug'] == 'footer' and t['source'] == 'custom']
if len(footer) != 1:
    sys.exit(f'{len(footer)} aangepaste footers gevonden (verwacht 1). Niets gewijzigd.')
footer = footer[0]
r76, rf = pag['content']['raw'], footer['content']['raw']

if '--terug' in sys.argv:
    k = json.load(open(sys.argv[sys.argv.index('--terug') + 1], encoding='utf-8'))
    n76, nf, meld = k['76'], k['footer'], []
else:
    meld, n76, nf = [], r76, rf
    if F_NIEUW in rf:
        print('footer: al gedaan')
    elif rf.count(F_OUD) != 1:
        meld.append(f'footer: oude voettekst {rf.count(F_OUD)} keer gevonden (verwacht 1)')
    else:
        nf = rf.replace(F_OUD, F_NIEUW)
        print(f'footer:\n  was:   {F_OUD}\n  wordt: {F_NIEUW}')
    if 'id="versie-en-wijzigingen"' in r76:
        print('#76: al gedaan')
    else:
        e = versies_einde(r76)
        if e < 0:
            meld.append('#76: sectie "Versies" niet precies één keer gevonden')
        elif r76.count(TOC_OUD) != 1:
            meld.append(f'#76: inhoudsopgave-regel "Versies" {r76.count(TOC_OUD)} keer gevonden (verwacht 1)')
        else:
            n76 = r76[:e] + SECTIE + r76[e:]
            n76 = n76.replace(TOC_OUD, TOC_NIEUW)
            print('#76: sectie "Versie en wijzigingen" na "Versies", regel in "Op deze pagina"')
print('Meldingen: ' + '; '.join(meld) if meld else 'Geen meldingen.')
if '--schrijf' not in sys.argv or meld:
    sys.exit(1 if meld else 0)
os.makedirs('backups', exist_ok=True)
pad = f'backups/footer-methode-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({'76': r76, 'footer': rf, 'status76': pag['status']}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
if n76 != r76:
    api('wp/v2/pages/76', {'content': n76})
    q = api('wp/v2/pages/76?context=edit')
    print(f'#76 opgeslagen; status {q["status"]} (was {pag["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == n76}')
if nf != rf:
    api(f'wp/v2/template-parts/{footer["id"]}', {'content': nf})
    q = [t for t in api('wp/v2/template-parts?context=edit&per_page=100') if t['id'] == footer['id']][0]
    print(f'footer opgeslagen; inhoud zoals bedoeld: {q["content"]["raw"] == nf}')
