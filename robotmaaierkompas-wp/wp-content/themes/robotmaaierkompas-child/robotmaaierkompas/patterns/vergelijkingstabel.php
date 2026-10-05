<?php
/**
 * Title: RMK – Vergelijkingstabel met filters
 * Slug: robotmaaierkompas/vergelijkingstabel
 * Categories: robotmaaierkompas
 * Description: Filter op navigatie, oppervlakte (eigen vuistregel), helling, budget en eindscore. Vereist rmk.js.
 * Viewport Width: 1280
 */
?>
<!-- wp:html -->
<div class="rmk-split" data-rmk-compare style="padding-bottom: 4rem">
  <aside class="rmk-split__side rmk-split__side--sticky" aria-labelledby="flt">
    <form class="rmk-filters">
      <h2 id="flt" style="font-size: var(--rmk-fs-md)">Filters</h2>
      <fieldset>
        <legend>Navigatie</legend>
        <div class="rmk-toggles">
          <label class="rmk-toggle"><input type="checkbox" name="nav" value="draad" checked>Draad</label>
          <label class="rmk-toggle"><input type="checkbox" name="nav" value="rtk" checked>RTK</label>
          <label class="rmk-toggle"><input type="checkbox" name="nav" value="camera" checked>Camera</label>
        </div>
      </fieldset>
      <div class="rmk-field">
        <label class="rmk-label" for="f-m2">Mijn gazon</label>
        <div class="rmk-inputgroup"><input id="f-m2" name="m2" class="rmk-input" inputmode="numeric" autocomplete="off"><span>m²</span></div>
        <label class="rmk-toggle" style="border-radius: 8px; justify-content: flex-start; margin-top: var(--rmk-space-2)"><input type="checkbox" name="zones">Zones of obstakels</label>
        <small data-out="need"></small>
        <details class="rmk-rule"><summary>Eigen vuistregel</summary><p>Geen meting en geen fabrikantnorm. We tonen maaiers waarvan de opgegeven capaciteit minstens 30% groter is dan je gazon, of 50% bij zones of obstakels, zodat de maaier niet aan zijn grens werkt.</p></details>
      </div>
      <div class="rmk-field">
        <label class="rmk-label" for="f-slope">Steilste helling</label>
        <div class="rmk-inputgroup"><input id="f-slope" name="slope" class="rmk-input" inputmode="numeric" autocomplete="off"><span>%</span></div>
      </div>
      <div class="rmk-field">
        <label class="rmk-label" for="f-budget">Budget</label>
        <div class="rmk-inputgroup"><span>€</span><input id="f-budget" name="budget" class="rmk-input" inputmode="numeric" autocomplete="off"></div>
        <small>Modellen zonder actuele prijs blijven zichtbaar.</small>
      </div>
      <label class="rmk-toggle" style="border-radius: 8px; justify-content: flex-start"><input type="checkbox" name="final" value="1">Alleen met eindscore</label>
      <button type="reset" class="rmk-btn rmk-btn--quiet">Filters wissen</button>
    </form>
  </aside>
  <section class="rmk-split__main" aria-labelledby="res" style="display: flex; flex-direction: column; gap: 1rem">
    <div class="rmk-resultbar">
      <h2 id="res" style="font-size: var(--rmk-fs-lg)" aria-live="polite" data-rmk-count>Modellen</h2>
      <div class="rmk-field" style="flex-direction: row; align-items: center; gap: .5rem">
        <label for="f-sort" class="rmk-meta">Sorteer op</label>
        <select id="f-sort" name="sort" class="rmk-select" style="width: auto"><option value="score">Score</option><option value="price">Prijs, laag naar hoog</option><option value="capacity">Capaciteit</option></select>
      </div>
    </div>
    <div class="rmk-legend" aria-label="Legenda status">
      <div><span class="rmk-status rmk-status--ok">Gecontroleerd</span></div><div><span class="rmk-status rmk-status--maker">Fabrikantclaim</span></div><div><span class="rmk-status rmk-status--shop">Winkelclaim</span></div><div><span class="rmk-status rmk-status--conflict">Tegenstrijdig</span></div><div><span class="rmk-status rmk-status--missing">Niet gevonden</span></div>
      <div><a href="/hoe-we-beoordelen/#statussen">Wat betekenen de statussen?</a></div>
    </div>
    <div class="rmk-tablewrap" role="region" aria-labelledby="res" tabindex="0">
      <table class="rmk-table rmk-table--sticky" style="min-width: 920px">
        <caption>Score volgens scoremodel v1.0 (concept tot bevriezing). Prijs: laagste prijs met bron en datum op de productpagina.</caption>
        <thead><tr><th scope="col">Model</th><th scope="col" class="is-num">Score</th><th scope="col">Navigatie</th><th scope="col">Capaciteit</th><th scope="col">Helling</th><th scope="col">Geluid</th><th scope="col">Doorgang</th><th scope="col" class="is-num">Prijs vanaf</th></tr></thead>
        <tbody>
          <!-- Eén rij per model. data-nav: draad | rtk | camera. data-capacity, data-slope, data-price: alleen getallen of leeg. -->
          <tr data-model="[model-slug]" data-nav="[draad|rtk|camera]" data-capacity="[m²]" data-slope="[%]" data-price="[€ of leeg]">
            <th scope="row"><a href="[url model]">[Modelnaam]</a></th>
            <td class="is-num"><div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div></td>
            <td>[navigatie]</td>
            <td><div style="display:flex;flex-direction:column;align-items:flex-start;gap:4px"><span>[waarde] m²</span><span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td>
            <td><div style="display:flex;flex-direction:column;align-items:flex-start;gap:4px"><span>[waarde]%</span><span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td>
            <td><div style="display:flex;flex-direction:column;align-items:flex-start;gap:4px"><span>[waarde] dB(A)</span><span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td>
            <td><div style="display:flex;flex-direction:column;align-items:flex-start;gap:4px"><span>[waarde] cm</span><span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span></div></td>
            <td class="is-num"><div style="display:flex;flex-direction:column;align-items:flex-end;gap:2px"><span class="rmk-num">€ [prijs]</span><span class="rmk-small">Bron: [winkel] · [datum]</span></div></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="rmk-callout" data-rmk-empty hidden><p>Geen modellen passen bij deze filters. Verruim de helling of het budget, of wis de filters.</p></div>
    <p class="rmk-small">Zie je een fout of een nieuwere specificatie? <a href="/redactiebeleid/#correcties">Meld een correctie</a>.</p>
  </section>
</div>
<!-- /wp:html -->
