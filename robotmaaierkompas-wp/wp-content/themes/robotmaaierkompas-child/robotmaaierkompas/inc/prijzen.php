<?php
/**
 * robotmaaierkompas.nl — prijs en knop in de productbox (besluit 6 oktober 2026)
 *
 * Bron: per model het veld "prijs" in modellen.json ({bedrag, winkel, datum, url, type}), gemaakt door
 * scripts/excel_naar_json.py uit het blad Prijzen. Een prijs wordt alleen getoond als hij geldig is:
 * - nieuw exemplaar en op voorraad (het script neemt alleen zulke regels over);
 * - van een winkel of de fabrikant (type "winkel" of "fabrikant"), geen marketplace, geen Bol;
 * - gezien op een datum van hoogstens 14 dagen geleden (RMK_PRIJS_MAX_DAGEN). Daarna verdwijnt hij vanzelf.
 * Tekst: "Laagste nieuwe prijs rond 899 euro bij Coolblue, gezien op 5 oktober 2026", met daaronder de knop
 * "Bekijk bij Coolblue": een gewone externe link naar de productpagina, zonder affiliatelink.
 * Geen geldige prijs: alleen de knop "Bekijk de actuele prijs" naar de fabrikantpagina (veld fabrikant_url).
 * Geen van beide: geen prijsblok.
 *
 * De productboxen in de pagina's hebben een scorecel met data-model="M002"; het prijsblok in die box wordt
 * bij het weergeven vervangen. Elke nacht leegt een taak de LiteSpeed-cache als er een prijs verlopen is.
 */

defined( 'ABSPATH' ) || exit;

const RMK_PRIJS_MAX_DAGEN = 14;

/** Domeinen waarvan we nooit een prijs of knop tonen: Bol en marketplaces. */
function rmk_price_blocked_hosts() {
	return apply_filters( 'rmk_price_blocked_hosts', array( 'bol.com', 'amazon.nl', 'amazon.de', 'amazon.com', 'amzn.to', 'ebay.nl', 'ebay.de', 'marktplaats.nl', 'aliexpress.com', 'temu.com', 'awin1.com', 'zenaps.com', 'ds1.nl' ) );
}

function rmk_price_url_ok( $url ) {
	$parts = wp_parse_url( (string) $url );
	if ( empty( $parts['scheme'] ) || 'https' !== strtolower( $parts['scheme'] ) || empty( $parts['host'] ) ) {
		return false;
	}
	$host = strtolower( preg_replace( '/^www\./i', '', $parts['host'] ) );
	foreach ( rmk_price_blocked_hosts() as $d ) {
		if ( $host === $d || substr( $host, -strlen( '.' . $d ) ) === '.' . $d ) {
			return false;
		}
	}
	return true;
}

/** Leeftijd in dagen van een datum (JJJJ-MM-DD) ten opzichte van vandaag in de tijdzone van de site; null bij een ongeldige datum. */
function rmk_price_age_days( $date, $today = null ) {
	$tz = wp_timezone();
	$d  = DateTimeImmutable::createFromFormat( '!Y-m-d', (string) $date, $tz );
	if ( ! $d || $d->format( 'Y-m-d' ) !== $date ) {
		return null;
	}
	$t = $today ? DateTimeImmutable::createFromFormat( '!Y-m-d', $today, $tz ) : new DateTimeImmutable( 'today', $tz );
	return (int) $d->diff( $t )->format( '%r%a' );
}

/** De geldige prijs van een model, of null. */
function rmk_valid_price( array $m, $today = null ) {
	$p = isset( $m['prijs'] ) && is_array( $m['prijs'] ) ? $m['prijs'] : null;
	if ( ! $p || ! isset( $p['bedrag'], $p['winkel'], $p['datum'], $p['url'] ) ) {
		return null;
	}
	if ( ! is_numeric( $p['bedrag'] ) || $p['bedrag'] <= 0 || '' === trim( (string) $p['winkel'] ) ) {
		return null;
	}
	if ( ! in_array( isset( $p['type'] ) ? $p['type'] : '', array( 'winkel', 'fabrikant' ), true ) || ! rmk_price_url_ok( $p['url'] ) ) {
		return null;
	}
	if ( false !== stripos( $p['winkel'], 'bol' ) ) {
		return null;
	}
	$age = rmk_price_age_days( $p['datum'], $today );
	if ( null === $age || $age < 0 || $age > RMK_PRIJS_MAX_DAGEN ) {
		return null;
	}
	return $p;
}

