#!/usr/bin/env python3
"""Ronde 69: drie tekstwijzigingen op de gepubliceerde pagina /mova-dreame-robotmaaier/ (#351).

Elke oude tekst moet precies één keer in de ruwe inhoud staan (en de nieuwe nog niet); anders meldt het script dat en
schrijft het niets. Garantie letterlijk uit het blad Bronnen/Modellen (M059, M060, M064 gelijk; M063 zonder LiDAR).
Status, slug, titel en meta blijven gelijk. Kopie vooraf in backups/. Wachtwoord alleen uit RMK_WP_APP_PASSWORD.
Gebruik:  python3 scripts/ronde69_mova_tekst.py [--schrijf]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api

PID = 351
G = '3 jaar hoofdeenheid, laadstation, adapter en motoren; 2 jaar accu en LiDAR; messen geen garantie (Mova aftersales-beleid NL)'
G63 = '3 jaar hoofdeenheid, laadstation, adapter en motoren; 2 jaar accu; messen geen garantie (Mova aftersales-beleid NL)'
STAPPEN = [
    ('Garantie', 'Voor de andere modellen hebben we dat niet gecontroleerd.',
     f'Bij de LiDAX Ultra 1600, de LiDAX Ultra 1000 AWD en de ViAX 500: {G}. Bij de ViAX 250: {G63}.'),
    ('Wat we nog niet weten', 'Alleen de ViAX 500 heeft onafhankelijke reviews; de reviews op Amazon komen uit meerdere landen en tellen niet mee.',
     'De ViAX 500 (6 reviews bij Coolblue) en de LiDAX Ultra 800 (5 bij MediaMarkt NL) hebben onafhankelijke reviews; de reviews op Amazon komen uit meerdere landen en tellen niet mee.'),
    ('Het korte antwoord', 'Mova verkoopt in Nederland acht robotmaaiers', 'Mova verkoopt in Nederland minstens acht robotmaaiers'),
]
p = api(f'wp/v2/pages/{PID}?context=edit')
raw = p['content']['raw']
meld = []
for wat, oud, nieuw in STAPPEN:
    n = raw.count(oud)
    if n != 1:
        meld.append(f'{wat}: oude tekst {n} keer gevonden (verwacht 1)')
    elif nieuw in raw:
        meld.append(f'{wat}: nieuwe tekst staat er al')
    else:
        raw = raw.replace(oud, nieuw, 1)
        print(f'{wat}: vervangen')
if meld:
    sys.exit('Meldingen, niets gewijzigd:\n  ' + '\n  '.join(meld))
if '--schrijf' not in sys.argv:
    sys.exit(0)
os.makedirs('backups', exist_ok=True)
fn = time.strftime(f'backups/ronde69-tekst-pagina{PID}-voor-%Y%m%d-%H%M%S.json')
json.dump({k: p[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta', 'modified')}, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Kopie:', fn)
api(f'wp/v2/pages/{PID}', {'content': raw})
q = api(f'wp/v2/pages/{PID}?context=edit')
print('status', q['status'], 'slug', q['slug'], '| inhoud zoals bedoeld:', q['content']['raw'] == raw,
      '| titel en meta gelijk:', q['title']['raw'] == p['title']['raw'] and q['meta'] == p['meta'])
