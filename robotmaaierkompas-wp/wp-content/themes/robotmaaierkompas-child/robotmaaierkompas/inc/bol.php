<?php
/**
 * robotmaaierkompas.nl — Bol-partnerkoppeling (1.3.6), vervangt inc/prijzen-bol.php.
 *
 * Bron voor de vorm van de API en de links: het Logboek van robotmaaierkompas_modeldata_v1.xlsx, rijen 136-148
 * (onderzoeksvenster, 12 oktober 2026). Niets daarbuiten is aangenomen.
 *
 * Instellen (in wp-config.php op de server, NOOIT in het thema of in git):
 *   define( 'RMK_BOL_CLIENT_ID', '…' );
 *   define( 'RMK_BOL_CLIENT_SECRET', '…' );
 *   define( 'RMK_BOL_SITE_ID', '…' );
 *   define( 'RMK_AFFILIATE_ACTIVE', true );   // de schakelaar; standaard uit
 * Ontbreekt een van de drie Bol-constanten: geen verzoeken, geen ingeplande taak, geen Bol-regel (alles zoals 1.3.5).
 * Staan de constanten er wel maar RMK_AFFILIATE_ACTIVE niet: de prijstaak draait (zodat /rmk/v1/bol-status iets
 * laat zien), maar er komt nergens een Bol-regel, -knop of -afbeelding op de site.
 *
 * API (Logboek 137-141):
 * - Token: POST https://login.bol.com/token?grant_type=client_credentials, Authorization: Basic base64(id:secret),
 *   Accept: application/json. Antwoord: access_token, token_type "Bearer", expires_in (599). Hergebruikt tot
 *   30 seconden voor afloop (transient, nooit gelogd).
 * - Aanbod: GET https://api.bol.com/marketing/catalog/v1/products/{ean}/offers/best?country-code=NL&include-seller=true
 *   met Authorization: Bearer, Accept: application/json, Accept-Language: nl. 200: price (euro), condition, isPreOrder,
 *   url, deliveryDescription, seller{name} ("bol.com" = bol zelf, anders een partner). 404 "Unable to find offer" =
 *   geen aanbod. Fouten als application/problem+json (type, title, status, detail, host, X-Request-ID).
 * 1.3.7: de prijs staat niet meer in de HTML maar komt uit de publieke route /rmk/v1/bol-prijs (nooit gecachet, via rmk.js);
 *   de ronde stopt na de eerste tokenfout; POST /rmk/v1/bol-ronde (alleen beheerders) start een ronde.
 * - Rate limit: x-ratelimit-limit 10, x-ratelimit-remaining, x-ratelimit-reset (seconden). Wij doen maximaal 10
 *   verzoeken per seconde (minstens 0,1 s ertussen) en wachten x-ratelimit-reset af als remaining 0 is of bij 429.
 *
 * Affiliatelink (Logboek 144-145, besluiten Mandy 13 oktober 2026: f=api en subid = paginaslug):
 *   https://partner.bol.com/click/click?p=2&t=url&s=<RMK_BOL_SITE_ID>&f=api&url=<bol-product-URL>&name=<modelnaam>&subid=<slug>
 *   Waarden volledig gecodeerd zoals Python urllib.parse.quote(waarde, safe="") (= PHP rawurlencode).
 *
 * Prijstaak: vier keer per dag (WP-Cron, elke 6 uur). WP-Cron draait alleen bij bezoek; zet daarom in hPanel een
 * echte cron (zie BOUWLOGBOEK ronde 30). Een prijs is 12 uur geldig. Geen aanbod, een fout of een 404: de Bol-regel
 * verdwijnt. Na elke ronde wordt de paginacache geleegd. Beoordelingen van bol.com worden niet opgehaald en niet
 * getoond (besluit Mandy: de Navimow-pool zegt niets over één model).
 */

defined( 'ABSPATH' ) || exit;

const RMK_BOL_AANBOD_OPTION = 'rmk_bol_aanbod';   // model-ID => laatste uitkomst
const RMK_BOL_LOG_OPTION    = 'rmk_bol_log';      // laatste rondes (zonder secrets)
const RMK_BOL_TOKEN_KEY     = 'rmk_bol_token';    // transient
const RMK_BOL_LOCK_KEY      = 'rmk_bol_lock';     // transient
const RMK_BOL_RONDE_HOOK    = 'rmk_bol_ronde';
const RMK_BOL_GELDIG        = 12 * HOUR_IN_SECONDS;
const RMK_BOL_API           = 'https://api.bol.com/marketing/catalog/v1';
const RMK_BOL_TOKEN_URL     = 'https://login.bol.com/token?grant_type=client_credentials';

