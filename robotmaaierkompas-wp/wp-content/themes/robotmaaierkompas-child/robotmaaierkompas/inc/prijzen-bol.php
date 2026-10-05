<?php
/**
 * robotmaaierkompas.nl — prijzen via de Bol-partner-API (Marketing Catalog API)
 *
 * - Een geplande taak (WP-Cron, liefst aangestuurd door een echte servercron) haalt per model
 *   met een EAN de beste aanbieding op en slaat prijs, link, levertekst, verkoper en tijdstip op.
 * - Maximaal 10 verzoeken per seconde (instelbaar, filter rmk_bol_max_rps), ook bij een 429
 *   wordt gewacht (Retry-After).
 * - Getoond wordt alleen een prijs die jonger is dan 24 uur, altijd met "Bron: bol.com".
 *   Ouder of geen prijs: de lege toestand "Prijs wordt bijgewerkt" uit het ontwerp.
 *
 * Instellen (in wp-config.php, NIET in het thema of in git):
 *   define( 'RMK_BOL_CLIENT_ID', '…' );
 *   define( 'RMK_BOL_CLIENT_SECRET', '…' );
 * EAN per model: wp rmk bol-ean M002 <EAN>   (komt nog niet uit het Excel-bestand)
 * Handmatig draaien: wp rmk bol-prijzen
 *
 * STAAT UIT (besluit 5 oktober 2026): voorlopig geen Bol-gegevens. Geen API-verzoeken, geen ingeplande taak,
 * geen prijzen. Productboxen tonen "Bekijk de prijs bij de winkel" zonder knop. Aanzetten kan pas na een nieuw
 * besluit: define( 'RMK_BOL_ENABLED', true ); in wp-config.php plus eigen sleutels voor deze site.
 *
 * LET OP: de endpoints hieronder zijn niet gecontroleerd tegen de API-documentatie (die was vanuit de
 * bouwomgeving niet bereikbaar). Controleer ze op https://api.bol.com/marketing/docs/catalog-api/ en
 * pas zo nodig de filters rmk_bol_token_url en rmk_bol_offer_url aan.
 */

defined( 'ABSPATH' ) || exit;

const RMK_BOL_OPTION     = 'rmk_bol_prijzen';
const RMK_BOL_EAN_OPTION = 'rmk_bol_ean';
const RMK_BOL_HOOK       = 'rmk_bol_prijzen_ophalen';
const RMK_BOL_MAX_AGE    = DAY_IN_SECONDS; // nooit een prijs tonen die ouder is dan 24 uur

function rmk_bol_enabled() {
	return defined( 'RMK_BOL_ENABLED' ) && true === RMK_BOL_ENABLED;
}

function rmk_bol_max_age() {
	return min( RMK_BOL_MAX_AGE, (int) apply_filters( 'rmk_bol_max_age', RMK_BOL_MAX_AGE ) );
}

/* ------------------------------------------------------------------ planning */

add_action( 'init', function () {
	if ( ! rmk_bol_enabled() ) {
		if ( wp_next_scheduled( RMK_BOL_HOOK ) ) {
			wp_clear_scheduled_hook( RMK_BOL_HOOK ); // uitgeschakeld: ook een eerder ingeplande taak weghalen
		}
		return;
	}
	if ( ! wp_next_scheduled( RMK_BOL_HOOK ) ) {
		// Twee keer per dag: één mislukte ronde laat de prijzen nog niet verlopen.
		wp_schedule_event( time() + 300, 'twicedaily', RMK_BOL_HOOK );
	}
} );
add_action( RMK_BOL_HOOK, 'rmk_bol_fetch_all' );

/**
 * Na elke prijsronde (ook als die mislukt) de paginacache legen. Zo blijft een prijs in een gecachte
 * pagina nooit langer staan dan tot de volgende ronde (12 uur) en verdwijnt hij uiterlijk na 24 uur.
 * Ondersteunt LiteSpeed Cache (Hostinger); andere caches kunnen inhaken op rmk_bol_na_ophalen.
 */
add_action( 'rmk_bol_na_ophalen', function () {
	do_action( 'litespeed_purge_all' );
	if ( function_exists( 'wp_cache_flush' ) ) {
		wp_cache_flush();
	}
} );
add_action( 'switch_theme', function () {
	wp_clear_scheduled_hook( RMK_BOL_HOOK );
} );

