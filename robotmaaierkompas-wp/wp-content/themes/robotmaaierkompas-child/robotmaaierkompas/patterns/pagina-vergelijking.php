<?php
/**
 * Title: RMK pagina – Vergelijkingen
 * Slug: robotmaaierkompas/pagina-vergelijking
 * Categories: robotmaaierkompas-paginas
 * Description: Filterbare vergelijkingstabel.
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
    <nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li><li aria-current="page">Vergelijkingen</li></ol></nav>
    <header class="rmk-pagehead rmk-pagehead--center">
      <img class="rmk-pageband__mark" src="<?php echo esc_url( RMK_URL ); ?>/logo/icoon-licht.svg" alt="" width="48" height="48">
    <p class="rmk-eyebrow">Vergelijkingstabel</p>
    <h1 id="pagina-titel">Robotmaaiers vergelijken op wat jouw tuin nodig heeft</h1>
    <p class="rmk-lead">Filter op navigatie, oppervlakte, helling en budget. Elke waarde laat zien hoe zeker hij is.</p>
    </header>
  </div>
</section>
<!-- /wp:html -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column">
<!-- wp:pattern {"slug":"robotmaaierkompas/eerlijkheidsblok"} /-->
</div>
<!-- /wp:group -->
<!-- wp:group {"className":"rmk-container rmk-block rmk-column rmk-column--wide","layout":{"type":"default"}} -->
<div class="wp-block-group rmk-container rmk-block rmk-column rmk-column--wide">
<!-- wp:pattern {"slug":"robotmaaierkompas/vergelijkingstabel"} /-->
</div>
<!-- /wp:group -->
</main>
<!-- /wp:group -->