/** Staan alle drie de Bol-constanten in wp-config.php? (De waarden zelf worden nergens getoond of gelogd.) */
function rmk_bol_geconfigureerd() {
	foreach ( array( 'RMK_BOL_CLIENT_ID', 'RMK_BOL_CLIENT_SECRET', 'RMK_BOL_SITE_ID' ) as $c ) {
		if ( ! defined( $c ) || '' === trim( (string) constant( $c ) ) ) {
			return false;
		}
	}
	return true;
}

/** Mag er een Bol-regel op de site? Alleen met de constanten én RMK_AFFILIATE_ACTIVE aan. */
function rmk_bol_zichtbaar() {
	return rmk_bol_geconfigureerd() && function_exists( 'rmk_affiliate_actief' ) && rmk_affiliate_actief();
}

/** Tijd, te vervangen in tests. */
function rmk_bol_nu() {
	return (int) apply_filters( 'rmk_bol_nu', time() );
}

/* ------------------------------------------------------------------ planning: vier keer per dag */

add_filter( 'cron_schedules', function ( $s ) {
	$s['rmk_zes_uur'] = array( 'interval' => 6 * HOUR_IN_SECONDS, 'display' => 'Elke 6 uur (Bol-prijzen)' );
	return $s;
} );

add_action( 'init', function () {
	// Oude opzet (tot 1.3.5): taak en opties opruimen.
	if ( wp_next_scheduled( 'rmk_bol_prijzen_ophalen' ) ) {
		wp_clear_scheduled_hook( 'rmk_bol_prijzen_ophalen' );
	}
	if ( ! rmk_bol_geconfigureerd() ) {
		if ( wp_next_scheduled( RMK_BOL_RONDE_HOOK ) ) {
			wp_clear_scheduled_hook( RMK_BOL_RONDE_HOOK );
		}
		return;
	}
	if ( ! wp_next_scheduled( RMK_BOL_RONDE_HOOK ) ) {
		wp_schedule_event( rmk_bol_nu() + 120, 'rmk_zes_uur', RMK_BOL_RONDE_HOOK );
	}
} );
add_action( RMK_BOL_RONDE_HOOK, 'rmk_bol_ronde' );
add_action( 'switch_theme', function () {
	wp_clear_scheduled_hook( RMK_BOL_RONDE_HOOK );
} );

/* Na elke ronde (ook een mislukte) de paginacache legen. */
add_action( 'rmk_bol_na_ronde', function () {
	do_action( 'litespeed_purge_all' );
} );

/* ------------------------------------------------------------------ HTTP */

/** Wacht zo nodig zodat er minstens 0,1 s tussen twee verzoeken zit (maximaal 10 per seconde). */
function rmk_bol_wacht() {
	static $vorige = 0.0;
	$min = max( 0.1, (float) apply_filters( 'rmk_bol_min_interval', 0.1 ) );
	$nu  = microtime( true );
	if ( $vorige && $nu - $vorige < $min ) {
		usleep( (int) round( ( $min - ( $nu - $vorige ) ) * 1e6 ) );
	}
	$vorige = microtime( true );
	do_action( 'rmk_bol_verzoek', $vorige ); // voor tests
}

/** Eén verzoek; volgt x-ratelimit-remaining/-reset en probeert na een 429 één keer opnieuw. */
function rmk_bol_http( $method, $url, array $headers, $body = null ) {
	for ( $poging = 0; $poging < 2; $poging++ ) {
		rmk_bol_wacht();
		$r = wp_remote_request( $url, array( 'method' => $method, 'headers' => $headers, 'body' => $body, 'timeout' => 15, 'redirection' => 0 ) );
		if ( is_wp_error( $r ) ) {
			return $r;
		}
		$code  = (int) wp_remote_retrieve_response_code( $r );
		$reset = (int) wp_remote_retrieve_header( $r, 'x-ratelimit-reset' );
		$rest  = wp_remote_retrieve_header( $r, 'x-ratelimit-remaining' );
		if ( 429 === $code || ( '' !== (string) $rest && 0 === (int) $rest ) ) {
			usleep( (int) ( 1e6 * min( 5, max( 1, $reset ) ) ) );
		}
		if ( 429 !== $code ) {
			return $r;
		}
	}
	return $r;
}

