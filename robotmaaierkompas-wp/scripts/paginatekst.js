#!/usr/bin/env node
// Volledige weergegeven tekst van een (concept)pagina als markdown: koppen, alinea's, lijsten, tabellen, kaarten,
// veelgestelde vragen (opengeklapt) en bronnen. Werkt met de weergegeven inhoud in de omhulling van de hub (zoals
// scripts/ronde71_controle.js), na rmk.js, op 1440 px.
// Gebruik:  node scripts/paginatekst.js <concept.json> <hub.html> <uit.md>
const fs = require('fs');
const { chromium } = require('playwright');
const [conceptPad, hubPad, uitPad] = process.argv.slice(2);
const concept = JSON.parse(fs.readFileSync(conceptPad));
const hub = fs.readFileSync(hubPad, 'utf8');
const html = hub.slice(0, hub.indexOf('<main')) + concept.rendered + hub.slice(hub.indexOf('</main>') + 7);
const PROEF = 'https://robotmaaierkompas.nl/__proef-paginatekst__/';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.route('**/*', r => {
    const u = r.request().url();
    if (u.startsWith(PROEF)) return r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: html });
    if (/bol\.com|awin|coolblue|amazon/.test(u)) return r.abort();
    return r.continue();
  });
  await page.goto(PROEF, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  const md = await page.evaluate(() => {
    const main = document.querySelector('main');
    main.querySelectorAll('details').forEach(d => d.open = true);
    const zichtbaar = e => { const s = getComputedStyle(e); return s.display !== 'none' && s.visibility !== 'hidden' && !e.hidden; };
    const schoon = t => t.replace(/\s+/g, ' ').trim();
    const uit = [];
    const loop = el => {
      for (const e of el.children) {
        if (!zichtbaar(e) || ['SCRIPT', 'STYLE', 'svg', 'SVG', 'IMG'].includes(e.tagName)) continue;
        const t = e.tagName;
        if (/^H[1-6]$/.test(t)) uit.push('\n' + '#'.repeat(+t[1]) + ' ' + schoon(e.textContent) + '\n');
        else if (t === 'P') { const s = schoon(e.innerText); if (s) uit.push(s + '\n'); }
        else if (t === 'UL' || t === 'OL') { for (const li of e.children) if (zichtbaar(li)) uit.push('- ' + schoon(li.innerText)); uit.push(''); }
        else if (t === 'TABLE') {
          const rijen = [...e.rows].map(r => [...r.cells].map(c => schoon(c.textContent).replace(/\|/g, '/')));
          uit.push('| ' + rijen[0].join(' | ') + ' |', '| ' + rijen[0].map(() => '---').join(' | ') + ' |', ...rijen.slice(1).map(r => '| ' + r.join(' | ') + ' |'), '');
        } else if (t === 'DETAILS') {
          uit.push('**' + schoon(e.querySelector('summary').textContent) + '**');
          const a = [...e.children].filter(c => c.tagName !== 'SUMMARY').map(c => schoon(c.innerText)).join(' ');
          uit.push(a + '\n');
        } else if (e.children.length === 0) { const s = schoon(e.innerText || ''); if (s) uit.push(s + '\n'); }
        else {
          // blokken met losse tekst naast kinderen (bijv. chips, scorecel): tekstknopen meenemen
          const los = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).filter(Boolean).join(' ');
          if (los) uit.push(schoon(los) + '\n');
          loop(e);
        }
      }
    };
    loop(main);
    return uit.join('\n').replace(/\n{3,}/g, '\n\n').trim() + '\n';
  });
  fs.writeFileSync(uitPad, md);
  console.log(`${uitPad}: ${md.length} tekens, ${md.split('\n').length} regels`);
  await browser.close();
})();
