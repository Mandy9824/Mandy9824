#!/usr/bin/env node
// Momentopname van alle openbare pagina's (Chromium, na rmk.js): per adres de kaarten (data-model + getoonde score),
// de volgorde van alle data-model-elementen, winkel-links (bol/coolblue/amazon, zonder ze te volgen) en de zichtbare tekst.
// Gebruik:  node scripts/momentopname.js <uit.json> <adres> [<adres> ...]
// Vergelijk twee opnames:  node scripts/momentopname.js --vergelijk <a.json> <b.json>
const fs = require('fs');
const args = process.argv.slice(2);
if (args[0] === '--vergelijk') {
  const a = JSON.parse(fs.readFileSync(args[1])), b = JSON.parse(fs.readFileSync(args[2]));
  let fout = 0;
  for (const u of new Set([...Object.keys(a), ...Object.keys(b)])) {
    const x = a[u] || {}, y = b[u] || {};
    for (const k of ['kaarten', 'volgorde', 'winkels', 'tekst']) {
      if (JSON.stringify(x[k]) !== JSON.stringify(y[k])) {
        fout++;
        if (k === 'tekst') {
          const xs = new Set(x.tekst || []), ys = new Set(y.tekst || []);
          console.log(`${u} tekst: weg ${JSON.stringify([...xs].filter(t => !ys.has(t))).slice(0, 600)} | erbij ${JSON.stringify([...ys].filter(t => !xs.has(t))).slice(0, 600)}`);
        } else console.log(`${u} ${k}: ${JSON.stringify(x[k]).slice(0, 400)} -> ${JSON.stringify(y[k]).slice(0, 400)}`);
      }
    }
  }
  console.log(fout ? `${fout} verschillen` : 'Geen verschillen.');
  process.exit(fout ? 1 : 0);
}
const { chromium } = require('playwright');
(async () => {
  const [uit, ...adressen] = args;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.route(/(bol\.com|s-bol\.com|awin|coolblue|amazon)/, r => r.abort());
  const res = {};
  for (const u of adressen) {
    const resp = await page.goto(u + (u.includes('?') ? '&' : '?') + 'nocache=' + Date.now(), { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);
    res[u] = await page.evaluate(() => {
      const main = document.querySelector('main') || document.body;
      main.querySelectorAll('details').forEach(d => d.open = true);
      const kaarten = [...main.querySelectorAll('article.rmk-product')].map(a => {
        const c = { dataset: { model: a.getAttribute('aria-labelledby') } };
        return [c ? c.dataset.model : null, (a.querySelector('[data-out="total"], .rmk-minis b') || {}).textContent || null,
                (a.querySelector('[data-out="kind"], .rmk-minis small') || {}).textContent || null];
      });
      const volgorde = [...main.querySelectorAll('[data-model]')].map(e => e.dataset.model + ':' + ((e.querySelector('b') || {}).textContent || '').trim());
      const winkels = [...main.querySelectorAll('a[href]')].map(a => a.href).filter(h => /bol\.com|coolblue|amazon|awin|\/ga\//.test(h)).map(h => h.replace(/([?&])(s|nocache)=\d+/g, '$1$2=X'));
      const tekst = main.innerText.split('\n').map(t => t.trim()).filter(Boolean)
        .filter(t => !/^(Prijs van|Bron: bol\.com|prijs van)/.test(t));
      return { kaarten, volgorde, winkels, tekst };
    });
    res[u].status = resp.status();
  }
  fs.writeFileSync(uit, JSON.stringify(res, null, 1));
  console.log(`${Object.keys(res).length} adressen opgeslagen in ${uit}: ` + Object.entries(res).map(([u, r]) => `${u.replace('https://robotmaaierkompas.nl', '')} ${r.status} ${r.kaarten.length}k`).join(', '));
  await browser.close();
})();