/** Korte, veilige foutomschrijving uit een application/problem+json-antwoord (geen headers, geen token). */
function rmk_bol_probleem( $r ) {
	if ( is_wp_error( $r ) ) {
		return 'verbinding: ' . $r->get_error_message();
	}
	$j   = json_decode( (string) wp_remote_retrieve_body( $r ), true );
	$txt = array();
	foreach ( array( 'title', 'detail' ) as $k ) {
		if ( ! empty( $j[ $k ] ) && is_string( $j[ $k ] ) ) {
			$txt[] = $j[ $k ];
		}
	}
	$id = ! empty( $j['X-Request-ID'] ) && is_string( $j['X-Request-ID'] ) ? ' (X-Request-ID ' . $j['X-Request-ID'] . ')' : '';
	return substr( 'HTTP ' . wp_remote_retrieve_response_code( $r ) . ( $txt ? ': ' . implode( ' – ', $txt ) : '' ) . $id, 0, 300 );
}

/* ------------------------------------------------------------------ token (Logboek 137) */

/** Geeft een geldig access_token, of een WP_Error. Hergebruikt het token tot 30 s voor afloop. */
function rmk_bol_token( $vernieuw = false ) {
	if ( ! $vernieuw ) {
		$t = get_transient( RMK_BOL_TOKEN_KEY );
		if ( is_array( $t ) && ! empty( $t['token'] ) && $t['tot'] > rmk_bol_nu() ) {
			return $t['token'];
		}
	}
	$r = rmk_bol_http( 'POST', apply_filters( 'rmk_bol_token_url', RMK_BOL_TOKEN_URL ), array(
		'Authorization' => 'Basic ' . base64_encode( RMK_BOL_CLIENT_ID . ':' . RMK_BOL_CLIENT_SECRET ),
		'Accept'        => 'application/json',
	) );
	if ( is_wp_error( $r ) || 200 !== (int) wp_remote_retrieve_response_code( $r ) ) {
		return new WP_Error( 'rmk_bol_token', 'Token: ' . rmk_bol_probleem( $r ) );
	}
	$j = json_decode( (string) wp_remote_retrieve_body( $r ), true );
	if ( empty( $j['access_token'] ) || ! is_string( $j['access_token'] ) || ( isset( $j['token_type'] ) && 'bearer' !== strtolower( (string) $j['token_type'] ) ) ) {
		return new WP_Error( 'rmk_bol_token', 'Token: onverwacht antwoord (geen access_token van het type Bearer).' );
	}
	$duur = isset( $j['expires_in'] ) && is_numeric( $j['expires_in'] ) ? (int) $j['expires_in'] : 0;
	$tot  = rmk_bol_nu() + max( 0, $duur - 30 );
	if ( $tot > rmk_bol_nu() ) {
		set_transient( RMK_BOL_TOKEN_KEY, array( 'token' => $j['access_token'], 'tot' => $tot ), max( 1, $duur - 30 ) );
	}
	return $j['access_token'];
}

/* ------------------------------------------------------------------ aanbod (Logboek 141) */

/**
 * Haalt /offers/best op voor één EAN. Geeft een uitkomst (zonder secrets):
 *   status 'ok' (prijs, verkoper, partner, url, tijd), 'geen_aanbod' (404), 'ongeldig' (200 maar niet bruikbaar) of 'fout'.
 */
