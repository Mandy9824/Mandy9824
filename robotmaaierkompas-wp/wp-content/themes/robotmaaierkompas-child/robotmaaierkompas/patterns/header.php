<?php
/**
 * Title: RMK – Header
 * Slug: robotmaaierkompas/header
 * Categories: robotmaaierkompas, header
 * Description: Logo en hoofdmenu; mobiel menu zonder JavaScript.
 * Viewport Width: 1280
 * Block Types: core/template-part/header
 */
?>
<!-- wp:html -->
<div class="rmk" style="position: relative">
  <a class="rmk-skip" href="#inhoud">Naar de inhoud</a>
  <header class="rmk-header">
    <div class="rmk-container rmk-header__bar">
      <?php echo rmk_logo_html( 'licht' ); // logo uit het afwerkpakket ?>
      <nav class="rmk-nav" aria-label="Hoofdmenu">
        <ul>
          <li><a href="/beste-robotmaaier/">Beste robotmaaiers</a></li>
          <li><a href="/kopersgids/">Kopersgids</a></li>
          <li><a href="/vergelijken/">Vergelijkingen</a></li>
          <li><a href="/hulp/">Hulp en onderhoud</a></li>
          <li><a href="/hoe-we-beoordelen/">Hoe we beoordelen</a></li>
          <li><a href="/over-ons/">Over ons</a></li>
        </ul>
      </nav>
      <details class="rmk-menu">
        <summary><svg class="rmk-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Menu</summary>
        <div class="rmk-menu__panel">
          <ul>
            <li><a href="/beste-robotmaaier/">Beste robotmaaiers</a></li>
            <li><a href="/kopersgids/">Kopersgids</a></li>
            <li><a href="/vergelijken/">Vergelijkingen</a></li>
            <li><a href="/hulp/">Hulp en onderhoud</a></li>
            <li><a href="/hoe-we-beoordelen/">Hoe we beoordelen</a></li>
            <li><a href="/over-ons/">Over ons</a></li>
          </ul>
        </div>
      </details>
    </div>
  </header>
</div>
<!-- /wp:html -->
