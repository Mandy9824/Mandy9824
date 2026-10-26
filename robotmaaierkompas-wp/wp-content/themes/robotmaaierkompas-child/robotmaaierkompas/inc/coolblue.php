<?php
/**
 * robotmaaierkompas.nl — Coolblue via de Awin-productfeed (1.3.10).
 *
 * Bronnen voor de vorm: het voorbeeldbestand coolblue-feed-robotmaaiers.csv (Awin-feed van Coolblue NL, 24 oktober 2026)
 * en het Logboek van robotmaaierkompas_modeldata_v1.xlsx, rijen 316-328 (koppeling, clickref, verversing, deeplink).
 * Niets daarbuiten is aangenomen.
 *
 * Instellen (in wp-config.php op de server, NOOIT in het thema of in git):
 *   define( 'RMK_COOLBLUE_FEED_URL', '…' );    // feed-URL van Awin, bevat een geheime sleutel
 *   define( 'RMK_COOLBLUE_AWMID', 85161 );      // adverteerder Coolblue NL (geen geheim)
 *   define( 'RMK_COOLBLUE_AWAFFID', 3126598 );  // publisher (geen geheim)
 *   define( 'RMK_COOLBLUE_ACTIVE', true );      // de schakelaar; standaard uit
 * Ontbreekt een van de drie eerste constanten: geen verzoeken, geen ingeplande taak, geen Coolblue-regel (alles zoals
 * 1.3.9). Staan ze er wel maar RMK_COOLBLUE_ACTIVE niet: de feedtaak draait (zodat het statusoverzicht iets laat zien),
 * maar er komt nergens een Coolblue-regel, -knop of -foto op de site. Onafhankelijk van RMK_AFFILIATE_ACTIVE (Bol).
 *
 * Feed (voorbeeldbestand): gzip-CSV met kopregel; per product onder meer merchant_product_id, search_price, in_stock,
 * merchant_image_url en merchant_deep_link. We pakken hem met PHP uit (inflate, met controle van het einde van de
 * gzip-stroom), lezen hem regel voor regel en bewaren alleen de producten waarvan merchant_product_id bij een model in
 * het blok "coolblue" van de modelgegevens staat (= blad Coolblue): prijs, voorraad, afbeeldings-URL en productpagina.
 * Per ronde ook het tijdstip en een SHA-256 van het hele uitgepakte bestand (de gzip-kop bevat een tijdstempel, dus een
 * hash van het gecomprimeerde bestand zou ook veranderen als de inhoud gelijk blijft). De feed zelf wordt niet bewaard.
 *
 * Versheid (besluit Mandy): een Coolblue-regel alleen als het product in de laatste feed staat met in_stock = 1 en een
 * prijs > 0, de feed in de laatste 26 uur is opgehaald én de hash in de laatste 48 uur is veranderd. Anders niets.
 *
 * Link (Logboek 327): https://www.awin1.com/cread.php?awinmid=<AWMID>&awinaffid=<AWAFFID>&clickref=<clickref>&ued=<url>
 * met ued = merchant_deep_link volledig gecodeerd (PHP rawurlencode = Python quote(url, safe="")). clickref (Logboek
 * 318): model-ID en paginaslug, kleine letters, alleen letters, cijfers en koppeltekens, hoogstens 50 tekens.
 *
 * Planning: elke nacht (WP-Cron, 04:20 in de tijdzone van de site). Reserve: is er 25 uur geen ronde gestart, dan start
 * hooguit één keer per uur een ronde aan het einde van een verzoek, nadat het antwoord al naar de bezoeker is gestuurd.
 * Zet in hPanel ook een echte cron (wp rmk coolblue-ronde). Na elke ronde wordt de paginacache geleegd.
 */

defined( 'ABSPATH' ) || exit;

const RMK_CB_STORE_OPTION    = 'rmk_coolblue_feed';       // laatste geslaagde feed: meta + gevonden producten
const RMK_CB_LOG_OPTION      = 'rmk_coolblue_log';        // laatste rondes (zonder secrets)
const RMK_CB_LOCK_KEY        = 'rmk_coolblue_lock';       // transient
const RMK_CB_RONDE_HOOK      = 'rmk_coolblue_ronde';
const RMK_CB_BEWAKING_HOOK   = 'rmk_coolblue_bewaking';
const RMK_CB_RESERVE_OPTION  = 'rmk_coolblue_reserve';    // vroegste tijd voor de volgende reservecontrole (autoload)
const RMK_CB_STORING_OPTION  = 'rmk_coolblue_storing';    // welke storing al gemeld is
const RMK_CB_OPGEHAALD_MAX   = 26 * HOUR_IN_SECONDS;
const RMK_CB_HASH_MAX        = 48 * HOUR_IN_SECONDS;
const RMK_CB_RESERVE_NA      = 25 * HOUR_IN_SECONDS;
const RMK_CB_MAX_BYTES       = 50 * MB_IN_BYTES;          // gecomprimeerd en uitgepakt
const RMK_CB_KOLOMMEN        = array( 'merchant_product_id', 'search_price', 'in_stock', 'merchant_image_url', 'merchant_deep_link' );