function rmk_bol_aanbod_ophalen( $ean, $token ) {
	$url = RMK_BOL_API . '/products/' . rawurlencode( $ean ) . '/offers/best?country-code=NL&include-seller=true';
	$hd  = function ( $tk ) {
		return array( 'Authorization' => 'Bearer ' . $tk, 'Accept' => 'application/json', 'Accept-Language' => 'nl' );
	};
	$r = rmk_bol_http( 'GET', $url, $hd( $token ) );
	if ( ! is_wp_error( $r ) && 401 === (int) wp_remote_retrieve_response_code( $r ) ) {
		// Token verlopen of ingetrokken: één keer vernieuwen en opnieuw proberen.
		$token = rmk_bol_token( true );
		if ( is_wp_error( $token ) ) {
			return array( 'status' => 'fout', 'detail' => $token->get_error_message(), 'tokenfout' => true );
		}
		$r = rmk_bol_http( 'GET', $url, $hd( $token ) );
	}
	if ( is_wp_error( $r ) ) {
		return array( 'status' => 'fout', 'detail' => rmk_bol_probleem( $r ) );
	}
	$code = (int) wp_remote_retrieve_response_code( $r );
	if ( 404 === $code ) {
		return array( 'status' => 'geen_aanbod', 'http' => 404, 'detail' => rmk_bol_probleem( $r ) );
	}
	if ( 200 !== $code ) {
		return array( 'status' => 'fout', 'http' => $code, 'detail' => rmk_bol_probleem( $r ) );
	}
	$j = json_decode( (string) wp_remote_retrieve_body( $r ), true );
	if ( ! is_array( $j ) ) {
		return array( 'status' => 'ongeldig', 'http' => 200, 'detail' => 'Geen JSON.' );
	}
	$prijs    = isset( $j['price'] ) && is_numeric( $j['price'] ) ? (float) $j['price'] : 0.0;
	$verkoper = isset( $j['seller']['name'] ) && is_string( $j['seller']['name'] ) ? trim( $j['seller']['name'] ) : '';
	$redenen  = array();
	if ( $prijs <= 0 ) {
		$redenen[] = 'geen prijs';
	}
	if ( isset( $j['condition'] ) && 'NEW' !== $j['condition'] ) {
		$redenen[] = 'niet nieuw (' . substr( (string) $j['condition'], 0, 20 ) . ')';
	}
	if ( ! empty( $j['isPreOrder'] ) ) {
		$redenen[] = 'voorbestelling';
	}
	if ( '' === $verkoper ) {
		$redenen[] = 'verkoper ontbreekt';
	}
	if ( isset( $j['ean'] ) && (string) $j['ean'] !== (string) $ean ) {
		$redenen[] = 'andere EAN in het antwoord';
	}
	if ( $redenen ) {
		return array( 'status' => 'ongeldig', 'http' => 200, 'detail' => implode( ', ', $redenen ) );
	}
	return array(
		'status'   => 'ok',
		'http'     => 200,
		'prijs'    => round( $prijs, 2 ),
		'verkoper' => substr( $verkoper, 0, 80 ),
		'partner'  => 'bol.com' !== strtolower( $verkoper ),
		'url'      => isset( $j['url'] ) && is_string( $j['url'] ) ? $j['url'] : '',
	);
}

/** Modellen met een EAN in de modelgegevens (veld ean), zonder dubbele EAN's. */
function rmk_bol_modellen() {
	$uit = array();
	foreach ( rmk_models_data()['modellen'] as $m ) {
		$ean = isset( $m['ean'] ) ? preg_replace( '/\D/', '', (string) $m['ean'] ) : '';
		if ( '' !== $ean && strlen( $ean ) >= 8 && strlen( $ean ) <= 14 ) {
			$uit[ $m['id'] ] = $ean;
		}
	}
	return $uit;
}

/** Eén ronde: alle modellen met een EAN. Bewaart per model de laatste uitkomst en een log zonder secrets. */
function rmk_bol_ronde() {
	$start = rmk_bol_nu();
	$log   = array( 'start' => $start, 'eind' => null, 'ok' => 0, 'geen_aanbod' => 0, 'ongeldig' => 0, 'fout' => 0, 'verzoeken' => 0, 'gestopt' => false, 'melding' => '' );
	if ( ! rmk_bol_geconfigureerd() ) {
		$log['melding'] = 'Bol-constanten ontbreken in wp-config.php: niets opgehaald.';
		return $log;
	}
	if ( get_transient( RMK_BOL_LOCK_KEY ) ) {
		$log['melding'] = 'Er draait al een ronde.';
		return $log;
	}
	set_transient( RMK_BOL_LOCK_KEY, 1, 10 * MINUTE_IN_SECONDS );
	$teller = function () use ( &$log ) {
		$log['verzoeken']++;
	};
	add_action( 'rmk_bol_verzoek', $teller );

	$store = (array) get_option( RMK_BOL_AANBOD_OPTION, array() );
	// 1.3.7: eerst één token. Lukt dat niet, dan stopt de ronde meteen (geen verzoek per model naar login.bol.com)
	// en blijven de opgeslagen uitkomsten staan; een prijs verloopt dan vanzelf na 12 uur.
	$token = rmk_bol_token();
	if ( is_wp_error( $token ) ) {
		$log['gestopt']  = true;
		$log['melding']  = 'Gestopt na de eerste tokenfout (' . $token->get_error_message() . '). Geen aanbiedingen opgehaald; controleer RMK_BOL_CLIENT_ID en RMK_BOL_CLIENT_SECRET.';
	} else {
		foreach ( rmk_bol_modellen() as $id => $ean ) {
			$token = rmk_bol_token(); // uit de transient; na een vernieuwing (401) meteen het nieuwe token
			$u     = is_wp_error( $token ) ? array( 'status' => 'fout', 'detail' => $token->get_error_message(), 'tokenfout' => true ) : rmk_bol_aanbod_ophalen( $ean, $token );
			if ( ! empty( $u['tokenfout'] ) ) {
				$log['gestopt'] = true;
				$log['melding'] = 'Gestopt na een tokenfout bij ' . $id . ' (' . $u['detail'] . '). Volgende modellen niet opgehaald.';
				break;
			}
			$u['ean']     = $ean;
			$u['tijd']    = rmk_bol_nu();
			$store[ $id ] = $u;
			$log[ $u['status'] ]++;
			$log['modellen'][ $id ] = $u['status'] . ( isset( $u['detail'] ) ? ': ' . $u['detail'] : '' );
		}
	}
	// Modellen die geen EAN meer hebben: weg.
	$store = array_intersect_key( $store, rmk_bol_modellen() );
	update_option( RMK_BOL_AANBOD_OPTION, $store, false );

	remove_action( 'rmk_bol_verzoek', $teller );
	delete_transient( RMK_BOL_LOCK_KEY );
	$log['eind'] = rmk_bol_nu();
	$hist        = (array) get_option( RMK_BOL_LOG_OPTION, array() );
	array_unshift( $hist, $log );
	update_option( RMK_BOL_LOG_OPTION, array_slice( $hist, 0, 20 ), false );
	do_action( 'rmk_bol_na_ronde', $log );
	return $log;
}