/* ------------------------------------------------------------------ API */

function rmk_bol_credentials() {
	if ( ! rmk_bol_enabled() ) {
		return null;
	}
	if ( ! defined( 'RMK_BOL_CLIENT_ID' ) || ! defined( 'RMK_BOL_CLIENT_SECRET' ) || ! RMK_BOL_CLIENT_ID || ! RMK_BOL_CLIENT_SECRET ) {
		return null;
	}
	return array( RMK_BOL_CLIENT_ID, RMK_BOL_CLIENT_SECRET );
}

/** Wacht zodat er nooit meer dan rmk_bol_max_rps verzoeken per seconde gaan. */
function rmk_bol_throttle() {
	static $last = 0.0;
	$rps = max( 1, min( 10, (int) apply_filters( 'rmk_bol_max_rps', 10 ) ) );
	$gap = 1.0 / $rps;
	$now = microtime( true );
	if ( $last && ( $now - $last ) < $gap ) {
		usleep( (int) ceil( ( $gap - ( $now - $last ) ) * 1e6 ) );
	}
	$last = microtime( true );
}

function rmk_bol_request( $method, $url, $args ) {
	for ( $try = 0; $try < 3; $try++ ) {
		rmk_bol_throttle();
		$res = 'POST' === $method ? wp_remote_post( $url, $args ) : wp_remote_get( $url, $args );
		if ( is_wp_error( $res ) || 429 !== (int) wp_remote_retrieve_response_code( $res ) ) {
			return $res;
		}
		$wait = (int) wp_remote_retrieve_header( $res, 'retry-after' );
		sleep( max( 1, min( 30, $wait ? $wait : 2 ) ) );
	}
	return $res;
}

function rmk_bol_token() {
	$cached = get_transient( 'rmk_bol_token' );
	if ( $cached ) {
		return $cached;
	}
	$cred = rmk_bol_credentials();
	if ( ! $cred ) {
		return new WP_Error( 'rmk_bol_config', 'RMK_BOL_CLIENT_ID en RMK_BOL_CLIENT_SECRET staan niet in wp-config.php.' );
	}
	$url = apply_filters( 'rmk_bol_token_url', 'https://login.bol.com/token?grant_type=client_credentials' );
	$res = rmk_bol_request( 'POST', $url, array(
		'timeout' => 15,
		'headers' => array( 'Authorization' => 'Basic ' . base64_encode( $cred[0] . ':' . $cred[1] ), 'Accept' => 'application/json' ),
	) );
	if ( is_wp_error( $res ) ) {
		return $res;
	}
	$body = json_decode( wp_remote_retrieve_body( $res ), true );
	if ( 200 !== (int) wp_remote_retrieve_response_code( $res ) || empty( $body['access_token'] ) ) {
		return new WP_Error( 'rmk_bol_token', 'Geen token van bol.com (HTTP ' . wp_remote_retrieve_response_code( $res ) . ').' );
	}
	$ttl = isset( $body['expires_in'] ) ? max( 60, (int) $body['expires_in'] - 60 ) : 240;
	set_transient( 'rmk_bol_token', $body['access_token'], $ttl );
	return $body['access_token'];
}

/** Zoekt een sleutel op in een geneste array (de precieze vorm van het antwoord is nog niet gecontroleerd). */
function rmk_bol_pick( $data, array $paths ) {
	foreach ( $paths as $path ) {
		$v = $data;
		foreach ( explode( '.', $path ) as $k ) {
			if ( ! is_array( $v ) || ! array_key_exists( $k, $v ) ) {
				$v = null;
				break;
			}
			$v = $v[ $k ];
		}
		if ( null !== $v && '' !== $v ) {
			return $v;
		}
	}
	return null;
}

