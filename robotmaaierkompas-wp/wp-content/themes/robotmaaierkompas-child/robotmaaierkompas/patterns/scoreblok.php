<?php
/**
 * Title: RMK – Scoreblok
 * Slug: robotmaaierkompas/scoreblok
 * Categories: robotmaaierkompas
 * Description: Scoremodel v1.0: zeven onderdelen (0–10), eindscore 0–100. Label wordt berekend: Eindscore, Functiescore (met uitleg) of geen score.
 * Viewport Width: 1280
 */
?>
<!-- wp:html -->
<section class="rmk-score" data-rmk-score aria-labelledby="score-[model-slug]">
  <!-- Vul per onderdeel data-value in (0 tot 10, of leeg laten als het onbekend is). Betrouwbaarheid telt pas mee vanaf 50 gelezen reviews (data-reviews).
       Label en score worden berekend: 7 van 7 bekend = Eindscore; 5 of 6 = Functiescore met de regel "Functiescore: wat deze maaier kan. Hoe we scoren"; minder dan 5 = geen score. -->
  <div class="rmk-score__head">
    <div class="rmk-score__total"><b data-out="total">–</b><span>/ 100</span></div>
    <div class="rmk-score__kind"><strong id="score-[model-slug]" data-out="kind">Score</strong><span class="rmk-provisional" data-out="label" hidden></span></div>
  </div>
  <div class="rmk-scale" role="img" data-out="bar" aria-label="Score"><i style="width:0%"></i></div>
  <ul class="rmk-parts">
    <li class="rmk-part" data-key="betrouwbaarheid" data-value="[0–10]" data-reviews="[aantal gelezen reviews]"><span class="rmk-part__label">Betrouwbaarheid uit reviews <small>25%</small></span><span class="rmk-part__val">[0–10]</span><div class="rmk-bar" role="img" aria-label="[0–10]"><i style="width:0%"></i></div></li>
    <li class="rmk-part" data-key="navigatie" data-value="[0–10]"><span class="rmk-part__label">Navigatie en dekking <small>20%</small></span><span class="rmk-part__val">[0–10]</span><div class="rmk-bar" role="img" aria-label="[0–10] van 10"><i style="width:0%"></i></div></li>
    <li class="rmk-part" data-key="prijskwaliteit" data-value="[0–10]"><span class="rmk-part__label">Prijs-kwaliteit <small>20%</small></span><span class="rmk-part__val">[0–10]</span><div class="rmk-bar" role="img" aria-label="[0–10] van 10"><i style="width:0%"></i></div></li>
    <li class="rmk-part" data-key="hellingen" data-value="[0–10]"><span class="rmk-part__label">Hellingen en terrein <small>10%</small></span><span class="rmk-part__val">[0–10]</span><div class="rmk-bar" role="img" aria-label="[0–10] van 10"><i style="width:0%"></i></div></li>
    <li class="rmk-part" data-key="app" data-value="[0–10]"><span class="rmk-part__label">App en bediening <small>10%</small></span><span class="rmk-part__val">[0–10]</span><div class="rmk-bar" role="img" aria-label="[0–10] van 10"><i style="width:0%"></i></div></li>
    <li class="rmk-part" data-key="veiligheid" data-value="[0–10]"><span class="rmk-part__label">Veiligheid <small>10%</small></span><span class="rmk-part__val">[0–10]</span><div class="rmk-bar" role="img" aria-label="[0–10] van 10"><i style="width:0%"></i></div></li>
    <li class="rmk-part" data-key="geluid" data-value="[0–10]"><span class="rmk-part__label">Geluid <small>5%</small></span><span class="rmk-part__val">[0–10]</span><div class="rmk-bar" role="img" aria-label="[0–10] van 10"><i style="width:0%"></i></div></li>
  </ul>
  <p class="rmk-small" data-out="note"></p>
  <div class="rmk-score__foot"><span>Bijgewerkt op [datum]</span><span>Scoremodel v1.0 (concept tot bevriezing)</span><a href="/hoe-we-beoordelen/#scoremodel">Hoe we scoren</a></div>
</section>
<!-- /wp:html -->
