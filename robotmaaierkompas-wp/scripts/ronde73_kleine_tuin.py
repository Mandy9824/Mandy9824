#!/usr/bin/env python3
"""Ronde 73: vier tekstwijzigingen op de gepubliceerde pagina /robotmaaier-kleine-tuin/ (#16), met de hand (opdracht Mandy).
Niet uit pagina-robotmaaier-kleine-tuin.md opnieuw te bouwen: ronde71_bouw.py zou deze wijzigingen (en de links van
ronde 72) weghalen. Elke oude tekst moet precies één keer voorkomen (en in het juiste lijstpunt of de juiste tabelrij);
anders schrijft het script niets. Status, slug, titel en meta blijven gelijk.
(a) Betrouwbaarheid: "De Roborock Q105 heeft nog helemaal geen reviews." -> zin over zeven van de twaalf modellen.
(b) "95 tot 239 euro" -> "94,99 tot 239 euro".
(c) 4G en GPS: losse module ook bij de Worx WR303E (149 euro).
(d) Keuzetabel, rij "Tuin tot 500 m² met hellingen tot 45%": Stihl iMOW 3 EVO (met draad) erbij.
Met --schrijf: kopie in backups/, opslaan, controle; LiteSpeed legen gebeurt via de dataroute (ronde73_modellen.py).
Gebruik:  python3 scripts/ronde73_kleine_tuin.py [--schrijf]
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

SCHRIJF = '--schrijf' in sys.argv
PID = 16
RIJ = '<th scope="row">Tuin tot 500 m² met hellingen tot 45%</th>'
STAPPEN = [  # (naam, oud, nieuw, context die het omringende lijstpunt/de rij moet bevatten)
    ('a', 'De Roborock Q105 heeft nog helemaal geen reviews.',
     'Voor zeven van de twaalf modellen hebben we geen reviews gevonden, waaronder de Roborock Q105 en de Stihl iMOW 3 EVO.',
     '<strong>Betrouwbaarheid:</strong>'),
    ('b', '95 tot 239 euro', '94,99 tot 239 euro', '<strong>Draad of geen draad:</strong>'),
    ('c', 'bij de Roborock Q105, Mova ViAX en Eufy C15 is het een losse module',
     'bij de Roborock Q105, Mova ViAX, Eufy C15 en Worx WR303E (149 euro) is het een losse module', '<strong>4G en GPS:</strong>'),
    ('d', RIJ + '<td>Navimow i205 AWD of Roborock RockNeo Q105</td>',
     RIJ + '<td>Navimow i205 AWD of Roborock RockNeo Q105 (zonder draad), of Stihl iMOW 3 EVO (met draad)</td>', None),
]

p = api(f'wp/v2/pages/{PID}?context=edit')
assert p['slug'] == 'robotmaaier-kleine-tuin', p['slug']
raw = p['content']['raw']
nieuw, meld = raw, []
for naam, oud, nw, ctx in STAPPEN:
    n = nieuw.count(oud)
    if n != 1:
        meld.append(f'({naam}) "{oud[:60]}" {n} keer gevonden (verwacht 1).')
        continue
    if ctx:
        li = re.search(r'<li>((?:(?!</li>).)*' + re.escape(oud) + r'.*?)</li>', nieuw, re.S)
        if not li or not li.group(1).startswith(ctx):
            meld.append(f'({naam}) staat niet in het lijstpunt dat begint met {ctx}.')
            continue
    if nieuw.count(nw) or (naam != 'd' and nw in raw):
        meld.append(f'({naam}) nieuwe tekst staat er al.')
        continue
    nieuw = nieuw.replace(oud, nw, 1)
    print(f'({naam}) vervangen')
print('Meldingen:\n  - ' + '\n  - '.join(meld) if meld else 'Geen meldingen.')
if not SCHRIJF:
    sys.exit(0)
if meld:
    sys.exit('Niets geschreven vanwege de meldingen.')
os.makedirs('backups', exist_ok=True)
pad = f'backups/ronde73-pagina16-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
json.dump({k: p[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta')}, open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', pad)
api(f'wp/v2/pages/{PID}', {'content': nieuw})
q = api(f'wp/v2/pages/{PID}?context=edit')
print(f'#{PID} opgeslagen; status {q["status"]} (was {p["status"]}); inhoud zoals bedoeld: {q["content"]["raw"] == nieuw}; '
      f'titel/slug/meta gelijk: {(q["title"]["raw"], q["slug"], q["meta"]) == (p["title"]["raw"], p["slug"], p["meta"])}')