/** Staan de drie Coolblue-constanten in wp-config.php? (De feed-URL wordt nergens getoond of gelogd.) */
function rmk_coolblue_geconfigureerd() {
	if ( ! defined( 'RMK_COOLBLUE_FEED_URL' ) || 0 !== strpos( trim( (string) RMK_COOLBLUE_FEED_URL ), 'https://' ) ) {
		return false;
	}
	foreach ( array( 'RMK_COOLBLUE_AWMID', 'RMK_COOLBLUE_AWAFFID' ) as $c ) {
		if ( ! defined( $c ) || ! preg_match( '/^\d{1,12}$/', trim( (string) constant( $c ) ) ) ) {
			return false;
		}
	}
	return true;
}

/** Mag er een Coolblue-regel op de site? Alleen met de constanten én RMK_COOLBLUE_ACTIVE aan. */
function rmk_coolblue_zichtbaar() {
	return rmk_coolblue_geconfigureerd() && defined( 'RMK_COOLBLUE_ACTIVE' ) && RMK_COOLBLUE_ACTIVE;
}

/** Tijd, te vervangen in tests. */
function rmk_coolblue_nu() {
	return (int) apply_filters( 'rmk_coolblue_nu', time() );
}

/** Tekst zonder de feed-URL (met sleutel) en zonder iets dat op een sleutel lijkt. */
function rmk_coolblue_zonder_secrets( $tekst ) {
	$tekst = (string) $tekst;
	if ( defined( 'RMK_COOLBLUE_FEED_URL' ) && strlen( trim( (string) RMK_COOLBLUE_FEED_URL ) ) >= 8 ) {
		$url   = trim( (string) RMK_COOLBLUE_FEED_URL );
		$tekst = str_replace( array( $url, rawurlencode( $url ), esc_url( $url ) ), '[feed-URL]', $tekst );
	}
	$tekst = preg_replace( '#https?://\S+#i', '[adres]', $tekst );
	return preg_replace( '/((?:apikey|api_key|key|token|secret)[=\/:]\s*)[A-Za-z0-9._~+\/=-]{6,}/i', '$1…', $tekst );
}

/* ------------------------------------------------------------------ planning: elke nacht, met reserve */

add_action( 'init', function () {
	if ( ! rmk_coolblue_geconfigureerd() ) {
		foreach ( array( RMK_CB_RONDE_HOOK, RMK_CB_BEWAKING_HOOK ) as $h ) {
			if ( wp_next_scheduled( $h ) ) {
				wp_clear_scheduled_hook( $h );
			}
		}
		return;
	}
	if ( ! wp_next_scheduled( RMK_CB_RONDE_HOOK ) ) {
		$t = new DateTimeImmutable( '@' . rmk_coolblue_nu() );
		$t = $t->setTimezone( wp_timezone() )->setTime( 4, 20 );
		if ( $t->getTimestamp() <= rmk_coolblue_nu() ) {
			$t = $t->modify( '+1 day' );
		}
		wp_schedule_event( $t->getTimestamp(), 'daily', RMK_CB_RONDE_HOOK );
	}
	if ( ! wp_next_scheduled( RMK_CB_BEWAKING_HOOK ) ) {
		wp_schedule_event( rmk_coolblue_nu() + 600, 'hourly', RMK_CB_BEWAKING_HOOK );
	}
} );
add_action( RMK_CB_RONDE_HOOK, 'rmk_coolblue_ronde' );
add_action( RMK_CB_BEWAKING_HOOK, 'rmk_coolblue_bewaking' );
add_action( 'switch_theme', function () {
	wp_clear_scheduled_hook( RMK_CB_RONDE_HOOK );
	wp_clear_scheduled_hook( RMK_CB_BEWAKING_HOOK );
} );

/* Na elke ronde (ook een mislukte) de paginacache legen. */
add_action( 'rmk_coolblue_na_ronde', function () {
	do_action( 'litespeed_purge_all' );
} );

/** Start van de laatste ronde (ook mislukt), 0 als er nog geen is. */
function rmk_coolblue_laatste_start() {
	$hist = (array) get_option( RMK_CB_LOG_OPTION, array() );
	return $hist ? (int) $hist[0]['start'] : 0;
}

/**
 * Reserve (de cron kan stilliggen): hooguit één keer per uur, aan het einde van een verzoek. Is er 25 uur geen ronde
 * gestart, dan eerst het antwoord naar de bezoeker sturen en daarna de ronde draaien. Ook de bewaking draait hier.
 */
