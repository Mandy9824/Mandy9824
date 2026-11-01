#!/usr/bin/env node
// Ronde 87: controle van de gepubliceerde pagina /husqvarna-robotmaaier/ (openbaar adres, na rmk.js), 390 en 1440 px.
// Meldt: HTTP-status, horizontale scroll, JavaScript-fouten, "[", "]", "{", "}", invulvelden, ankers die niet bestaan,
// verzoeken naar winkels, kaarten met score en prijsregels; daarna de interne links (HTTP-status).
// Gebruik:  node scripts/ronde87_controle.js [adres]
const { chromium } = require('playwright');
const URL = process.argv[2] || 'https://robotmaaierkompas.nl/husqvarna-robotmaaier/';
(async () => {
  const browser = await chromium.launch();
  let links = null, fout = 0;
  for (const breedte of [390, 1440]) {
    const page = await browser.newPage({ viewport: { width: breedte, height: 900 } });
    const js = [], winkels = [];
    page.on('pageerror', e => js.push(String(e)));
    page.on('console', m => { if (m.type() === 'error' && !/s-bol\.com/.test(m.text())) js.push(m.text()); });
    await page.route('**/*', r => { const u = r.request().url(); if (/bol\.com|awin|coolblue|amazon/.test(u)) { winkels.push(u); return r.abort(); } return r.continue(); });
    const resp = await page.goto(URL + '?nocache=' + Date.now(), { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);
    const r = await page.evaluate(() => {
      const main = document.querySelector('main');
      main.querySelectorAll('details').forEach(d => d.open = true);
      const t = main.innerText;
      const ankers = [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.getElementById(h.slice(1)));
      const kaarten = [...main.querySelectorAll('article.rmk-product')].map(a => ({
        titel: a.querySelector('h3').innerText.trim(),
        score: (a.querySelector('[data-out="total"]') || {}).innerText,
        prijs: [...a.querySelectorAll('.rmk-offers a')].map(x => x.innerText.trim() + ' -> ' + x.href),
      }));
      return {
        scroll: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        haken: (t.match(/[\[\]{}]/g) || []).length,
        invul: main.querySelectorAll('input, select, textarea').length,
        ankers, kaarten,
        links: [...new Set([...main.querySelectorAll('a[href]')].map(a => a.href).filter(h => h.startsWith(location.origin)).map(h => h.split('#')[0]))],
      };
    });
    const ok = resp.status() === 200 && r.scroll <= 0 && !js.length && !r.haken && !r.invul && !r.ankers.length && !winkels.length;
    if (!ok) fout++;
    console.log(`${breedte} px: HTTP ${resp.status()}, horizontale scroll ${r.scroll} px, JS-fouten ${js.length}${js.length ? ' ' + JSON.stringify(js) : ''}, ` +
      `haken/accolades ${r.haken}, invulvelden ${r.invul}, dode ankers ${JSON.stringify(r.ankers)}, winkelverzoeken ${winkels.length}`);
    if (breedte === 1440) { r.kaarten.forEach(k => console.log(`  ${k.titel}: ${k.score} | ${k.prijs.join(' ; ')}`)); links = r.links; }
    await page.close();
  }
  const ctx = await browser.newContext();
  for (const l of links) {
    const s = (await ctx.request.get(l, { maxRedirects: 0 })).status();
    if (s !== 200) fout++;
    console.log(`  ${s} ${l}`);
  }
  await browser.close();
  console.log(fout ? `${fout} fouten` : 'Geen fouten.');
  process.exit(fout ? 1 : 0);
})();
