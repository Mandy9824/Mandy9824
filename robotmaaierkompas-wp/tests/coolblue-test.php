<?php
/**
 * Test van de Coolblue-koppeling (thema 1.3.10, inc/coolblue.php) met NAGEBOOTSTE antwoorden, zonder netwerk en zonder
 * echte sleutel. De feed is het voorbeeldbestand van Awin (coolblue-feed-robotmaaiers.csv, niet in de repository) en
 * varianten die de test daaruit maakt. Vorm van de link: Logboek 318 en 327 van robotmaaierkompas_modeldata_v1.xlsx.
 * Er wordt geen enkele link gevolgd of aangeklikt.
 *
 * Draaien: php tests/coolblue-test.php <pad naar coolblue-feed-robotmaaiers.csv>          (alles aan)
 *          php tests/coolblue-test.php <csv> uit      (constanten wel, RMK_COOLBLUE_ACTIVE niet: geen regel op de site)
 *          php tests/coolblue-test.php <csv> zonder   (geen Coolblue-constanten: er mag niets veranderen)
 */
require __DIR__ . '/wp-stub.php';
$T = dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas';
define( 'RMK_DIR', $T );
$CSV   = $argv[1] ?? '';
$MODUS = $argv[2] ?? 'aan';
if ( ! is_readable( $CSV ) ) {
	fwrite( STDERR, "Gebruik: php tests/coolblue-test.php <coolblue-feed-robotmaaiers.csv> [uit|zonder]\n" );
	exit( 2 );
}
const FEED_URL = 'https://productdata.awin.com/datafeed/download/apikey/GEHEIM0123456789abcdef/fid/95886/format/csv/compression/gzip/';
if ( 'zonder' !== $MODUS ) {
	define( 'RMK_COOLBLUE_FEED_URL', FEED_URL );
	define( 'RMK_COOLBLUE_AWMID', 85161 );
	define( 'RMK_COOLBLUE_AWAFFID', 3126598 );
}
if ( 'aan' === $MODUS ) {
	define( 'RMK_COOLBLUE_ACTIVE', true );
}

// Aanvullingen op de stub (alleen wat inc/coolblue.php gebruikt)
function wp_remote_get( $url, $args = array() ) { return wp_remote_request( $url, $args + array( 'method' => 'GET' ) ); }
function get_temp_dir() { return sys_get_temp_dir() . '/'; } // zoals WordPress (wp-includes); wp_tempnam() bestaat NIET buiten wp-admin
function register_shutdown_function_test() {}
$GLOBALS['mails'] = array();
function wp_mail( $aan, $onderwerp, $tekst ) { $GLOBALS['mails'][] = compact( 'aan', 'onderwerp', 'tekst' ); return true; }
$GLOBALS['wp_options']['admin_email'] = 'beheer@example.test';

// Modelgegevens: het bestand uit het thema, met het blok "coolblue" uit het blad Coolblue (zoals excel_naar_json.py het maakt).
$CB = array( 'M002' => '975016', 'M006' => '975391', 'M008' => '962143', 'M011' => '959330', 'M015' => '975020' );
$data = json_decode( file_get_contents( $T . '/data/modellen.json' ), true );
foreach ( $data['modellen'] as &$m ) {
	if ( isset( $CB[ $m['id'] ] ) ) {
		$m['coolblue'] = array( 'merchant_product_id' => $CB[ $m['id'] ], 'product_url' => 'https://www.coolblue.nl/product/' . $CB[ $m['id'] ] . '/x.html' );
	}
}
unset( $m );
$MODELLEN = tempnam( sys_get_temp_dir(), 'rmkmod' );
file_put_contents( $MODELLEN, json_encode( $data ) );
add_filter( 'rmk_models_file', function () use ( $MODELLEN ) { return $MODELLEN; }, 20 );

require $T . '/inc/data.php';
require $T . '/inc/score.php';
require $T . '/inc/bol.php';
require $T . '/inc/coolblue.php';
require $T . '/inc/prijzen.php';
require $T . '/inc/redactie.php';