/* ------------------------------------------------------------------ weergave */

/** Geldig Bol-aanbod voor model $m (array uit de modelgegevens), of null. Alleen als de Bol-regel zichtbaar mag zijn. */
function rmk_bol_aanbod( array $m ) {
	if ( ! rmk_bol_zichtbaar() || empty( $m['id'] ) || empty( $m['ean'] ) || empty( $m['bol']['product_url'] ) ) {
		return null;
	}
	$store = (array) get_option( RMK_BOL_AANBOD_OPTION, array() );
	$a     = isset( $store[ $m['id'] ] ) ? $store[ $m['id'] ] : null;
	if ( ! $a || 'ok' !== $a['status'] || (string) $a['ean'] !== preg_replace( '/\D/', '', (string) $m['ean'] ) ) {
		return null;
	}
	$leeftijd = rmk_bol_nu() - (int) $a['tijd'];
	if ( $leeftijd < 0 || $leeftijd > RMK_BOL_GELDIG || ! rmk_bol_product_url_ok( $m['bol']['product_url'] ) ) {
		return null;
	}
	return $a;
}

function rmk_bol_product_url_ok( $url ) {
	$p = wp_parse_url( (string) $url );
	return ! empty( $p['scheme'] ) && 'https' === $p['scheme'] && isset( $p['host'] ) && 'www.bol.com' === strtolower( $p['host'] );
}

function rmk_bol_afbeelding_ok( $url ) {
	$p = wp_parse_url( (string) $url );
	return ! empty( $p['scheme'] ) && 'https' === $p['scheme'] && isset( $p['host'] ) && 'media.s-bol.com' === strtolower( $p['host'] );
}

/** Paginaslug als subid: kleine letters, cijfers en koppeltekens. */
function rmk_bol_subid( $slug = null ) {
	if ( null === $slug ) {
		$id   = get_the_ID() ? get_the_ID() : get_queried_object_id();
		$slug = $id ? (string) get_post_field( 'post_name', $id ) : '';
	}
	$slug = trim( preg_replace( '/-+/', '-', preg_replace( '/[^a-z0-9-]/', '', strtolower( (string) $slug ) ) ), '-' );
	return '' === $slug ? 'onbekend' : substr( $slug, 0, 100 );
}

/** De affiliatelink in de vorm uit het Logboek (rij 144), met f=api en subid (besluiten 13 oktober 2026). */
function rmk_bol_link( $product_url, $naam, $subid ) {
	return 'https://partner.bol.com/click/click?p=2&t=url&s=' . rawurlencode( (string) RMK_BOL_SITE_ID ) . '&f=api'
		. '&url=' . rawurlencode( (string) $product_url ) . '&name=' . rawurlencode( (string) $naam ) . '&subid=' . rawurlencode( rmk_bol_subid( $subid ) );
}

function rmk_bol_bedrag( $p ) {
	$p = round( (float) $p, 2 );
	return floor( $p ) == $p ? number_format( $p, 0, ',', '.' ) : number_format( $p, 2, ',', '.' );
}

