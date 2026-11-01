"""Ronde 88: gedeelde hulp voor gerichte vervangingen op gepubliceerde pagina's (MET DE HAND; niets bouwen).
pas_toe(pid, stappen, schrijf, naam, meta=None): kopie vooraf in backups/, elke zoektekst moet precies één keer voorkomen
(anders schrijft hij niets), status blijft gelijk. stappen: lijst van (zoek, vervang, omschrijving).
meta: optioneel {sleutel: (was, wordt)} voor Yoast-velden; titel: optioneel (was, wordt).
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api


def pas_toe(pid, stappen, schrijf, naam, meta=None, titel=None):
    p = api(f'wp/v2/pages/{pid}?context=edit')
    os.makedirs('backups', exist_ok=True)
    pad = f'backups/{"" if naam.startswith(("r89", "r90")) else "ronde88-"}{naam}-pagina{pid}-voor-{time.strftime("%Y%m%d-%H%M%S")}.json'
    json.dump({k: p[k] for k in ('id', 'status', 'slug', 'parent', 'title', 'content', 'meta', 'modified')},
              open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'#{pid} {p["slug"]} ({p["status"]}, gewijzigd {p["modified"]}); kopie: {pad}')
    raw = p['content']['raw']
    meld = []
    for zoek, vervang, wat in stappen:
        n = raw.count(zoek)
        if n != 1:
            meld.append(f'{wat}: {n} keer gevonden (verwacht 1).')
        else:
            raw = raw.replace(zoek, vervang)
            print(f'  {wat}: ok')
    nieuw_meta = {}
    for k, (was, wordt) in (meta or {}).items():
        if p['meta'].get(k) != was:
            meld.append(f'meta {k}: is {p["meta"].get(k)!r}, verwacht {was!r}.')
        else:
            nieuw_meta[k] = wordt
            print(f'  meta {k}: ok')
    if titel:
        if p['title']['raw'] != titel[0]:
            meld.append(f'titel: is {p["title"]["raw"]!r}, verwacht {titel[0]!r}.')
        else:
            print('  titel: ok')
    print('  Meldingen:' if meld else '  Geen meldingen.')
    for m in meld:
        print('    - ' + m)
    if not schrijf:
        return raw, meld
    if meld:
        sys.exit('Niets geschreven vanwege de meldingen.')
    data = {'content': raw}
    if nieuw_meta:
        data['meta'] = nieuw_meta
    if titel:
        data['title'] = titel[1]
    api(f'wp/v2/pages/{pid}', data)
    q = api(f'wp/v2/pages/{pid}?context=edit')
    ok = q['content']['raw'] == raw and q['status'] == p['status'] and q['slug'] == p['slug'] and \
        all(q['meta'].get(k) == v for k, v in nieuw_meta.items()) and (not titel or q['title']['raw'] == titel[1])
    print(f'  #{pid} opgeslagen; status {q["status"]} (was {p["status"]}); zoals bedoeld: {ok}')
    if not ok:
        sys.exit('Live inhoud wijkt af van bedoeld.')
    return raw, meld
