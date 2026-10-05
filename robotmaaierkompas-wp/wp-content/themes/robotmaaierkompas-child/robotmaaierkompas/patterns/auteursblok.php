<?php
/**
 * Title: RMK – Auteursblok
 * Slug: robotmaaierkompas/auteursblok
 * Categories: robotmaaierkompas
 * Description: Auteur, rol, korte bio, laatst nagekeken.
 * Viewport Width: 1280
 *
 * Foto: de bijlage "mandy-van-den-broek-400" uit Media (alt-tekst uit Media). Zonder bijlage: initialen.
 */
$rmk_foto = get_posts( array( 'post_type' => 'attachment', 'name' => 'mandy-van-den-broek-400', 'numberposts' => 1, 'post_status' => 'inherit' ) );
$rmk_img  = $rmk_foto ? wp_get_attachment_image( $rmk_foto[0]->ID, array( 96, 96 ), false, array( 'class' => 'rmk-avatar', 'loading' => 'lazy' ) ) : '<div class="rmk-avatar" aria-hidden="true">MB</div>';

?>
<!-- wp:html -->
<div class="rmk-author">
  <?php echo $rmk_img; // phpcs:ignore ?>
  <div class="rmk-author__body">
    <p class="rmk-author__name">Mandy van den Broek</p>
    <div class="rmk-author__roles"><span class="rmk-chip">[rol]</span></div>
    <p class="rmk-small">[Eén of twee zinnen relevante, controleerbare ervaring.] Vergelijkt en analyseert; test niet zelf.</p>
    <p class="rmk-small">Laatst nagekeken op [datum] · <a href="/over-ons/mandy-van-den-broek/">Profiel</a></p>
  </div>
</div>
<!-- /wp:html -->
