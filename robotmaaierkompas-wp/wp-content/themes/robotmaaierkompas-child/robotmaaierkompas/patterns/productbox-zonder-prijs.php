<?php
/**
 * Title: RMK – Productbox (prijs wordt bijgewerkt / leeg)
 * Slug: robotmaaierkompas/productbox-zonder-prijs
 * Categories: robotmaaierkompas
 * Description: Toestanden: geen foto, prijs wordt bijgewerkt, leeg prijsveld, nog geen reviews.
 * Viewport Width: 1280
 */
?>
<!-- wp:html -->
<article class="rmk-product" aria-labelledby="p-[model-slug]">
  <div class="rmk-product__head">
    <div class="rmk-product__media"><!-- Met foto (alleen met een duidelijke gebruiksvoorwaarde): vervang de figure door het fotokader uit patterns-bron/afwerking/fotokader.html, met rmk-photo--square en het bijschrift "Foto: [fabrikant]". Zonder foto wordt dit blok bij het weergeven weggehaald. --><figure class="rmk-photo rmk-photo--square rmk-photo--placeholder"><div class="rmk-photo__frame"><img src="<?php echo esc_url( RMK_URL ); ?>/illustraties/foto-plaatsvervanger.svg" alt="" width="400" height="300"></div><figcaption>Foto volgt</figcaption></figure></div>
    <div class="rmk-product__title">
      <span class="rmk-rank">[positie] · [categorie]</span>
      <h3 id="p-[model-slug]">[Modelnaam]</h3>
      <p class="rmk-bestfor"><span>Beste voor</span><b>[beste voor]</b></p>
      <div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div>
      <p class="rmk-reviews"><span>Nog geen reviews gevonden</span> <span class="rmk-src">Gezocht op [winkel] op [datum]</span></p>
    </div>
  </div>
  <div class="rmk-proscons">
    <div><h4>Pluspunten</h4><ul class="rmk-pros"><li>[pluspunt]</li></ul></div>
    <div><h4>Minpunten</h4><ul class="rmk-cons"><li>[minpunt]</li></ul></div>
  </div>
  <div class="rmk-product__aside rmk-offers">
    <div class="rmk-offer"><a class="rmk-btn rmk-btn--secondary" href="[fabrikantpagina]">Bekijk de actuele prijs</a></div>
  </div>
</article>
<!-- /wp:html -->