/** "bijgewerkt om 14:05" (vandaag) of "bijgewerkt gisteren om 21:05". */
function rmk_bol_tijd( $t ) {
	$tz  = wp_timezone();
	$dag = ( new DateTimeImmutable( '@' . (int) $t ) )->setTimezone( $tz );
	$nu  = ( new DateTimeImmutable( '@' . rmk_bol_nu() ) )->setTimezone( $tz );
	$wat = $dag->format( 'Y-m-d' ) === $nu->format( 'Y-m-d' ) ? 'om ' : ( $dag->format( 'Y-m-d' ) === $nu->modify( '-1 day' )->format( 'Y-m-d' ) ? 'gisteren om ' : 'op ' . $dag->format( 'j-n' ) . ' om ' );
	return 'bijgewerkt ' . $wat . $dag->format( 'H:i' );
}

/** Laatste uitkomst van de prijstaak voor model $m, of null. */
function rmk_bol_uitkomst( array $m ) {
	$store = (array) get_option( RMK_BOL_AANBOD_OPTION, array() );
	$a     = isset( $m['id'], $store[ $m['id'] ] ) ? $store[ $m['id'] ] : null;
	return $a && ! empty( $m['ean'] ) && (string) $a['ean'] === preg_replace( '/\D/', '', (string) $m['ean'] ) ? $a : null;
}

/**
 * Mag de Bol-knop in de kaart (1.3.7)? Schakelaar en constanten aan, model met EAN en bol-product-URL, en de laatste
 * ronde zei niet "geen aanbod" of "ongeldig". Bij een fout of nog geen ronde staat de knop er wel, zonder prijs.
 */
function rmk_bol_knop_zichtbaar( array $m ) {
	if ( ! rmk_bol_zichtbaar() || empty( $m['id'] ) || empty( $m['ean'] ) || empty( $m['bol']['product_url'] ) || ! rmk_bol_product_url_ok( $m['bol']['product_url'] ) ) {
		return false;
	}
	$a = rmk_bol_uitkomst( $m );
	return ! $a || ! in_array( $a['status'], array( 'geen_aanbod', 'ongeldig' ), true );
}

/**
 * De Bol-regel in de productkaart (1.3.7): alleen de knop, de bronregel en een leeg prijsvak. De prijs staat niet in de
 * HTML (die kan op de CDN blijven staan) maar komt bij het laden uit /rmk/v1/bol-prijs (nooit gecachet), via rmk.js.
 * Zonder JavaScript, bij een fout of een verlopen prijs blijft alleen de knop.
 */
function rmk_bol_regel_html( array $m, $subid = null ) {
	if ( ! rmk_bol_knop_zichtbaar( $m ) ) {
		return '';
	}
	$link = rmk_bol_link( $m['bol']['product_url'], $m['naam'], $subid );
	return '<div class="rmk-offer rmk-offer--stack rmk-offer--bol" data-rmk-bol data-rmk-bol-model="' . esc_attr( $m['id'] ) . '">'
		. '<span class="rmk-offer__line" data-rmk-bol-prijs hidden></span>'
		. '<a class="rmk-btn rmk-btn--primary" href="' . esc_url( $link ) . '" rel="sponsored nofollow" data-rmk-bol-link>Bekijk bij bol.com</a>'
		. '<span class="rmk-offer__src">Je gaat naar bol.com. Bron: bol.com.</span></div>';
}

/**
 * Wat de publieke prijsroute per model teruggeeft: alleen tekst die al op de site mag staan (prijs, tijdstip, verkoper,
 * EAN). Status "ok" alleen bij een geldig aanbod (niet ouder dan 12 uur); "geen_aanbod" bij geen aanbod of ongeldig;
 * anders (fout, nog geen ronde) niets, en dan blijft in de kaart alleen de knop.
 */
