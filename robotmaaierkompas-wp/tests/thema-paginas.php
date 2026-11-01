<?php
/**
 * Hele pagina's renderen met een themaversie (ronde 80, thema 1.3.14; afgeleid van tests/amazon-paginas.php), zonder netwerk.
 * Anders dan amazon-paginas.php worden ook de shortcodes van het thema uitgevoerd (rmk_scoretabel, rmk_scoreblok; via
 * the_content op prioriteit 11 zoals WordPress) en kent get_post_field('post_content') de paginainhoud.
 * Modus "zonder": geen enkele affiliateconstante of schakelaar (Bol, Coolblue, Amazon). Modus "live": zoals live
 * (Bol, Coolblue en Amazon aan).
 * Invoer (niet in de repository, alleen gelezen van de live site via GET): ruwe inhoud van de gepubliceerde pagina's,
 * de live modelgegevens (eventueel met blok amazon), en /rmk/v1/bol-status en /rmk/v1/coolblue-status (om de Bol- en
 * Coolblue-regels na te bootsen zoals ze live staan). Uitvoer: JSON slug => gerenderde HTML.
 *
 * Gebruik: php tests/thema-paginas.php <themamap>/robotmaaierkompas <zonder|live> <paginas-raw.json>
 *              <modellen.json> <bol-status.json> <cb-status.json> <uit.json>
 * Vergelijk daarna 1.3.13 en 1.3.14 met tests/thema-paginas-vergelijk.py.
 */
require __DIR__ . '/wp-stub.php';
list( , $T, $MODUS, $PAG, $MOD, $BOL, $CB, $UIT ) = $argv;
define( 'RMK_DIR', $T );

if ( 'live' === $MODUS ) {
	define( 'RMK_BOL_CLIENT_ID', 'test-id' );
	define( 'RMK_BOL_CLIENT_SECRET', 'test-geheim' );
	define( 'RMK_BOL_SITE_ID', '1549381' );
	define( 'RMK_AFFILIATE_ACTIVE', true );
	define( 'RMK_COOLBLUE_FEED_URL', 'https://example.test/feed' );
	define( 'RMK_COOLBLUE_AWMID', 85161 );
	define( 'RMK_COOLBLUE_AWAFFID', 3126598 );
	define( 'RMK_COOLBLUE_ACTIVE', true );
	define( 'RMK_AMAZON_TAG', 'robotmaaier-21' );
	define( 'RMK_AMAZON_ACTIVE', true );
}
function wp_remote_get( $url, $args = array() ) { return wp_remote_request( $url, $args + array( 'method' => 'GET' ) ); }
function get_temp_dir() { return sys_get_temp_dir() . '/'; }
function wp_mail() { return true; }
function get_post_type() { return 'page'; }
function get_post_modified_time() { return '2026-10-31'; }
function get_the_modified_date() { return '31 oktober 2026'; }
$GLOBALS['verzoeken'] = array();
add_filter( 'pre_http_request', function ( $pre, $a, $url ) { $GLOBALS['verzoeken'][] = $url; return new WP_Error( 'x', 'geen netwerk' ); }, 10, 3 );
add_filter( 'rmk_models_file', function () use ( $MOD ) { return $MOD; }, 20 );
$GLOBALS['nu'] = strtotime( '2026-10-31 15:00:00 Europe/Amsterdam' );
add_filter( 'rmk_coolblue_nu', function () { return $GLOBALS['nu']; } );
add_filter( 'rmk_bol_nu', function () { return $GLOBALS['nu']; } );

foreach ( array( 'data', 'score', 'bol', 'coolblue', 'prijzen', 'redactie', 'amazon' ) as $f ) {
	if ( is_readable( "$T/inc/$f.php" ) ) {
		require "$T/inc/$f.php";
	}
}

add_filter( 'the_content', function ( $h ) { // alleen de shortcodes van het thema; andere blijven staan
	return preg_replace_callback( '/\\[(rmk_scoretabel|rmk_scoreblok)\b[^\\]]*\\]/', function ( $m ) { return do_shortcode( $m[0] ); }, $h );
}, 11 );

// Bol- en Coolblue-stand zoals live (uit de beheerroutes).
$bol   = json_decode( file_get_contents( $BOL ), true );
$store = array();
foreach ( $bol['modellen'] as $id => $b ) {
	if ( 'nog niet opgehaald' === $b['uitkomst'] ) {
		continue;
	}
	$store[ $id ] = array( 'status' => $b['uitkomst'], 'prijs' => (float) $b['prijs'], 'verkoper' => (string) $b['verkoper'], 'partner' => (bool) $b['partner'],
		'url' => '', 'ean' => $b['ean'], 'tijd' => $GLOBALS['nu'] - 1800 );
}
update_option( RMK_BOL_AANBOD_OPTION, $store );
$cb  = json_decode( file_get_contents( $CB ), true );
$pro = array();
foreach ( rmk_models_data()['modellen'] as $m ) {
	$c = $cb['modellen'][ $m['id'] ] ?? null;
	if ( $c && $c['in_feed'] && ! empty( $m['coolblue']['product_url'] ) ) {
		$pro[ $m['id'] ] = array( 'merchant_product_id' => $c['merchant_product_id'], 'prijs' => (float) $c['prijs'], 'in_stock' => $c['in_stock'] ? 1 : 0, 'afbeelding' => '', 'url' => $m['coolblue']['product_url'] );
	}
}
update_option( RMK_CB_STORE_OPTION, array( 'opgehaald' => $GLOBALS['nu'] - 3600, 'hash' => str_repeat( 'a', 64 ), 'hash_sinds' => $GLOBALS['nu'] - 3600, 'rijen' => 2563, 'producten' => $pro ) );

$uit = array();
foreach ( json_decode( file_get_contents( $PAG ), true ) as $p ) {
	$GLOBALS['wp_post'] = array( 'id' => $p['id'], 'slug' => $p['slug'], 'content' => $p['raw'] );
	// Elk core/html-blok apart door render_block (zoals WordPress), daarna the_content.
	$html = preg_replace_callback( '#<!-- wp:html -->(.*?)<!-- /wp:html -->#s', function ( $b ) {
		return apply_filters( 'render_block', $b[1], array( 'blockName' => 'core/html' ) );
	}, $p['raw'] );
	$uit[ $p['slug'] ] = apply_filters( 'the_content', $html );
}
file_put_contents( $UIT, json_encode( array( 'paginas' => $uit, 'verzoeken' => $GLOBALS['verzoeken'] ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) );
echo count( $uit ) . " pagina's, " . count( $GLOBALS['verzoeken'] ) . " HTTP-verzoeken\n";