add_action( 'shutdown', function () {
	if ( ! rmk_coolblue_geconfigureerd() || (int) get_option( RMK_CB_RESERVE_OPTION, 0 ) > rmk_coolblue_nu() ) {
		return;
	}
	update_option( RMK_CB_RESERVE_OPTION, rmk_coolblue_nu() + HOUR_IN_SECONDS, true );
	if ( rmk_coolblue_nu() - rmk_coolblue_laatste_start() > RMK_CB_RESERVE_NA ) {
		if ( function_exists( 'litespeed_finish_request' ) ) {
			litespeed_finish_request();
		} elseif ( function_exists( 'fastcgi_finish_request' ) ) {
			fastcgi_finish_request();
		}
		rmk_coolblue_ronde( 'reserve' );
	}
	rmk_coolblue_bewaking();
}, 20 );

/* ------------------------------------------------------------------ modelgegevens */

/** Modellen met een blok "coolblue" (merchant_product_id) in de modelgegevens: merchant_product_id => model-ID. */
function rmk_coolblue_modellen() {
	$uit = array();
	foreach ( rmk_models_data()['modellen'] as $m ) {
		$id = isset( $m['coolblue']['merchant_product_id'] ) ? trim( (string) $m['coolblue']['merchant_product_id'] ) : '';
		if ( preg_match( '/^\d{1,12}$/', $id ) && ! isset( $uit[ $id ] ) ) {
			$uit[ $id ] = $m['id'];
		}
	}
	return $uit;
}

function rmk_coolblue_url_ok( $url, $host = 'www.coolblue.nl' ) {
	$p = wp_parse_url( (string) $url );
	return ! empty( $p['scheme'] ) && 'https' === $p['scheme'] && isset( $p['host'] ) && $host === strtolower( $p['host'] );
}

function rmk_coolblue_afbeelding_ok( $url ) {
	return rmk_coolblue_url_ok( $url, 'coolblue.bynder.com' );
}

/* ------------------------------------------------------------------ ophalen en lezen */

/**
 * Pakt het gzip-bestand $gz uit naar een tijdelijke stroom en berekent de SHA-256 van de uitgepakte inhoud.
 * Geeft [stroom, hash, bytes] of een WP_Error (leeg, geen gzip, kapot of afgebroken, te groot).
 */
function rmk_coolblue_uitpakken( $gz ) {
	$in = @fopen( $gz, 'rb' );
	if ( ! $in ) {
		return new WP_Error( 'rmk_cb_bestand', 'Gedownload bestand niet te openen.' );
	}
	$kop = fread( $in, 2 );
	if ( false === $kop || strlen( $kop ) < 2 ) {
		fclose( $in );
		return new WP_Error( 'rmk_cb_leeg', 'Leeg bestand (geen gzip-gegevens).' );
	}
	if ( "\x1f\x8b" !== $kop ) {
		// 1.3.12: geen gzip. Is het al een CSV met onze kolommen (feed zonder compressie, of onderweg uitgepakt), dan lezen we
		// hem zoals hij is; anders een melding met het begin van het antwoord, zonder adressen of sleutels.
		rewind( $in );
		$begin = (string) fread( $in, 4096 );
		$regel = strtolower( strtok( $begin, "\n" ) );
		if ( false !== strpos( $regel, 'merchant_product_id' ) && false !== strpos( $regel, ',' ) ) {
			rewind( $in );
			$uit  = fopen( 'php://temp/maxmemory:' . ( 2 * MB_IN_BYTES ), 'w+b' );
			$hash = hash_init( 'sha256' );
			$n    = 0;
			while ( ! feof( $in ) && false !== ( $blok = fread( $in, 65536 ) ) ) {
				$n += strlen( $blok );
				if ( $n > RMK_CB_MAX_BYTES ) {
					fclose( $in );
					fclose( $uit );
					return new WP_Error( 'rmk_cb_groot', 'Feed groter dan 50 MB.' );
				}
				hash_update( $hash, $blok );
				fwrite( $uit, $blok );
			}
			fclose( $in );
			rewind( $uit );
			return array( $uit, hash_final( $hash ), $n, 'niet gecomprimeerd' );
		}
		fclose( $in );
		$kort = trim( preg_replace( '/\s+/', ' ', preg_replace( '/[^\x20-\x7E\xC0-\xFF]/', ' ', substr( $begin, 0, 80 ) ) ) );
		return new WP_Error( 'rmk_cb_geen_gzip', 'Geen gzip-bestand en geen CSV met merchant_product_id; het antwoord begint met: "' . rmk_coolblue_zonder_secrets( $kort ) . '".' );
	}
	rewind( $in );
	$z    = inflate_init( ZLIB_ENCODING_GZIP );
	$uit  = fopen( 'php://temp/maxmemory:' . ( 2 * MB_IN_BYTES ), 'w+b' );
	$hash = hash_init( 'sha256' );
	$n    = 0;
	$eind = false;
	while ( ! feof( $in ) ) {
		$blok = fread( $in, 65536 );
		if ( false === $blok ) {
			break;
		}
		if ( $eind ) {
			if ( '' !== trim( $blok, "\0" ) ) {
				break; // gegevens na het einde van de gzip-stroom: meerdelige gzip lezen we niet
			}
			continue;
		}
		$data = @inflate_add( $z, $blok, ZLIB_SYNC_FLUSH );
		if ( false === $data ) {
			fclose( $in );
			fclose( $uit );
			return new WP_Error( 'rmk_cb_kapot', 'Kapotte gzip-gegevens.' );
		}
		$n += strlen( $data );
		if ( $n > RMK_CB_MAX_BYTES ) {
			fclose( $in );
			fclose( $uit );
			return new WP_Error( 'rmk_cb_groot', 'Uitgepakte feed groter dan 50 MB.' );
		}
		hash_update( $hash, $data );
		fwrite( $uit, $data );
		if ( ZLIB_STREAM_END === inflate_get_status( $z ) ) {
			$eind = true;
		}
	}
	fclose( $in );
	if ( ! $eind ) {
		fclose( $uit );
		return new WP_Error( 'rmk_cb_afgebroken', 'Gzip-bestand afgebroken (geen einde van de stroom).' );
	}
	if ( 0 === $n ) {
		fclose( $uit );
		return new WP_Error( 'rmk_cb_leeg', 'Uitgepakte feed is leeg.' );
	}
	rewind( $uit );
	return array( $uit, hash_final( $hash ), $n );
}

