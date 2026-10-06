<?php
/**
 * Title: RMK – Footer
 * Slug: robotmaaierkompas/footer
 * Categories: robotmaaierkompas, footer
 * Description: Logo, eerlijkheidsverklaring, verdienmodel, navigatie, juridische links.
 * Viewport Width: 1280
 * Block Types: core/template-part/footer
 */
?>
<!-- wp:html -->
<footer class="rmk-footer">
  <div class="rmk-container rmk-footer__top">
    <div class="rmk-footer__brand">
      <?php echo rmk_logo_html( 'donker' ); // logo uit het afwerkpakket ?>
      <p>Wij vergelijken robotmaaiers op specificaties, kosten en reviews. Zie <a href="/hoe-we-beoordelen/">Hoe we beoordelen</a>.</p>
      <p>Wij kunnen een commissie ontvangen bij aankopen via links op deze site. Zie de <a href="/affiliate-melding/">affiliate-melding</a>.</p>
    </div>
    <nav aria-label="Kiezen">
      <h2>Kiezen</h2>
      <ul><li><a href="/beste-robotmaaier/">Beste robotmaaiers</a></li><li><a href="/vergelijken/">Vergelijkingen</a></li><li><a href="/robotmaaier-kosten/">Kostencalculator</a></li></ul>
    </nav>
    <nav aria-label="Leren">
      <h2>Leren</h2>
      <ul><li><a href="/kopersgids/">Kopersgids</a></li><li><a href="/hulp/">Hulp en onderhoud</a></li></ul>
    </nav>
    <nav aria-label="Over ons">
      <h2>Over ons</h2>
      <ul><li><a href="/hoe-we-beoordelen/">Hoe we beoordelen</a></li><li><a href="/over-ons/">Over ons</a></li><li><a href="/contact/">Contact</a></li><li><a href="/redactiebeleid/">Redactiebeleid en correcties</a></li></ul>
    </nav>
  </div>
  <div class="rmk-container rmk-footer__bottom">
    <span>© robotmaaierkompas.nl · Scoremodel v1.0 (concept tot bevriezing)</span>
    <nav aria-label="Juridisch" style="display: flex; flex-wrap: wrap; gap: 8px 20px">
      <a href="/privacy/">Privacy</a><a href="/cookies/">Cookies</a><a href="/affiliate-melding/">Affiliate-melding</a><a href="/colofon/">Colofon</a><a href="#cookie-instellingen">Cookie-instellingen</a>
    </nav>
  </div>
</footer>
<!-- /wp:html -->