$GLOBALS['fail'] = 0;
function t( $n, $ok, $info = '' ) {
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $n . ( $info && ! $ok ? "\n       $info" : '' ) . "\n";
	$GLOBALS['fail'] += $ok ? 0 : 1;
}
$GLOBALS['nu'] = strtotime( '2026-10-24 04:20:00 Europe/Amsterdam' );
add_filter( 'rmk_coolblue_nu', function () { return $GLOBALS['nu']; } );
add_filter( 'rmk_bol_nu', function () { return $GLOBALS['nu']; } );
$H = HOUR_IN_SECONDS;

/* ---------------------------------------------------------------- nagebootste feed (gzip-CSV, zoals het voorbeeld) */
$fh    = fopen( $CSV, 'r' );
$KOPV  = fgetcsv( $fh, 0, ',', '"', '' );
$RIJEN = array();
while ( false !== ( $r = fgetcsv( $fh, 0, ',', '"', '' ) ) ) {
	if ( array( null ) !== $r ) {
		$RIJEN[] = $r;
	}
}
fclose( $fh );
$KOLOM = array_flip( $KOPV );
$KOP   = implode( ',', $KOPV );
/** CSV-tekst met aanpassingen per merchant_product_id: [id => [kolom => waarde]] of [id => null] (weglaten). */
function feed_csv( array $wijzig = array() ) {
	global $RIJEN, $KOP, $KOLOM;
	$uit = $KOP . "\n";
	foreach ( $RIJEN as $v ) {
		$id = $v[ $KOLOM['merchant_product_id'] ];
		if ( array_key_exists( $id, $wijzig ) && null === $wijzig[ $id ] ) {
			continue;
		}
		foreach ( $wijzig[ $id ] ?? array() as $k => $w ) {
			$v[ $KOLOM[ $k ] ] = $w;
		}
		$f = fopen( 'php://memory', 'w+' );
		fputcsv( $f, $v, ',', '"', '' );
		rewind( $f );
		$uit .= stream_get_contents( $f );
		fclose( $f );
	}
	return $uit;
}
$GLOBALS['feed'] = array( 'code' => 200, 'body' => gzencode( feed_csv() ), 'fout' => null, 'verzoeken' => 0, 'tijdens' => null );
add_filter( 'pre_http_request', function ( $pre, $args, $url ) {
	$GLOBALS['feed']['verzoeken']++;
	$GLOBALS['feed']['url'] = $url;
	$GLOBALS['feed']['args'] = $args;
	if ( $GLOBALS['feed']['tijdens'] ) {
		$GLOBALS['feed']['tweede'] = call_user_func( $GLOBALS['feed']['tijdens'] ); // een tweede ronde tijdens het ophalen
	}
	if ( $GLOBALS['feed']['fout'] ) {
		return new WP_Error( 'http_request_failed', $GLOBALS['feed']['fout'] );
	}
	if ( ! empty( $args['filename'] ) ) {
		file_put_contents( $args['filename'], $GLOBALS['feed']['body'] );
	}
	return array( 'response' => array( 'code' => $GLOBALS['feed']['code'] ), 'body' => '', 'headers' => array( 'content-type' => 'application/x-gzip' ) );
}, 10, 3 );
function feed( $body, $code = 200, $fout = null ) {
	$GLOBALS['feed'] = array_merge( $GLOBALS['feed'], array( 'body' => $body, 'code' => $code, 'fout' => $fout, 'verzoeken' => 0, 'tijdens' => null ) );
}

/* ---------------------------------------------------------------- hulpjes */
function kaart( $id ) { // productkaart zoals op de hub en pagina 1
	$m = rmk_get_model( $id );
	$a = 'p-' . $m['slug'];
	return '<article class="rmk-product" aria-labelledby="' . $a . '"><div class="rmk-product__head rmk-product__head--nomedia" style="grid-template-columns: 1fr"><div class="rmk-product__title"><h3 id="' . $a . '">' . $m['naam'] . '</h3>'
		. '<div class="rmk-scorecell" data-rmk-score data-model="' . $id . '"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div></div></div>'
		. '<div class="rmk-product__aside rmk-offers"><div class="rmk-offer"></div></div></article>';
}
function cbregel( $html ) {
	return preg_match( '#<div class="rmk-offer rmk-offer--stack rmk-offer--coolblue".*?</div>#s', $html, $m ) ? $m[0] : '';
}
function route( $ids ) {
	return json_decode( json_encode( rmk_bol_prijzen_publiek( $ids ) ), true );
}
function opties_zonder_secret() {
	return false === strpos( json_encode( $GLOBALS['wp_options'] + $GLOBALS['wp_trans'] ), 'GEHEIM0123456789' )
		&& false === strpos( json_encode( $GLOBALS['wp_options'] ), 'productdata.awin.com' );
}
$IDS        = 'M001,M002,M004,M005,M006,M008,M011,M015,M016,M017,M018';
$referentie = array();
foreach ( explode( ',', $IDS ) as $id ) {
	if ( rmk_get_model( $id ) ) {
		$referentie[ $id ] = $id; // vul na de constanten-check
	}
}