/** Getal uit search_price ("729", "729.00" of "1.099,00"); 0 bij iets anders. */
function rmk_coolblue_prijs( $v ) {
	$v = trim( (string) $v );
	if ( preg_match( '/^\d+(\.\d{1,2})?$/', $v ) ) {
		return round( (float) $v, 2 );
	}
	if ( preg_match( '/^\d{1,3}(\.\d{3})*(,\d{1,2})?$/', $v ) ) {
		return round( (float) str_replace( array( '.', ',' ), array( '', '.' ), $v ), 2 );
	}
	return 0.0;
}

/**
 * Leest de uitgepakte CSV regel voor regel. Geeft [producten (alleen die uit het blad Coolblue), rijen] of een WP_Error.
 */
function rmk_coolblue_lezen( $stroom, array $gezocht ) {
	$kop = fgetcsv( $stroom, 0, ',', '"', '' );
	if ( ! is_array( $kop ) || ! $kop ) {
		return new WP_Error( 'rmk_cb_kop', 'Geen kopregel in de feed.' );
	}
	$kop  = array_map( function ( $k ) { return strtolower( trim( (string) $k, " \t\r\n\xEF\xBB\xBF" ) ); }, $kop );
	$plek = array_flip( $kop );
	$mist = array_diff( RMK_CB_KOLOMMEN, $kop );
	if ( $mist ) {
		return new WP_Error( 'rmk_cb_kolommen', 'Kolommen ontbreken in de feed: ' . implode( ', ', $mist ) . '.' );
	}
	$producten = array();
	$rijen     = 0;
	while ( false !== ( $r = fgetcsv( $stroom, 0, ',', '"', '' ) ) ) {
		if ( array( null ) === $r ) {
			continue; // lege regel
		}
		$rijen++;
		$id = trim( (string) ( $r[ $plek['merchant_product_id'] ] ?? '' ) );
		if ( ! isset( $gezocht[ $id ] ) || isset( $producten[ $id ] ) ) {
			continue;
		}
		$producten[ $id ] = array(
			'prijs'      => rmk_coolblue_prijs( $r[ $plek['search_price'] ] ?? '' ),
			'in_stock'   => '1' === trim( (string) ( $r[ $plek['in_stock'] ] ?? '' ) ),
			'afbeelding' => substr( trim( (string) ( $r[ $plek['merchant_image_url'] ] ?? '' ) ), 0, 500 ),
			'url'        => substr( trim( (string) ( $r[ $plek['merchant_deep_link'] ] ?? '' ) ), 0, 500 ),
		);
	}
	return array( $producten, $rijen );
}

/** Downloadt de feed naar een tijdelijk bestand. Geeft het pad of een WP_Error (zonder de URL). */
function rmk_coolblue_downloaden() {
	// 1.3.11: wp_tempnam() staat in wp-admin/includes/file.php en bestaat niet bij cron, REST of een bezoek.
	$tmp = @tempnam( get_temp_dir(), 'rmk-coolblue' );
	if ( ! $tmp ) {
		return new WP_Error( 'rmk_cb_tmp', 'Geen tijdelijk bestand.' );
	}
	$r = wp_remote_get( trim( (string) RMK_COOLBLUE_FEED_URL ), array( 'timeout' => 120, 'redirection' => 3, 'stream' => true, 'filename' => $tmp,
		'limit_response_size' => RMK_CB_MAX_BYTES, 'headers' => array( 'Accept-Encoding' => 'identity' ) ) );
	if ( is_wp_error( $r ) ) {
		@unlink( $tmp );
		return new WP_Error( 'rmk_cb_http', 'Verbinding: ' . rmk_coolblue_zonder_secrets( $r->get_error_message() ) );
	}
	$code = (int) wp_remote_retrieve_response_code( $r );
	if ( 200 !== $code ) {
		@unlink( $tmp );
		return new WP_Error( 'rmk_cb_http', 'HTTP ' . $code . '.' );
	}
	return $tmp;
}

