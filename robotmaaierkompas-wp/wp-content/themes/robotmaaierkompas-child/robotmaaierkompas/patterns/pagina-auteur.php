<?php
/**
 * Title: RMK pagina – Auteur
 * Slug: robotmaaierkompas/pagina-auteur
 * Categories: robotmaaierkompas-paginas
 * Description: Auteursprofiel.
 * Viewport Width: 1280
 * Block Types: core/post-content
 * Post Types: page, post
 */
?>
<!-- wp:group {"tagName":"main","anchor":"inhoud","className":"rmk","layout":{"type":"default"}} -->
<main class="wp-block-group rmk" id="inhoud">
<!-- wp:html -->
<div class="rmk-container" style="padding-bottom: 64px">
  <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li><a href="/over-ons/">Over ons</a></li><li aria-current="page">[Naam auteur]</li></ol></nav>
  <header class="rmk-pagehead" style="flex-direction: row; flex-wrap: wrap; align-items: center; gap: 32px">
    <div class="rmk-avatar rmk-avatar--lg" role="img" aria-label="Portret van [Naam auteur]">[initialen]</div>
    <div style="flex: 1 1 24rem; display: flex; flex-direction: column; gap: 12px">
      <p class="rmk-eyebrow">Redactie</p>
      <h1>[Naam auteur]</h1>
      <div class="rmk-author__roles"><span class="rmk-chip rmk-chip--brand">[rol]</span></div>
    </div>
  </header>
  <div class="rmk-split">
    <div class="rmk-split__main rmk-prose">
      <h2 style="margin-top: 0">Achtergrond</h2>
      <p>[Relevante, controleerbare ervaring.]</p>
      <h2>Verantwoordelijk voor</h2>
      <ul><li>[taak]</li><li>[taak]</li></ul>
      <h2>Werkwijze</h2>
      <p>[Voornaam] vergelijkt en analyseert, maar test geen maaiers. Elke pagina wordt voor publicatie nagekeken op bronnen en data.</p>
    </div>
    <aside class="rmk-split__side"><div class="rmk-card"><h2 style="font-size: var(--rmk-fs-md)">Contact</h2><p class="rmk-small">Vragen of correcties over een artikel?</p><a class="rmk-btn rmk-btn--secondary" href="/redactiebeleid/#correcties">Meld een correctie</a></div></aside>
  </div>
  <section class="rmk-section" aria-labelledby="art" style="display: flex; flex-direction: column; gap: 16px">
    <h2 id="art" style="font-size: var(--rmk-fs-xl)">Artikelen van [Naam auteur]</h2>
    <div class="rmk-grid rmk-grid--wide">
      <a class="rmk-card" href="[url]"><span class="rmk-meta">[Type] · [datum]</span><h3>[Titel]</h3></a>
      <a class="rmk-card" href="[url]"><span class="rmk-meta">[Type] · [datum]</span><h3>[Titel]</h3></a>
    </div>
  </section>
</div>
<!-- /wp:html -->
</main>
<!-- /wp:group -->