function rmk_bol_prijs_data( array $m ) {
	if ( ! rmk_bol_zichtbaar() || empty( $m['ean'] ) ) {
		return null;
	}
	$a = rmk_bol_aanbod( $m );
	if ( $a ) {
		$tz = wp_timezone();
		return array(
			'status'      => 'ok',
			'model'       => $m['id'],
			'ean'         => (string) $a['ean'],
			'prijs'       => (float) $a['prijs'],
			'prijs_tekst' => rmk_bol_bedrag( $a['prijs'] ),
			'verkoper'    => (string) $a['verkoper'],
			'partner'     => (bool) $a['partner'],
			'tijd'        => ( new DateTimeImmutable( '@' . (int) $a['tijd'] ) )->setTimezone( $tz )->format( DATE_ATOM ),
			'tijd_tekst'  => rmk_bol_tijd( $a['tijd'] ),
			'geldig_tot'  => ( new DateTimeImmutable( '@' . ( (int) $a['tijd'] + RMK_BOL_GELDIG ) ) )->setTimezone( $tz )->format( DATE_ATOM ),
		);
	}
	$u = rmk_bol_uitkomst( $m );
	if ( $u && in_array( $u['status'], array( 'geen_aanbod', 'ongeldig' ), true ) ) {
		return array( 'status' => 'geen_aanbod', 'model' => $m['id'], 'ean' => (string) $u['ean'] );
	}
	return null;
}

/** Antwoord van GET /rmk/v1/bol-prijs?modellen=M001,M002 (maximaal 30 model-ID's). */
function rmk_bol_prijzen_publiek( $ids ) {
	$uit = array();
	foreach ( array_slice( array_unique( array_filter( array_map( 'trim', explode( ',', (string) $ids ) ) ) ), 0, 30 ) as $id ) {
		if ( ! preg_match( '/^M\d{3,4}$/', $id ) || ! ( $m = rmk_get_model( $id ) ) ) {
			continue;
		}
		$d = rmk_bol_prijs_data( $m );
		if ( $d ) {
			$uit[ $id ] = $d;
		}
	}
	return array( 'bron' => 'bol.com', 'modellen' => (object) $uit );
}

/** Foto van bol.com (550 px, oorspronkelijke URL) voor de specificatiekaart, alleen bij een geldig aanbod. */
function rmk_bol_foto( array $m ) {
	if ( ! rmk_bol_aanbod( $m ) || empty( $m['bol']['afbeelding']['url'] ) || ! rmk_bol_afbeelding_ok( $m['bol']['afbeelding']['url'] ) ) {
		return null;
	}
	$f = $m['bol']['afbeelding'];
	// De foto staat wel in de HTML: paginacache (LiteSpeed) niet langer bewaren dan het aanbod geldig is.
	$a = rmk_bol_aanbod( $m );
	do_action( 'litespeed_control_set_ttl', max( 60, RMK_BOL_GELDIG - ( rmk_bol_nu() - (int) $a['tijd'] ) ) );
	return array( 'url' => $f['url'], 'fabrikant' => 'bol.com', 'breedte' => (int) ( $f['breedte'] ?? 550 ), 'hoogte' => (int) ( $f['hoogte'] ?? 550 ), 'bron' => 'bol' );
}

/* Advertentie-regel: met RMK_AFFILIATE_ACTIVE aan één keer per pagina boven de eerste Bol-knop, als er nog geen staat. */
add_filter( 'the_content', function ( $html ) {
	if ( ! rmk_bol_zichtbaar() || false === strpos( (string) $html, 'data-rmk-bol' ) ) {
		return $html;
	}
	$pos = strpos( $html, 'data-rmk-bol' );
	if ( false !== strpos( substr( $html, 0, $pos ), 'rmk-affnote' ) ) {
		return $html;
	}
	$art = strrpos( substr( $html, 0, $pos ), '<article' );
	if ( false === $art ) {
		return $html;
	}
	return substr( $html, 0, $art ) . rmk_bol_advertentie_html() . substr( $html, $art );
}, 25 );

function rmk_bol_advertentie_html() {
	// Tekst: de instelling rmk_advertentie_tekst (via /wp/v2/settings, zie scripts/ronde30_affiliate_teksten.py), anders de
	// huidige tekst van het patroon affiliate-melding. Zo kan de tekst uit tekstwijzigingen-affiliate-live.md (punt 8) op
	// het moment dat de schakelaar aan gaat worden gezet, zonder nieuwe thema-zip.
	$tekst = trim( (string) get_option( 'rmk_advertentie_tekst', '' ) );
	if ( '' === $tekst ) {
		$tekst = 'Advertentie: via deze knoppen krijgen wij mogelijk een commissie. Dat verandert de score niet.';
	}
	return '<p class="rmk-affnote"><svg class="rmk-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.01"/></svg><span>'
		. esc_html( apply_filters( 'rmk_bol_advertentie_tekst', $tekst ) ) . '</span></p>';
}
add_action( 'init', function () {
	register_setting( 'general', 'rmk_advertentie_tekst', array(
		'type'              => 'string',
		'description'       => 'Tekst van de advertentie-regel boven de eerste Bol-knop (alleen zichtbaar met RMK_AFFILIATE_ACTIVE).',
		'sanitize_callback' => 'sanitize_text_field',
		'show_in_rest'      => true,
		'default'           => '',
	) );
} );

