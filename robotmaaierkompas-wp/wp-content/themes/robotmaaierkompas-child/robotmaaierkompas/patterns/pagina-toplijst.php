<?php
/**
 * Title: RMK pagina – Toplijst
 * Slug: robotmaaierkompas/pagina-toplijst
 * Categories: robotmaaierkompas-paginas
 * Description: Snelkeuze, scoretabel, productboxen, methode, FAQ, bronnen, auteur.
 * Viewport Width: 1280
 * Block Types: core/post-content
 * Post Types: page, post
 */
?>
<!-- wp:group {"tagName":"main","anchor":"inhoud","className":"rmk","layout":{"type":"default"}} -->
<main class="wp-block-group rmk" id="inhoud">
<!-- wp:html -->
<section class="rmk-pageband" aria-labelledby="pagina-titel">
  <div class="rmk-container rmk-column">
    <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li aria-current="page">Beste robotmaaiers</li></ol></nav>
    <header class="rmk-pagehead rmk-pagehead--center">
      <img class="rmk-pageband__mark" src="<?php echo esc_url( RMK_URL ); ?>/logo/icoon-licht.svg" alt="" width="48" height="48">
    <p class="rmk-eyebrow">Toplijst · [maand jaar]</p>
    <h1 id="pagina-titel">De beste robotmaaiers van [jaar]: [aantal] modellen vergeleken</h1>
    <p class="rmk-lead">We vergeleken [aantal] robotmaaiers op specificaties en gebruikersreviews en hielden er [aantal] over die elk in een eigen situatie het sterkst zijn. Kijk eerst naar je tuin, dan naar de score.</p>
    <p class="rmk-meta">Door <a href="[url auteurspagina]">[Naam auteur]</a> · bijgewerkt op [datum]</p>
    </header>
  </div>
</section>
<!-- /wp:html -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column">
<!-- wp:pattern {"slug":"robotmaaierkompas/eerlijkheidsblok"} /-->
</div>
<!-- /wp:group -->
<!-- wp:html -->
<section class="rmk-container rmk-section--tight rmk-column" aria-labelledby="snel" style="display: flex; flex-direction: column; gap: 16px">
  <h2 id="snel" style="font-size: var(--rmk-fs-xl)">Snel kiezen</h2>
  <div class="rmk-grid">
    <a class="rmk-card" href="#p-[model-slug]"><span class="rmk-chip rmk-chip--brand">[categorie]</span><h3>[Modelnaam]</h3><p class="rmk-small">[één regel waarom]</p><div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div></a>
    <a class="rmk-card" href="#p-[model-slug]"><span class="rmk-chip rmk-chip--brand">[categorie]</span><h3>[Modelnaam]</h3><p class="rmk-small">[één regel waarom]</p><div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div></a>
    <a class="rmk-card" href="#p-[model-slug]"><span class="rmk-chip rmk-chip--brand">[categorie]</span><h3>[Modelnaam]</h3><p class="rmk-small">[één regel waarom]</p><div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=[0–10]; navigatie=[0–10]; prijskwaliteit=[0–10]; hellingen=[0–10]; app=[0–10]; veiligheid=[0–10]; geluid=[0–10]; reviews=[aantal gelezen reviews]"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div></a>
  </div>
</section>
<div class="rmk-container rmk-resultbar rmk-column" style="padding-top: 24px"><h2 style="font-size: var(--rmk-fs-xl)">Alle modellen op een rij</h2><a href="/robotmaaier-test-vergelijking/">Zelf filteren</a></div>
<!-- /wp:html -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column">
<!-- wp:pattern {"slug":"robotmaaierkompas/scoretabel"} /-->
</div>
<!-- /wp:group -->
<!-- wp:html -->
<div class="rmk-container rmk-column" style="padding-top: 24px"><h2 style="font-size: var(--rmk-fs-xl)">De modellen</h2></div>
<!-- /wp:html -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column">
<!-- wp:pattern {"slug":"robotmaaierkompas/productbox"} /-->
</div>
<!-- /wp:group -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column">
<!-- wp:pattern {"slug":"robotmaaierkompas/productbox-zonder-prijs"} /-->
</div>
<!-- /wp:group -->
<!-- wp:html -->
<section class="rmk-container rmk-section rmk-column" aria-labelledby="hoe">
  <div class="rmk-prose">
    <h2 id="hoe" style="margin-top: 0; font-size: var(--rmk-fs-xl)">Zo hebben we vergeleken</h2>
    <p>Voor elk model verzamelen we specificaties en geven we elke waarde een status: gecontroleerd, fabrikantclaim, winkelclaim, tegenstrijdig of niet gevonden. Ons scoremodel beoordeelt zeven onderdelen op een schaal van 0 tot 10.</p>
    <p>Een eindscore (0 tot 100) tonen we alleen als alle zeven onderdelen bekend zijn. Betrouwbaarheid telt pas mee vanaf 50 gelezen reviews. Bij vijf of zes bekende onderdelen zie je een functiescore met het label "voorlopig, zonder" en de ontbrekende onderdelen; bij minder dan vijf geven we geen score.</p>
    <p><a href="/hoe-we-beoordelen/#scoremodel">Lees de volledige methode</a></p>
  </div>
</section>
<div class="rmk-container rmk-column"><h2 style="font-size: var(--rmk-fs-xl)">Veelgestelde vragen</h2></div>
<!-- /wp:html -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column">
<!-- wp:pattern {"slug":"robotmaaierkompas/faq"} /-->
</div>
<!-- /wp:group -->
<!-- wp:html -->
<div class="rmk-container rmk-column" style="padding-top: 24px"><h2 style="font-size: var(--rmk-fs-xl)">Bronnen</h2></div>
<!-- /wp:html -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column">
<!-- wp:pattern {"slug":"robotmaaierkompas/bronnenlijst"} /-->
</div>
<!-- /wp:group -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column">
<!-- wp:pattern {"slug":"robotmaaierkompas/auteursblok"} /-->
</div>
<!-- /wp:group -->
</main>
<!-- /wp:group -->
