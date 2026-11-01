#!/usr/bin/env node
// Ronde 82 (van ronde 71): controle van het concept robotmaaier-grote-tuin (#15) zonder in te loggen in de browser.
// De weergegeven inhoud (REST, content.rendered, ingelogd opgehaald) wordt in de omhulling van de hub (/beste-robotmaaier/)
// gezet en op een proefadres op het eigen domein geladen, zodat CSS en rmk.js van de site gewoon laden.
// Gebruik:  node scripts/ronde71_controle.js <concept.json> <hub.html> <uit-tekst.md>
// Meldt per breedte (390 en 1440 px): horizontale scroll, JavaScript-fouten, "[", "]", "{", "}", invulvelden,
// ankers die niet bestaan, verzoeken naar winkels; daarna de interne links en de volledige tekst (FAQ opengeklapt).
const fs = require('fs');
const { chromium } = require('playwright');
const [conceptPad, hubPad, uitPad] = process.argv.slice(2);
const concept = JSON.parse(fs.readFileSync(conceptPad));
const hub = fs.readFileSync(hubPad, 'utf8');
const begin = hub.indexOf('<main'), eind = hub.indexOf('</main>') + 7;
const html = hub.slice(0, begin) + concept.rendered + hub.slice(eind);
const PROEF = 'https://robotmaaierkompas.nl/__proef-grote-tuin__/';

(async () => {
  const browser = await chromium.launch();
  let tekst = null, links = null, fout = 0;
  for (const breedte of [390, 1440]) {
    const page = await browser.newPage({ viewport: { width: breedte, height: 900 } });
    const jsFouten = [], winkels = [];
    page.on('pageerror', e => jsFouten.push(String(e)));
    page.on('console', m => { if (m.type() === 'error' && !/s-bol\.com/.test(m.text())) jsFouten.push(m.text()); });
    await page.route('**/*', r => {
      const u = r.request().url();
      if (u.startsWith(PROEF)) return r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: html });
      if (/bol\.com|awin|coolblue|amazon/.test(u)) { winkels.push(u); return r.abort(); }
      return r.continue();
    });
    await page.goto(PROEF, { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);
    const r = await page.evaluate(() => {
      const main = document.querySelector('main');
      main.querySelectorAll('details').forEach(d => d.open = true);
      const doc = document.documentElement;
      const t = main.innerText;
      const ankers = [...main.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.getElementById(h.slice(1)));
      const breed = [...main.querySelectorAll('*')].filter(e => e.getBoundingClientRect().right > doc.clientWidth + 1 && !e.closest('.rmk-tablewrap')).map(e => e.tagName + '.' + e.className).slice(0, 5);
      const tabel = [...main.querySelectorAll('.rmk-tablewrap')].map(w => `${w.scrollWidth} px in ${w.clientWidth} px`);
      const kaarten = [...main.querySelectorAll('article.rmk-product')].map(a => a.getAttribute('aria-labelledby') + ' ' + ((a.querySelector('[data-out="total"]') || {}).textContent || '').trim());
      const intern = [...new Set([...main.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => h.startsWith('/') || h.startsWith('https://robotmaaierkompas.nl')))];
      return { scroll: doc.scrollWidth > doc.clientWidth, sw: doc.scrollWidth, cw: doc.clientWidth, haken: (t.match(/[\[\]{}]/g) || []).length,
               invul: main.querySelectorAll('input, select, textarea').length, ankers, breed, tabel, kaarten, intern, t };
    });
    console.log(`${breedte} px: horizontale scroll ${r.scroll} (${r.sw}/${r.cw}), JS-fouten ${jsFouten.length}${jsFouten.length ? ' ' + JSON.stringify(jsFouten.slice(0, 3)) : ''}, ` +
      `[]{}: ${r.haken}, invulvelden ${r.invul}, ontbrekende ankers ${JSON.stringify(r.ankers)}, te brede elementen ${JSON.stringify(r.breed)}, ` +
      `tabellen ${JSON.stringify(r.tabel)}, verzoeken naar winkels ${winkels.length}`);
    console.log(`  kaarten: ${r.kaarten.join(' · ')}`);
    fout += (r.scroll ? 1 : 0) + jsFouten.length + r.haken + r.invul + r.ankers.length + winkels.length;
    tekst = r.t; links = r.intern;
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(uitPad, tekst);
  fs.writeFileSync(uitPad + '.links.json', JSON.stringify(links));
  console.log(`Interne links: ${links.join(' ')}`);
  console.log(fout ? `${fout} problemen` : 'Geen problemen.');
})();