/* ================================================================ zonder constanten */
if ( 'zonder' === $MODUS ) {
	echo "\nZonder Coolblue-constanten\n";
	$voor = $GLOBALS['wp_options'];
	do_action( 'init' );
	t( 'geen ingeplande Coolblue-taak', ! wp_next_scheduled( RMK_CB_RONDE_HOOK ) && ! wp_next_scheduled( RMK_CB_BEWAKING_HOOK ) );
	$l = rmk_coolblue_ronde();
	t( 'ronde haalt niets op', 0 === $GLOBALS['feed']['verzoeken'] && false !== strpos( $l['melding'], 'ontbreken' ) );
	do_action( 'shutdown' );
	t( 'geen enkele optie veranderd (ook niet via shutdown)', $voor === $GLOBALS['wp_options'] );
	$r = route( $IDS );
	t( 'prijsroute: geen deel "coolblue" (antwoord zoals 1.3.9)', ! array_key_exists( 'coolblue', $r ) && array( 'bron', 'modellen' ) === array_keys( $r ) );
	$k = rmk_fill_offers( kaart( 'M002' ) );
	t( 'kaart zonder Coolblue-regel en zonder Coolblue-foto', false === strpos( $k, 'coolblue' ) && false === strpos( $k, 'Coolblue' ) );
	t( 'rmk_config zonder prijsroute (Bol ook uit)', ! isset( apply_filters( 'rmk_config', array() )['bolPrijsUrl'] ) );
	t( 'status: geen ingeplande taak, constanten afwezig', false === rmk_coolblue_status()['constanten_aanwezig'] );
	echo "\n" . ( $GLOBALS['fail'] ? $GLOBALS['fail'] . ' FOUT(EN)' : 'Alles geslaagd' ) . "\n";
	exit( $GLOBALS['fail'] ? 1 : 0 );
}

/* ================================================================ planning */
echo "\nA. Planning\n";
do_action( 'init' );
$volgende = wp_next_scheduled( RMK_CB_RONDE_HOOK );
t( 'elke nacht om 04:20 ingepland', $volgende && '04:20' === wp_date( 'H:i', $volgende ) && 'daily' === $GLOBALS['wp_cron'][ RMK_CB_RONDE_HOOK ][1], $volgende ? wp_date( 'Y-m-d H:i', $volgende ) : 'geen' );
t( 'bewaking elk uur ingepland', 'hourly' === ( $GLOBALS['wp_cron'][ RMK_CB_BEWAKING_HOOK ][1] ?? '' ) );

