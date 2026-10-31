<?php
/**
 * robotmaaierkompas.nl — Amazon-knop op de productkaart (1.3.13).
 *
 * Bron: blad Amazon van robotmaaierkompas_modeldata_v1.xlsx (31 oktober 2026) en tekstwijzigingen-amazon-affiliate.md
 * punt 9. Per model alleen de ASIN en of er een knop mag komen ("Knop: ja" in kolom J). Niets daarbuiten.
 *
 * Instellen (in wp-config.php op de server; geen geheimen):
 *   define( 'RMK_AMAZON_TAG', 'robotmaaier-21' );   // de tracking-ID van het Amazon-partnerprogramma
 *   define( 'RMK_AMAZON_ACTIVE', true );            // de schakelaar; standaard uit
 * Ontbreekt een van de twee (of is de tag geen geldige tag die eindigt op -21): nergens een Amazon-knop, en elke
 * pagina is byte voor byte gelijk aan 1.3.12. Onafhankelijk van RMK_AFFILIATE_ACTIVE (Bol) en RMK_COOLBLUE_ACTIVE.
 *
 * De knop is een gewone, statische link (werkt zonder JavaScript), altijd ONDER de Bol- en Coolblue-regel:
 *   <a href="https://www.amazon.nl/dp/<ASIN>?tag=<RMK_AMAZON_TAG>" rel="sponsored nofollow">Bekijk bij Amazon</a>
 *   "Je gaat naar Amazon.nl. Prijs, beschikbaarheid en verkoper bekijk je daar."
 * Geen andere parameters, geen verkorte links. Geen prijs, foto, beoordelingen, doorgestreepte prijs of korting van
 * Amazon: het thema doet geen enkel verzoek naar Amazon (geen API, geen feed, geen afbeelding).
 *
 * Modelgegevens: blok "amazon" = { "asin": "B0…", "knop": true|false } (zie inc/data.php en scripts/excel_naar_json.py).
 * Een knop alleen bij knop === true en een geldige ASIN, en nooit bij een model in rmk_amazon_uitgesloten().
 */

defined( 'ABSPATH' ) || exit;

/**
 * Modellen die nooit een Amazon-knop krijgen, ook niet met "Knop: ja" in het blad Amazon (model-ID => reden).
 * M050 (Worx WR165E): bij de hercontrole op 31-10-2026 verkocht een partner (Nesk®) de standaardaanbieding in plaats
 * van Amazon zelf (besluit Mandy, ronde 74). Weghalen kan alleen met een nieuwe themaversie.
 */
function rmk_amazon_uitgesloten() {
	return (array) apply_filters( 'rmk_amazon_uitgesloten', array(
		'M050' => 'Standaardaanbieding bij een partner (Nesk®) in plaats van Amazon zelf (hercontrole 31-10-2026).',
	) );
}

/** Geldige tracking-ID (Amazon.nl eindigt op -21), of ''. */
function rmk_amazon_tag() {
	if ( ! defined( 'RMK_AMAZON_TAG' ) ) {
		return '';
	}
	$tag = trim( (string) RMK_AMAZON_TAG );
	return preg_match( '/^[a-z0-9][a-z0-9-]{0,60}-21$/', $tag ) ? $tag : '';
}

/** Mag er een Amazon-knop op de site? Alleen met een geldige RMK_AMAZON_TAG én RMK_AMAZON_ACTIVE aan. */
function rmk_amazon_zichtbaar() {
	return '' !== rmk_amazon_tag() && defined( 'RMK_AMAZON_ACTIVE' ) && RMK_AMAZON_ACTIVE;
}

/** ASIN: 10 tekens, hoofdletters en cijfers. */
function rmk_amazon_asin_ok( $asin ) {
	return is_string( $asin ) && 1 === preg_match( '/^[A-Z0-9]{10}$/', $asin );
}

/** De ASIN voor de knop van model $m, of '' (geen knop). */
function rmk_amazon_asin( array $m ) {
	if ( empty( $m['id'] ) || empty( $m['amazon'] ) || ! is_array( $m['amazon'] ) ) {
		return '';
	}
	if ( true !== ( $m['amazon']['knop'] ?? null ) || isset( rmk_amazon_uitgesloten()[ $m['id'] ] ) ) {
		return '';
	}
	$asin = $m['amazon']['asin'] ?? '';
	return rmk_amazon_asin_ok( $asin ) ? $asin : '';
}

/** De link, exact https://www.amazon.nl/dp/<ASIN>?tag=<tag>. */
function rmk_amazon_link( $asin, $tag ) {
	return 'https://www.amazon.nl/dp/' . $asin . '?tag=' . $tag;
}

/** De Amazon-regel in de productkaart (onder Bol en Coolblue), of ''. */
function rmk_amazon_regel_html( array $m ) {
	if ( ! rmk_amazon_zichtbaar() ) {
		return '';
	}
	$asin = rmk_amazon_asin( $m );
	if ( '' === $asin ) {
		return '';
	}
	// esc_attr() in plaats van esc_url(): de link moet exact blijven. ASIN en tag zijn hierboven streng gecontroleerd
	// (alleen letters, cijfers en koppeltekens), dus esc_attr() verandert er niets aan.
	return '<div class="rmk-offer rmk-offer--stack rmk-offer--amazon" data-rmk-amazon="' . esc_attr( $m['id'] ) . '">'
		. '<a class="rmk-btn rmk-btn--primary" href="' . esc_attr( rmk_amazon_link( $asin, rmk_amazon_tag() ) ) . '" rel="sponsored nofollow">Bekijk bij Amazon</a>'
		. '<span class="rmk-offer__src">Je gaat naar Amazon.nl. Prijs, beschikbaarheid en verkoper bekijk je daar.</span></div>';
}

/** Voor het statusoverzicht: alleen of de constanten er zijn (de tag is geen geheim, maar wordt niet getoond). */
function rmk_amazon_status_tekst() {
	if ( '' === rmk_amazon_tag() ) {
		return defined( 'RMK_AMAZON_TAG' ) ? 'uit: RMK_AMAZON_TAG is geen geldige tag (eindigt op -21)' : 'uit: RMK_AMAZON_TAG ontbreekt (geen Amazon-knop)';
	}
	if ( ! rmk_amazon_zichtbaar() ) {
		return 'tag aanwezig, Amazon-knop verborgen (RMK_AMAZON_ACTIVE uit)';
	}
	$n = 0;
	foreach ( rmk_models_data()['modellen'] as $m ) {
		$n += '' !== rmk_amazon_asin( $m ) ? 1 : 0;
	}
	return 'tag aanwezig, Amazon-knop zichtbaar (' . $n . ' modellen met een knop in de modelgegevens)';
}