/** Haalt de beste aanbieding voor één EAN op. */
function rmk_bol_fetch_offer( $ean, $token ) {
	$url = apply_filters( 'rmk_bol_offer_url', 'https://api.bol.com/marketing/catalog/v1/products/' . rawurlencode( $ean ) . '/offers/best?country-code=NL&include-seller=true', $ean );
	$res = rmk_bol_request( 'GET', $url, array(
		'timeout' => 15,
		'headers' => array( 'Authorization' => 'Bearer ' . $token, 'Accept' => 'application/json', 'Accept-Language' => 'nl' ),
	) );
	if ( is_wp_error( $res ) ) {
		return $res;
	}
	$code = (int) wp_remote_retrieve_response_code( $res );
	if ( 404 === $code ) {
		return array( 'status' => 'geen aanbod' );
	}
	if ( 200 !== $code ) {
		return new WP_Error( 'rmk_bol_http', 'HTTP ' . $code );
	}
	$d     = json_decode( wp_remote_retrieve_body( $res ), true );
	$price = rmk_bol_pick( $d, array( 'offer.price', 'price', 'bestOffer.price', 'offer.price.value' ) );
	if ( null === $price || ! is_numeric( $price ) ) {
		return array( 'status' => 'geen prijs in antwoord' );
	}
	return array(
		'status'     => 'ok',
		'prijs'      => (float) $price,
		'url'        => rmk_bol_pick( $d, array( 'url', 'offer.url', 'product.url' ) ),
		'levering'   => rmk_bol_pick( $d, array( 'offer.deliveryDescription', 'deliveryDescription' ) ),
		'verkoper'   => rmk_bol_pick( $d, array( 'offer.seller.name', 'seller.name', 'offer.sellerName' ) ),
		'staat'      => rmk_bol_pick( $d, array( 'offer.condition', 'condition' ) ),
	);
}

function rmk_bol_eans() {
	$eans = (array) get_option( RMK_BOL_EAN_OPTION, array() );
	foreach ( rmk_models_data()['modellen'] as $m ) {
		if ( ! empty( $m['ean'] ) && empty( $eans[ $m['id'] ] ) ) {
			$eans[ $m['id'] ] = $m['ean'];
		}
	}
	return array_filter( $eans );
}

/** De geplande taak. Geeft een korte samenvatting terug (ook voor WP-CLI). */
function rmk_bol_fetch_all() {
	if ( ! rmk_bol_enabled() ) {
		return array( 'start' => time(), 'ok' => 0, 'fout' => array( 'Prijstaak staat uit (RMK_BOL_ENABLED).' ), 'zonder_ean' => array() );
	}
	$eans = rmk_bol_eans();
	$log  = array( 'start' => time(), 'ok' => 0, 'fout' => array(), 'zonder_ean' => array() );
	foreach ( rmk_models_data()['modellen'] as $m ) {
		if ( empty( $eans[ $m['id'] ] ) ) {
			$log['zonder_ean'][] = $m['id'];
		}
	}
	if ( ! $eans ) {
		update_option( 'rmk_bol_laatste_run', $log, false );
		return $log;
	}
	$token = rmk_bol_token();
	if ( is_wp_error( $token ) ) {
		$log['fout'][] = $token->get_error_message();
		update_option( 'rmk_bol_laatste_run', $log, false );
		do_action( 'rmk_bol_na_ophalen', $log );
		return $log;
	}
	$store = (array) get_option( RMK_BOL_OPTION, array() );
	foreach ( $eans as $id => $ean ) {
		$offer = rmk_bol_fetch_offer( $ean, $token );
		if ( is_wp_error( $offer ) ) {
			$log['fout'][] = $id . ': ' . $offer->get_error_message();
			continue; // oude prijs blijft staan maar verloopt vanzelf na 24 uur
		}
		$store[ $id ] = array_merge( $offer, array( 'ean' => $ean, 'opgehaald' => time() ) );
		if ( 'ok' === $offer['status'] ) {
			$log['ok']++;
		}
	}
	update_option( RMK_BOL_OPTION, $store, false );
	update_option( 'rmk_bol_laatste_run', $log, false );
	do_action( 'rmk_bol_na_ophalen', $log );
	return $log;
}

/* ------------------------------------------------------------------ tonen */

/** Actuele Bol-prijs voor een model, of null als er geen is of als hij ouder is dan 24 uur. */
function rmk_bol_price( $model_id ) {
	if ( ! rmk_bol_enabled() ) {
		return null;
	}
	$store = (array) get_option( RMK_BOL_OPTION, array() );
	$p     = isset( $store[ $model_id ] ) ? $store[ $model_id ] : null;
	if ( ! $p || 'ok' !== $p['status'] || empty( $p['opgehaald'] ) ) {
		return null;
	}
	if ( time() - (int) $p['opgehaald'] > rmk_bol_max_age() ) {
		return null;
	}
	return $p;
}