/* ================================================================ eerste ronde: voorbeeldbestand */
echo "\nB. Voorbeeldbestand (15 robotmaaiers)\n";
feed( gzencode( feed_csv() ) );
$l = rmk_coolblue_ronde();
$f = get_option( RMK_CB_STORE_OPTION );
t( 'ronde gelukt, 15 rijen gelezen', $l['gelukt'] && 15 === $l['rijen'], json_encode( $l ) );
t( 'één verzoek, naar de feed-URL, als bestand (stream)', 1 === $GLOBALS['feed']['verzoeken'] && FEED_URL === $GLOBALS['feed']['url'] && ! empty( $GLOBALS['feed']['args']['stream'] ) );
t( 'alleen onze producten bewaard (5 modellen met coolblue)', array( 'M002', 'M006', 'M008', 'M011', 'M015' ) == array_keys( $f['producten'] ) || 5 === count( $f['producten'] ), implode( ',', array_keys( $f['producten'] ) ) );
t( 'per product alleen prijs, voorraad, afbeelding, productpagina en id', array( 'merchant_product_id', 'prijs', 'in_stock', 'afbeelding', 'url' ) === array_keys( $f['producten']['M002'] ) );
t( 'M002: prijs 899, op voorraad, afbeelding coolblue.bynder.com', 899.0 === $f['producten']['M002']['prijs'] && true === $f['producten']['M002']['in_stock'] && rmk_coolblue_afbeelding_ok( $f['producten']['M002']['afbeelding'] ) );
t( 'hash = SHA-256 van het hele uitgepakte bestand', hash( 'sha256', feed_csv() ) === $f['hash'] );
t( 'tijdstip van ophalen bewaard', $GLOBALS['nu'] === $f['opgehaald'] && $GLOBALS['nu'] === $f['hash_sinds'] );
t( 'de feed zelf niet bewaard (opties klein, geen beschrijvingen)', strlen( json_encode( $GLOBALS['wp_options'] ) ) < 8000 && false === strpos( json_encode( $GLOBALS['wp_options'] ), 'vierkante meter' ) );
t( 'tijdelijk bestand opgeruimd', ! file_exists( $GLOBALS['feed']['args']['filename'] ) );
t( 'geen feed-URL of sleutel in opties en log', opties_zonder_secret() );
t( 'paginacache geleegd na de ronde', ( $GLOBALS['wp_acties']['litespeed_purge_all'] ?? 0 ) >= 1 );

