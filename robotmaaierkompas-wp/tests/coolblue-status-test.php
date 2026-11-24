<?php
/**
 * Test thema 1.3.15: de beheerroute /rmk/v1/coolblue-status geeft per model alleen het domein (host) en het schema van
 * merchant_image_url, nooit de volledige URL, pad, query of feedsleutel. Zonder netwerk en zonder voorbeeldfeed: de
 * opgeslagen feed (optie rmk_coolblue_feed) wordt direct nagebootst, zoals de ronde hem bewaart.
 * Draaien: php tests/coolblue-status-test.php
 */
require __DIR__ . '/wp-stub.php';
$T = dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas';
define( 'RMK_DIR', $T );
const FEED_URL = 'https://productdata.awin.com/datafeed/download/apikey/GEHEIM0123456789abcdef/fid/95886/format/csv/compression/gzip/';
define( 'RMK_COOLBLUE_FEED_URL', FEED_URL );
define( 'RMK_COOLBLUE_AWMID', 85161 );
define( 'RMK_COOLBLUE_AWAFFID', 3126598 );
define( 'RMK_COOLBLUE_ACTIVE', true );
function wp_remote_get( $url, $args = array() ) { $GLOBALS['verzoeken'] = ( $GLOBALS['verzoeken'] ?? 0 ) + 1; return new WP_Error( 'x', 'geen netwerk' ); }
function get_temp_dir() { return sys_get_temp_dir() . '/'; }
add_filter( 'pre_http_request', function () { $GLOBALS['verzoeken'] = ( $GLOBALS['verzoeken'] ?? 0 ) + 1; return new WP_Error( 'x', 'geen netwerk' ); } );

// Modelgegevens: thema-bestand met het blok "coolblue" voor zeven modellen (nummers uit het blad Coolblue).
$CB   = array( 'M002' => '975016', 'M006' => '975391', 'M008' => '962143', 'M011' => '959330', 'M015' => '975020', 'M053' => '979968', 'M058' => '973529' );
$data = json_decode( file_get_contents( $T . '/data/modellen.json' ), true );
$ids  = array_column( $data['modellen'], 'id' );
foreach ( array( 'M053' => 'Eufy C15 Solo', 'M058' => 'Ecovacs GOAT A3000 LiDAR Pro' ) as $id => $naam ) {
	if ( ! in_array( $id, $ids, true ) ) { // het thema-bestand is ouder dan de live gegevens
		$data['modellen'][] = array( 'id' => $id, 'slug' => strtolower( str_replace( ' ', '-', $naam ) ), 'naam' => $naam, 'scores' => array() );
	}
}
foreach ( $data['modellen'] as &$m ) {
	if ( isset( $CB[ $m['id'] ] ) ) {
		$m['coolblue'] = array( 'merchant_product_id' => $CB[ $m['id'] ], 'product_url' => 'https://www.coolblue.nl/product/' . $CB[ $m['id'] ] . '/x.html' );
	}
}
unset( $m );
$MODELLEN = tempnam( sys_get_temp_dir(), 'rmkmod' );
file_put_contents( $MODELLEN, json_encode( $data ) );
add_filter( 'rmk_models_file', function () use ( $MODELLEN ) { return $MODELLEN; }, 20 );
foreach ( array( 'data', 'score', 'bol', 'coolblue', 'prijzen' ) as $f ) {
	require "$T/inc/$f.php";
}
$GLOBALS['fail'] = 0;
function t( $n, $ok, $info = '' ) {
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $n . ( $info && ! $ok ? "\n       $info" : '' ) . "\n";
	$GLOBALS['fail'] += $ok ? 0 : 1;
}

$BYNDER = 'https://coolblue.bynder.com/transform/008bc3f3-b05f-49ec-a780-60bcadd25e0e/962143?io=transform:fit,height:800,width:800';
$prod   = function ( $id, $img ) {
	return array( 'merchant_product_id' => $id, 'prijs' => 699.0, 'in_stock' => true, 'afbeelding' => $img, 'url' => 'https://www.coolblue.nl/product/' . $id . '/x.html' );
};
$nu = time();
$GLOBALS['wp_options'][ RMK_CB_STORE_OPTION ] = array( 'opgehaald' => $nu - 3600, 'hash_sinds' => $nu - 3600, 'rijen' => 5082, 'producten' => array(
	'M008' => $prod( '962143', $BYNDER ),
	'M058' => $prod( '973529', 'http://coolblue.bynder.com/transform/x/973529?io=a' ),
	'M053' => $prod( '979968', 'https://Images2.ProductServe.com/?w=200&url=ssl%3Acoolblue.bynder.com%2Fa.jpg&feedId=95886' ),
	'M002' => $prod( '975016', '' ),
	'M006' => $prod( '975391', 'geen url maar tekst' ),
	'M011' => $prod( '959330', 'https://user:geheim@image.coolblue.nl:8443/max/500x500/p.jpg#x' ),
	// M015 ontbreekt in de feed
) );

