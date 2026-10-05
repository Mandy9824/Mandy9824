<?php
/**
 * Title: RMK – Productbox (eerste op de pagina)
 * Slug: robotmaaierkompas/productbox
 * Categories: robotmaaierkompas
 * Description: Productbox met de lege prijstoestand "Bekijk de prijs bij de winkel" (voorlopig geen winkelprijzen en geen winkelknoppen).
 * Viewport Width: 1280
 */
?>
<!-- wp:html -->
<article class="rmk-product rmk-product--top" aria-labelledby="p-[model-slug]">
  <div class="rmk-product__head">
    <div class="rmk-product__media"><!-- Vervang door <img src="..." alt="[Modelnaam]" width="400" height="400" loading="lazy"> zodra er een foto met toestemming is. --><div class="rmk-ph"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 15.5c0-3.6 4-6.5 9-6.5s9 2.9 9 6.5v1H3v-1Z"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/></svg><span>Foto volgt</span></div></div>
    <div class="rmk-product__title">
      <span class="rmk-rank">[positie] · [categorie]</span>
      <h3 id="p-[model-slug]">[Modelnaam]</h3>
      <p class="rmk-bestfor"><span>Beste voor</span><b>[beste voor]</b></p>
      <div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div>
      <p class="rmk-reviews"><b>[gemiddelde]</b> van 5 uit <b>[aantal]</b> reviews <span class="rmk-src">Bron: [winkel], geteld op [datum]</span></p>
    </div>
  </div>
  <div class="rmk-proscons">
    <div><h4>Pluspunten</h4><ul class="rmk-pros"><li>[pluspunt]</li><li>[pluspunt]</li></ul></div>
    <div><h4>Minpunten</h4><ul class="rmk-cons"><li>[minpunt]</li><li>[minpunt]</li></ul></div>
  </div>
  <div class="rmk-product__aside rmk-offers">
    <div class="rmk-offer"><span class="rmk-offer__shop">[winkel]</span><span class="rmk-offer__price rmk-offer__price--empty">Bekijk de prijs bij de winkel</span><span class="rmk-offer__src">We tonen voorlopig geen winkelprijzen.</span></div>
  </div>
</article>
<!-- /wp:html -->