function rmk_bol_time( $p ) {
	return wp_date( 'j F Y, H:i', (int) $p['opgehaald'] );
}

/** Prijsregel in de productbox, met bronvermelding. */
/** Lege prijstoestand zonder winkelknop (geen affiliatelinks). */
function rmk_offer_empty_html() {
	return '<div class="rmk-offer"><span class="rmk-offer__price rmk-offer__price--empty">Bekijk de prijs bij de winkel</span>'
		. '<span class="rmk-offer__src">We tonen voorlopig geen winkelprijzen.</span></div>';
}

function rmk_bol_offer_html( $model_id, $slug ) {
	if ( ! rmk_bol_enabled() ) {
		return rmk_offer_empty_html();
	}
	$p    = rmk_bol_price( $model_id );
	$link = home_url( '/ga/bol/' . $slug . '/' );
	if ( ! $p ) {
		return '<div class="rmk-offer rmk-offer--stale"><span class="rmk-offer__shop">bol.com</span><span class="rmk-offer__price">Prijs wordt bijgewerkt</span>'
			. '<a class="rmk-btn rmk-btn--primary" href="' . esc_url( $link ) . '" rel="sponsored nofollow">Bekijk de prijs bij bol.com</a>'
			. '<span class="rmk-offer__src">Bron: bol.com</span></div>';
	}
	$extra = $p['verkoper'] ? ' · verkoper: ' . esc_html( $p['verkoper'] ) : '';
	return '<div class="rmk-offer"><span class="rmk-offer__shop">bol.com</span><span class="rmk-offer__price">€ ' . esc_html( number_format( $p['prijs'], 2, ',', '.' ) ) . '</span>'
		. '<a class="rmk-btn rmk-btn--primary" href="' . esc_url( $link ) . '" rel="sponsored nofollow">Naar bol.com</a>'
		. '<span class="rmk-offer__src">Bron: bol.com · prijs van ' . esc_html( rmk_bol_time( $p ) ) . $extra . '</span></div>';
}

/** Cel "Prijs vanaf" in de scoretabel: alleen een actuele Bol-prijs, anders verwijzen naar de winkel. */
function rmk_price_cell( array $m ) {
	$p = rmk_bol_price( $m['id'] );
	if ( ! $p ) {
		return '<span class="rmk-small">bij de winkel</span>';
	}
	return '€ ' . esc_html( number_format( $p['prijs'], 0, ',', '.' ) ) . '<br><span class="rmk-small">Bron: bol.com · ' . esc_html( rmk_bol_time( $p ) ) . '</span>';
}

add_shortcode( 'rmk_bolprijs', function ( $atts ) {
	$a = shortcode_atts( array( 'model' => '' ), $atts );
	$m = rmk_get_model( $a['model'] );
	return $m ? rmk_bol_offer_html( $m['id'], $m['slug'] ) : '';
} );

/* ------------------------------------------------------------------ WP-CLI */

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::add_command( 'rmk bol-prijzen', function () {
		if ( ! rmk_bol_enabled() ) {
			WP_CLI::error( 'Prijstaak staat uit (voorlopig geen Bol-gegevens).' );
		}
		$log = rmk_bol_fetch_all();
		WP_CLI::log( wp_json_encode( $log, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE ) );
	} );
	WP_CLI::add_command( 'rmk bol-ean', function ( $args ) {
		if ( ! rmk_bol_enabled() ) {
			WP_CLI::error( 'Prijstaak staat uit (voorlopig geen Bol-gegevens).' );
		}
		list( $id, $ean ) = array_pad( $args, 2, '' );
		if ( ! preg_match( '/^\d{8,14}$/', $ean ) ) {
			WP_CLI::error( 'Gebruik: wp rmk bol-ean M002 <EAN van 8 tot 14 cijfers>' );
		}
		$eans        = (array) get_option( RMK_BOL_EAN_OPTION, array() );
		$eans[ $id ] = $ean;
		update_option( RMK_BOL_EAN_OPTION, $eans, false );
		WP_CLI::success( "EAN voor $id opgeslagen." );
	} );
}
