<?php
/**
 * Title: RMK pagina – Homepage
 * Slug: robotmaaierkompas/pagina-homepage
 * Categories: robotmaaierkompas-paginas
 * Description: Hero met kompasmotief, vertrouwensstrook, vier ingangen, keuzehulp-link, werkwijze, automatisch "Onlangs bijgewerkt" (afwerkpakket v1.2).
 * Viewport Width: 1280
 * Block Types: core/post-content
 * Post Types: page, post
 */
?>
<!-- wp:group {"tagName":"main","anchor":"inhoud","className":"rmk","layout":{"type":"default"}} -->
<main class="wp-block-group rmk" id="inhoud">
<!-- wp:html -->
<section class="rmk-hero rmk-hero--motif rmk-hero--center" aria-labelledby="h1">
  <div class="rmk-container rmk-hero__inner">
    <div class="rmk-hero__text">
      <span class="rmk-hero__badge"><img src="<?php echo esc_url( RMK_URL ); ?>/logo/icoon-donker.svg" alt="" width="40" height="40"></span>
      <p class="rmk-eyebrow">Onafhankelijk vergeleken</p>
      <h1 id="h1">[Paginatitel]</h1>
      <p class="rmk-lead">[Introductie: wat we vergelijken en hoe, met bron en datum.]</p>
      <div class="rmk-row">
        <a class="rmk-btn rmk-btn--inverse" href="[url kernpagina]">[Knoptekst]</a>
        <a class="rmk-btn rmk-btn--ghost-inverse" href="/robotmaaier-test-vergelijking/">Zelf vergelijken</a>
      </div>
    </div>
  </div>
</section>
<section class="rmk-trust" aria-label="Waarom je ons kunt volgen">
  <div class="rmk-container rmk-column">
    <ul>
      <li><span class="rmk-trust__icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 3h7l5 5v12a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z"/><path d="M14 3v5h5"/><circle cx="12" cy="15" r="3"/><path d="M12 13.6V15l.9.9"/></svg></span>Elke waarde met bron en datum</li>
      <li><span class="rmk-trust__icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M4 20h16"/><path d="M6.5 20v-6M11 20V9M15.5 20v-8M20 20V5"/></svg></span>Openbaar scoremodel</li>
      <li><span class="rmk-trust__icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M6 3h12v18l-2-1.4-2 1.4-2-1.4-2 1.4-2-1.4L6 21Z"/><path d="M14.5 8.7a3 3 0 1 0 0 4.6M9 10.2h4M9 11.8h4"/><path d="M9 16.5h6"/></svg></span>Kosten die op geen winkelpagina staan</li>
    </ul>
  </div>
</section>
<section class="rmk-section rmk-section--alt" aria-labelledby="ingangen-titel">
  <div class="rmk-container rmk-column">
    <div class="rmk-section-head">
        <h2 id="ingangen-titel">Waar wil je mee beginnen?</h2>
    </div>
    <div class="rmk-entries">
      <a class="rmk-entry" href="[url]">
        <span class="rmk-entry__icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M10 6.5h10M10 12h10M10 17.5h10"/><path d="m3.5 6.5 1.5 1.5 2.5-3"/><path d="M4.5 12h2M4.5 17.5h2"/></svg></span>
        <h3>[Titel]</h3>
        <p>[Eén regel uitleg]</p>
        <span class="rmk-entry__more">[Linktekst]<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
      </a>
      <a class="rmk-entry" href="[url]">
        <span class="rmk-entry__icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="3" y="4" width="7.5" height="16" rx="1.5"/><rect x="13.5" y="4" width="7.5" height="16" rx="1.5"/><path d="M5.5 8.5h2.5M5.5 12h2.5M16 8.5h2.5M16 12h2.5"/></svg></span>
        <h3>[Titel]</h3>
        <p>[Eén regel uitleg]</p>
        <span class="rmk-entry__more">[Linktekst]<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
      </a>
      <a class="rmk-entry" href="[url]">
        <span class="rmk-entry__icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/><path d="M16.2 7.8 13.3 13.3 10.7 10.7Z"/><path d="M7.8 16.2 10.7 10.7 13.3 13.3Z"/></svg></span>
        <h3>[Titel]</h3>
        <p>[Eén regel uitleg]</p>
        <span class="rmk-entry__more">[Linktekst]<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
      </a>
      <a class="rmk-entry" href="[url]">
        <span class="rmk-entry__icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/><path d="M15 8.6a4 4 0 1 0 0 6.8M7.5 11h5.5M7.5 13.2h5.5"/></svg></span>
        <h3>[Titel]</h3>
        <p>[Eén regel uitleg]</p>
        <span class="rmk-entry__more">[Linktekst]<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
      </a>
    </div>
  </div>
</section>
<section class="rmk-section rmk-section--brand" aria-labelledby="hulp">
  <div class="rmk-container rmk-column rmk-split" style="align-items: center">
    <div class="rmk-stack" style="flex: 1 1 20rem; display: flex; flex-direction: column; gap: 16px; align-items: flex-start">
      <h2 id="hulp">Begin bij je tuin, niet bij het merk</h2>
      <p>[Eén of twee zinnen over de keuzehulp]</p>
      <a class="rmk-btn rmk-btn--primary" href="/robotmaaier-zonder-draad/#keuzehulp">Naar de keuzehulp</a>
    </div>
    <figure class="rmk-illustration" style="flex: 1 1 20rem"><img src="<?php echo esc_url( RMK_URL ); ?>/illustraties/tuin.svg" alt="" width="640" height="400" loading="lazy"></figure>
  </div>
</section>
<!-- /wp:html -->
<!-- wp:shortcode -->
[rmk_onlangs_bijgewerkt]
<!-- /wp:shortcode -->
<!-- wp:html -->
<section class="rmk-section rmk-section--dark" aria-labelledby="hoe">
  <div class="rmk-container rmk-column">
    <div class="rmk-section-head" style="margin-bottom: 0">
      <h2 id="hoe">Hoe we beoordelen</h2>
      <p>[Eén zin over het scoremodel]</p>
      <a href="/hoe-we-beoordelen/" style="font-weight: 700">Lees hoe we beoordelen</a>
    </div>
  </div>
</section>
<!-- /wp:html -->
</main>
<!-- /wp:group -->