/**
 * Eén ronde: feed ophalen, uitpakken, regel voor regel lezen, alleen onze producten bewaren. Bij een fout blijft de vorige
 * feed staan (de versheidsregels laten de Coolblue-regel dan na 26 uur vanzelf verdwijnen). Log zonder secrets.
 */
function rmk_coolblue_ronde( $aanleiding = 'taak' ) {
	$start = rmk_coolblue_nu();
	$log   = array( 'start' => $start, 'eind' => null, 'aanleiding' => (string) $aanleiding, 'gelukt' => false, 'rijen' => 0, 'gevonden' => 0,
		'op_voorraad' => 0, 'hash_veranderd' => null, 'melding' => '' );
	if ( ! rmk_coolblue_geconfigureerd() ) {
		$log['melding'] = 'Coolblue-constanten ontbreken in wp-config.php: niets opgehaald.';
		return $log;
	}
	if ( get_transient( RMK_CB_LOCK_KEY ) ) {
		$log['melding'] = 'Er draait al een ronde.';
		return $log; // niet in het log: de lopende ronde schrijft zelf
	}
	set_transient( RMK_CB_LOCK_KEY, 1, 15 * MINUTE_IN_SECONDS );
	// 1.3.11: genoeg tijd voor download en uitpakken, en een vangnet als de ronde toch afbreekt (tijdslimiet, geheugen,
	// fatale fout): dan wordt het slot vrijgegeven en komt de ronde met de foutmelding (zonder secrets) in het log.
	if ( function_exists( 'set_time_limit' ) ) {
		@set_time_limit( 300 );
	}
	$GLOBALS['rmk_cb_lopend'] = $log;
	register_shutdown_function( 'rmk_coolblue_vangnet' );
	$gezocht = rmk_coolblue_modellen();
	$gz      = rmk_coolblue_downloaden();
	$uitkomst = is_wp_error( $gz ) ? $gz : rmk_coolblue_uitpakken( $gz );
	if ( ! is_wp_error( $gz ) ) {
		@unlink( $gz );
	}
	if ( ! is_wp_error( $uitkomst ) ) {
		list( $stroom, $hash, $bytes ) = $uitkomst;
		$log['bestand'] = $uitkomst[3] ?? 'gzip';
		$gelezen = rmk_coolblue_lezen( $stroom, $gezocht );
		fclose( $stroom );
		if ( is_wp_error( $gelezen ) ) {
			$uitkomst = $gelezen;
		} elseif ( 0 === $gelezen[1] ) {
			$uitkomst = new WP_Error( 'rmk_cb_leeg', 'Feed zonder producten.' );
		}
	}
	if ( is_wp_error( $uitkomst ) ) {
		$log['melding'] = rmk_coolblue_zonder_secrets( $uitkomst->get_error_message() );
	} else {
		list( $producten, $rijen ) = $gelezen;
		$oud   = (array) get_option( RMK_CB_STORE_OPTION, array() );
		$zelfde = ! empty( $oud['hash'] ) && hash_equals( (string) $oud['hash'], $hash );
		$per    = array();
		foreach ( $producten as $pid => $p ) {
			$per[ $gezocht[ $pid ] ] = array( 'merchant_product_id' => (string) $pid ) + $p;
		}
		update_option( RMK_CB_STORE_OPTION, array(
			'opgehaald'  => $start,
			'hash'       => $hash,
			'hash_sinds' => $zelfde && ! empty( $oud['hash_sinds'] ) ? (int) $oud['hash_sinds'] : $start,
			'bytes'      => (int) $bytes,
			'rijen'      => (int) $rijen,
			'producten'  => $per,
		), false );
		$log['gelukt']         = true;
		$log['rijen']          = (int) $rijen;
		$log['gevonden']       = count( $per );
		$log['op_voorraad']    = count( array_filter( $per, function ( $p ) { return $p['in_stock'] && $p['prijs'] > 0; } ) );
		$log['hash_veranderd'] = ! $zelfde;
		$log['niet_in_feed']   = array_values( array_diff( array_values( $gezocht ), array_keys( $per ) ) );
	}
	unset( $GLOBALS['rmk_cb_lopend'] );
	delete_transient( RMK_CB_LOCK_KEY );
	$log['eind'] = rmk_coolblue_nu();
	$hist        = (array) get_option( RMK_CB_LOG_OPTION, array() );
	array_unshift( $hist, $log );
	update_option( RMK_CB_LOG_OPTION, array_slice( $hist, 0, 20 ), false );
	do_action( 'rmk_coolblue_na_ronde', $log );
	return $log;
}

