// Laadt rmk.js in een minimale browseromgeving en rekent de testgevallen door.
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, '../wp-content/themes/robotmaaierkompas-child/robotmaaierkompas/rmk.js'), 'utf8');
const doc = { querySelector: () => null, querySelectorAll: () => [] };
const win = { rmkConfig: {}, addEventListener() {}, dispatchEvent() {} };
new Function('window', 'document', 'localStorage', 'location', src)(win, doc, {}, { search: '' });
const cases = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify(cases.map(c => {
  const r = win.rmkScore(c.v, c.reviews);
  return { kind: r.kind, value: r.value, label: r.label, shown: r.value == null ? '–' : win.rmkFormatScore(r.value) };
})));
