<?php
/**
 * Title: RMK – Productbox (eerste op de pagina)
 * Slug: robotmaaierkompas/productbox
 * Categories: robotmaaierkompas
 * Description: Productbox. Het prijsblok wordt bij het weergeven ingevuld uit modellen.json (inc/prijzen.php): een geldige prijs met knop "Bekijk bij (winkel)", anders "Bekijk de actuele prijs" naar de fabrikant.
 * Viewport Width: 1280
 */
?>
<!-- wp:html -->
<article class="rmk-product rmk-product--top" aria-labelledby="p-[model-slug]">
  <div class="rmk-product__head">
    <!-- Specificatiekaart (pakket v1.3). In pagina's met data-model in de scorecel wordt deze kaart bij het weergeven gevuld uit modellen.json; met foto wordt het de fotovariant met "Foto: (fabrikant)". --><div class="rmk-speccard"><figure class="rmk-speccard__figure"><div class="rmk-speccard__visual" aria-hidden="true"><p class="rmk-speccard__brand">[Merk]</p><p class="rmk-speccard__model">[Modelnaam]</p></div><figcaption class="rmk-speccard__caption">Geen productfoto beschikbaar</figcaption></figure><dl class="rmk-speccard__specs" aria-label="Belangrijkste kenmerken"><div class="rmk-spec rmk-spec--oppervlak"><dt>Oppervlak</dt><dd>[m²] m²</dd></div><div class="rmk-spec rmk-spec--helling"><dt>Helling</dt><dd>[%]%</dd></div><div class="rmk-spec rmk-spec--navigatie"><dt>Navigatie</dt><dd>[RTK | camera | LiDAR | draad]</dd></div><div class="rmk-spec rmk-spec--geluid"><dt>Geluid</dt><dd>[dB] dB</dd></div><div class="rmk-spec rmk-spec--verbinding"><dt>Verbinding</dt><dd>[4G | module | geen]</dd></div></dl></div>
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
    <div class="rmk-offer"><a class="rmk-btn rmk-btn--secondary" href="[fabrikantpagina]">Bekijk de actuele prijs</a></div>
  </div>
</article>
<!-- /wp:html -->