function rmk_date_nl( $date ) {
	$maanden = array( 1 => 'januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december' );
	$d       = DateTimeImmutable::createFromFormat( '!Y-m-d', (string) $date );
	return $d ? $d->format( 'j' ) . ' ' . $maanden[ (int) $d->format( 'n' ) ] . ' ' . $d->format( 'Y' ) : '';
}

/** Prijsblok voor de productbox. */
function rmk_offer_html( array $m, $today = null ) {
	$p = rmk_valid_price( $m, $today );
	if ( $p ) {
		$winkel = trim( (string) $p['winkel'] );
		$bedrag = number_format( round( (float) $p['bedrag'] ), 0, ',', '.' );
		return '<div class="rmk-offer rmk-offer--stack"><span class="rmk-offer__line">Laagste nieuwe prijs rond <strong>' . esc_html( $bedrag ) . ' euro</strong> bij '
			. esc_html( $winkel ) . ', gezien op ' . esc_html( rmk_date_nl( $p['datum'] ) ) . '</span>'
			. '<a class="rmk-btn rmk-btn--primary" href="' . esc_url( $p['url'] ) . '" data-rmk-direct>Bekijk bij ' . esc_html( $winkel ) . '</a></div>';
	}
	$fab = isset( $m['fabrikant_url'] ) ? (string) $m['fabrikant_url'] : '';
	if ( $fab && rmk_price_url_ok( $fab ) ) {
		return '<div class="rmk-offer rmk-offer--stack"><a class="rmk-btn rmk-btn--secondary" href="' . esc_url( $fab ) . '" data-rmk-direct>Bekijk de actuele prijs</a></div>';
	}
	return '';
}

/** Vervangt in elke productbox (article.rmk-product met data-model) het prijsblok door rmk_offer_html(). */
function rmk_fill_offers( $html ) {
	if ( false === strpos( (string) $html, 'rmk-product' ) || false === strpos( (string) $html, 'rmk-offer' ) ) {
		return $html;
	}
	return preg_replace_callback( '#<article class="rmk-product"[^>]*>.*?</article>#s', function ( $a ) {
		if ( ! preg_match( '#data-model="([A-Za-z0-9-]+)"#', $a[0], $id ) || ! ( $m = rmk_get_model( $id[1] ) ) ) {
			return $a[0];
		}
		$offer = rmk_offer_html( $m );
		$done  = false;
		return preg_replace_callback( '#<div class="rmk-offer(?: [^"]*)?"[^>]*>(?:(?!</div>).)*</div>#s', function () use ( $offer, &$done ) {
			$out  = $done ? '' : $offer;
			$done = true;
			return $out;
		}, $a[0] );
	}, $html );
}
add_filter( 'render_block', function ( $content, $block ) {
	return 'core/html' === $block['blockName'] ? rmk_fill_offers( $content ) : $content;
}, 12, 2 ); // vóór de server-side score (prioriteit 15 en 16), die data-model uit de scorecel haalt

/* Elke nacht: is er sinds gisteren een prijs verlopen, leeg dan de paginacache zodat hij ook daar verdwijnt. */
add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'rmk_prijzen_verloop' ) ) {
		$t = new DateTimeImmutable( 'tomorrow 00:10', wp_timezone() );
		wp_schedule_event( $t->getTimestamp(), 'daily', 'rmk_prijzen_verloop' );
	}
} );
add_action( 'rmk_prijzen_verloop', function () {
	$tz        = wp_timezone();
	$gisteren  = ( new DateTimeImmutable( 'yesterday', $tz ) )->format( 'Y-m-d' );
	$verlopen  = false;
	foreach ( rmk_models_data()['modellen'] as $m ) {
		if ( rmk_valid_price( $m, $gisteren ) && ! rmk_valid_price( $m ) ) {
			$verlopen = true;
		}
	}
	if ( $verlopen ) {
		do_action( 'litespeed_purge_all' );
	}
} );
