/* robotmaaierkompas.nl — rmk.js (v1.1)
   Afhankelijkheidsvrij, laden met `defer`. Onderdelen:
   1. Scoremodel v1.0 (concept tot bevriezing): eindscore / functiescore / geen score, dynamisch label
   2. Vergelijkingsfilter   3. Kostencalculator   4. Tuingrootte-keuzehulp   5. Cookiebanner
   Instellingen kunnen worden overschreven via window.rmkConfig (zie robotmaaierkompas-setup.php). */
(function () {
  'use strict';
  var CFG = window.rmkConfig || {};
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  /* Getal uit tekst; placeholders zoals "[0–10]" of lege velden geven null. */
  var parse = function (v) {
    var t = String(v == null ? '' : v).trim();
    if (!t || /[\[\]]/.test(t)) return null;
    var n = parseFloat(t.replace(/\s/g, '').replace(/\.(?=\d{3}(\D|$))/g, '').replace(',', '.'));
    return isFinite(n) ? n : null;
  };
  var nl = function (n, d) { return n.toLocaleString('nl-NL', { minimumFractionDigits: 0, maximumFractionDigits: d == null ? 1 : d }); };
  var eur = function (n) { return '€ ' + nl(Math.round(n), 0); };
  /* Score: altijd één decimaal (92,7). Rangschikken gebeurt op de onafgeronde waarde. */
  var fmtScore = function (v) { return (Math.round(v * 10) / 10).toLocaleString('nl-NL', { minimumFractionDigits: 1, maximumFractionDigits: 1 }); };

  /* ======================= 1. SCOREMODEL ======================= */
  var MODEL = CFG.scoreModel || [
    { key: 'betrouwbaarheid', label: 'Betrouwbaarheid uit reviews', w: 25 },
    { key: 'navigatie',       label: 'Navigatie en dekking',        w: 20 },
    { key: 'prijskwaliteit',  label: 'Prijs-kwaliteit',             w: 20 },
    { key: 'hellingen',       label: 'Hellingen en terrein',        w: 10 },
    { key: 'app',             label: 'App en bediening',            w: 10 },
    { key: 'veiligheid',      label: 'Veiligheid',                  w: 10 },
    { key: 'geluid',          label: 'Geluid',                      w: 5 }
  ];
  var MIN_REVIEWS = CFG.minReviews || 50;   /* betrouwbaarheid pas vanaf dit aantal gelezen reviews */
  var MIN_PARTS = 5;                         /* minder bekende onderdelen = geen score */

  /* values: {key: getal 0–10 of null}, reviews: aantal gelezen reviews of null */
  function computeScore(values, reviews) {
    var known = [], missing = [], sumW = 0, sumWV = 0;
    MODEL.forEach(function (p) {
      var v = values[p.key];
      if (p.key === 'betrouwbaarheid' && (reviews == null || reviews < MIN_REVIEWS)) v = null;
      if (v != null && v >= 0 && v <= 10) { known.push(p); sumW += p.w; sumWV += p.w * v; }
      else missing.push(p);
    });
    var res = { known: known.length, total: MODEL.length, missing: missing, value: null, kind: 'geen', label: '' };
    if (known.length === MODEL.length) { res.kind = 'eind'; res.value = sumWV / 10; }
    else if (known.length >= MIN_PARTS) {
      res.kind = 'functie';
      res.value = sumWV / sumW * 10;   /* gewogen gemiddelde van de bekende onderdelen, op 0–100, onafgerond */
      res.label = 'voorlopig, zonder ' + joinNames(missing.map(function (p) { return p.label.charAt(0).toLowerCase() + p.label.slice(1); }));
    }
    return res;
  }
  function joinNames(a) { return a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' en ' + a[a.length - 1]; }
  var KIND = { eind: 'Eindscore', functie: 'Functiescore', geen: 'Geen score' };

  /* Volledig scoreblok: <section data-rmk-score> met <li data-key data-value> (+ data-reviews op betrouwbaarheid) */
  $$('section[data-rmk-score]').forEach(function (box) {
    var values = {}, reviews = null;
    $$('li[data-key]', box).forEach(function (li) {
      values[li.dataset.key] = parse(li.dataset.value);
      if (li.dataset.key === 'betrouwbaarheid') reviews = parse(li.dataset.reviews);
    });
    var r = computeScore(values, reviews);
    box.classList.toggle('rmk-score--provisional', r.kind === 'functie');
    box.classList.toggle('rmk-score--none', r.kind === 'geen');
    $('[data-out="total"]', box).textContent = r.value == null ? '–' : fmtScore(r.value);
    box.dataset.total = r.value == null ? '' : r.value;
    $('[data-out="kind"]', box).textContent = KIND[r.kind];
    var lab = $('[data-out="label"]', box); lab.textContent = r.label; lab.hidden = !r.label;
    var bar = $('[data-out="bar"]', box);
    bar.setAttribute('aria-label', r.value == null ? 'Geen score' : KIND[r.kind] + ' ' + fmtScore(r.value) + ' van 100');
    $('i', bar).style.width = (r.value == null ? 0 : Math.round(r.value * 10) / 10) + '%';
    $('[data-out="note"]', box).textContent = r.kind === 'eind' ? '' :
      (r.kind === 'functie' ? 'Berekend over ' + r.known + ' van ' + r.total + ' onderdelen.' :
       'Te weinig gegevens: ' + r.known + ' van ' + r.total + ' onderdelen bekend, minimaal ' + MIN_PARTS + ' nodig.');
    $$('li[data-key]', box).forEach(function (li) {
      var p = MODEL.filter(function (m) { return m.key === li.dataset.key; })[0]; if (!p) return;
      var v = values[p.key], isMissing = r.missing.indexOf(p) > -1;
      li.classList.toggle('rmk-part--empty', isMissing);
      $('.rmk-part__label', li).innerHTML = p.label + ' <small>' + p.w + '%</small>';
      $('.rmk-part__val', li).textContent = isMissing ? 'onvoldoende data' : nl(v) + ' / 10';
      var b = $('.rmk-bar', li);
      b.setAttribute('aria-label', isMissing ? (p.key === 'betrouwbaarheid' && v != null ? 'Onvoldoende data: minder dan ' + MIN_REVIEWS + ' gelezen reviews' : 'Onvoldoende data') : nl(v) + ' van 10');
      $('i', b).style.width = isMissing ? '0%' : (v * 10) + '%';   /* balkbreedte = waarde × 10 */
    });
  });

  /* Compacte score: <div data-rmk-score data-scores="betrouwbaarheid=…; navigatie=…; …; reviews=…"> */
  $$('div[data-rmk-score]').forEach(function (el) {
    var values = {}, reviews = null;
    String(el.dataset.scores || '').split(';').forEach(function (pair) {
      var kv = pair.split('='); if (kv.length < 2) return;
      var k = kv[0].trim(), v = parse(kv.slice(1).join('='));
      if (k === 'reviews') reviews = v; else values[k] = v;
    });
    var r = computeScore(values, reviews);
    el.dataset.kind = r.kind; el.dataset.total = r.value == null ? '' : r.value;   /* onafgerond: sorteren */
    var m = $('.rmk-minis', el);
    m.classList.toggle('rmk-minis--provisional', r.kind === 'functie');
    m.classList.toggle('rmk-minis--none', r.kind === 'geen');
    $('[data-out="total"]', el).textContent = r.value == null ? '–' : fmtScore(r.value);
    $('[data-out="kind"]', el).textContent = KIND[r.kind] + (r.value == null ? '' : ', van 100');
    var lab = $('[data-out="label"]', el); if (lab) { lab.textContent = r.label; lab.hidden = !r.label; }
  });

  /* ======================= Vuistregel (eigen, geen bron) =======================
     Fabrikanten noemen de maximale oppervlakte onder gunstige omstandigheden. Onze eigen
     vuistregel telt daar marge bij op: +30% voor een open gazon, +50% bij zones/obstakels. */
  var MARGIN = CFG.margin || { open: 1.3, complex: 1.5 };
  var needCapacity = function (m2, complex) { return Math.ceil(m2 * (complex ? MARGIN.complex : MARGIN.open) / 100) * 100; };

  /* ======================= 2. VERGELIJKINGSFILTER ======================= */
  $$('[data-rmk-compare]').forEach(function (root) {
    var form = $('form', root), tbody = $('tbody', root), count = $('[data-rmk-count]', root), empty = $('[data-rmk-empty]', root);
    var rows = $$('tr[data-model]', tbody), sortEl = $('[name="sort"]', root), need = $('[data-out="need"]', root);
    var q = new URLSearchParams(location.search);
    if (q.get('m2') && form.m2) form.m2.value = q.get('m2');
    if (q.get('helling') && form.slope) form.slope.value = q.get('helling');
    if (q.get('zones') === '1' && form.zones) form.zones.checked = true;
    function apply() {
      var navs = $$('[name="nav"]:checked', form).map(function (i) { return i.value; });
      var m2 = parse(form.m2 && form.m2.value), slope = parse(form.slope && form.slope.value), budget = parse(form.budget && form.budget.value);
      var cap = m2 ? needCapacity(m2, form.zones && form.zones.checked) : null;
      if (need) need.textContent = cap ? 'Minimaal ' + nl(cap, 0) + ' m² opgegeven capaciteit (eigen vuistregel).' : '';
      var onlyFinal = form.final && form.final.checked, sort = sortEl ? sortEl.value : 'score';
      var visible = rows.filter(function (r) {
        var d = r.dataset, price = parse(d.price), sc = $('[data-rmk-score]', r);
        var ok = navs.indexOf(d.nav) > -1 &&
          (!cap || (parse(d.capacity) || 0) >= cap) &&
          (!slope || (parse(d.slope) || 0) >= slope) &&
          (!budget || price == null || price <= budget) &&
          (!onlyFinal || (sc && sc.dataset.kind === 'eind'));
        r.hidden = !ok; return ok;
      });
      var tot = function (r) { var s = $('[data-rmk-score]', r); return s && s.dataset.total ? +s.dataset.total : -1; };
      visible.sort(function (a, b) {
        if (sort === 'price') return (parse(a.dataset.price) || 1e12) - (parse(b.dataset.price) || 1e12);
        if (sort === 'capacity') return (parse(b.dataset.capacity) || 0) - (parse(a.dataset.capacity) || 0);
        return tot(b) - tot(a);
      }).forEach(function (r) { tbody.appendChild(r); });
      if (count) count.textContent = visible.length === 1 ? '1 model past' : visible.length + ' modellen passen';
      if (empty) empty.hidden = visible.length > 0;
    }
    form.addEventListener('input', apply);
    form.addEventListener('change', apply);
    if (sortEl) sortEl.addEventListener('change', apply);
    form.addEventListener('submit', function (e) { e.preventDefault(); apply(); });
    form.addEventListener('reset', function () { setTimeout(apply, 0); });
    apply();
  });

  /* ======================= 3. KOSTENCALCULATOR =======================
     Geen standaardwaarden. Waarden komen van de bezoeker of uit het modelbestand
     (CFG.modelsUrl, JSON). Elk veld uit het modelbestand toont bron en datum. */
  var FIELDS = [
    ['aanschaf', 'Aanschaf'], ['installatie', 'Installatie'], ['antidiefstal', 'Antidiefstalmodule'],
    ['antenne_gateway', 'Antenne of gateway'], ['messen_per_jaar', 'Messen'], ['accu_prijs', 'Accu'],
    ['accu_levensduur_jaren', null], ['stroom_kwh_per_seizoen', null], ['stroomprijs_per_kwh', null],
    ['verbinding_per_jaar', 'Verbinding'], ['gratis_periode_jaren', null], ['onderhoud_per_jaar', 'Onderhoud']
  ];
  $$('[data-rmk-calc]').forEach(function (root) {
    var form = $('form', root), models = [], general = {};
    var f = function (k) { return form.elements[k]; };
    var src = function (k) { return $('[data-src-for="' + k + '"]', root); };
    function calc() {
      var v = {}; FIELDS.forEach(function (x) { v[x[0]] = parse(f(x[0]) && f(x[0]).value); });
      var yrs = parse(f('jaren').value);
      var ready = v.aanschaf != null && yrs != null && yrs >= 1;
      $('[data-rmk-ready]', root).hidden = !ready;
      $('[data-rmk-notready]', root).hidden = ready;
      if (!ready) return;
      yrs = Math.round(yrs);
      var accCount = v.accu_levensduur_jaren ? Math.floor((yrs - 0.001) / v.accu_levensduur_jaren) : 0;
      var paidYears = Math.max(0, yrs - (v.gratis_periode_jaren || 0));
      var parts = {
        aanschaf: v.aanschaf, installatie: v.installatie || 0, antidiefstal: v.antidiefstal || 0, antenne_gateway: v.antenne_gateway || 0,
        messen_per_jaar: (v.messen_per_jaar || 0) * yrs, accu_prijs: (v.accu_prijs || 0) * accCount,
        stroom: (v.stroom_kwh_per_seizoen || 0) * (v.stroomprijs_per_kwh || 0) * yrs,
        verbinding_per_jaar: (v.verbinding_per_jaar || 0) * paidYears, onderhoud_per_jaar: (v.onderhoud_per_jaar || 0) * yrs
      };
      var total = 0, max = 1;
      Object.keys(parts).forEach(function (k) { total += parts[k]; max = Math.max(max, parts[k]); });
      $('[data-out="years"]', root).textContent = yrs;
      $('[data-out="total"]', root).textContent = eur(total);
      $('[data-out="per"]', root).textContent = eur(total / yrs) + ' per jaar · ' + eur(total / yrs / 12) + ' per maand';
      $('[data-out="accCount"]', root).textContent = v.accu_levensduur_jaren ? accCount + ' keer' : 'niet berekend (levensduur leeg)';
      Object.keys(parts).forEach(function (k) {
        var row = $('[data-part="' + k + '"]', root); if (!row) return;
        $('.rmk-num', row).textContent = eur(parts[k]);
        $('.rmk-bar > i', row).style.width = Math.round(parts[k] / max * 100) + '%';
      });
      var empty = FIELDS.filter(function (x) { return v[x[0]] == null && x[0] !== 'aanschaf'; }).map(function (x) { return f(x[0]).dataset.name; });
      $('[data-out="missing"]', root).textContent = empty.length ? 'Leeg en dus niet meegeteld: ' + empty.join(', ') + '.' : '';
    }
    function fill(entry, key) {
      var el = f(key), s = src(key); if (!el) return;
      var w = entry && entry.waarde != null && parse(entry.waarde) != null ? entry.waarde : '';
      el.value = w === '' ? '' : String(w).replace('.', ',');
      if (s) { s.hidden = false; s.textContent = w === '' ? 'Niet in het modelbestand' : 'Bron: ' + (entry.bron || 'onbekend') + (entry.datum ? ' · ' + entry.datum : ''); }
    }
    var sel = f('model');
    if (sel && CFG.modelsUrl) {
      fetch(CFG.modelsUrl, { credentials: 'same-origin' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (data) {
        if (!data || !data.modellen) return;
        general = data.algemeen || {};
        models = data.modellen.filter(function (m) { return m.slug && m.naam && !/[\[\]]/.test(m.naam); });
        models.forEach(function (m) { var o = document.createElement('option'); o.value = m.slug; o.textContent = m.naam; sel.appendChild(o); });
      }).catch(function () {});
    }
    if (sel) sel.addEventListener('change', function () {
      var m = models.filter(function (x) { return x.slug === sel.value; })[0];
      FIELDS.forEach(function (x) {
        var k = x[0];
        if (!m) { f(k).value = ''; if (src(k)) src(k).hidden = true; return; }
        fill(k === 'stroomprijs_per_kwh' ? general[k] : (m.kosten || {})[k], k);
      });
      calc();
    });
    form.addEventListener('input', function (e) {
      var s = e.target.name && src(e.target.name);
      if (s && e.target.name !== 'model') { s.hidden = false; s.textContent = 'Eigen invoer'; }
      calc();
    });
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    calc();
  });

  /* ======================= 4. TUINGROOTTE-KEUZEHULP ======================= */
  $$('[data-rmk-helper]').forEach(function (root) {
    var form = $('form', root);
    function run() {
      var m2 = parse(form.m2.value), slope = parse(form.slope.value), complex = form.zones.checked;
      var ok = m2 != null && m2 > 0;
      $('[data-rmk-ready]', root).hidden = !ok;
      $('[data-rmk-notready]', root).hidden = ok;
      if (!ok) return;
      var cap = needCapacity(m2, complex);
      $('[data-out="cap"]', root).textContent = nl(cap, 0);
      $('[data-out="margin"]', root).textContent = complex ? '+50%' : '+30%';
      var sl = $('[data-out="slope"]', root);
      sl.textContent = slope != null ? ' en een opgegeven maximale helling van minstens ' + nl(slope, 0) + '%' : '';
      var link = $('[data-out="link"]', root);
      link.href = link.dataset.base + '?m2=' + m2 + (slope != null ? '&helling=' + slope : '') + (complex ? '&zones=1' : '');
    }
    form.addEventListener('input', run);
    form.addEventListener('change', run);
    form.addEventListener('submit', function (e) { e.preventDefault(); run(); });
    run();
  });

  /* ======================= 5. COOKIEBANNER =======================
     Bewaart alleen de keuze. Koppel je tags aan: window.addEventListener('rmk:consent', e => …) */
  var banner = $('[data-rmk-cookie]');
  if (banner) {
    var KEY = 'rmk_consent';
    var read = function () { try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; } };
    var store = function (c) {
      try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {}
      document.cookie = KEY + '=' + (c.stats ? 's' : '') + (c.aff ? 'a' : '') + '-;max-age=31536000;path=/;SameSite=Lax';
      window.dispatchEvent(new CustomEvent('rmk:consent', { detail: c }));
      banner.hidden = true;
    };
    var main = $('[data-view="main"]', banner), settings = $('[data-view="settings"]', banner);
    var show = function (view) { banner.hidden = false; main.hidden = view !== 'main'; settings.hidden = view !== 'settings'; };
    var saved = read();
    if (saved) window.dispatchEvent(new CustomEvent('rmk:consent', { detail: saved })); else show('main');
    banner.addEventListener('click', function (e) {
      var a = e.target.closest('[data-action]'); if (!a) return;
      var act = a.dataset.action;
      if (act === 'reject') store({ stats: false, aff: false });
      if (act === 'accept') store({ stats: true, aff: true });
      if (act === 'settings') { show('settings'); var c = read() || {}; settings.querySelector('[name="stats"]').checked = !!c.stats; settings.querySelector('[name="aff"]').checked = !!c.aff; }
      if (act === 'save') store({ stats: settings.querySelector('[name="stats"]').checked, aff: settings.querySelector('[name="aff"]').checked });
    });
    $$('[data-rmk-cookie-open], a[href="#cookie-instellingen"]').forEach(function (l) {
      l.addEventListener('click', function (e) { e.preventDefault(); show('settings'); });
    });
  }

  window.rmkScore = computeScore;   /* voor tests en eigen scripts */
  window.rmkFormatScore = fmtScore;
})();
