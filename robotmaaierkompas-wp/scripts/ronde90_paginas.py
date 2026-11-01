#!/usr/bin/env python3
"""Ronde 90: drie gerichte wijzigingen (MET DE HAND; niets bouwen), kopie vooraf per pagina (scripts/ronde88_lib.py).
1. Pagina 1 (#11): kaart M070 (450V NERA) direct na de kaart M069 (430V NERA).
2. Grote tuin (#15): "elf robotmaaiers ..." -> "veertien ..." in het korte antwoord ("zeven zonder score" stond er al).
3. Gardena (#21): korte antwoord, max 1200 en de smart Gateway.
Gebruik:  python3 scripts/ronde90_paginas.py [--schrijf]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ronde88_lib import pas_toe
from affiliate_teksten_lib import api
SCHRIJF = '--schrijf' in sys.argv
r11 = api('wp/v2/pages/11?context=edit')['content']['raw']
def kaartgroep(slug):
    """Het hele groepsblok van een kaart op pagina 1, inclusief de voorafgaande lege regel."""
    m = list(re.finditer(r'\n\n<!-- wp:group \{"className":"rmk-container rmk-block rmk-column","layout":\{"type":"default"\}\} -->\n'
                         r'<div class="wp-block-group rmk-container rmk-block rmk-column"><!-- wp:html -->\n<!-- wp:html -->\n'
                         r'<article class="rmk-product" aria-labelledby="p-' + re.escape(slug) + r'">.*?<!-- /wp:group -->', r11, re.S))
    assert len(m) == 1, f'{slug}: {len(m)} keer'
    return m[0].group(0)
k69, k70 = kaartgroep('husqvarna-automower-430v-nera'), kaartgroep('husqvarna-automower-450v-nera')
assert k69.count('<article') == 1 and k70.count('<article') == 1
STAPPEN = {
    11: [(k70, '', '1 kaart M070 weg na de i205'), (k69, k69 + k70, '1 kaart M070 na M069')],
    15: [('elf robotmaaiers zonder draad die nu nieuw te koop zijn en een score hebben',
          'veertien robotmaaiers zonder draad die nu nieuw te koop zijn en een score hebben', '2 korte antwoord')],
    21: [('kaart, zones en GPS alleen met een losse smart Gateway', 'kaart en zones alleen met een losse smart Gateway; GPS heeft hij ook dan niet', '3 korte antwoord')],
}
for pid, st in STAPPEN.items():
    print(f'\n=== #{pid}')
    raw, _ = pas_toe(pid, st, SCHRIJF, 'r90')
    if pid == 11:
        print('  kaartvolgorde:', re.findall(r'<article class="rmk-product" aria-labelledby="p-([^"]+)"', raw)[:6])