/** Vangnet (1.3.11): brak een ronde af zonder af te ronden, dan het slot vrijgeven en de fout loggen. */
function rmk_coolblue_vangnet() {
	if ( empty( $GLOBALS['rmk_cb_lopend'] ) ) {
		return;
	}
	$log = $GLOBALS['rmk_cb_lopend'];
	unset( $GLOBALS['rmk_cb_lopend'] );
	$e              = error_get_last();
	$log['eind']    = rmk_coolblue_nu();
	$log['melding'] = 'Ronde afgebroken' . ( $e && in_array( $e['type'], array( E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR ), true )
		? ': ' . rmk_coolblue_zonder_secrets( substr( preg_replace( '#\s+in\s+/\S+#', '', (string) $e['message'] ), 0, 200 ) ) : '' ) . '.';
	delete_transient( RMK_CB_LOCK_KEY );
	$hist = (array) get_option( RMK_CB_LOG_OPTION, array() );
	array_unshift( $hist, $log );
	update_option( RMK_CB_LOG_OPTION, array_slice( $hist, 0, 20 ), false );
}

/* ------------------------------------------------------------------ versheid en weergave */

/** Is de laatste feed vers genoeg? Geeft [vers (bool), reden]. */
function rmk_coolblue_feed_vers( $feed = null ) {
	$feed = null === $feed ? (array) get_option( RMK_CB_STORE_OPTION, array() ) : $feed;
	$nu   = rmk_coolblue_nu();
	if ( empty( $feed['opgehaald'] ) ) {
		return array( false, 'nog geen feed opgehaald' );
	}
	if ( $nu - (int) $feed['opgehaald'] > RMK_CB_OPGEHAALD_MAX || (int) $feed['opgehaald'] > $nu ) {
		return array( false, 'laatste feed ouder dan 26 uur' );
	}
	if ( empty( $feed['hash_sinds'] ) || $nu - (int) $feed['hash_sinds'] > RMK_CB_HASH_MAX ) {
		return array( false, 'feed verouderd: niet veranderd in 48 uur' );
	}
	return array( true, '' );
}

/** Geldig Coolblue-product voor model $m, of null. Alleen als de Coolblue-regel zichtbaar mag zijn. */
function rmk_coolblue_aanbod( array $m ) {
	if ( ! rmk_coolblue_zichtbaar() || empty( $m['id'] ) || empty( $m['coolblue']['merchant_product_id'] ) ) {
		return null;
	}
	$feed = (array) get_option( RMK_CB_STORE_OPTION, array() );
	if ( ! rmk_coolblue_feed_vers( $feed )[0] ) {
		return null;
	}
	$p = $feed['producten'][ $m['id'] ] ?? null;
	if ( ! $p || (string) $p['merchant_product_id'] !== trim( (string) $m['coolblue']['merchant_product_id'] )
		|| empty( $p['in_stock'] ) || ! ( (float) $p['prijs'] > 0 ) || ! rmk_coolblue_url_ok( $p['url'] ) ) {
		return null;
	}
	return $p + array( 'tijd' => (int) $feed['opgehaald'] );
}

/** clickref: model-ID en paginaslug, kleine letters, alleen letters, cijfers en koppeltekens, hoogstens 50 tekens. */
function rmk_coolblue_clickref( $model_id, $slug = null ) {
	$slug = function_exists( 'rmk_bol_subid' ) ? rmk_bol_subid( $slug ) : (string) $slug;
	$ref  = strtolower( (string) $model_id . '-' . $slug );
	$ref  = trim( preg_replace( '/-+/', '-', preg_replace( '/[^a-z0-9-]/', '', $ref ) ), '-' );
	return rtrim( substr( $ref, 0, 50 ), '-' );
}

/** De Awin-deeplink in de vorm uit het Logboek (rij 327). */
function rmk_coolblue_link( $product_url, $clickref ) {
	return 'https://www.awin1.com/cread.php?awinmid=' . rawurlencode( trim( (string) RMK_COOLBLUE_AWMID ) )
		. '&awinaffid=' . rawurlencode( trim( (string) RMK_COOLBLUE_AWAFFID ) )
		. '&clickref=' . rawurlencode( (string) $clickref ) . '&ued=' . rawurlencode( (string) $product_url );
}

/**
 * De Coolblue-regel in de productkaart: knop, bronregel en een leeg prijsvak. De prijs staat niet in de HTML maar komt uit
 * /rmk/v1/bol-prijs (nooit gecachet), via rmk.js. Is het product daar niet (meer) geldig, dan haalt rmk.js de regel weg.
 */
