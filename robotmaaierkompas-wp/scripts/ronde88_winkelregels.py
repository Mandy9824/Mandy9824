#!/usr/bin/env python3
"""Ronde 88: Coolblue- en Amazon-regels per kaart op alle openbare adressen tegen de schakelaars en prijstaken.
Coolblue-regel alleen als /rmk/v1/coolblue-status het model op_de_site noemt; Amazon-regel alleen bij amazon.knop true,
href exact https://www.amazon.nl/dp/<ASIN>?tag=robotmaaier-21 met rel="sponsored nofollow". Bol: zie bol_regel_controle.py.
Alleen lezen, volgt geen links. Gebruik:  python3 scripts/ronde88_winkelregels.py <adres> [<adres> ...]"""
import re, sys, os, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import api
cb = api('rmk/v1/coolblue-status')['modellen']
mod = {m['slug']: m for m in api('rmk/v1/modellen')['data']['modellen']}
fout = n = 0
for u in sys.argv[1:]:
    h = urllib.request.urlopen(urllib.request.Request(u + '?n=x', headers={'User-Agent': 'Mozilla/5.0 rmk-controle', 'Cache-Control': 'no-cache'}), timeout=60).read().decode()
    for a in re.finditer(r'<article class="rmk-product" aria-labelledby="p-([^"]+)">(.*?)</article>', h, re.S):
        m = mod[a.group(1)]; seg = a.group(2); n += 1
        heeft_cb = 'awin1.com' in seg
        moet_cb = bool(cb.get(m['id'], {}).get('op_de_site'))
        am = re.findall(r'<a[^>]+href="(https://www\.amazon\.nl/[^"]+)"[^>]*>', seg)
        moet_am = bool((m.get('amazon') or {}).get('knop'))
        ok_am = (not am and not moet_am) or (moet_am and am == [f'https://www.amazon.nl/dp/{m["amazon"]["asin"]}?tag=robotmaaier-21']
                                             and re.search(r'href="https://www\.amazon\.nl/[^"]+"[^>]*rel="sponsored nofollow"|rel="sponsored nofollow"[^>]*href="https://www\.amazon\.nl/', seg))
        if heeft_cb != moet_cb or not ok_am:
            fout += 1
            print(f'FOUT {u} {m["id"]}: coolblue {heeft_cb} (verwacht {moet_cb}), amazon {am} (knop {moet_am})')
print(f'{n} kaarten nagelopen, {fout} fouten')
