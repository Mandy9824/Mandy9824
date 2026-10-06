<?php
/**
 * Title: RMK – Scoretabel (toplijst)
 * Slug: robotmaaierkompas/scoretabel
 * Categories: robotmaaierkompas
 * Description: Overzicht met berekende score per model; op mobiel een kaartenlijst.
 * Viewport Width: 1280
 */
?>
<!-- wp:html -->
<div class="rmk-tablewrap">
  <table class="rmk-table rmk-table--cards">
    <caption>Scores volgens scoremodel v1.0 (concept tot bevriezing). "Laagste nieuwe prijs" komt uit modellen.json (winkel of fabrikant, hoogstens 14 dagen oud); de datum staat onder de tabel.</caption>
    <thead><tr><th scope="col">#</th><th scope="col">Model</th><th scope="col">Beste voor</th><th scope="col" class="is-num">Score</th><th scope="col" class="is-num">Laagste nieuwe prijs</th><th scope="col"><span class="rmk-sr">Details</span></th></tr></thead>
    <tbody>
      <!-- Eén rij per model. De score wordt berekend uit data-scores (zelfde waarden als in het scoreblok). -->
      <tr><td class="c-rank"><span class="rmk-ranknum">[#]</span></td><th scope="row" class="c-model">[Modelnaam]</th><td class="c-best">[beste voor]</td><td class="is-num c-score"><div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div></td><td class="is-num c-price" data-label="Laagste nieuwe prijs" data-rmk-price="[model-id]"></td><td class="c-go"><a href="#p-[model-slug]">Details</a></td></tr>
      <tr><td class="c-rank"><span class="rmk-ranknum">[#]</span></td><th scope="row" class="c-model">[Modelnaam]</th><td class="c-best">[beste voor]</td><td class="is-num c-score"><div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div></td><td class="is-num c-price" data-label="Laagste nieuwe prijs" data-rmk-price="[model-id]"></td><td class="c-go"><a href="#p-[model-slug]">Details</a></td></tr>
    </tbody>
  </table>
</div>
<!-- /wp:html -->