function rmk_coolblue_regel_html( array $m, $slug = null ) {
	$p = rmk_coolblue_aanbod( $m );
	if ( ! $p ) {
		return '';
	}
	$link = rmk_coolblue_link( $p['url'], rmk_coolblue_clickref( $m['id'], $slug ) );
	// De HTML bevat de knop: paginacache (LiteSpeed) niet langer bewaren dan de feed vers is.
	do_action( 'litespeed_control_set_ttl', max( 60, RMK_CB_OPGEHAALD_MAX - ( rmk_coolblue_nu() - (int) $p['tijd'] ) ) );
	return '<div class="rmk-offer rmk-offer--stack rmk-offer--coolblue" data-rmk-cb data-rmk-cb-model="' . esc_attr( $m['id'] ) . '">'
		. '<span class="rmk-offer__line" data-rmk-cb-prijs hidden></span>'
		. '<a class="rmk-btn rmk-btn--primary" href="' . esc_url( $link ) . '" rel="sponsored nofollow" data-rmk-cb-link>Bekijk bij Coolblue</a>'
		. '<span class="rmk-offer__src">Je gaat naar Coolblue. Bron: Coolblue.</span></div>';
}

/** Foto van Coolblue (merchant_image_url, ongewijzigd) als het model geen Bol-foto heeft maar wel een geldige Coolblue-regel. */
function rmk_coolblue_foto( array $m ) {
	$p = rmk_coolblue_aanbod( $m );
	if ( ! $p || ! rmk_coolblue_afbeelding_ok( $p['afbeelding'] ) ) {
		return null;
	}
	return array( 'url' => $p['afbeelding'], 'fabrikant' => 'Coolblue', 'breedte' => 800, 'hoogte' => 800, 'bron' => 'coolblue' );
}

/** Wat de publieke prijsroute per model voor Coolblue teruggeeft: alleen model, prijs, tijdstip en winkel. */
function rmk_coolblue_prijs_data( array $m ) {
	$p = rmk_coolblue_aanbod( $m );
	if ( ! $p ) {
		return null;
	}
	return array(
		'model'    => (string) $m['id'],
		'prijs'    => (float) $p['prijs'],
		'tijdstip' => ( new DateTimeImmutable( '@' . (int) $p['tijd'] ) )->setTimezone( wp_timezone() )->format( DATE_ATOM ),
		'winkel'   => 'Coolblue',
	);
}

/* ------------------------------------------------------------------ bewaking: één e-mail per storing */

/**
 * Storing: geen geslaagde ronde in 26 uur, of een feed waarvan de hash 48 uur niet veranderd is. Eén e-mail per storing
 * (sleutel: soort + tijdstip van de laatste geslaagde feed of de hash); na een verse feed is de storing voorbij.
 */
function rmk_coolblue_bewaking() {
	if ( ! rmk_coolblue_geconfigureerd() ) {
		return array( 'status' => 'uit' );
	}
	$feed = (array) get_option( RMK_CB_STORE_OPTION, array() );
	$hist = (array) get_option( RMK_CB_LOG_OPTION, array() );
	if ( ! $feed && ! $hist ) {
		return array( 'status' => 'ok', 'reden' => 'nog geen ronde' );
	}
	list( $vers, $reden ) = rmk_coolblue_feed_vers( $feed );
	if ( $vers ) {
		if ( false !== get_option( RMK_CB_STORING_OPTION, false ) ) {
			delete_option( RMK_CB_STORING_OPTION );
		}
		return array( 'status' => 'ok' );
	}
	$soort = ( ! empty( $feed['opgehaald'] ) && rmk_coolblue_nu() - (int) $feed['opgehaald'] <= RMK_CB_OPGEHAALD_MAX ) ? 'verouderd' : 'ophalen';
	$sleutel = $soort . ':' . ( 'verouderd' === $soort ? (string) $feed['hash'] : (string) ( $feed['opgehaald'] ?? 0 ) );
	$gemeld  = get_option( RMK_CB_STORING_OPTION, false );
	if ( is_array( $gemeld ) && $gemeld['sleutel'] === $sleutel ) {
		return array( 'status' => 'al_gemeld', 'reden' => $reden );
	}
	$laatste = $hist ? $hist[0] : null;
	$fout    = 'geen';
	foreach ( $hist as $l ) {
		if ( ! empty( $l['gelukt'] ) ) {
			break;
		}
		if ( ! empty( $l['melding'] ) ) {
			$fout = wp_date( 'j-n-Y H:i', (int) $l['start'] ) . ': ' . $l['melding'];
			break;
		}
	}
	$next   = wp_next_scheduled( RMK_CB_RONDE_HOOK );
	$regels = array(
		'De Coolblue-regels staan niet op de site: ' . $reden . '.',
		'Laatste geslaagde feed: ' . ( ! empty( $feed['opgehaald'] ) ? wp_date( 'j-n-Y H:i', (int) $feed['opgehaald'] ) : 'nog geen' ) . '.',
		'Hash van de feed ongewijzigd sinds: ' . ( ! empty( $feed['hash_sinds'] ) ? wp_date( 'j-n-Y H:i', (int) $feed['hash_sinds'] ) : '-' ) . '.',
		'Laatste ronde: ' . ( $laatste ? wp_date( 'j-n-Y H:i', (int) $laatste['start'] ) . ( $laatste['gelukt'] ? ' (gelukt)' : ' (mislukt)' ) : 'geen' ) . '.',
		'Laatste fout: ' . $fout,
		'Volgende geplande ronde: ' . ( $next ? wp_date( 'j-n-Y H:i', $next ) . ( $next < rmk_coolblue_nu() - 15 * MINUTE_IN_SECONDS ? ' (al voorbij: de cron lijkt niet te draaien)' : '' ) : 'geen' ) . '.',
		'',
		'verouderd' === $soort
			? 'De feed wordt wel opgehaald, maar is in 48 uur niet veranderd. Controleer in Awin (Toolbox > My Product Feeds, kolom Last Imported) of Coolblue de feed nog bijwerkt.'
			: 'Controleer het statusoverzicht in wp-admin (Gereedschap > Robotmaaierkompas), de cron in hPanel (wp rmk coolblue-ronde) en of de feed-URL in wp-config.php nog klopt.',
		'Over deze storing krijg je geen nieuwe e-mail. Zodra er weer een verse feed is, is de storing voorbij.',
	);
	$ok = wp_mail( get_option( 'admin_email' ), '[Robotmaaierkompas] Coolblue-feed: ' . ( 'verouderd' === $soort ? 'verouderd' : 'niet opgehaald' ), rmk_coolblue_zonder_secrets( implode( "\n", $regels ) ) );
	if ( $ok ) {
		update_option( RMK_CB_STORING_OPTION, array( 'sleutel' => $sleutel, 'gemeld' => rmk_coolblue_nu() ), false );
	}
	return array( 'status' => $ok ? 'gemeld' : 'mail_mislukt', 'reden' => $reden );
}