/* ================================================================ weergave */
echo "\nC. Weergave en route" . ( 'uit' === $MODUS ? ' (RMK_COOLBLUE_ACTIVE uit)' : '' ) . "\n";
$k  = rmk_fill_offers( kaart( 'M002' ) );
$cr = cbregel( $k );
$r  = route( $IDS );
if ( 'uit' === $MODUS ) {
	t( 'geen Coolblue-regel en geen Coolblue-foto op de site', '' === $cr && false === strpos( $k, 'Coolblue' ) );
	t( 'prijsroute zonder deel "coolblue"', ! array_key_exists( 'coolblue', $r ) );
	t( 'status: feed vers, Coolblue-regel niet zichtbaar', true === rmk_coolblue_status()['feed_vers'] && false === rmk_coolblue_status()['modellen']['M002']['op_de_site'] );
	echo "\n" . ( $GLOBALS['fail'] ? $GLOBALS['fail'] . ' FOUT(EN)' : 'Alles geslaagd' ) . "\n";
	exit( $GLOBALS['fail'] ? 1 : 0 );
}
$link = 'https://www.awin1.com/cread.php?awinmid=85161&awinaffid=3126598&clickref=m002-robotmaaier-zonder-draad&ued=https%3A%2F%2Fwww.coolblue.nl%2Fproduct%2F975016%2Fsegway-navimow-i206-awd.html';
t( 'M002: Coolblue-regel met knop "Bekijk bij Coolblue"', false !== strpos( $cr, '>Bekijk bij Coolblue</a>' ) );
t( 'link in de vorm van het Logboek (rij 327), clickref model + paginaslug', false !== strpos( $cr, 'href="' . esc_url( $link ) . '"' ), $cr );
t( 'ued = merchant_deep_link volledig gecodeerd (= Logboek-kolom J met clickref)', rawurlencode( 'https://www.coolblue.nl/product/975016/segway-navimow-i206-awd.html' ) === 'https%3A%2F%2Fwww.coolblue.nl%2Fproduct%2F975016%2Fsegway-navimow-i206-awd.html' );
t( 'rel="sponsored nofollow"', false !== strpos( $cr, 'rel="sponsored nofollow"' ) );
t( 'eronder "Je gaat naar Coolblue. Bron: Coolblue."', false !== strpos( $cr, '<span class="rmk-offer__src">Je gaat naar Coolblue. Bron: Coolblue.</span>' ) );
t( 'geen prijs in de HTML (leeg prijsvak)', false === strpos( $cr, '899' ) && false !== strpos( $cr, 'data-rmk-cb-prijs hidden></span>' ) );
t( 'geen lokkertjes, beoordelingen of korting', ! preg_match( '/gratis|verzend|korting|beoordel|review|cijfer|9,\d|van\s*€|<del|<s>|rrp|saving/i', $cr ) );
t( 'foto van Coolblue (geen Bol-foto), ongewijzigde URL, "Foto: Coolblue"', false !== strpos( $k, 'src="' . esc_url( $GLOBALS['wp_options'][ RMK_CB_STORE_OPTION ]['producten']['M002']['afbeelding'] ) . '"' ) && false !== strpos( $k, 'Foto: Coolblue' ) && false !== strpos( $k, 'data-rmk-foto-bron="coolblue"' ) );
t( 'clickref: alleen kleine letters, cijfers, koppeltekens, hoogstens 50 tekens', 'm002-' . str_repeat( 'a', 45 ) === rmk_coolblue_clickref( 'M002', str_repeat( 'A', 80 ) ) && 'm011-gardena-robotmaaier' === rmk_coolblue_clickref( 'M011', 'Gardena-Robotmaaier!' ) && 'm002-beste-robotmaaier' === rmk_coolblue_clickref( 'M002', 'beste-robotmaaier' ) );
t( 'clickref eindigt niet op een koppelteken na afkappen', '-' !== substr( rmk_coolblue_clickref( 'M002', str_repeat( 'ab-', 30 ) ), -1 ) && strlen( rmk_coolblue_clickref( 'M002', str_repeat( 'ab-', 30 ) ) ) <= 50 );
$c2 = $r['coolblue']['M002'] ?? null;
t( 'route: deel "coolblue" met alleen model, prijs, tijdstip en winkel', $c2 && array( 'model', 'prijs', 'tijdstip', 'winkel' ) === array_keys( $c2 ) && 'M002' === $c2['model'] && 899 == $c2['prijs'] && 'Coolblue' === $c2['winkel'], json_encode( $c2 ) );
t( 'route: tijdstip = moment van ophalen (ISO, Amsterdam)', '2026-10-24T04:20:00+02:00' === $c2['tijdstip'] );
t( 'route: geen deeplink, afbeelding, voorraad of hash', ! preg_match( '/awin|bynder|in_stock|hash|apikey/i', json_encode( $r['coolblue'] ) ) );
t( 'route: alle vijf modellen op voorraad in de feed', array( 'M002', 'M006', 'M008', 'M011', 'M015' ) === array_keys( $r['coolblue'] ), implode( ',', array_keys( $r['coolblue'] ) ) );
t( 'rmk_config: prijsroute bekend (ook zonder Bol)', isset( apply_filters( 'rmk_config', array() )['bolPrijsUrl'] ) );
$html = apply_filters( 'the_content', '<p>Inleiding</p>' . rmk_fill_offers( kaart( 'M001' ) ) . $k );
t( 'advertentie-regel één keer, boven de eerste Coolblue-knop (zonder Bol)', 1 === substr_count( $html, 'rmk-affnote' ) && strpos( $html, 'rmk-affnote' ) < strpos( $html, 'data-rmk-cb' ) && strpos( $html, 'rmk-affnote' ) > strpos( $html, 'Inleiding' ) );
t( 'M001 (niet in het blad Coolblue): geen regel', '' === cbregel( rmk_fill_offers( kaart( 'M001' ) ) ) );

/* ================================================================ varianten */
echo "\nD. Varianten van de feed\n";
$GLOBALS['nu'] += 24 * $H;
feed( gzencode( feed_csv( array( '962143' => null, '975020' => array( 'in_stock' => '0' ), '975016' => array( 'search_price' => '849.00' ) ) ) ) );
$l = rmk_coolblue_ronde();
$r = route( $IDS );
t( 'ronde gelukt, hash veranderd', $l['gelukt'] && true === $l['hash_veranderd'] );
t( 'model afwezig (M008 niet in de feed): geen regel, niet in de route', '' === cbregel( rmk_fill_offers( kaart( 'M008' ) ) ) && ! isset( $r['coolblue']['M008'] ) && in_array( 'M008', $l['niet_in_feed'], true ) );
t( 'uit voorraad (M015 in_stock 0): geen regel, niet in de route', '' === cbregel( rmk_fill_offers( kaart( 'M015' ) ) ) && ! isset( $r['coolblue']['M015'] ) );
t( 'prijs veranderd (M002 849): route 849', 849.0 === (float) $r['coolblue']['M002']['prijs'] );
t( 'prijs 0: geen regel', ( function () use ( $IDS ) { feed( gzencode( feed_csv( array( '975016' => array( 'search_price' => '0' ) ) ) ) ); rmk_coolblue_ronde(); return ! isset( route( $IDS )['coolblue']['M002'] ); } )() );