$s   = rmk_coolblue_status();
$per = $s['modellen'];
$v   = function ( $id ) use ( $per ) { return array( $per[ $id ]['afbeelding_host'], $per[ $id ]['afbeelding_schema'] ); };
t( 'M008 bynder: coolblue.bynder.com / https', array( 'coolblue.bynder.com', 'https' ) === $v( 'M008' ), json_encode( $v( 'M008' ) ) );
t( 'M058 http: coolblue.bynder.com / http', array( 'coolblue.bynder.com', 'http' ) === $v( 'M058' ), json_encode( $v( 'M058' ) ) );
t( 'M053 Awin-beeldserver, hoofdletters: images2.productserve.com / https', array( 'images2.productserve.com', 'https' ) === $v( 'M053' ), json_encode( $v( 'M053' ) ) );
t( 'M002 leeg veld: null / null', array( null, null ) === $v( 'M002' ), json_encode( $v( 'M002' ) ) );
t( 'M006 geen URL: null / onbekend', array( null, 'onbekend' ) === $v( 'M006' ), json_encode( $v( 'M006' ) ) );
t( 'M011 met gebruiker, poort en fragment: alleen image.coolblue.nl / https', array( 'image.coolblue.nl', 'https' ) === $v( 'M011' ), json_encode( $v( 'M011' ) ) );
t( 'M015 niet in de feed: null / null en in_feed false', array( null, null ) === $v( 'M015' ) && false === $per['M015']['in_feed'] );

$json = json_encode( $s );
t( 'geen volledige URL, pad, query of fragment in de status', ! preg_match( '#https?://|/transform/|io=transform|feedId|962143\?|max/500|\#x#i', $json ), $json );
t( 'geen feedsleutel, feed-URL, gebruikersnaam, wachtwoord of poort', false === strpos( $json, 'GEHEIM' ) && false === strpos( $json, 'productdata.awin' ) && false === strpos( $json, 'apikey' ) && false === strpos( $json, 'geheim' ) && false === strpos( $json, 'user' ) && false === strpos( $json, '8443' ) );
t( 'per model precies de bekende velden plus de twee nieuwe', array( 'model', 'merchant_product_id', 'in_feed', 'prijs', 'in_stock', 'op_de_site', 'afbeelding_host', 'afbeelding_schema' ) === array_keys( $per['M008'] ) );
t( 'bestaande velden ongewijzigd (M008: in feed, 699, op voorraad, op de site)', true === $per['M008']['in_feed'] && 699.0 === $per['M008']['prijs'] && true === $per['M008']['in_stock'] && true === $per['M008']['op_de_site'] );
t( 'bovenste niveau ongewijzigd', array( 'constanten_aanwezig', 'coolblue_actief', 'feed_vers', 'reden', 'opgehaald', 'hash_ongewijzigd_sinds', 'rijen', 'volgende_ronde', 'laatste_ronde', 'modellen' ) === array_keys( $s ) );

// De foto-regel van de site is niet veranderd: alleen https://coolblue.bynder.com geeft een Coolblue-foto.
$foto = function ( $id ) { $f = rmk_coolblue_foto( rmk_get_model( $id ) ); return $f ? $f['url'] : null; };
t( 'foto blijft alleen bij https + coolblue.bynder.com (M008 ja; M058, M053, M011 nee)', $BYNDER === $foto( 'M008' ) && null === $foto( 'M058' ) && null === $foto( 'M053' ) && null === $foto( 'M011' ) );
do_action( 'rest_api_init' );
$r = $GLOBALS['wp_routes']['rmk/v1/coolblue-status'] ?? null;
$GLOBALS['wp_admin'] = false;
$geen = $r ? call_user_func( $r['permission_callback'] ) : null;
$GLOBALS['wp_admin'] = true;
$wel  = $r ? call_user_func( $r['permission_callback'] ) : null;
t( 'route bestaat (GET) en is alleen voor beheerders', $r && 'GET' === $r['methods'] && false === $geen && true === $wel, json_encode( array( $geen, $wel ) ) );
t( 'geen HTTP-verzoeken', 0 === ( $GLOBALS['verzoeken'] ?? 0 ) );

echo $GLOBALS['fail'] ? "\n{$GLOBALS['fail']} FOUT\n" : "\nAlles OK\n";
exit( $GLOBALS['fail'] ? 1 : 0 );