/* ------------------------------------------------------------------ beheer: /rmk/v1/bol-status en WP-CLI */

function rmk_bol_status() {
	$store = (array) get_option( RMK_BOL_AANBOD_OPTION, array() );
	$hist  = (array) get_option( RMK_BOL_LOG_OPTION, array() );
	$per   = array();
	foreach ( rmk_models_data()['modellen'] as $m ) {
		if ( empty( $m['ean'] ) ) {
			continue;
		}
		$a          = isset( $store[ $m['id'] ] ) ? $store[ $m['id'] ] : null;
		$per[ $m['id'] ] = array(
			'model'       => $m['naam'],
			'ean'         => (string) $m['ean'],
			'uitkomst'    => $a ? $a['status'] : 'nog niet opgehaald',
			'prijs'       => $a && 'ok' === $a['status'] ? $a['prijs'] : null,
			'verkoper'    => $a && 'ok' === $a['status'] ? $a['verkoper'] : null,
			'partner'     => $a && 'ok' === $a['status'] ? $a['partner'] : null,
			'detail'      => $a && isset( $a['detail'] ) ? $a['detail'] : null,
			'opgehaald'   => $a ? wp_date( 'Y-m-d H:i', (int) $a['tijd'] ) : null,
			'geldig_tot'  => $a && 'ok' === $a['status'] ? wp_date( 'Y-m-d H:i', (int) $a['tijd'] + RMK_BOL_GELDIG ) : null,
			'op_de_site'  => (bool) rmk_bol_aanbod( $m ),
		);
	}
	$volgende = wp_next_scheduled( RMK_BOL_RONDE_HOOK );
	return array(
		'constanten_aanwezig' => rmk_bol_geconfigureerd(),
		'affiliate_actief'    => function_exists( 'rmk_affiliate_actief' ) && rmk_affiliate_actief(),
		'volgende_ronde'      => $volgende ? wp_date( 'Y-m-d H:i', $volgende ) : null,
		'laatste_ronde'       => $hist ? $hist[0] : null,
		'modellen'            => $per,
	);
}

/* rmk.js krijgt het adres van de prijsroute alleen als de Bol-regel zichtbaar mag zijn. */
add_filter( 'rmk_config', function ( $c ) {
	if ( rmk_bol_zichtbaar() ) {
		$c['bolPrijsUrl'] = rest_url( 'rmk/v1/bol-prijs' );
	}
	return $c;
} );

add_action( 'rest_api_init', function () {
	// Publiek (1.3.7): de enige rmk-route die zonder inloggen gegevens geeft. Nooit gecachet (inc/techniek.php zet
	// Cache-Control: no-store, CDN-Cache-Control: no-store en X-LiteSpeed-Cache-Control: no-cache op alle /wp-json/).
	register_rest_route( 'rmk/v1', '/bol-prijs', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'args'                => array( 'modellen' => array( 'type' => 'string', 'required' => true ) ),
		'callback'            => function ( WP_REST_Request $r ) {
			return rest_ensure_response( rmk_bol_prijzen_publiek( $r->get_param( 'modellen' ) ) );
		},
	) );
	// Beheer (1.3.7): één ronde starten. Alleen beheerders, nooit gecachet.
	register_rest_route( 'rmk/v1', '/bol-ronde', array(
		'methods'             => 'POST',
		'permission_callback' => function () {
			return current_user_can( 'manage_options' );
		},
		'callback'            => function () {
			return rest_ensure_response( rmk_bol_ronde() );
		},
	) );
	register_rest_route( 'rmk/v1', '/bol-status', array(
		'methods'             => 'GET',
		'permission_callback' => function () {
			return current_user_can( 'manage_options' );
		},
		'callback'            => function () {
			return rest_ensure_response( rmk_bol_status() ); // nooit gecachet: zie inc/techniek.php (alle /wp-json/)
		},
	) );
} );

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	// Echte cron (hPanel): wp --path=<pad> rmk bol-ronde
	WP_CLI::add_command( 'rmk bol-ronde', function () {
		$log = rmk_bol_ronde();
		WP_CLI::log( wp_json_encode( $log, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );
	} );
	WP_CLI::add_command( 'rmk bol-status', function () {
		WP_CLI::log( wp_json_encode( rmk_bol_status(), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );
	} );
}