echo "\nE. Verouderde feed\n";
$GLOBALS['nu'] += $H;
$zelfde = gzencode( feed_csv() );
feed( $zelfde );
rmk_coolblue_ronde();
$sinds = get_option( RMK_CB_STORE_OPTION )['hash_sinds'];
foreach ( array( 20, 40 ) as $uren ) {
	$GLOBALS['nu'] += 20 * $H;
	feed( gzencode( feed_csv(), 9 ) ); // andere compressie, zelfde inhoud: zelfde hash
	$l = rmk_coolblue_ronde();
}
t( 'zelfde inhoud: hash niet veranderd, hash_sinds blijft', false === $l['hash_veranderd'] && $sinds === get_option( RMK_CB_STORE_OPTION )['hash_sinds'] );
t( 'na 40 uur zelfde hash: nog vers', true === rmk_coolblue_feed_vers()[0] );
$GLOBALS['nu'] += 9 * $H; // 49 uur sinds de laatste verandering, feed 9 uur geleden opgehaald
t( 'na 49 uur zelfde hash: verouderd, geen Coolblue-regel en niet in de route', false === rmk_coolblue_feed_vers()[0] && '' === cbregel( rmk_fill_offers( kaart( 'M002' ) ) ) && empty( route( $IDS )['coolblue'] ) );
$GLOBALS['mails'] = array();
$b1 = rmk_coolblue_bewaking();
$b2 = rmk_coolblue_bewaking();
t( 'bewaking: één e-mail "verouderd", daarna niet opnieuw', 'gemeld' === $b1['status'] && 'al_gemeld' === $b2['status'] && 1 === count( $GLOBALS['mails'] ) && false !== strpos( $GLOBALS['mails'][0]['onderwerp'], 'verouderd' ) );
t( 'e-mail zonder feed-URL of sleutel', false === strpos( json_encode( $GLOBALS['mails'] ), 'GEHEIM' ) && false === strpos( json_encode( $GLOBALS['mails'] ), 'productdata' ) );
feed( gzencode( feed_csv( array( '975016' => array( 'search_price' => '879' ) ) ) ) );
rmk_coolblue_ronde();
t( 'nieuwe inhoud: weer vers, regel terug, storing voorbij', true === rmk_coolblue_feed_vers()[0] && '' !== cbregel( rmk_fill_offers( kaart( 'M002' ) ) ) && 'ok' === rmk_coolblue_bewaking()['status'] && false === get_option( RMK_CB_STORING_OPTION, false ) );
$GLOBALS['nu'] += 27 * $H; // geen nieuwe ronde
t( 'feed ouder dan 26 uur: geen regel', false === rmk_coolblue_feed_vers()[0] && '' === cbregel( rmk_fill_offers( kaart( 'M002' ) ) ) );

echo "\nF. Fouten: de vorige feed blijft staan, log zonder secrets\n";
$GLOBALS['nu'] -= 27 * $H;
$voor = get_option( RMK_CB_STORE_OPTION );
$gevallen = array(
	'kapotte gzip (afgebroken)' => array( substr( gzencode( feed_csv() ), 0, 3000 ), 200, null, 'afgebroken' ),
	'kapotte gzip (beschadigd)' => array( substr_replace( gzencode( feed_csv() ), str_repeat( "\xff", 200 ), 400, 200 ), 200, null, 'apot' ),
	'lege gzip (0 bytes)'       => array( '', 200, null, 'Leeg' ),
	'gzip zonder inhoud'        => array( gzencode( '' ), 200, null, 'leeg' ),
	'gzip met alleen de kop'    => array( gzencode( $KOP . "\n" ), 200, null, 'zonder producten' ),
	'geen gzip (HTML)'          => array( '<html>Fout</html>', 200, null, 'Geen gzip' ),
	'kolommen ontbreken'        => array( gzencode( "a,b\n1,2\n" ), 200, null, 'Kolommen ontbreken' ),
	'HTTP 500'                  => array( '', 500, null, 'HTTP 500' ),
	'HTTP 403'                  => array( '', 403, null, 'HTTP 403' ),
	'verbinding (met URL)'      => array( '', 0, 'cURL error 28: Operation timed out after 120001 milliseconds for ' . FEED_URL, 'Verbinding' ),
);
foreach ( $gevallen as $naam => $g ) {
	feed( $g[0], $g[1], $g[2] );
	$l = rmk_coolblue_ronde();
	t( $naam . ': ronde mislukt met melding', false === $l['gelukt'] && false !== stripos( $l['melding'], $g[3] ), $l['melding'] );
	t( $naam . ': vorige feed onveranderd, geen secret in de melding', $voor === get_option( RMK_CB_STORE_OPTION ) && false === strpos( $l['melding'], 'GEHEIM' ) && false === strpos( $l['melding'], 'productdata' ) );
}
t( 'na de fouten: regel blijft zolang de vorige feed vers is', '' !== cbregel( rmk_fill_offers( kaart( 'M002' ) ) ) );
t( 'geen secret in opties, log of transients', opties_zonder_secret() );

