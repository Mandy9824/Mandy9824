<?php
/**
 * Title: RMK pagina – Kop-aan-kop
 * Slug: robotmaaierkompas/pagina-kop-aan-kop
 * Categories: robotmaaierkompas-paginas
 * Description: Twee modellen naast elkaar.
 * Viewport Width: 1280
 * Block Types: core/post-content
 * Post Types: page, post
 */
?>
<!-- wp:group {"tagName":"main","anchor":"inhoud","className":"rmk","layout":{"type":"default"}} -->
<main class="wp-block-group rmk" id="inhoud">
<!-- wp:html -->
<div class="rmk-container rmk-column">
  <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li><a href="/vergelijken/">Vergelijkingen</a></li><li aria-current="page">[Model A] of [Model B]</li></ol></nav>
  <header class="rmk-pagehead">
    <p class="rmk-eyebrow">Kop-aan-kop</p>
    <h1>[Model A] of [Model B]: [het belangrijkste verschil]</h1>
    <p class="rmk-lead">[Twee zinnen: wat de modellen gemeen hebben en waar ze verschillen.]</p>
  </header>
</div>
<!-- /wp:html -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column">
<!-- wp:pattern {"slug":"robotmaaierkompas/eerlijkheidsblok"} /-->
</div>
<!-- /wp:group -->
<!-- wp:html -->
<section class="rmk-container rmk-section--tight rmk-column" aria-label="De twee modellen">
  <div class="rmk-h2h">
    <div class="rmk-h2h__col"><div class="rmk-product__media"><!-- Met foto (alleen met een duidelijke gebruiksvoorwaarde): vervang de figure door het fotokader uit patterns-bron/afwerking/fotokader.html, met rmk-photo--square en het bijschrift "Foto: [fabrikant]". Zonder foto wordt dit blok bij het weergeven weggehaald. --><figure class="rmk-photo rmk-photo--square rmk-photo--placeholder"><div class="rmk-photo__frame"><img src="<?php echo esc_url( RMK_URL ); ?>/illustraties/foto-plaatsvervanger.svg" alt="" width="400" height="300"></div><figcaption>Foto volgt</figcaption></figure></div><h2 style="font-size: var(--rmk-fs-lg)">[Model A]</h2><div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div><p class="rmk-bestfor"><span>Beste voor</span><b>[beste voor]</b></p></div>
    <div class="rmk-h2h__col"><div class="rmk-product__media"><!-- Met foto (alleen met een duidelijke gebruiksvoorwaarde): vervang de figure door het fotokader uit patterns-bron/afwerking/fotokader.html, met rmk-photo--square en het bijschrift "Foto: [fabrikant]". Zonder foto wordt dit blok bij het weergeven weggehaald. --><figure class="rmk-photo rmk-photo--square rmk-photo--placeholder"><div class="rmk-photo__frame"><img src="<?php echo esc_url( RMK_URL ); ?>/illustraties/foto-plaatsvervanger.svg" alt="" width="400" height="300"></div><figcaption>Foto volgt</figcaption></figure></div><h2 style="font-size: var(--rmk-fs-lg)">[Model B]</h2><div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div><p class="rmk-bestfor"><span>Beste voor</span><b>[beste voor]</b></p></div>
  </div>
</section>
<section class="rmk-container rmk-section--tight rmk-column" aria-labelledby="verschil" style="display: flex; flex-direction: column; gap: 16px">
  <h2 id="verschil" style="font-size: var(--rmk-fs-xl)">Specificaties naast elkaar</h2>
  <div class="rmk-tablewrap" role="region" aria-labelledby="verschil" tabindex="0">
    <table class="rmk-specs rmk-diff" style="min-width: 640px">
      <thead><tr><th scope="col" style="width: 28%"><span class="rmk-sr">Kenmerk</span></th><th scope="col">[Model A]</th><th scope="col">[Model B]</th></tr></thead>
      <tbody>
        <!-- Zet class="is-win" op de cel met de gunstigste waarde, alleen als beide waarden bekend zijn. -->
        <tr><th scope="row">Navigatie</th><td><div class="rmk-specs__val">[waarde]<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td><td><div class="rmk-specs__val">[waarde]<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td></tr>
        <tr><th scope="row">Maximale oppervlakte</th><td><div class="rmk-specs__val">[waarde] m²<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td><td><div class="rmk-specs__val">[waarde] m²<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td></tr>
        <tr><th scope="row">Maximale helling</th><td><div class="rmk-specs__val">[waarde]%<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td><td><div class="rmk-specs__val">[waarde]%<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td></tr>
        <tr><th scope="row">Geluid</th><td><div class="rmk-specs__val">[waarde] dB(A)<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td><td><div class="rmk-specs__val">[waarde] dB(A)<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td></tr>
        <tr><th scope="row">Verbinding na gratis periode</th><td><div class="rmk-specs__val">[waarde]<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td><td><div class="rmk-specs__val">[waarde]<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td></tr>
      </tbody>
    </table>
  </div>
  <p class="rmk-small">"Beter" geeft alleen aan welke waarde gunstiger is op papier, niet hoe het in jouw tuin uitpakt.</p>
</section>
<section class="rmk-container rmk-section--tight rmk-column" aria-labelledby="oordeel" style="display: flex; flex-direction: column; gap: 16px">
  <h2 id="oordeel" style="font-size: var(--rmk-fs-xl)">Welke past bij jou?</h2>
  <div class="rmk-verdict">
    <div><h3 style="font-size: var(--rmk-fs-md)">Kies [Model A] als…</h3><ul class="rmk-small" style="padding-left: 18px; display: flex; flex-direction: column; gap: 6px; color: var(--rmk-text)"><li>[situatie]</li><li>[situatie]</li></ul></div>
    <div><h3 style="font-size: var(--rmk-fs-md)">Kies [Model B] als…</h3><ul class="rmk-small" style="padding-left: 18px; display: flex; flex-direction: column; gap: 6px; color: var(--rmk-text)"><li>[situatie]</li><li>[situatie]</li></ul></div>
  </div>
</section>
<section class="rmk-container rmk-section--tight rmk-column" aria-labelledby="prijs" style="display: flex; flex-direction: column; gap: 16px; padding-bottom: 64px">
  <h2 id="prijs" style="font-size: var(--rmk-fs-xl)">Prijzen</h2>
  <p class="rmk-affnote"><svg class="rmk-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.01"/></svg><span>Advertentie: via deze knoppen krijgen wij mogelijk een commissie. Dat verandert de vergelijking niet.</span></p>
  <div class="rmk-h2h">
    <div class="rmk-offers"><div class="rmk-offer"><a class="rmk-btn rmk-btn--secondary" href="[fabrikantpagina Model A]">Bekijk de actuele prijs</a></div></div>
    <div class="rmk-offers"><div class="rmk-offer"><a class="rmk-btn rmk-btn--secondary" href="[fabrikantpagina Model B]">Bekijk de actuele prijs</a></div></div>
  </div>
</section>
<!-- /wp:html -->
</main>
<!-- /wp:group -->
