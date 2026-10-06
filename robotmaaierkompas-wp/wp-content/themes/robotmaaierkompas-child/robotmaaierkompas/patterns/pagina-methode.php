<?php
/**
 * Title: RMK pagina – Hoe we beoordelen en over ons
 * Slug: robotmaaierkompas/pagina-methode
 * Categories: robotmaaierkompas-paginas
 * Description: Scoremodel v1.0, statussen, prijzen, verdienmodel, over ons.
 * Viewport Width: 1280
 * Block Types: core/post-content
 * Post Types: page, post
 */
?>
<!-- wp:group {"tagName":"main","anchor":"inhoud","className":"rmk","layout":{"type":"default"}} -->
<main class="wp-block-group rmk" id="inhoud">
<!-- wp:html -->
<div class="rmk-container rmk-column rmk-column--narrow">
  <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li aria-current="page">Hoe we beoordelen</li></ol></nav>
  <header class="rmk-pagehead" style="max-width: 48rem">
    <p class="rmk-eyebrow">Scoremodel v1.0 (concept tot bevriezing)</p>
    <h1>Hoe we robotmaaiers beoordelen, en wat we niet doen</h1>
    <p class="rmk-lead">We testen robotmaaiers niet zelf. We verzamelen specificaties, lezen gebruikersreviews en rekenen met een openbaar scoremodel. Op deze pagina staat precies hoe.</p>
  </header>
  <section class="rmk-section--tight" aria-label="Wel en niet" style="display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr))">
    <div class="rmk-callout" style="flex-direction: column"><b style="font-family: var(--rmk-font-display); font-size: var(--rmk-fs-md)">Wat we doen</b><ul style="padding-left: 18px; display: flex; flex-direction: column; gap: 6px"><li>Specificaties opzoeken in handleidingen, bij fabrikanten en bij winkels</li><li>Gebruikersreviews lezen</li><li>Scoren met vaste, openbare gewichten</li><li>Bron en datum tonen bij elke waarde</li></ul></div>
    <div class="rmk-card" style="border-style: dashed"><b style="font-family: var(--rmk-font-display); font-size: var(--rmk-fs-md)">Wat we niet doen</b><ul style="padding-left: 18px; display: flex; flex-direction: column; gap: 6px; font-size: var(--rmk-fs-sm)"><li>Maaiers zelf in een tuin gebruiken</li><li>Geluid, maaitijd of accuduur zelf meten</li><li>Scores aanpassen voor adverteerders</li><li>Prijzen schatten als we er geen hebben</li></ul></div>
  </section>
  <div class="rmk-split" style="padding-bottom: 64px">
    <aside class="rmk-split__side rmk-split__side--sticky" style="flex-basis: 15rem">
      <nav class="rmk-toc" aria-labelledby="toc"><b id="toc" style="font-family: var(--rmk-font-display)">Op deze pagina</b>
        <ol><li><a href="#scoremodel">Het scoremodel</a></li><li><a href="#label">Eindscore, functiescore of geen score</a></li><li><a href="#statussen">Statussen</a></li><li><a href="#prijzen">Prijzen</a></li><li><a href="#verdienmodel">Zo verdienen we geld</a></li><li><a href="/over-ons/">Over ons</a></li><li><a href="#correcties">Correcties</a></li></ol>
      </nav>
    </aside>
    <div class="rmk-split__main" style="display: flex; flex-direction: column; gap: 48px; max-width: 48rem">
      <section id="scoremodel" aria-labelledby="model-t" style="display: flex; flex-direction: column; gap: 16px">
        <h2 id="model-t" style="font-size: var(--rmk-fs-xl)">Het scoremodel</h2>
        <p>Zeven onderdelen, elk beoordeeld op een schaal van 0 tot 10. De balk bij elk onderdeel is de waarde maal tien procent breed. De eindscore (0 tot 100) is het gewogen gemiddelde met deze gewichten:</p>
        <div class="rmk-tablewrap"><table class="rmk-table">
          <thead><tr><th scope="col">Onderdeel</th><th scope="col" class="is-num">Gewicht</th><th scope="col">Wat telt mee</th></tr></thead>
          <tbody>
            <tr><th scope="row">Betrouwbaarheid uit reviews</th><td class="is-num">25%</td><td>Alleen bij minstens 50 gelezen reviews. [toelichting]</td></tr>
            <tr><th scope="row">Navigatie en dekking</th><td class="is-num">20%</td><td>[toelichting]</td></tr>
            <tr><th scope="row">Prijs-kwaliteit</th><td class="is-num">20%</td><td>[toelichting]</td></tr>
            <tr><th scope="row">Hellingen en terrein</th><td class="is-num">10%</td><td>[toelichting]</td></tr>
            <tr><th scope="row">App en bediening</th><td class="is-num">10%</td><td>[toelichting]</td></tr>
            <tr><th scope="row">Veiligheid</th><td class="is-num">10%</td><td>[toelichting]</td></tr>
            <tr><th scope="row">Geluid</th><td class="is-num">5%</td><td>[toelichting]</td></tr>
          </tbody>
        </table></div>
        <p class="rmk-small">Eindscore = som van (gewicht × waarde) ÷ 10. Voorbeeld van de rekenregel: als alle onderdelen 10 zijn, is de eindscore 100.</p>
      </section>

      <section id="label" class="rmk-prose" aria-labelledby="label-t">
        <h2 id="label-t" style="margin-top: 0">Eindscore, functiescore of geen score</h2>
        <ul>
          <li><b>Alle zeven onderdelen bekend:</b> we tonen de <b>eindscore</b>.</li>
          <li><b>Vijf of zes onderdelen bekend:</b> we tonen een <b>functiescore</b> met het label <span class="rmk-provisional">voorlopig, zonder …</span>, gevolgd door de namen van de ontbrekende onderdelen. De functiescore is het gewogen gemiddelde van alleen de bekende onderdelen, omgerekend naar 0 tot 100.</li>
          <li><b>Minder dan vijf onderdelen bekend:</b> <b>geen score</b>.</li>
        </ul>
        <p>Een onderdeel zonder gegevens krijgt "onvoldoende data". Betrouwbaarheid geldt als onbekend zolang we minder dan 50 reviews van het model hebben gelezen. We gebruiken geen sterren.</p>
      </section>

      <section id="statussen" aria-labelledby="status-t" style="display: flex; flex-direction: column; gap: 16px">
        <h2 id="status-t" style="font-size: var(--rmk-fs-xl)">Statussen bij specificaties</h2>
        <table class="rmk-specs"><tbody>
          <tr><th scope="row"><span class="rmk-status rmk-status--ok">Gecontroleerd</span></th><td style="font-weight: 400">Gelezen in de handleiding of op de officiële pagina van de fabrikant.</td></tr>
          <tr><th scope="row"><span class="rmk-status rmk-status--maker">Fabrikantclaim</span></th><td style="font-weight: 400">Alleen genoemd in een datasheet of reclame van de fabrikant.</td></tr>
          <tr><th scope="row"><span class="rmk-status rmk-status--shop">Winkelclaim</span></th><td style="font-weight: 400">Alleen een winkel noemt het.</td></tr>
          <tr><th scope="row"><span class="rmk-status rmk-status--conflict">Tegenstrijdig</span></th><td style="font-weight: 400">Bronnen geven verschillende waarden. We tonen beide en rekenen met de minst gunstige waarde.</td></tr>
          <tr><th scope="row"><span class="rmk-status rmk-status--missing">Niet gevonden</span></th><td style="font-weight: 400">We hebben geen bron gevonden.</td></tr>
        </tbody></table>
      </section>

      <section id="prijzen" class="rmk-prose" aria-labelledby="prijs-t">
        <h2 id="prijs-t" style="margin-top: 0">Prijzen</h2>
        <p>[Uitleg prijzen: voorlopig tonen we geen winkelprijzen; bij elk model staat "Bekijk de prijs bij de winkel".]</p>
      </section>

      <section id="verdienmodel" class="rmk-prose" aria-labelledby="geld-t">
        <h2 id="geld-t" style="margin-top: 0">Zo verdienen we geld</h2>
        <p>Koop je iets via een winkelknop, dan kan de winkel ons een commissie betalen. Jij betaalt niets extra. De volgorde in toplijsten volgt de score, niet de commissie, en fabrikanten kunnen geen plek kopen. Boven de eerste winkelknop van elke pagina staat een korte melding, en winkellinks zijn gemarkeerd als gesponsord.</p>
      </section>
    </div>
  </div>
</div>
<!-- /wp:html -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column rmk-column--narrow","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column rmk-column--narrow">
<!-- wp:pattern {"slug":"robotmaaierkompas/auteursblok"} /-->
</div>
<!-- /wp:group -->
<!-- wp:html -->
<section class="rmk-container rmk-section--tight rmk-column rmk-column--narrow" id="correcties" aria-labelledby="corr-t" style="padding-bottom: 64px">
  <div class="rmk-callout"><svg class="rmk-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5h14a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1h-8l-4 3v-3H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z"/></svg><p><b id="corr-t">Fout gezien?</b> Mail naar [e-mailadres] met het model en de bron. We passen het aan en noemen de wijziging bij de pagina.</p></div>
</section>
<!-- /wp:html -->
</main>
<!-- /wp:group -->
