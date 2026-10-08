<?php
/**
 * robotmaaierkompas.nl — redactie (1.3.5): automatische datums en de affiliate-melding.
 *
 * Datums: de datum in de paginakop (<p class="rmk-meta">… bijgewerkt op 5 oktober 2026</p>, op juridische
 * pagina's "Laatst bijgewerkt: oktober 2026") en in het eerlijkheidsblok (.rmk-honesty__text, "Bijgewerkt op …")
 * wordt bij het renderen vervangen door de datum van de laatste wijziging van de pagina, net als
 * "Laatst nagekeken op" in het auteursblok (inc/auteur.php). Andere datums (per model in tabellen, "gezien op"
 * bij prijzen) blijven zoals ze in de tekst staan.
 *
 * Affiliate-melding (instellen in wp-config.php, niet in git):
 *   define( 'RMK_AFFILIATE_ACTIVE', true );   // standaard uit: de regel "Advertentie: …" wordt dan niet getoond
 * Zolang de instelling uit staat, haalt het thema elke <p class="rmk-affnote"> uit de uitvoer: uit het patroon
 * robotmaaierkompas/affiliate-melding en uit losse kopieën in de inhoud (bijv. het patroon kop-aan-kop).
 */

defined( 'ABSPATH' ) || exit;

/** Staan de affiliatelinks aan? Standaard niet. */
function rmk_affiliate_actief() {
	return defined( 'RMK_AFFILIATE_ACTIVE' ) && RMK_AFFILIATE_ACTIVE;
}

/** "8 oktober 2026" als <time> met de wijzigingsdatum van pagina $id. */
function rmk_wijzigingsdatum_html( $id ) {
	return '<time datetime="' . esc_attr( get_post_modified_time( 'Y-m-d', false, $id ) ) . '" data-rmk-modified>' . esc_html( get_the_modified_date( 'j F Y', $id ) ) . '</time>';
}

/** Vervangt de vaste datums in de paginakop en het eerlijkheidsblok door de wijzigingsdatum. */
function rmk_datums_automatisch( $html, $id ) {
	$maand = '(?:januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december)';
	$datum = '(?:\d{1,2}\s+' . $maand . '\s+\d{4}|' . $maand . '\s+\d{4})';
	$tijd  = rmk_wijzigingsdatum_html( $id );
	$vervang = function ( $m ) use ( $datum, $tijd ) {
		return preg_replace( '/((?:[Bb]ijgewerkt op|Laatst bijgewerkt:)\s*)' . $datum . '/u', '${1}' . $tijd, $m[0], 1 );
	};
	// Paginakop: <p class="rmk-meta">…</p>
	$html = preg_replace_callback( '/<p class="rmk-meta"[^>]*>.*?<\/p>/su', $vervang, $html );
	// Eerlijkheidsblok: de eerste alinea in .rmk-honesty__text
	$html = preg_replace_callback( '/<div class="rmk-honesty__text"[^>]*>\s*<p>.*?<\/p>/su', $vervang, $html );
	return $html;
}

add_filter( 'render_block', function ( $content, $block ) {
	if ( 'core/html' !== $block['blockName'] ) {
		return $content;
	}
	if ( ! rmk_affiliate_actief() && false !== strpos( $content, 'rmk-affnote' ) ) {
		$content = preg_replace( '/<p class="rmk-affnote"[^>]*>.*?<\/p>\s*/su', '', $content );
	}
	if ( false !== strpos( $content, 'rmk-meta' ) || false !== strpos( $content, 'rmk-honesty__text' ) ) {
		$id = get_the_ID() ? get_the_ID() : get_queried_object_id();
		if ( $id && 'page' === get_post_type( $id ) ) {
			$content = rmk_datums_automatisch( $content, $id );
		}
	}
	return $content;
}, 16, 2 );