echo "\nG. Tweede ronde tijdens het ophalen\n";
feed( gzencode( feed_csv() ) );
$GLOBALS['feed']['tijdens'] = function () { return rmk_coolblue_ronde( 'tweede' ); };
$aantal = count( get_option( RMK_CB_LOG_OPTION ) );
$l      = rmk_coolblue_ronde();
t( 'tweede ronde stopt meteen ("Er draait al een ronde")', 'Er draait al een ronde.' === $GLOBALS['feed']['tweede']['melding'] && false === $GLOBALS['feed']['tweede']['gelukt'] );
t( 'één download, eerste ronde gelukt, één logregel erbij', 1 === $GLOBALS['feed']['verzoeken'] && $l['gelukt'] && $aantal + 1 === count( get_option( RMK_CB_LOG_OPTION ) ) );
t( 'slot weer vrij na de ronde', false === get_transient( RMK_CB_LOCK_KEY ) );

echo "\nG2. Vangnet als een ronde afbreekt (1.3.11)\n";
set_transient( RMK_CB_LOCK_KEY, 1, 900 );
$GLOBALS['rmk_cb_lopend'] = array( 'start' => $GLOBALS['nu'], 'eind' => null, 'aanleiding' => 'taak', 'gelukt' => false, 'melding' => '' );
$aantal = count( get_option( RMK_CB_LOG_OPTION ) );
rmk_coolblue_vangnet();
$eerste = get_option( RMK_CB_LOG_OPTION )[0];
t( 'afgebroken ronde: slot vrij en "Ronde afgebroken" in het log', false === get_transient( RMK_CB_LOCK_KEY ) && $aantal + 1 === count( get_option( RMK_CB_LOG_OPTION ) ) && 0 === strpos( $eerste['melding'], 'Ronde afgebroken' ) );
rmk_coolblue_vangnet();
t( 'na een gewone ronde doet het vangnet niets', $aantal + 1 === count( get_option( RMK_CB_LOG_OPTION ) ) );
t( 'geen wp_tempnam nodig (bestaat niet buiten wp-admin)', ! function_exists( 'wp_tempnam' ) );

echo "\nH. Reserve als de nachtelijke taak niet draait\n";
$GLOBALS['nu'] += 26 * $H;
feed( gzencode( feed_csv( array( '975016' => array( 'search_price' => '869' ) ) ) ) );
delete_option( RMK_CB_RESERVE_OPTION );
do_action( 'shutdown' );
t( 'na 26 uur zonder ronde: reserve start één ronde', 1 === $GLOBALS['feed']['verzoeken'] && 'reserve' === get_option( RMK_CB_LOG_OPTION )[0]['aanleiding'] );
do_action( 'shutdown' );
t( 'binnen het uur geen tweede reserveronde', 1 === $GLOBALS['feed']['verzoeken'] );
$GLOBALS['nu'] += 2 * $H;
do_action( 'shutdown' );
t( 'ronde minder dan 25 uur geleden: geen reserveronde', 1 === $GLOBALS['feed']['verzoeken'] );

