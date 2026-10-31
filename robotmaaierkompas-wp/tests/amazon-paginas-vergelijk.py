#!/usr/bin/env python3
"""Vergelijkt de uitvoer van tests/amazon-paginas.php (ronde 74): 1.3.12 tegen 1.3.13.
Gebruik: python3 -I tests/amazon-paginas-vergelijk.py <map met r-oud-live.json, r-oud.json, r-zonder-live.json, r-zonder.json, r-uit.json, r-aan.json> <modellen.json>
Controleert: zonder constanten en zonder schakelaar byte voor byte gelijk; met schakelaar alleen Amazon-regels erbij,
op de juiste kaarten, onder Bol en Coolblue, met de exacte link; scores, volgorde en Bol-/Coolblue-regels gelijk."""
import json, re, sys

D, MOD = sys.argv[1], sys.argv[2]
r = {n: json.load(open(f'{D}/r-{n}.json', encoding='utf-8')) for n in ('oud-live', 'oud', 'zonder-live', 'zonder', 'uit', 'aan')}
mod = {m['id']: m for m in json.load(open(MOD, encoding='utf-8'))['modellen']}
slug = {'p-' + m['slug']: i for i, m in mod.items()}
KNOP = {i for i, m in mod.items() if m.get('amazon', {}).get('knop') and i != 'M050'}
fout = 0


def t(naam, ok, info=''):
    global fout
    print(('OK   ' if ok else 'FOUT ') + naam + (f'\n       {info}' if info and not ok else ''))
    fout += 0 if ok else 1


AM = re.compile(r'<div class="rmk-offer rmk-offer--stack rmk-offer--amazon" data-rmk-amazon="(M\d+)">'
                r'<a class="rmk-btn rmk-btn--primary" href="([^"]*)" rel="sponsored nofollow">Bekijk bij Amazon</a>'
                r'<span class="rmk-offer__src">Je gaat naar Amazon\.nl\. Prijs, beschikbaarheid en verkoper bekijk je daar\.</span></div>')

for n in ('oud', 'zonder-live', 'zonder', 'uit', 'aan'):
    t(f'{n}: geen HTTP-verzoeken', r[n]['verzoeken'] == [])
t('1.3.12: modelgegevens met blok amazon geven dezelfde pagina\'s als zonder', r['oud']['paginas'] == r['oud-live']['paginas'])
t('1.3.13 zonder Amazon-constanten, huidige live modelgegevens: alle pagina\'s byte voor byte gelijk aan 1.3.12', r['zonder-live']['paginas'] == r['oud-live']['paginas'])
t('1.3.13 zonder Amazon-constanten, met blok amazon: byte voor byte gelijk', r['zonder']['paginas'] == r['oud']['paginas'])
t('1.3.13 met RMK_AMAZON_TAG maar zonder schakelaar: byte voor byte gelijk', r['uit']['paginas'] == r['oud']['paginas'])
t('zonder schakelaar nergens "amazon" in de kaarten', not any('rmk-offer--amazon' in h for h in r['uit']['paginas'].values()))

oud, aan = r['oud']['paginas'], r['aan']['paginas']
totaal, per = 0, {}
for s in oud:
    a, o = aan[s], oud[s]
    regels = AM.findall(a)
    AF = re.compile(r'<p class="rmk-affnote".*?</p>', re.S)
    # De advertentie-regel staat boven de eerste knop (Bol, Coolblue of Amazon); is dat nu een Amazon-knop, dan schuift
    # hij omhoog of komt hij erbij (pagina zonder Bol en Coolblue). Verder mag er niets veranderen.
    t(f'{s}: alleen de Amazon-regels erbij ({len(regels)}), verder gelijk', AF.sub('', AM.sub('', a)) == AF.sub('', o))
    eerste = min([i for i in (a.find('data-rmk-bol'), a.find('data-rmk-cb'), a.find('data-rmk-amazon')) if i >= 0], default=-1)
    if eerste >= 0:
        art = a.rfind('<article', 0, eerste)
        t(f'{s}: advertentie-regel één keer, direct boven de kaart met de eerste knop',
          len(AF.findall(a)) == 1 and a.find('rmk-affnote') < eerste and a.find('rmk-affnote') > a.rfind('</article>', 0, art)
          and AF.findall(a) == (AF.findall(o) or AF.findall(a)))
    arts_o = re.findall(r'<article class="rmk-product" aria-labelledby="([^"]+)".*?</article>', o, re.S)
    arts = re.findall(r'<article class="rmk-product" aria-labelledby="([^"]+)"(.*?)</article>', a, re.S)
    t(f'{s}: volgorde van de kaarten gelijk', arts_o == [x[0] for x in arts])
    for lab, body in arts:
        mid = slug.get(lab)
        m = AM.search(body)
        if mid in KNOP:
            t(f'{s} {mid}: Amazon-knop', bool(m))
            if not m:
                continue
            t(f'{s} {mid}: link exact https://www.amazon.nl/dp/{mod[mid]["amazon"]["asin"]}?tag=robotmaaier-21',
              m.group(2) == f'https://www.amazon.nl/dp/{mod[mid]["amazon"]["asin"]}?tag=robotmaaier-21' and m.group(1) == mid, m.group(2))
            na = body[m.end():]
            t(f'{s} {mid}: Amazon-regel is de laatste regel (onder Bol en Coolblue)', 'rmk-offer' not in na and body.count('rmk-offer--amazon') == 1)
            per.setdefault(s, []).append(mid)
            totaal += 1
        else:
            t(f'{s} {mid}: geen Amazon-knop' + (' (M050 uitgesloten)' if mid == 'M050' else ''), not m)
    sc = lambda h: re.findall(r'data-total="([^"]*)"|<b data-out="total">([^<]*)</b>', h)
    t(f'{s}: scores gelijk', sc(a) == sc(o))
    bc = lambda h: re.findall(r'<div class="rmk-offer rmk-offer--stack rmk-offer--(?:bol|coolblue)".*?</div>', h, re.S)
    t(f'{s}: Bol- en Coolblue-regels gelijk', bc(a) == bc(o))
print('\nAmazon-knoppen per pagina:', json.dumps(per), '\nTotaal', totaal)
print('\n' + (f'{fout} FOUT(EN)' if fout else 'Alles geslaagd'))
sys.exit(1 if fout else 0)