/* ------------------------------------------------------------------ beheer: status, route en WP-CLI */

function rmk_coolblue_status() {
	$feed = (array) get_option( RMK_CB_STORE_OPTION, array() );
	$hist = (array) get_option( RMK_CB_LOG_OPTION, array() );
	list( $vers, $reden ) = rmk_coolblue_feed_vers( $feed );
	$per = array();
	foreach ( rmk_models_data()['modellen'] as $m ) {
		if ( empty( $m['coolblue']['merchant_product_id'] ) ) {
			continue;
		}
		$p             = $feed['producten'][ $m['id'] ] ?? null;
		$per[ $m['id'] ] = array(
			'model'               => $m['naam'],
			'merchant_product_id' => (string) $m['coolblue']['merchant_product_id'],
			'in_feed'             => (bool) $p,
			'prijs'               => $p ? $p['prijs'] : null,
			'in_stock'            => $p ? $p['in_stock'] : null,
			'op_de_site'          => (bool) rmk_coolblue_aanbod( $m ),
		);
	}
	$volgende = wp_next_scheduled( RMK_CB_RONDE_HOOK );
	return array(
		'constanten_aanwezig' => rmk_coolblue_geconfigureerd(),
		'coolblue_actief'     => defined( 'RMK_COOLBLUE_ACTIVE' ) && RMK_COOLBLUE_ACTIVE,
		'feed_vers'           => $vers,
		'reden'               => $reden,
		'opgehaald'           => ! empty( $feed['opgehaald'] ) ? wp_date( 'Y-m-d H:i', (int) $feed['opgehaald'] ) : null,
		'hash_ongewijzigd_sinds' => ! empty( $feed['hash_sinds'] ) ? wp_date( 'Y-m-d H:i', (int) $feed['hash_sinds'] ) : null,
		'rijen'               => $feed['rijen'] ?? null,
		'volgende_ronde'      => $volgende ? wp_date( 'Y-m-d H:i', $volgende ) : null,
		'laatste_ronde'       => $hist ? $hist[0] : null,
		'modellen'            => $per,
	);
}

add_action( 'rest_api_init', function () {
	$admin = function () {
		return current_user_can( 'manage_options' );
	};
	// Beheer: één ronde starten. Alleen beheerders, nooit gecachet (inc/techniek.php, alle /wp-json/).
	register_rest_route( 'rmk/v1', '/coolblue-ronde', array(
		'methods'             => 'POST',
		'permission_callback' => $admin,
		'callback'            => function () {
			return rest_ensure_response( rmk_coolblue_ronde( 'beheerroute' ) );
		},
	) );
	register_rest_route( 'rmk/v1', '/coolblue-status', array(
		'methods'             => 'GET',
		'permission_callback' => $admin,
		'callback'            => function () {
			return rest_ensure_response( rmk_coolblue_status() );
		},
	) );
} );

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	// Echte cron (hPanel): wp --path=<pad> rmk coolblue-ronde
	WP_CLI::add_command( 'rmk coolblue-ronde', function () {
		WP_CLI::log( wp_json_encode( rmk_coolblue_ronde( 'wp-cli' ), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );
	} );
	WP_CLI::add_command( 'rmk coolblue-status', function () {
		WP_CLI::log( wp_json_encode( rmk_coolblue_status(), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );
	} );
}