echo "\nI. Samen met Bol\n";
define( 'RMK_BOL_CLIENT_ID', 'test-id' );
define( 'RMK_BOL_CLIENT_SECRET', 'test-geheim' );
define( 'RMK_BOL_SITE_ID', '1549381' );
define( 'RMK_AFFILIATE_ACTIVE', true );
$m2 = rmk_get_model( 'M002' );
update_option( RMK_BOL_AANBOD_OPTION, array( 'M002' => array( 'status' => 'ok', 'prijs' => 899.0, 'verkoper' => 'bol.com', 'partner' => false, 'url' => '', 'ean' => preg_replace( '/\D/', '', $m2['ean'] ), 'tijd' => $GLOBALS['nu'] ) ) );
$k = rmk_fill_offers( kaart( 'M002' ) );
t( 'zonder JavaScript: Bol-regel boven de Coolblue-regel', false !== strpos( $k, 'data-rmk-bol-model' ) && strpos( $k, 'data-rmk-bol-model' ) < strpos( $k, 'data-rmk-cb-model' ) );
t( 'geldige Bol-foto blijft (geen Coolblue-foto)', false !== strpos( $k, 'Foto: bol.com' ) && false === strpos( $k, 'Foto: Coolblue' ) );
$r = route( 'M002' );
t( 'route: Bol-deel ongewijzigd naast het Coolblue-deel', 'ok' === $r['modellen']['M002']['status'] && 869.0 === (float) $r['coolblue']['M002']['prijs'] );
$html = apply_filters( 'the_content', $k );
t( 'advertentie-regel één keer, boven de eerste knop', 1 === substr_count( $html, 'rmk-affnote' ) && strpos( $html, 'rmk-affnote' ) < strpos( $html, 'data-rmk-bol' ) );

echo "\nJ. Modelgegevens (dataroute)\n";
$ok  = $data;
$fout = function ( $cb ) use ( $data ) { $d = $data; $d['modellen'][1]['coolblue'] = $cb; return rmk_validate_modellen( $d ); };
t( 'blok coolblue met merchant_product_id en product_url: toegestaan', array() === rmk_validate_modellen( $ok ) );
t( 'extra velden (prijs) geweigerd', (bool) $fout( array( 'merchant_product_id' => '975016', 'prijs' => 899 ) ) );
t( 'merchant_product_id geen cijfers: geweigerd', (bool) $fout( array( 'merchant_product_id' => '97x' ) ) );
t( 'product_url niet op www.coolblue.nl: geweigerd', (bool) $fout( array( 'merchant_product_id' => '975016', 'product_url' => 'https://www.awin1.com/cread.php' ) ) );

echo "\nK. Statusoverzicht en beheerroute\n";
$s = rmk_coolblue_status();
t( 'status: constanten aanwezig, actief, feed vers', $s['constanten_aanwezig'] && $s['coolblue_actief'] && $s['feed_vers'] );
t( 'status zonder feed-URL of sleutel', false === strpos( json_encode( $s ), 'GEHEIM' ) && false === strpos( json_encode( $s ), 'productdata' ) );
do_action( 'rest_api_init' );
$ronde = $GLOBALS['wp_routes']['rmk/v1/coolblue-ronde'] ?? null;
$GLOBALS['wp_admin'] = false;
t( 'POST /rmk/v1/coolblue-ronde alleen voor beheerders', $ronde && 'POST' === $ronde['methods'] && false === call_user_func( $ronde['permission_callback'] ) );
$GLOBALS['wp_admin'] = true;
t( 'beheerder mag', true === call_user_func( $ronde['permission_callback'] ) );
t( 'GET /rmk/v1/coolblue-status alleen voor beheerders', isset( $GLOBALS['wp_routes']['rmk/v1/coolblue-status'] ) );
t( 'publieke route blijft /rmk/v1/bol-prijs (geen nieuwe publieke route)', '__return_true' === $GLOBALS['wp_routes']['rmk/v1/bol-prijs']['permission_callback'] && ! array_filter( $GLOBALS['wp_routes'], function ( $a, $k ) { return 'rmk/v1/bol-prijs' !== $k && '__return_true' === ( $a['permission_callback'] ?? '' ); }, ARRAY_FILTER_USE_BOTH ) );

echo "\n" . ( $GLOBALS['fail'] ? $GLOBALS['fail'] . ' FOUT(EN)' : 'Alles geslaagd' ) . "\n";
exit( $GLOBALS['fail'] ? 1 : 0 );
